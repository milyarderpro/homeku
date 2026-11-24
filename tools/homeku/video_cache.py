"""Bounded disposable cache. Frozen media always receives canonical extractor bytes."""
import hashlib
import io
import json
import os
import subprocess
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from PIL import Image
from .common import LibraryError, dumps, read_json, require, sha256
from .audit_performance import safe_path, event, timed

ACTIVE = ContextVar("homeku_video_cache", default=None)

def atomic(path, data):
    path = safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name("." + path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temp.open("xb") as f:
            f.write(data)
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()

class FrameCache:
    def __init__(self, source, root, *, max_bytes=512*1024*1024, log=None):
        from . import video
        self.source = Path(source).resolve()
        require(self.source.is_file(), "Source unavailable")
        self.root = safe_path(root)
        code_root = Path(__file__).resolve().parents[2]
        require(not self.root.resolve().is_relative_to((code_root/"references").resolve()), "Cache must stay outside accepted references")
        self.source_stamp = self._stamp()
        self.source_hash = sha256(self.source)
        self.max_bytes = max_bytes
        self.log = log
        version = subprocess.run(["ffmpeg","-version"], capture_output=True, text=True, check=True, timeout=15).stdout.splitlines()[0]
        signature = "".join(sha256(Path(__file__).with_name(name)) for name in
                            ("video.py","video_cache.py","media.py","media_incremental.py","media_v2_2.py","media_v2_2_1.py","camera_notation.py")) + version
        self.signature = hashlib.sha256(signature.encode()).hexdigest()
        self.bucket = safe_path(self.root/self.source_hash/self.signature)
        self.bucket.mkdir(parents=True, exist_ok=True)
        self.index_path = safe_path(self.bucket/"index.json")
        try:
            self.index = read_json(self.index_path)
            require(isinstance(self.index,dict) and self.index.get("source_sha256")==self.source_hash and self.index.get("signature")==self.signature and
                    isinstance(self.index.get("blobs"),dict), "Invalid cache inventory")
        except (LibraryError, OSError, ValueError, TypeError):
            self.index = {"source_sha256":self.source_hash, "signature":self.signature, "blobs":{}}
        self.stats = {"hits":0, "misses":0, "canonical_decodes":0, "batch_passes":0, "batch_frames":0, "batch_equal":0, "ffmpeg_calls":0, "batch_retries":0}
        data = self._get("metadata.json")
        try:
            meta = json.loads(data) if data else None
            require(isinstance(meta, dict) and isinstance(meta.get("times"),list) and meta["times"] and
                    isinstance(meta.get("info"),dict) and all(a<b for a,b in zip(meta["times"],meta["times"][1:])),
                    "Invalid cached metadata")
        except (LibraryError, ValueError, TypeError):
            meta = {"info":video._probe_video_uncached(self.source), "times":video._frame_times_uncached(self.source)}
            self._put("metadata.json", dumps(meta).encode())
        self.info, self.times = meta["info"], meta["times"]
        self.ensure_source()

    def _stamp(self):
        value=self.source.stat()
        return (value.st_dev,value.st_ino,value.st_size,value.st_mtime_ns,value.st_ctime_ns)

    def ensure_source(self):
        stamp=self._stamp()
        if stamp!=self.source_stamp:
            require(sha256(self.source)==self.source_hash,"Source changed during cached operation; use a new session")
            self.source_stamp=stamp

    def _get(self, name):
        self.ensure_source()
        path = safe_path(self.bucket/name)
        digest = self.index["blobs"].get(name)
        if not path.is_file() or digest is None:
            self.stats["misses"] += 1
            return None
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest:
            self.stats["misses"] += 1
            return None
        self.stats["hits"] += 1
        return data

    def _put(self, name, data):
        require("/" not in name and "\\" not in name and name not in {".",".."}, "Invalid cache member")
        path = safe_path(self.bucket/name)
        used = sum(safe_path(p).stat().st_size for p in self.bucket.rglob("*") if p.is_file())
        previous = path.stat().st_size if path.is_file() else 0
        require(used-previous+len(data) <= self.max_bytes, "Cache size limit exceeded; use bounded audit intervals")
        atomic(path,data)
        self.index["blobs"][name]=hashlib.sha256(data).hexdigest()
        atomic(self.index_path,dumps(self.index).encode())

    def matches(self, source, stream=None):
        self.ensure_source()
        return Path(source).resolve()==self.source and (stream is None or stream==self.info["video_stream_index"])

    def frame(self, index, stream=None):
        from .video import _extract_frame_uncached
        require(isinstance(index,int) and 0<=index<len(self.times), "Frame outside source")
        require(stream is None or stream==self.info["video_stream_index"], "Cache stream mismatch")
        key=f"canonical-{index:06d}.jpg"
        data=self._get(key)
        if data is None:
            # Qualify each final-media frame against the unchanged extractor.
            # Batch pictures are analysis-only until canonical bytes are obtained.
            data=_extract_frame_uncached(self.source,index,self.info["video_stream_index"])
            self.ensure_source()
            self.stats["canonical_decodes"]+=1
            candidate=self._get(f"analysis-{index:06d}.jpg")
            if candidate==data:
                self.stats["batch_equal"]+=1
            self._put(key,data)
        return data

    def extract_many(self, indices):
        ids=sorted(set(indices))
        require(ids and len(ids)<=1000 and all(type(i) is int and 0<=i<len(self.times) for i in ids),
                "Use at most 1000 valid native indices per batch")
        result={}
        missing=[]
        for i in ids:
            data=self._get(f"canonical-{i:06d}.jpg") or self._get(f"analysis-{i:06d}.jpg")
            if data is None:missing.append(i)
            else:result[i]=data
        def decode(batch, depth=0):
            expression="+".join(f"eq(n\\,{i})" for i in batch)
            self.stats["ffmpeg_calls"]+=1
            try:
                completed=subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-protocol_whitelist","file,pipe",
                    "-i",str(self.source),"-map",f"0:{self.info['video_stream_index']}","-vf","select="+expression,
                    "-vsync","0","-frames:v",str(len(batch)),"-f","image2pipe","-vcodec","mjpeg","-q:v","2","-threads","1","-"],
                    capture_output=True,check=True,timeout=120)
            except subprocess.CalledProcessError as exc:
                detail=(exc.stderr or b"").decode("utf-8","replace") if isinstance(exc.stderr,bytes) else str(exc.stderr or "")
                message=detail.lower()
                expression_error=("select" in message or "expression" in message) and any(v in message for v in ("evaluating","parsing","expression","cannot allocate memory"))
                if expression_error and len(batch)>1 and depth<5:
                    self.stats["batch_retries"]+=1
                    event(self.log,"batch-retry",frames=len(batch),depth=depth)
                    middle=len(batch)//2;decode(batch[:middle],depth+1);decode(batch[middle:],depth+1)
                    return
                raise LibraryError("Cannot batch-extract native frames: "+detail[-700:]) from exc
            except (OSError,subprocess.SubprocessError) as exc:
                raise LibraryError(f"Cannot batch-extract native frames: {exc}") from exc
            self.ensure_source()
            data=completed.stdout;chunks=[];offset=0
            while offset<len(data):
                end=data.find(b"\xff\xd9",offset)+2
                require(end>1 and data[offset:offset+2]==b"\xff\xd8","Invalid batch JPEG stream")
                chunk=data[offset:end]
                with Image.open(io.BytesIO(chunk)) as im:im.load()
                chunks.append(chunk);offset=end
            require(len(chunks)==len(batch),"Batch frame count differs from native selection")
            self.stats["batch_passes"]+=1;self.stats["batch_frames"]+=len(batch)
            for i,data in zip(batch,chunks):
                self._put(f"analysis-{i:06d}.jpg",data);result[i]=data
        # Bound expression size before FFmpeg 5.x's recursive parser is reached.
        for offset in range(0,len(missing),32):
            decode(missing[offset:offset+32])
        event(self.log,"extract-batch",requested=len(ids),new=len(missing),**self.stats)
        return result

    @contextmanager
    def activate(self):
        token=ACTIVE.set(self)
        try:
            yield self
        finally:
            ACTIVE.reset(token)

def _cached_media(folder, audit, source_path, source, config):
    """Cache individual media dependencies without editing registered media engines."""
    from .media import expected_media
    if config["media"]=="2.2.1":
        from .media_v2_2_1 import build_media
    else:
        from .media_v2_2 import build_media
    from .common import sha256
    cache=ACTIVE.get()
    if cache is None:
        return build_media(folder,audit,source_path,source,config)
    root=cache.bucket/"media"
    safe_path(root).mkdir(parents=True,exist_ok=True)
    # Geometry and text already contain every visible dependency of the
    # immutable layout. Storyboard additionally binds its child collage keys.
    def key(meta, design, children):
        fonts=design.get("fonts",{})
        value={"source":cache.source_hash,"extractor":cache.signature,"config":config,
               "dimensions":[source["width"],source["height"]],"meta":meta,"texts":design.get("texts",[]),
               "spec":design["spec"],"header_lines":design.get("header_lines",[]),
               "margin":design.get("margin"),"line_height":design.get("line_height"),
               "font_sizes":{name:font.size for name,font in fonts.items()},
               "header_font":design["font"].size if "font" in design else None,
               "children":children}
        return hashlib.sha256(dumps(value).encode()).hexdigest()
    wanted=list(expected_media(audit,source,config))
    keys={}
    reused=0
    for meta,_,design,_ in wanted:
        children=[keys[b["derived_from"]] for b in meta.get("blocks",[])] if meta["kind"]=="storyboard" else []
        digest=key(meta,design,children);keys[meta["path"]]=digest
        item=root/(digest+".jpg");receipt=root/(digest+".sha256")
        safe_path(item);safe_path(receipt)
        if item.is_file() and receipt.is_file() and sha256(item)==receipt.read_text().strip():
            dest=safe_path(folder/meta["path"]);dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(item.read_bytes());reused+=1
    if reused==len(wanted):
        event(cache.log,"media",reused=reused,rendered=0)
        return [{**meta,"sha256":sha256(folder/meta["path"])} for meta,*_ in wanted]
    # The immutable engine can render a subset via an isolated expected-media
    # iterator wrapper implemented by the dispatcher (no global monkeypatch).
    from .media import render_missing_media
    rendered=render_missing_media(folder,audit,source_path,source,config,
                                  {meta["path"] for meta,*_ in wanted if not (folder/meta["path"]).is_file()})
    for meta in rendered:
        digest=keys[meta["path"]]
        data=(folder/meta["path"]).read_bytes()
        used=sum(safe_path(p).stat().st_size for p in cache.bucket.rglob("*") if p.is_file())
        require(used+len(data)<=cache.max_bytes,"Cache size limit exceeded; start a fresh bounded workspace")
        atomic(root/(digest+".jpg"),data)
        atomic(root/(digest+".sha256"),(meta["sha256"]+"\n").encode())
    event(cache.log,"media",reused=reused,rendered=len(rendered),**cache.stats)
    return [{**meta,"sha256":sha256(folder/meta["path"])} for meta,*_ in wanted]


def cached_media(folder,audit,source_path,source,config):
    cache=ACTIVE.get()
    with timed(cache.log if cache else None,"render-media"):
        return _cached_media(folder,audit,source_path,source,config)
