# Authoring HOMEKU2.4

Baca visual-audit.md sebelum menyimpulkan isi. Helper menghitung metadata; AI menulis pengamatan. audit.json satu sumber final. Semua perintah berjalan di workspace chat; tidak ada pekerjaan teknis tambahan untuk pengguna.

## 1. Siapkan sumber dan baseline sekali

Jalankan inspect, periksa cut nyata pada sumber dan catat indeks frame pertama setiap shot sesudah shot01. Simpan sebagai array JSON di work/cuts.json; [] bila satu take. Cut adalah edit video, bukan pergantian area. Jangan menyalin cut dari video contoh.

~~~sh
python tools/audit.py inspect /path/<id>.mp4
python tools/audit.py prepare /path/<id>.mp4 --cuts-file work/cuts.json --output work/audit
~~~

Hasil: audit.json kerangka, audit-info.json, session.json, pass/sheets dan performance.jsonl. PTS, frame awal/akhir, midpoint dan selected dihitung otomatis. Kerangka belum audit valid: area/Overview/fakta/gaya dan narasi harus diisi AI setelah melihat.

prepare membuat baseline6FPS seluruh shot dalam satu batch dan tambahan midpoint jika belum tercakup. Sumber≤6FPS/shot<1s native. Lihat semua sheet sebelum menyatakan viewed. Gunakan prepare dengan --resume untuk session yang sama; isi pengamatan tidak ditimpa. Sumber/cut berbeda memerlukan workspace baru; frame cache tetap hanya alat kerja.

## 2. Isi pengamatan dan nyatakan viewed

Tulis identitas/profil English, detail Indonesia, estimasi luas rentang wajib, area fisik/visibility/route, arsitektur/furnitur/lingkungan, fakta/coverage/facet_roles, Camera Start, komposisi, gerakan sederhana/teknis dan tempo. Contoh sintetik ada di audit/examples/normal/ dan multi/, bukan isi audit nyata.

Notasi fase menjadi input kamera utama; complete menghitung parsed metadata dan summary. Pan/Orbit jelas memakai perkiraan ~°; Dolly/Zoom ~×. Asumsi wajar sah; tidak perlu focal length/kalibrasi. scale_measurement boleh null; estimate_basis cukup singkat. Semua moderate sah. Tidak ada SIFT/RANSAC rutin atau esai pembuktian.

Setelah benar-benar melihat seluruh frame yang disediakan:
~~~sh
python tools/audit.py mark-viewed work/audit/session.json --all-passes --all
~~~
Jika baru melihat sebagian, gunakan --pass-id <ID> --frames <INDEKS...>. Jangan memakai --all sebelum pemeriksaan. Selected/cache bukan viewed. Pass ID/daftar sheet tersedia pada output prepare/session.

Pendalaman hanya untuk pertanyaan spesifik:
~~~sh
python tools/audit.py sample --session work/audit/session.json --shot-id shot-02 --fps 10 --start <PTS_AWAL> --end <PTS_AKHIR> --reason "Perubahan oklusi kusen belum membedakan Orbit dan Pan"
~~~
Boleh --native atau seluruh shot jika memang perlu. Tanpa --start/--end memakai batas shot presisi session. Periksa frame tambahan lalu deklarasikan viewed untuk pass tersebut. Tidak otomatis mengulang10FPS semua shot. Untuk pilihan panel/Overview baru yang belum tercakup, gunakan sample --session work/audit/session.json --frames <INDEKS...> --reason "Pilihan panel/Overview tambahan"; helper menyiapkan record native presisi. Lihat gambar lalu deklarasikan viewed.

## 3. Lengkapi metadata dan periksa sebelum render

Isi provider/model yang diketahui pada audit-info; build tidak diketahui null. native memakai mode frame-by-frame, bukan native; helper sudah menghitung recordnya.
~~~sh
python tools/audit.py complete work/audit/audit.json --session work/audit/session.json
python tools/audit.py check-input /path/<id>.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json
~~~

complete hanya memperbarui whitelist mekanis: batas/PTS/midpoint/parser/summary/pengaruh gaya dari klaim profil/log pass. Ia tidak menebak ruang, memindahkan evidence, membuat fakta, atau mengubah arah/besaran/tempo. Area/shot yang tertukar dilaporkan. Tidak mengonversi JSON lama atau mengedit kandidat ter-render. Perubahan mekanis ditampilkan; isi audit tetap pada audit.json.

check-input mengumpulkan kesalahan independen tanpa JPEG. Perbaiki path yang ditunjuk. Bila schema rusak, perbaiki dahulu agar pemeriksaan lanjut aman. Jangan mengarang bukti/angka/fakta untuk lolos. Tidak perlu menulis skrip builder khusus video.

## 4. Kandidat, koreksi dan ekspor

~~~sh
python tools/audit.py draft-v2 /path/<id>.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json --output work/candidate
python tools/audit.py review work/candidate/<id> --source /path/<id>.mp4 --output work/review.md
~~~

draft memeriksa input sebelum render dan memakai cache/frame/media yang cocok. Check-input manual berguna saat mengisi; tidak wajib diulang bila langsung draft. Tampilkan MD lengkap enam bagian, Overview, Storyboard dan semua kolase. Progres singkat saat berpindah tahap jika UI mendukung; tanpa jeda konfirmasi internal.

Koreksi sumber kerja, complete bila metadata terkait berubah, lalu draft/review lagi. Cache tidak menggantikan tinjauan snapshot terbaru. Setelah persetujuan keseluruhan nyata:
~~~sh
python tools/audit.py export-v2 work/candidate/<id> --source /path/<id>.mp4 --receipt work/review.md.json --output work/final
~~~

Export tidak merender ulang. ZIP tanpa video, cache, log, sheet atau receipt. MP4 kanonis lokal terpisah. performance.jsonl mencatat durasi alat/cache/retry; selang percakapan dan jeda persetujuan bukan durasi komputasi.
