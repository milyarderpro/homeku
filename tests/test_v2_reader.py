"""End-to-end V2 ZIP/ingest/reader, revisions, mixed legacy and capacity."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.fixtures.factory import make_v2_inputs,isolated_root,make_folder,package_folder
from homeku.common import LibraryError,read_json,dumps,sha256,snapshot_hash,content_hash
from homeku.exporter import assemble_v2,review_v2,export_v2
from homeku.engine import ingest,check,build
from homeku.generation import render,generator_fingerprint
from homeku.reader import search,read_reference,extract_panel
from homeku.validation import validate_folder,extract_package


class V2ReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared=tempfile.TemporaryDirectory();base=Path(cls.shared.name)
        cls.source,cls.audit,cls.info=make_v2_inputs(base/"input",multi=True)
        result=assemble_v2(cls.source,cls.audit,cls.info,base/"candidate",purpose="fixture",include_source=True)
        cls.template=Path(result["candidate"])
    @classmethod
    def tearDownClass(cls):cls.shared.cleanup()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.work=Path(self.temp.name)
        self.folder=self.work/"candidate"/self.template.name;shutil.copytree(self.template,self.folder)
        self.root=isolated_root(self.work/"repo")
    def tearDown(self):self.temp.cleanup()
    def publish(self):
        pkg=export_v2(self.folder,self.work/"packages",snapshot_hash(self.folder))
        result=ingest(self.root,[Path(pkg["package"])])
        self.assertEqual(result["results"][0]["status"],"imported",result)
        return Path(pkg["package"])

    def test_roundtrip_snapshot_review_and_registry_source_hash(self):
        digest=snapshot_hash(self.folder)
        result=review_v2(self.folder,self.work/"review.md")
        self.assertEqual(result["snapshot_sha256"],digest)
        self.assertFalse(any("receipt" in p.name for p in self.folder.rglob("*")))
        pkg=self.publish()
        restored=extract_package(pkg,self.work/"restored")
        self.assertEqual(snapshot_hash(restored),digest)
        entry=read_json(self.root/"data/registry.json")["references"][self.folder.name]
        self.assertEqual(entry["audit_sha256"],sha256(self.folder/"audit.json"))
        self.assertEqual(entry["contract_version"],"2.0")
        self.assertEqual(check(self.root)["shots"],1)
        self.assertEqual(ingest(self.root,[pkg])["changed"],[])
        self.assertEqual(build(self.root,full=True)["changed"],[])

    def test_any_snapshot_mutation_rejects_export_without_reencoding(self):
        for name in ["audit.json","analysis.md","manifest.json","media/shot-01.jpg","media/storyboard.jpg"]:
            path=self.folder/name;before=path.read_bytes();digest=snapshot_hash(self.folder)
            path.write_bytes(before+b" ")
            with self.assertRaisesRegex(LibraryError,"changed since"):
                export_v2(self.folder,self.work/"packages",digest)
            path.write_bytes(before)
        with patch("homeku.media.build_media",side_effect=AssertionError("must not encode")):
            self.publish()

    def test_md_is_output_only_and_audit_tampering_is_rejected(self):
        path=self.folder/"analysis.md";original=path.read_text();path.write_text(original+"Manual fact\n")
        with self.assertRaisesRegex(LibraryError,"differs from"):
            validate_folder(self.folder,self.work)
        path.write_text(original)
        a=read_json(self.folder/"audit.json");a["identity"]["name"]="Manual edit"
        (self.folder/"audit.json").write_text(dumps(a))
        with self.assertRaisesRegex(LibraryError,"hash mismatch"):
            validate_folder(self.folder,self.work)

    def test_search_tempo_route_alias_style_family_and_partial_area(self):
        self.publish();rid=self.folder.name
        result=search(self.root,style="american cottage",scale="small",tempo="fast",route=["living","kitchen"])
        self.assertEqual(result["total"],1)
        self.assertEqual(search(self.root,style="cottage")["total"],0)
        self.assertEqual(search(self.root,style="cottage",style_relation="family")["total"],1)
        self.assertEqual(search(self.root,style="american cottage",include_uncertain=False)["total"],0)
        identity=read_reference(self.root,rid);self.assertNotIn("frame_reviews",str(identity))
        selected=read_reference(self.root,rid,part="area",shot="shot-01",area="kitchen-1")
        self.assertEqual(len(selected["shot"]["design"]),1)
        self.assertEqual(len(selected["shot"]["route"]),2)
        self.assertEqual(len(selected["shot"]["phases"]),1)
        self.assertEqual(search(self.root,configuration="overhead cabinet")["total"],0)
        native=self.work/"native.jpg";extract_panel(self.root,rid,"frame:shot-01:2",native,native=True)
        self.assertTrue(native.is_file())
        panel=self.work/"panel.png";extract_panel(self.root,rid,"p-start",panel)
        self.assertTrue(panel.is_file())

    def test_mixed_legacy_is_not_misread_as_one_continuous_route(self):
        self.publish()
        legacy=make_folder(self.work/"legacy",rid="legacy-cuts")
        result=ingest(self.root,[package_folder(legacy,self.work/"legacy-cuts-r0001.zip")])
        self.assertEqual(result["results"][0]["status"],"imported")
        self.assertEqual(check(self.root)["references"],2)
        result=search(self.root,route=["bathroom","kitchen"])
        self.assertEqual(result["total"],0)
        old=read_reference(self.root,"legacy-cuts")
        self.assertIsNone(old["size"]);self.assertIsNone(old["identity"])
        self.assertEqual(old["profile"],[])

    def test_revision_removes_stale_derived_facts_and_wrong_supersedes_rejected(self):
        self.publish();rid=self.folder.name
        entry=read_json(self.root/"data/registry.json")["references"][rid]
        a=read_json(self.audit);a["revision"]=2;a["shots"][0]["facts"][0]["value"]="new configuration"
        path=self.work/"rev2.json";path.write_text(dumps(a))
        result=assemble_v2(self.source,path,self.info,self.work/"revision2",purpose="fixture",include_source=True,supersedes={"revision":1,"content_sha256":"0"*64})
        pkg=export_v2(Path(result["candidate"]),self.work/"r2bad",result["snapshot_sha256"])
        self.assertEqual(ingest(self.root,[Path(pkg["package"])])["results"][0]["status"],"failed")
        result=assemble_v2(self.source,path,self.info,self.work/"revision2",purpose="fixture",include_source=True,supersedes={"revision":1,"content_sha256":entry["content_sha256"]})
        pkg=export_v2(Path(result["candidate"]),self.work/"r2good",result["snapshot_sha256"])
        self.assertEqual(ingest(self.root,[Path(pkg["package"])])["results"][0]["status"],"imported")
        self.assertEqual(search(self.root,configuration="new configuration")["total"],1)
        self.assertEqual(check(self.root)["references"],1)
        self.assertEqual(read_json(self.root/"data/registry.json")["references"][rid]["revision"],2)
        for p in (self.root/"catalogs/design").rglob("*.md"):
            for row in p.read_text().splitlines():
                if "| living |" in row:self.assertNotIn("curved island",row)

    def test_corrupt_cache_recovers_and_assets_are_fingerprinted(self):
        self.publish();rid=self.folder.name
        path=self.root/f"data/projections/{rid}.json";path.write_text("{}")
        self.assertIn("data/projections",build(self.root)["changed"])
        self.assertEqual(check(self.root)["status"],"ok")
        before=generator_fingerprint(self.root)
        from homeku.validation import CODE_ROOT
        actual_sha=sha256
        with patch("homeku.generation.sha256",side_effect=lambda p:"0"*64 if str(p).endswith("DejaVuSans.ttf") else actual_sha(p)):
            self.assertNotEqual(before,generator_fingerprint(self.root))

    def test_300_v2_models_keep_index_small_and_counts_unique(self):
        _,template,_=validate_folder(self.folder,self.work)
        models={}
        for i in range(300):
            rid=f"capacity-{i:03d}";m=copy.deepcopy(template);m["id"]=rid
            m["source"]["path"]=f"video/{rid}.mp4";models[rid]=m
        outputs=render(self.root,models)
        index=json.loads(outputs["data/search-index.json"])
        self.assertEqual(len(index["references"]),300)
        self.assertLess(len(outputs["data/search-index.json"].encode()),4_000_000)
        self.assertNotIn("frame_reviews",outputs["data/search-index.json"])
        self.assertNotIn("architecture",outputs["data/search-index.json"])
        self.assertNotIn("viewed_frame_indices",outputs["data/search-index.json"])
        for page in outputs:
            if page.startswith("knowledge/comparisons/") and page.endswith("index.json"):
                self.assertEqual(json.loads(outputs[page])["denominator"],300)
        self.assertEqual(outputs,render(self.root,models))

    def test_complete_source_values_and_all_json_pointers_survive_projection(self):
        self.publish();payload=read_reference(self.root,self.folder.name,part="full")
        authored=read_json(self.audit);model=payload["reference"]
        for key,value in authored.items():
            if key=="shots":
                for original,projected in zip(value,model["shots"]):
                    for field in original:self.assertEqual(original[field],projected[field])
            else:self.assertEqual(value,model[key])
        for pointer,proof in payload["provenance"].items():
            node=payload
            for part in pointer.strip("/").split("/"):
                node=node[int(part)] if isinstance(node,list) else node[part]
            if proof["json"]:
                source=authored
                for part in proof["source_pointer"].strip("/").split("/") if proof["source_pointer"] else []:
                    source=source[int(part)] if isinstance(source,list) else source[part]
            for key in proof.get("evidence_ids",[]):self.assertIn(key,payload["evidence_inventory"])

    def test_optional_source_and_v2_package_security_are_versioned(self):
        from homeku.engine import fixture_allowed
        from homeku.validation import CODE_ROOT
        manifest=read_json(self.folder/"manifest.json")
        with self.assertRaisesRegex(LibraryError,"Synthetic fixture rejected"):
            fixture_allowed(CODE_ROOT,manifest)
        source=self.folder/"source.mp4";source_bytes=source.read_bytes();source.unlink()
        canonical=self.root/f"video/{self.folder.name}.mp4";canonical.parent.mkdir();canonical.write_bytes(source_bytes)
        digest=snapshot_hash(self.folder)
        package=export_v2(self.folder,self.work/"without-source",digest,canonical)
        self.assertEqual(ingest(self.root,[Path(package["package"])])["results"][0]["status"],"imported")
        self.assertFalse((self.root/"references"/self.folder.name/"source.mp4").exists())
        import zipfile
        bad=self.work/"bad"/Path(package["package"]).name;bad.parent.mkdir()
        with zipfile.ZipFile(package["package"]) as original,zipfile.ZipFile(bad,"w") as output:
            for name in original.namelist():output.writestr(name,original.read(name))
            output.writestr(self.folder.name+"/receipt.json","{}")
        with self.assertRaisesRegex(LibraryError,"Unsupported file"):
            extract_package(bad,self.work/"bad-extract")

    def test_native_frame_mentions_in_narratives_are_not_provenance_claims(self):
        a=read_json(self.audit);a["limitations"]+=" Contoh teks frame:shot-01:999999 bukan bukti."
        path=self.work/"narrative.json";path.write_text(dumps(a))
        result=assemble_v2(self.source,path,self.info,self.work/"narrative",purpose="fixture",include_source=True)
        _,model,_=validate_folder(Path(result["candidate"]),self.work)
        self.assertNotIn("frame:shot-01:999999",model["native_evidence"])

    def test_kit_v2_technical_pipeline_runs_without_repository(self):
        import subprocess,sys,zipfile
        from tests.test_audit import kit_builder
        workspace=self.work/"empty-chat";workspace.mkdir()
        kit=self.work/"kit.zip";kit.write_bytes(kit_builder.build_bytes())
        with zipfile.ZipFile(kit) as archive:archive.extractall(workspace)
        boot=subprocess.run([sys.executable,str(workspace/"homeku_runtime.py"),"--output",str(workspace)],capture_output=True,text=True)
        self.assertEqual(boot.returncode,0,boot.stdout+boot.stderr)
        info=self.work/"info.json";info.write_text(dumps(self.info))
        def run(*args):
            p=subprocess.run([sys.executable,str(workspace/"tools/audit.py"),*map(str,args)],cwd=workspace,capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr);return json.loads(p.stdout)
        draft=run("draft-v2",self.source,self.audit,"--audit-info",info,"--output",self.work/"portable-candidate","--include-source")
        review=run("review",draft["candidate"],"--output",self.work/"portable-review.md")
        result=run("export-v2",draft["candidate"],"--output",self.work/"portable-packages","--receipt",str(self.work/"portable-review.md.json"))
        self.assertEqual(snapshot_hash(Path(draft["candidate"])),result["snapshot_sha256"])
        self.assertTrue(Path(result["package"]).is_file())
        # Same candidate path, changed bytes: a receipt must not authorize re-export.
        candidate=Path(draft["candidate"])
        original=(candidate/"analysis.md").read_bytes()
        (candidate/"analysis.md").write_bytes(original+b"\n")
        failed=subprocess.run([sys.executable,str(workspace/"tools/audit.py"),"export-v2",str(candidate),"--output",str(self.work/"stale"),"--receipt",str(self.work/"portable-review.md.json")],cwd=workspace,capture_output=True,text=True)
        self.assertNotEqual(failed.returncode,0)
        self.assertIn("changed since whole-snapshot review",failed.stderr)
        (candidate/"analysis.md").write_bytes(original)
        receipt=json.loads((self.work/"portable-review.md.json").read_text())
        receipt["candidate"]=str(self.work/"different-candidate")
        (self.work/"wrong-receipt.json").write_text(json.dumps(receipt))
        failed=subprocess.run([sys.executable,str(workspace/"tools/audit.py"),"export-v2",str(candidate),"--output",str(self.work/"wrong"),"--receipt",str(self.work/"wrong-receipt.json")],cwd=workspace,capture_output=True,text=True)
        self.assertNotEqual(failed.returncode,0)
        self.assertIn("another candidate",failed.stderr)

    def test_bounded_search_over_300_entries_and_partial_payload(self):
        from homeku.reader import load_reader
        self.publish();rid=self.folder.name
        entry=read_json(self.root/"data/search-index.json")["references"][0]
        entries=[{**copy.deepcopy(entry),"id":f"bounded-{i:03d}"} for i in range(300)]
        registry={e["id"]:{"revision":e["revision"]} for e in entries}
        with patch("homeku.reader._generated",return_value={"references":entries}),patch("homeku.reader._registry",return_value={"references":registry}):
            result=search(self.root,tempo="fast",limit=7,offset=14)
        self.assertEqual((result["total"],len(result["results"]),result["next_offset"]),(300,7,21))
        identity=read_reference(self.root,rid)
        shot=read_reference(self.root,rid,part="shot",shot="shot-01")
        self.assertNotIn("frame_reviews",json.dumps(identity))
        self.assertNotIn("frame_reviews",json.dumps(shot))
        self.assertLess(len(json.dumps(identity)),len(json.dumps(load_reader(self.root,rid))))
