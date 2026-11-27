"""Read-only Google Drive access for the local batch command."""

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile

from .common import LibraryError, read_json, require


API = "https://www.googleapis.com/drive/v3/files"
SCOPE = "https://www.googleapis.com/auth/drive.readonly"
TIMEOUT = (10, 60)
FOLDER = "application/vnd.google-apps.folder"
FIELDS = "id,name,mimeType,parents,trashed,size,sha256Checksum"
FILE_ID = re.compile(r"[A-Za-z0-9_-]+")


@dataclass(frozen=True)
class DriveItem:
    id: str
    name: str
    mime: str
    parents: tuple[str, ...]
    trashed: bool = False
    size: int | None = None
    sha256: str | None = None

    @classmethod
    def from_data(cls, data):
        file_id, name, mime = (data.get(key) for key in ("id", "name", "mimeType"))
        require(isinstance(file_id, str) and FILE_ID.fullmatch(file_id) and
                isinstance(name, str) and isinstance(mime, str), "Metadata file Drive tidak lengkap.")
        size = data.get("size")
        digest = data.get("sha256Checksum")
        require(digest is None or isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest),
                "Format SHA-256 dari Drive tidak valid.")
        try:
            size = int(size) if size is not None else None
        except (TypeError, ValueError):
            raise LibraryError("Ukuran file Drive tidak valid.") from None
        require(size is None or size >= 0, "Ukuran file Drive tidak valid.")
        return cls(file_id, name, mime, tuple(data.get("parents", ())), data.get("trashed", False), size, digest)

    def is_child(self, parent_id):
        return not self.trashed and self.parents == (parent_id,)


class DriveClient:
    def __init__(self, session):
        self.session = session

    def request(self, file_id="", *, params, stream=False):
        from google.auth.exceptions import GoogleAuthError
        from requests import RequestException
        from urllib.parse import quote

        url = f"{API}/{quote(file_id, safe='')}" if file_id else API
        try:
            response = self.session.get(url, params=params, timeout=TIMEOUT, stream=stream)
        except GoogleAuthError:
            raise LibraryError("Otorisasi Drive gagal. Perbarui izin akun atau gunakan jalur token OAuth baru.") from None
        except RequestException:
            raise LibraryError("Koneksi ke Google Drive gagal. Periksa koneksi dan coba kembali.") from None
        if not response.ok:
            response.close()
            raise LibraryError(f"Google Drive mengembalikan HTTP {response.status_code}. Periksa akses dan konfigurasi Drive.")
        return response

    def metadata(self, file_id):
        with self.request(file_id, params={"fields": FIELDS, "supportsAllDrives": "true"}) as response:
            return DriveItem.from_data(response.json())

    def children(self, parent_id):
        require(FILE_ID.fullmatch(parent_id), "ID folder Drive tidak valid.")
        params = {"q": f"'{parent_id}' in parents and trashed = false",
                  "fields": f"nextPageToken,incompleteSearch,files({FIELDS})", "pageSize": 100,
                  "supportsAllDrives": "true", "includeItemsFromAllDrives": "true"}
        seen_tokens = set()
        seen_ids = set()
        files = []
        while True:
            try:
                with self.request(params=params) as response:
                    page = response.json()
            except LibraryError as error:
                raise LibraryError(f"Pemindaian folder Drive {parent_id} tidak selesai. {error}") from error
            require(not page.get("incompleteSearch"), f"Daftar anak folder Drive {parent_id} belum lengkap.")
            for item in map(DriveItem.from_data, page.get("files", ())):
                if item.is_child(parent_id):
                    require(item.id not in seen_ids, f"Daftar folder Drive {parent_id} berubah saat dipindai.")
                    files.append(item)
                    seen_ids.add(item.id)
            token = page.get("nextPageToken")
            if not token:
                return files
            require(token not in seen_tokens, f"Halaman daftar Drive berulang untuk folder {parent_id}.")
            seen_tokens.add(token)
            params["pageToken"] = token


    def download(self, item, destination, *, limit=None):
        from requests import RequestException

        if limit is not None and item.size is not None:
            require(item.size <= limit, f"File Drive melebihi batas {limit} byte.")
        digest = hashlib.sha256()
        size = 0
        with destination.open("xb") as output:
            try:
                with self.request(item.id, params={"alt": "media", "supportsAllDrives": "true"},
                                  stream=True) as response:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        size += len(chunk)
                        require((limit is None or size <= limit) and (item.size is None or size <= item.size),
                                "Unduhan lebih besar daripada ukuran yang diizinkan.")
                        digest.update(chunk)
                        output.write(chunk)
                require(item.size is None or size == item.size, "Unduhan Drive tidak lengkap.")
            except RequestException:
                destination.unlink(missing_ok=True)
                raise LibraryError("Transfer dari Drive terputus.") from None
            except (LibraryError, OSError, KeyboardInterrupt):
                destination.unlink(missing_ok=True)
                raise
        return digest.hexdigest()


def _save_token(path, value):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


@contextmanager
def connect(client_path, token_path, root):
    """Load credentials from local files and refresh them only for an invoked run."""
    from json import JSONDecodeError

    for path in (client_path, token_path):
        require(not path.is_symlink() and all(not path.resolve().is_relative_to(repo) for repo in
                    (root.resolve(), Path(__file__).resolve().parents[2])),
                "Simpan file OAuth di luar repo dan gunakan file biasa.")
    require(not client_path.resolve() == token_path.resolve(),
            "Gunakan jalur berbeda untuk konfigurasi klien OAuth dan token OAuth.")
    require(client_path.is_file(), f"Klien OAuth desktop belum tersedia. Simpan JSON klien di {client_path} "
                                    "atau berikan --credentials.")
    try:
        from google.auth.exceptions import GoogleAuthError
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from oauthlib.oauth2 import OAuth2Error
        from requests import RequestException
    except ImportError:
        raise LibraryError("Pasang dependensi Drive dengan python -m pip install -r requirements-drive.txt.") from None

    client = read_json(client_path)
    require(isinstance(client, dict) and isinstance(client.get("installed"), dict) and
            isinstance(client["installed"].get("client_id"), str),
            "Gunakan JSON klien OAuth bertipe Desktop app.")
    if token_path.exists():
        require(token_path.is_file() and token_path.stat().st_mode & 0o077 == 0,
                f"Token OAuth harus berupa file yang hanya dapat diakses pemilik: {token_path}. Gunakan chmod 600.")
        data = read_json(token_path)
        require(isinstance(data, dict) and data.get("scopes") == [SCOPE],
                "Token harus menggunakan cakupan Drive baca saja. Berikan --token dengan jalur baru.")
        require(data.get("client_id") == client["installed"]["client_id"],
                "Token memakai klien OAuth yang berbeda. Berikan --token dengan jalur baru.")
        try:
            credentials = Credentials.from_authorized_user_info(data, scopes=[SCOPE])
        except ValueError:
            raise LibraryError("Token OAuth tidak valid. Berikan --token dengan jalur baru untuk login ulang.") from None
    else:
        try:
            flow = InstalledAppFlow.from_client_config(client, scopes=[SCOPE], autogenerate_code_verifier=True)
            credentials = flow.run_local_server(host="127.0.0.1", port=0, timeout_seconds=180)
        except (AttributeError, ValueError, GoogleAuthError, OAuth2Error, RequestException, OSError):
            raise LibraryError("Login Drive gagal. Periksa konfigurasi OAuth desktop dan selesaikan login di browser.") from None
        _save_token(token_path, credentials.to_json())

    initial = credentials.to_json()
    try:
        with AuthorizedSession(credentials) as session:
            yield DriveClient(session)
    except JSONDecodeError:
        raise LibraryError("Google Drive mengembalikan respons yang tidak dapat dibaca.") from None
    finally:
        updated = credentials.to_json()
        if updated != initial:
            _save_token(token_path, updated)
