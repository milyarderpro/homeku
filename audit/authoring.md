# Menyiapkan audit HOMEKU 3.0

Baca [panduan visual](visual-audit.md). Tulis pengamatan di satu `audit.json`. Helper menyiapkan frame dan metadata dari video sumber.

## Siapkan workspace

Jalankan `inspect` dan tentukan cut nyata pada video. Simpan indeks native **frame pertama setelah setiap cut** dalam `work/cuts.json`. Gunakan `[]` untuk satu take kontinu, termasuk jika kamera melewati beberapa area.

~~~sh
python tools/audit.py inspect /path/rumah.mp4
python tools/audit.py prepare /path/rumah.mp4 --cuts-file work/cuts.json --output work/audit
~~~

Workspace berisi `session.json`, kerangka `audit.json`, `audit-info.json` dan sheet. Baseline mencakup 6 FPS dan batas native. Sumber ≤6 FPS atau shot <1 detik memakai seluruh frame native. Helper menyiapkan pula frame terdekat dari midpoint. Gunakan `--resume` pada sumber dan cut yang sama untuk mempertahankan isi serta deklarasi sebelumnya.

## Tulis pengamatan

Isi nama gaya dalam bahasa Inggris dan narasi dalam bahasa Indonesia. Tulis rentang luas lantai, identitas area, detail desain beserta fakta dan bukti, framing awal, Overview, serta kamera dan tempo. [Panduan JSON](json-guide.md) menjelaskan field. Contoh normal dan multi area merupakan fixture sintetis.

Tulis pengamatan depth, translation dan rotation sebelum notasi tiap fase. Angka skala dan sudut opsional per komponen. Angka tunggal dan rentang sama-sama sah. Contoh `Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out)`.

Periksa sheet lalu tandai frame yang sudah dilihat. Gunakan `--all-passes --all` setelah semua pass selesai diperiksa atau `--pass-id <ID> --frames <INDEKS...>` untuk bagian yang sudah dilihat.

~~~sh
python tools/audit.py mark-viewed work/audit/session.json --all-passes --all
python tools/audit.py sample --session work/audit/session.json --shot-id shot-02 --fps 10 --start 2.4 --end 2.9 --reason "Perubahan oklusi kusen untuk membedakan Orbit dan Pan"
~~~

Sesuaikan waktu pendalaman dengan PTS nyata dalam shot. Gunakan `--native` bila diperlukan, atau `sample --session work/audit/session.json --frames 24 31 --reason "Pilihan Overview tambahan"` untuk indeks tertentu. Lihat frame baru sebelum mendeklarasikan viewed.

Koreksi satu shot dapat dikirim lewat file berisi objek JSON, misalnya `{"camera":{"description":"Kamera mundur menuju lorong."}}`. Helper menggabungkan objek dan mengganti array utuh bila disertakan. Update area global langsung di sumber. Shot ID, batas waktu dan jenis transisi terkunci pada helper.

~~~sh
python tools/audit.py update-shot work/audit/session.json --shot-id shot-02 --patch work/koreksi.json
~~~

## Periksa input

Isi metode, batas pemeriksaan dan identitas model yang diketahui di `audit-info.json`. Build yang tidak diketahui diisi `null`. `complete` menata notasi, menetapkan pilihan panel native yang ditentukan kontrak, dan menyalin deklarasi viewed dari sesi.

~~~sh
python tools/audit.py complete work/audit/audit.json --session work/audit/session.json
python tools/audit.py check-input /path/rumah.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json
~~~

Perbaiki field yang ditunjuk `check-input`. Untuk bukti yang belum dilihat, ambil frame yang tepat dan periksa sebelum memperbarui deklarasi. Untuk tahap peninjauan dan penyerahan, ikuti [kontrak paket](contracts/package.md).

Untuk pertanyaan visual yang masih ambigu, gunakan [bantuan statistik gerak 2D](visual-audit.md#bantuan-statistik-gerak-2d) bila lingkungan mendukungnya.

## Periksa isi sebelum memperlihatkan kandidat

- Cocokkan cut, scope area, pengamatan tiga sumbu, notasi, tempo, dan bukti pada shot yang sama.
- Baca narasi desain bersama fakta yang terkait. Periksa detail yang mudah tertukar, seperti bentuk bukaan, bahan tampak, lampu dan fungsi furnitur.
- Periksa panel awal terhadap posisi Camera Start. Lihat cakupan setiap Overview pada frame terpilih.
- Baca laporan enam bagian dan periksa caption serta gambar pada semua kolase. Untuk penyesuaian ukuran, ubah parameter render sebelum peninjauan berikutnya.

Draft memakai kualitas JPEG 91 dan skala 1 secara default. Gunakan `--scale`, `--overview-scale`, `--storyboard-scale` atau `--columns` jika tata letak melebihi batas. Satu JPEG dapat memuat sampai 60 juta piksel dengan sisi sampai 65.000 px. Batas file 95 MiB dan batas ZIP terurai 256 MiB.

## Tinjau kandidat dan serahkan ZIP

~~~sh
python tools/audit.py draft /path/rumah.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json --output work/candidate
python tools/audit.py review work/candidate/rumah --output work/review.md
~~~

Tampilkan laporan enam bagian, Overview, Storyboard, dan semua kolase. Jika ada koreksi, perbarui audit kerja dan ulangi draft serta review. Simpan receipt terbaru di luar folder kandidat. Setelah persetujuan pengguna atas seluruh snapshot, jalankan ekspor.

~~~sh
python tools/audit.py export work/candidate/rumah --receipt work/review.md.json --output work/final
~~~

Serahkan satu ZIP final tanpa video. Untuk revisi, gunakan nomor berikutnya pada audit dan berikan `--supersedes` dengan revision dan content_sha256 dari entri aktif.
