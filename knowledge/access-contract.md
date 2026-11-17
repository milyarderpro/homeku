# Akses pengetahuan melalui web dan konektor GitHub

Kedua jalur membaca pustaka yang sama. URL repository mengidentifikasi sumber; branch atau commit pada URL menentukan versi. Mulai dari [pengetahuan inti](ai-knowledge.md), lalu gunakan [peta bacaan](README.md).

## Jalur bacaan yang ringkas

Inti → tema terkait → direktori dan profil relevan → bukti yang diperlukan. Direktori repository bukan urutan baca wajib. Sampel temporal dan JSON pendukung tidak perlu dimuat sekaligus.

| Peran | Berkas kanonis |
| --- | --- |
| Pintu masuk | README.md |
| Pengetahuan inti | knowledge/ai-knowledge.md |
| Peta tema | knowledge/README.md |
| Menemukan contoh | knowledge/directories/README.md |
| Memahami satu sumber | knowledge/reference-profiles/REFERENCE_ID.md |
| Rincian hubungan dan framing | knowledge/design-evidence/REFERENCE_ID.md |
| Anotasi sumber | references/REFERENCE_ID/analysis.yaml |
| Narasi sumber | references/REFERENCE_ID/analysis.md |
| Gambar sumber | references/REFERENCE_ID/shot-NN.jpg |

## Web

Buka README dan ikuti tautan Markdown pada versi repository yang dipilih. [Konten mentah pengetahuan inti pada branch default](https://raw.githubusercontent.com/milyarderpro/homeku/main/knowledge/ai-knowledge.md) merupakan alternatif bila alat dapat membaca konten mentah. Untuk versi yang dikunci, gunakan commit yang sama pada URL halaman dan URL mentah.

Halaman GitHub dapat mengandung navigasi tambahan. Gagal memuat halaman, gambar atau raw file merupakan kegagalan akses berkas tersebut; jangan mengisi isinya dari dugaan atau menganggap semua file repository sudah dibaca.

## Konektor GitHub

Gunakan owner/repo, path kanonis di atas dan ref yang sama. Pencarian file dapat membantu bila alat mendukung dan indeksnya memuat versi yang dicari. Hasil pencarian branch default belum membuktikan isi commit lain; pembacaan file dengan ref eksplisit menjadi rujukan versinya.

Tidak perlu clone, menjalankan skrip, memasang database atau memakai API pencarian buatan khusus. Repository privat memerlukan jalur terautentikasi yang memiliki akses.

## Teks dan bukti visual

Profil dan modul tematik dapat dibaca sebagai teks. Deskripsi tersebut melaporkan pengetahuan atau anotasi tersimpan; pembacaan teks tidak membuktikan AI sudah melihat gambar maupun video.

Label gerak tetap interpretasi sampai didukung pemeriksaan yang sesuai. Tiga sampel temporal tidak membuktikan seluruh durasi. Bukti baru yang tidak bisa diakses tetap belum diperiksa.

## Pendukung yang dibuka bila diperlukan

| Pendukung | Fungsi |
| --- | --- |
| taxonomy/ dan enrichment/ | Kamus dan pemetaan label, bukan verifikasi visual |
| design-evidence/*.json | Pointer dan catatan terstruktur pendamping halaman bukti |
| temporal/ | Gambar sampel dan timestamp |
| reviews/ | Cakupan review AI dan keterbatasannya |
| aggregates.json dan diversity.json | Definisi hitungan dan daftar sumber |
| release.json, releases/, source-manifest.json | Identitas snapshot dan revisi sumber |
| similarity/ | Kandidat kemiripan untuk pemeliharaan |

Request penyimpanan, fixture tes, rencana implementasi, laporan evaluasi dan instruksi pemeliharaan berada di luar bacaan kreatif utama. Penambahan arsip tidak otomatis memperbarui snapshot pengetahuan.

## Penafsiran versi dan klaim

[Snapshot sumber](release.json) mengikat ID dan hash anotasi/video. Commit Git mengikat versi dokumen yang dibaca. Bandingkan web dan konektor pada commit yang sama; jangan menyamakan keberhasilan satu jalur dengan jalur lainnya.

Confidence dan cakupan review menjelaskan klaim sumber. Semua referensi tersimpan tetap boleh menginspirasi desain baru. Tidak ada syarat verifikasi manual.

Hasil uji akses dan batas penilaiannya dicatat dalam [catatan evaluasi akses](../evaluations/stage7/README.md). Keberhasilan membuka file dan kualitas jawaban AI adalah pengukuran berbeda.
