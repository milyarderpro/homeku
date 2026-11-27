# Alur audit HOMEKU 3.1

Jalankan empat fase berurutan dalam satu chat. Satu `audit.json` menyimpan isi audit dari awal sampai ekspor. Mulai dari [prompt audit](prompts/01-audit.md).

Periksa runtime dan MP4 dengan `python tools/audit.py readiness /path/rumah.mp4 --workspace work/audit`. Pasang dependensi dari `requirements.txt` jika pemeriksaan modul gagal. Lanjutkan setelah semua cek lulus.

## Waktu audit

Catat `start` sebelum memulai tiap fase dan `finish` setelah fasenya selesai. Gunakan workspace audit yang sama, termasuk sebelum `prepare`. Empat nama fase CLI secara berurutan adalah `shot-mapping`, `camera`, `design-media`, dan `validation-export`. Akhiri fase kamera setelah `check-camera` lulus dan fase terakhir setelah ekspor ZIP selesai. Saat melanjutkan fase yang terputus, periksa ringkasan dan gunakan penanda yang sudah dibuka.

~~~sh
python tools/audit.py phase work/audit shot-mapping start
python tools/audit.py phase work/audit shot-mapping finish
python tools/audit.py performance work/audit
~~~

`performance` merangkum waktu berlalu tiap fase serta durasi dan percobaan perintah. Gunakan `--session` pada `review` dan `export` agar hasilnya masuk log workspace yang sama. Ringkasan dapat disimpan di workspace untuk pilot.

## Fase 1 — Pemetaan shot

Tonton perjalanan video, jalankan `inspect`, lalu konfirmasi cut sebenarnya. Opsi `inspect /path/rumah.mp4 --cut-preview work/cut-preview` menampilkan maksimal 12 dugaan dari perubahan gambar, dengan pasangan frame native dan PTS. Periksa kedua gambar dan perjalanan video sebelum mengambil indeks `after.index`. Abaikan perubahan yang terjadi dalam satu take. Simpan indeks native **frame pertama setelah setiap cut** dalam `work/cuts.json`. Gunakan `[]` untuk satu take kontinu, termasuk ketika kamera melewati beberapa area.

~~~sh
python tools/audit.py inspect /path/rumah.mp4
python tools/audit.py prepare /path/rumah.mp4 --cuts-file work/cuts.json --output work/audit
~~~

Workspace berisi `session.json`, kerangka `audit.json`, `audit-info.json` dan lembar frame. Prepare menyiapkan baseline 6 FPS, batas native dan midpoint. Sumber ≤6 FPS atau shot <1 detik memakai seluruh native. Gunakan `--resume` dengan MP4 dan cut yang sama. Jalankan `python tools/audit.py status work/audit/session.json` untuk melihat frame baseline yang belum dilihat dan status pemeriksaan kamera per shot. Field `incomplete_passes` mencantumkan ID pass dan indeks frame yang deklarasinya belum lengkap pada pass itu, termasuk saat frame yang sama sudah dilihat lewat pass lain. Sertakan `--candidate work/candidate/rumah --receipt work/review.md.json` untuk membandingkan kandidat dengan receipt. Buka frame yang belum diperiksa sebelum memperbarui deklarasi viewed.

## Fase 2 — Audit kamera

Baca [metode visual](visual-audit.md) dan [contoh kamera](camera-cases.md). Periksa frame secara kronologis sebelum mengisi kamera per shot. Gunakan `motion-hints` untuk meninjau tren dan gap pada baseline. Gunakan [pengukuran jangkar](visual-audit.md#pengukuran-dimensi-jangkar) untuk membandingkan ukuran bagian yang sama pada dua frame. Catat batas setiap fase, `notation`, pengamatan depth, translation, rotation, bukti, tempo, narasi Indonesia, dan Production Start jika awal sumber tertutup transisi. Tentukan label atau fungsi area yang diperlukan untuk fokus tanpa menunda analisis kamera untuk mengisi profil desain.

Saat pertanyaan visual belum terjawab, ambil frame tambahan pada interval terkait. Sesuaikan waktu contoh dengan PTS shot dan jelaskan apa yang diperiksa.

~~~sh
python tools/audit.py sample --session work/audit/session.json --shot-id shot-02 --fps 10 --start 2.4 --end 2.9 --reason "Perubahan oklusi kusen untuk membedakan Orbit dan Pan"
~~~

Gunakan `--native` jika interval tersebut perlu diperiksa lebih rapat. Untuk bukti tertentu, gunakan `sample --session work/audit/session.json --frames 24 31 --reason "Periksa frame Production Start"`. Lihat gambar lalu deklarasikan viewed. Gunakan `--all-passes --all` setelah seluruh pass dilihat atau `--pass-id <ID> --frames <INDEKS...>` sesuai pemeriksaan.

~~~sh
python tools/audit.py mark-viewed work/audit/session.json --all-passes --all
python tools/audit.py check-camera work/audit/session.json
~~~

Sebelum menjalankan `check-camera`, cocokkan notasi dengan observasi dan frame pada masing-masing fase. Periksa arah badan, sapuan, Orbit dan Pan bersamaan, serta komponen, qualifier atau perkiraan besaran yang terlewat. Setelah pemeriksaan lulus, ringkas gerakan, tempo, dan Production Start per shot di chat. Lanjutkan ke fase 3 dalam chat yang sama.

Selesaikan interpretasi visual secara independen sebelum menyimpan notasi final. Gunakan contoh kamera sebagai acuan kedalaman analisis dan tingkat detail, bukan sebagai pengganti pemeriksaan frame.

Jika suatu komponen, qualifier, atau estimasi besaran belum dicantumkan, pastikan aspek tersebut telah dinilai dan bukan sekadar terlewat.

Prioritaskan notasi yang informatif untuk reproduksi kamera tanpa melampaui bukti visual yang tersedia. Jangan mengakhiri fase kamera hanya karena pemeriksaan teknis telah lulus.

## Fase 3 — Audit desain dan kurasi media

Baca [panduan desain](design-audit.md) dan [panduan JSON](json-guide.md). Isi identitas desain, proporsi, kronologi area, detail dan fakta, framing, pencahayaan, panel, serta Overview. Pilih bukti dari frame yang sudah dilihat dan tandai viewed setelah memeriksa pilihan tambahan.

Jika ada koreksi kamera yang disengaja, periksa kembali shot tersebut dengan bukti terkait. Untuk satu fase atau fakta area, gunakan [`edit-record`](json-guide.md#mengisi-satu-fase-atau-fakta). File patch `update-shot` berisi objek JSON yang digabungkan ke shot. Array yang diberikan mengganti array utuh dan ID, batas, serta jenis transisi terikat pada sesi.

~~~sh
python tools/audit.py update-shot work/audit/session.json --shot-id shot-02 --patch work/koreksi.json
python tools/audit.py check-camera work/audit/session.json --shot-id shot-02
~~~

Jalankan ulang pemeriksaan per shot untuk setiap perubahan kamera atau Production Start. Jika MP4 atau batas cut berubah, siapkan workspace baru dan ulangi pemetaan serta audit kamera.

## Fase 4 — Validasi dan ekspor

Isi metode, batas pemeriksaan, dan identitas model yang diketahui di `audit-info.json`. Build model yang tidak diketahui diisi `null`. Complete mempertahankan pilihan panel shot biasa, menyamakan panel Start dengan Production Start bila dipilih, dan menyalin deklarasi viewed. Jalankan preflight sebelum render.

~~~sh
python tools/audit.py complete work/audit/audit.json --session work/audit/session.json
python tools/audit.py check-input /path/rumah.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json --session work/audit/session.json
python tools/audit.py draft /path/rumah.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json --session work/audit/session.json --output work/candidate
~~~

Untuk revisi, isi nomor baru pada audit dan berikan `--supersedes work/supersedes.json` pada `check-input` dan `draft`. File itu berisi `revision` dan `content_sha256` dari entri aktif. Jika input gagal, perbaiki path yang dilaporkan dan ulangi pemeriksaan terkait.

Cocokkan laporan dan media kandidat dengan isi audit. Periksa laporan enam bagian, urutan kolase, caption, Overview, dan Storyboard. Default JPEG memakai kualitas 91 serta skala 1. Bila dimensi perlu diperkecil, sesuaikan `--scale`, `--overview-scale`, `--storyboard-scale` atau `--columns` sebelum review. Batas tiap JPEG 60 juta piksel, sisi 65.000 px, 95 MiB. Batas ZIP terurai 256 MiB.

~~~sh
python tools/audit.py review work/candidate/rumah --output work/review.md --session work/audit/session.json
python tools/audit.py export work/candidate/rumah --receipt work/review.md.json --output work/final --session work/audit/session.json
~~~

Gunakan Markdown dari field `checklist` untuk menelusuri hasil validasi teknis dan membuka gambar kandidat yang sudah dirender. Review dengan `--session` memeriksa metadata sumber, PTS native, dan deklarasi viewed terhadap MP4 sesi. Centang pemeriksaan visual setelah melihat laporan dan media. Gunakan sesi yang sama untuk setiap `review` agar lembar menampilkan perubahan notasi, bukti, panel termasuk cakupan areanya, dan media dibanding snapshot berbeda yang terakhir direview. Langsung ekspor setelah review berhasil. Ambil tautan laporan dan gambar dari checklist snapshot yang dikembalikan `review`. Ambil tautan ZIP dari field `package` keluaran `export`. Tampilkan ringkasan shot, laporan, media, dan tautan ZIP dalam satu balasan agar pengguna bisa memeriksa dan memilihnya. Berikan ZIP terbaru sesudah koreksi. [Kontrak paket](contracts/package.md)
