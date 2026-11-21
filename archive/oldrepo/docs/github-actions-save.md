# Homeku v1.4 — Filename-Based Parallel Save (CURRENT)

**Plan:** [Issue #4](https://github.com/milyarderpro/homeku/issues/4). This section supersedes the historical v1.3 sequential-save directions below. Apply only after the v1.4 PR is merged into main.

## Normal operation

1. Upload an MP4 to `main/video/<filename>.mp4`; ChatGPT analyzes all shots, writes reviewed YAML 2.1 and Indonesian `shot_narratives` without any GitHub mutation. Verify the source Git blob SHA if possible.
2. An independent, standalone exact `save now` authorizes ChatGPT's GitHub **create_file** of `main/requests/pending/<video-stem>.json` (not update_file on shared save.json). Stem is the exact filename without `.mp4` and preserves case; new stems match `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}`.
3. Preflight ALL `references/*/analysis.yaml` (including old `VID-XXX`) for duplicate `video.filename`, plus pending/results and case-insensitive collisions. `edh001.mp4` is already `VID-004`, `edh014.mp4` is `VID-007`, and `edh010.mp4` is `VID-010`; do not create second archives for them. If metadata is missing/corrupt, fail closed.
4. Create one immutable request JSON with `schema_version=1.0`, `status=approved`, stable `request_id`, `video.path`, Git blob `video.blob_sha` (40 lowercase hex), `keyframe_times_s`, full string `analysis_yaml` (2.1), and **complete** `shot_narratives` (three categories per shot, indices covering every YAML detail). No AI runs in Actions and no narratives are embedded in YAML.
5. One GitHub Actions run is triggered per push adding a request, or by manual `workflow_dispatch` for one existing request path. The runner checks out **event SHA**, not moving main, and rejects multiple requests in one event, modified/deleted pending requests, or bad paths. It validates MP4+SHA, YAML, narratives and timestamps, creates FFmpeg JPGs, Pillow storyboard and Markdown.
6. Each runner atomically commits **only** `references/<stem>/*` + `requests/results/<stem>.json`. It uses fetch, remote request blob comparison, existing-archive check, rebase, fast-forward push, up to five bounded retries; NEVER force-push or overwrite different/partial results. Remote files and request marker must validate before reporting Saved. Actions jobs for different videos may run concurrently.
7. `requests/results/<stem>.json` holds last successful result for that video; it is **not** live status. Check the matching Actions run for Queued/Processing/Failed. Old `requests/save.json`/`requests/result.json` remain read-only archival files.

## Recovery

For network/FFmpeg/GitHub failures, **do not create a second pending file or change request_id**. Open GitHub → Actions → Homeku - Parallel Save v1.4 → Run workflow on main → enter `request_path` such as `requests/pending/edh011.json`. The runner rechecks the immutable request blob SHA against main and returns Already saved if a complete matching package already exists. Different request IDs, partial packages, corrupt legacy YAML, case collisions, or changed request payloads cause a hard failure rather than silent overwrites. If a request needs correction, cancel active runs, confirm no Saved package exists, use an explicitly authorized PR with SHA-aware edits, then dispatch from the new snapshot.

## Release and rollback

First run the historical 44 regression tests and new parallel tests on an isolated branch; confirm two independent local Git runner copies can rebase and publish without losing packages. Before production cutover ensure no legacy save run is active. After merge run production smoke for **3 previously unsaved videos** with overlapping Actions timestamps, then 5; verify package+result per video, original video identity and no altered legacy archives. Keep Issue #4 open until those acceptance tests are evidenced. Roll back the workflow through a PR if needed, without deleting pending/results/references; resume pending requests via dispatch once repaired. FFmpeg install caching remains outside this release.

**Project Instructions:** the GitHub commit does not automatically update ChatGPT Project Instructions. Copy the replacement v1.4 instructions from README.

---

# Historical operating guide: v1.3 Sequential Save (NO LONGER CURRENT AFTER v1.4 MERGE)

# Homeku v1.3 — Pengoperasian GitHub Actions (Sequential Save)

Dokumen ini menjelaskan kontrak Homeku v1.3 yang dibahas pada [Issue #1](https://github.com/milyarderpro/homeku/issues/1) dan diajukan melalui [PR #2](https://github.com/milyarderpro/homeku/pull/2). Perilaku produksi yang berlaku selalu ditentukan oleh kode yang telah di-merge ke `main`; isi branch PR belum otomatis aktif di produksi.

## Yang sudah dan belum dibuktikan

- **Lulus di branch pengujian:** Actions run [41454322381](https://github.com/milyarderpro/homeku/actions/runs/41454322381) mengambil MP4 asli `dreamsHouse002.mp4`, menerima request teks dari konektor GitHub, mengekstrak 4 JPEG + 1 storyboard, membentuk YAML/Markdown, dan meng-commit 7 berkas di branch `actions-jpg-test`. Analisis di run ini **fixture integrasi**, bukan draft final yang direview pengguna.
- **Lulus tes idempotensi di branch pengujian:** [41454495367](https://github.com/milyarderpro/homeku/actions/runs/41454495367) memproses request_id yang sama tanpa membuat folder video kedua.
- **Lulus di main (idle):** [41454647109](https://github.com/milyarderpro/homeku/actions/runs/41454647109) menjalankan 8 tes dan melewatkan commit video karena request masih `idle`.
- **Produksi sudah dibuktikan untuk workflow lama:** [run 41636775788](https://github.com/milyarderpro/homeku/actions/runs/41636775788) menyimpan [VID-004](../references/VID-004/analysis.md) sebelum v1.3. Jalur **narasi v1.3** belum bisa diklaim teruji di produksi sampai PR dan uji khusus diselesaikan.

Workflow produksi `.github/workflows/save-analysis.yml` sekarang hanya memicu pada **push ke main yang mengubah `requests/save.json`**. Workflow tidak memiliki `workflow_dispatch` dan tidak dipicu hanya oleh upload MP4. Jangan menyuruh pengguna memilih `actions-jpg-test` untuk prosedur produksi; itu branch pengujian historis.

## Asosiasi kawasan gaya (`common_regions`)

- Pada draft baru dalam YAML schema `2.1`, sertakan `architecture.common_regions` sebagai list nilai `north_america`, `south_america`, `europe`, `asia`, `africa`, atau `oceania` (boleh lebih dari satu, tanpa duplikat, `[]` jika tidak diketahui).
- Field ini hanya asosiasi gaya desain, **bukan** negara tempat bangunan berada, bukan peringkat prevalensi, dan bukan hasil identifikasi lokasi berdasarkan salju/lanskap.
- `scripts/validate_analysis.py` memeriksa field ketika hadir; analisis lama tanpa field tetap valid. `scripts/save_analysis_action.py` merender **Wilayah terkait gaya desain** pada Identitas Desain, dengan **Tidak diketahui** untuk list kosong atau field absen.
- Perubahan ini hanya menambah metadata visual: format request, trigger Actions, ID, ekstraksi JPEG, dan prosedur `save now` tidak berubah.

## Detail visual & narasi bahasa Indonesia (v1.3)

- **ChatGPT saja yang berperan sebagai AI.** ChatGPT mengamati tiap shot secara lengkap, menyusun English snake_case di `analysis.yaml` Schema 2.1 dan menulis narasi bahasa Indonesia natural dari YAML untuk tiga kategori `visible_details`. GitHub Actions **tidak** memanggil AI, tidak memerlukan API key AI atau SDK AI.
- Analisis exterior + lingkungan mencakup bentuk rumah, material/warna, ukuran/posisi pohon, daun, sawah/ladang (jika jelas), lanskap/pegunungan, langit, cuaca, dan relasi spasial yang terlihat. Interior mencakup geometri, material/finishing, furnitur, dekorasi, cahaya, hubungan antarobjek dan pandangan keluar jendela. Jangan berhalusinasi atau mewajibkan kuota label.
- Sebelum `save now`, ChatGPT membuat dan mereview `shot_narratives` **per shot dan per kategori**, berdasarkan YAML. Saat YAML diperbaiki, indeks dan narasi ikut diperbarui.
- Kontrak tambahan di `requests/save.json` tetap memakai request `schema_version: "1.0"`. Objek `shot_narratives` adalah properti **top-level** yang *opsional untuk kompatibilitas request historis*, tetapi **wajib untuk setiap analisis baru**.
- Struktur: kunci `shot-01`, `shot-02`, dst; setiap shot memiliki tepat kategori `architectural`, `furniture_and_props`, `environment`. Masing-masing berupa `{"text": "...", "covered_indices": [0, 1]}`.
- `covered_indices` merujuk **indeks 0-based** dalam daftar YAML kategori yang sama. Untuk setiap sumber berisi n item, daftar harus mencakup tepat `0..n-1` masing-masing sekali (urutan bebas). Untuk kategori sumber `[]`, isinya wajib `{"text": null, "covered_indices": []}`.
- Python menolak shot/kategori hilang atau ekstra, teks kosong/terlalu panjang, indeks duplikat/hilang/di luar rentang, tipe yang salah, atau input `shot_narratives` yang hadir tetapi invalid. Teks narasi diperlakukan sebagai **plain text** dan di-escape sebelum dimasukkan Markdown; tidak boleh menjadi HTML/Markdown aktif.
- Periksa kesetaraan makna di **review ChatGPT + manusia** sebelum persetujuan. Pemeriksaan indeks oleh Python hanya memastikan **kelengkapan struktural**, bukan bukti sempurna kesamaan semantik.
- **Tidak ada perubahan Schema 2.1**, tidak ada field narasi di YAML, tidak ada berkas narasi tambahan dalam `references/VID-XXX/`, tidak ada migrasi otomatis paket VID lama. Request lama tanpa `shot_narratives` masih memakai renderer bullet teknis lama; field hadir tetapi rusak **harus gagal aman tanpa fallback**.

Lihat [templates/shot-narratives.json](../templates/shot-narratives.json) untuk contoh payload yang perlu dicocokkan dengan YAML tiap video.

## Prasyarat pengguna

1. Unggah MP4 ke `main/video/<nama-file>.mp4` sebelum analisis, **langsung** di dalam folder `video` (tanpa subfolder). Contoh: `video/dreamsHouse002.mp4`. Saat ini README di folder video hanya petunjuk; keberadaan folder bukan berarti semua MP4 sudah tersedia.
2. Upload video yang sama ke chat untuk dianalisis **secara detail sepanjang shot**, susun YAML + narasi Indonesia, lalu review keduanya. AI boleh membaca GitHub sepanjang fase ini, tetapi **dilarang menulis** sebelum pesan valid `save now`.
3. Nama file sumber harus sama persis (case-sensitive) dengan `video.filename` di YAML. Video lokal yang nama filenya cocok **tidak otomatis terbukti memiliki byte identik**: sebaiknya bandingkan Git blob SHA-1 lokal dengan SHA pada tree main. Jika tidak bisa, jelaskan keterbatasan lalu minta konfirmasi pengguna sebelum menganggap sumber sesuai.
4. Pengguna menyimpan video **satu per satu**. Pastikan request sebelumnya sudah selesai/terverifikasi sebelum mengganti `requests/save.json`.
5. Izin Actions untuk menulis ke repository harus aktif; workflow sendiri mendeklarasikan `permissions: contents: write`. Jika push ditolak, periksa pengaturan GitHub dan log run.

MP4 asli tetap berada di `video/` setelah penyimpanan, sehingga ukuran riwayat Git dapat meningkat. Video berukuran besar mungkin memerlukan strategi penyimpanan lain; integrasi Git LFS **belum diterapkan**.

## Otorisasi dan format request

Pesan pengguna tersendiri persis `save now` (trim spasi, case-insensitive) adalah satu-satunya otorisasi standar untuk menyimpan hasil analisis. Pesan yang sekadar **menyebut** frasa itu bukan otorisasi. Pembaruan rules/kode lewat perintah terpisah tidak dihitung sebagai izin save analisis.

Saat pertama dibuat, `requests/save.json` berisi:

```json
{"schema_version": "1.0", "status": "idle"}
```

Setelah pesan `save now` valid, ChatGPT **menggunakan GitHub connector update_file** pada `main/requests/save.json`, menyertakan SHA blob request yang terbaru. Buat request_id stabil dan unik, lalu kirim **teks JSON** dengan struktur:

```json
{
  "schema_version": "1.0",
  "status": "approved",
  "request_id": "contoh-video-20261102-001",
  "video": {
    "path": "video/contoh.mp4",
    "blob_sha": "<SHA-GIT-BLOB-40-HEX-ASLI>"
  },
  "keyframe_times_s": [2.5, 7.3],
  "analysis_yaml": "<TEKS YAML 2.1 LENGKAP, bukan contoh ringkas>",
  "shot_narratives": {
    "shot-01": {
      "architectural": {"text": "Jendela besar terlihat berbingkai hitam.", "covered_indices": [0]},
      "furniture_and_props": {"text": null, "covered_indices": []},
      "environment": {"text": null, "covered_indices": []}
    }
  }
}
```

**Contoh di atas adalah cuplikan ilustratif dan bukan request siap dikirim.** Field `shot_narratives` harus mencakup *semua* shot dan cocok dengan setiap item sumber YAML. Template menunjukkan bentuk payload; AI menyiapkan narasi final saat review di chat. Ganti placeholder dengan path MP4 yang ditemukan, SHA aslinya, dan analisis YAML lengkap yang sudah direview; jumlah timestamp sama dengan `video.shot_count`, semuanya di dalam rentang waktu masing-masing shot. `video.id` boleh bernilai `PENDING` sampai runner menetapkan VID final. Tidak perlu mengirim `analysis_md`, JPEG, Base64, ZIP, atau MP4 melalui konektor. Seluruh AI tetap di chat; runner hanya membaca teks yang disetujui.

Path MP4 yang diterima runner: `video/<nama>.mp4` langsung, nama diawali alfanumerik dan berisi alfanumerik, titik, underscore atau dash. `blob_sha` harus SHA Git blob sumber pada HEAD yang dipakai runner, **bukan checksum SHA-256**. Request_id dibatasi 8–80 karakter dari huruf/angka/dash/underscore, dimulai alfanumerik. Tidak ada penguncian otomatis yang mencegah pengguna mengganti request saat Actions masih berjalan: disiplin **sequential save** wajib dijaga.

Jika respons konektor saat update tidak pasti, **baca ulang requests/save.json dan daftar run** sebelum mencoba lagi; gunakan request_id yang sama. Setelah request berhasil ditulis, statusnya **Processing/Queued**, bukan Saved.

## Perilaku runner yang benar-benar diimplementasikan

Saat request `approved` ditemukan, `scripts/save_analysis_action.py`:
1. Menghindari penyimpanan ulang dari request_id yang sudah memiliki marker di `references/VID-*/analysis.md`.
2. Memastikan `video/` path aman, file ada, Git blob SHA dari checkout sesuai request, serta jumlah shot dan waktu keyframe konsisten.
3. Jika properti `shot_narratives` hadir, validasi kesesuaian semua shot, kategori dan cakupan item YAML **sebelum** membuat folder. Payload yang rusak harus gagal aman; request lama tanpa properti tersebut diproses dengan renderer legacy.
4. Menentukan ID terkecil yang masih kosong `VID-XXX` berdasarkan folder yang ada pada checkout.
5. Mengambil frame video dari waktu yang dipilih dan mengodekannya menjadi JPEG melalui FFmpeg. Generator [`scripts/storyboard.py`](../scripts/storyboard.py) menyusun storyboard dengan Pillow mengikuti acuan gambar pengguna: **1–5 shot = 1 baris dengan jumlah kolom sesuai shot; >5 shot = 3 kolom, baris otomatis**. Tiap frame memakai rasio asli (padding bila perlu), margin seragam, judul/subtitle, dan caption scene/waktu/kamera. **Keyframe berasal dari frame video**, bukan file JPEG byte-identik dengan file preview ChatGPT; kompresi/ukuran gambar dapat berbeda.
6. Memperbarui `video.id` dan `shots[].keyframe` di YAML; membentuk laporan Markdown lewat fungsi `markdown()` dari YAML dan teks narasi yang sudah direview di chat (atau legacy renderer jika request lama). Narasi di-escape sebagai teks biasa. `templates/analysis.md` adalah **referensi susunan**, bukan mesin template yang dipakai otomatis.
7. Memanggil `scripts/validate_analysis.py`, lalu menulis `requests/result.json` dengan status `saved` dan request_id.
8. GitHub Actions meng-commit paket `references/VID-XXX/` dan `requests/result.json` **bersamaan**, push tanpa force, serta memverifikasi keberadaan file dan hasil validator pada runner.

Proses tidak memakai antrean paralel, retry otomatis konflik HEAD, ataupun Git Data API untuk memindahkan byte JPEG. Jika branch berubah dan push ditolak, Actions **gagal**; periksa run dan branch sebelum mengulang request dengan ID yang sama.

Saat request sudah tersimpan, eksekusi ulang menghasilkan `already_saved` dan melewati commit. Ini mencegah duplikasi berdasarkan **request_id**, bukan otomatis mencegah video yang sama tersimpan dengan request_id baru.

## Bagaimana memeriksa status dengan benar

- **Processing:** update request sudah berhasil, tetapi run yang sesuai masih antre/berjalan atau belum dapat dibuktikan selesai.
- **Saved:** run yang relevan benar-benar `success`, `requests/result.json` berisi `status: saved` dengan **request_id persis sama** dengan `requests/save.json`, folder final tersedia di `main/references/VID-XXX/`, dan berkas serta commit terverifikasi.
- **Not saved:** run gagal, SHA video tidak cocok, request bermasalah, commit gagal, atau verifikasi tidak lengkap. Cari alasan pada log Actions.
- **Already saved:** request_id yang sama ditemukan pada laporan video lama; tampilkan ID lama dan jangan buat yang baru.

**Penting:** `requests/result.json` hanya diperbarui pada *save baru yang berhasil*, bukan saat antre/gagal dan bukan status live. Field `run_id` dalam hasil berasal dari lingkungan Actions dan membantu menghubungkan status dengan run yang benar. Jika file result berisi request_id lama, statusnya **bukan** Saved untuk request baru.

Catatan: GitHub-generated push menggunakan GITHUB_TOKEN tidak memicu workflow push baru. Tindakan berhasilnya update request melalui connector sudah diuji di branch uji, tetapi pengguna harus memastikan run baru pada branch main saat save produksi.

**Perubahan layout tidak retroaktif:** update kode generator hanya berlaku untuk request yang menghasilkan paket baru. Folder `references/VID-XXX/` yang sudah tersimpan tidak disentuh oleh revisi script; jika ingin mengganti storyboard lama, perlu instruksi eksplisit terpisah dan verifikasi ulang.

## Troubleshooting cepat

| Kondisi | Tindakan |
|---|---|
| `video/<file>.mp4` tidak ditemukan | Upload MP4 ke `main/video/`, jangan hanya ke chat atau branch uji |
| MP4 mirip namanya tetapi SHA berbeda | Cocokkan video yang benar; jangan memaksa SHA |
| Tidak ada run baru | Periksa commit yang **mengubah** requests/save.json di main dan konfigurasi Actions |
| Run gagal saat tes | Periksa log instalasi Python, Pillow, FFmpeg dan keseluruhan unit test terbaru; jangan klaim Saved |
| Run gagal saat push | Periksa permission contents:write / branch protection dan perubahan HEAD; jangan force-push |
| Result JSON masih milik video lama | Jangan keliru menganggap Saved; periksa request_id dan run aktif |
| Request berulang tidak membuat commit | Normal jika sudah tersimpan dengan request_id sama |
| Narasi baru ditolak | Periksa semua shot/kategori, `covered_indices`, null untuk sumber kosong dan panjang teks; jangan fallback ke legacy secara diam-diam |
| Tidak ada folder baru sesudah upload video | Normal: MP4 upload **bukan** pemicu save |

## Riwayat migrasi

Alur lama ChatGPT Python → Git Data API → Base64 JPG telah dihapus dari jalur produksi, termasuk script, fixture, dan dokumentasi yang terkait. Uji historis branch `actions-jpg-test` tidak dibawa sebagai sumber analisis produksi. Data lama `references/VID-001/` tetap utuh.
