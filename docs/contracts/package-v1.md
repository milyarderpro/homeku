# Kontrak paket HOMEKU 1.1 — provisional

Paket baru memakai 1.1. Parser tetap menerima 1.0 sebagai format lama secara eksplisit; isi dan cakupannya tidak dianggap telah memenuhi audit 1.1.

Format 1.1 menyempurnakan kontrak teknis awal Phase 1. Pengalaman tujuh pilot pada Phase 2 dapat menghasilkan revisi berversi; parser tidak menebak atau menerima versi baru secara diam-diam.

## Identitas dan ZIP

Nama `<id>-r0001.zip`; satu folder teratas `<id>/`. ID mengikuti stem MP4, 1–80 karakter ASCII huruf/angka/underscore/hyphen, dimulai huruf atau angka. Kapitalisasi dipertahankan; tabrakan kapitalisasi ditolak. Revisi 1–9999, dimulai 1 dan bertambah satu.

```text
<id>/
  analysis.md
  manifest.json
  source.mp4                  # Hanya jika sumber belum tersedia
  media/
    storyboard.jpg
    shot-01/
      area-overview.jpg
      start.jpg
      middle.jpg
      end.jpg
      reveal-01.jpg           # Opsional
      detail-01.jpg           # Opsional
    shot-02/
      ...
```

Tidak ada motion/, klip per shot, seluruh frame video, executable atau file tambahan yang tidak tercantum. ZIP maksimal 256 MiB terkompresi maupun hasil ekstraksi, 2000 entri, 95 MiB per file; analysis.md dan manifest.json maksimal 2 MiB masing-masing. Direktori ZIP boleh ada; symlink, file spesial, path traversal, path absolut, enkripsi dan path bentrok ditolak. Gambar harus JPEG yang dapat didekode, maksimal 60 juta piksel.

## Manifest

[Schema JSON](manifest-v1.schema.json) adalah definisi field yang diperiksa. Seluruh field wajib, termasuk nilai null yang diizinkan.

| Field | Isi |
| --- | --- |
| contract_version | String `1.1` untuk audit baru; `1.0` masih dibaca sebagai legacy |
| purpose | `reference` untuk paket nyata; `fixture` hanya untuk tes terisolasi |
| id, revision | Identitas yang sama dengan ZIP, folder dan tabel identitas MD |
| supersedes | null pada revisi 1; berikutnya objek revision dan content_sha256 versi aktif yang diganti |
| source | path `video/<id>.mp4`, SHA-256 aktual, duration_s stream, width/height tampilan, fps numerator/denominator, video_stream_index |
| audit | method, reviewed_ranges, limitations, created_at berzona waktu dan identitas AI yang diketahui |
| media | Semua JPEG: path, SHA-256, kind, shot_id, timestamp_s, width, height, derived_from, crop |

`audit.reviewed_ranges` berisi start_s/end_s dan mode `sampling`, `playback`, atau `frame-by-frame`. Gabungan rentang mencakup durasi sumber; mode menjelaskan metode yang benar-benar digunakan. Nilai `model_build` boleh null; versi model yang tidak diketahui tidak dikarang.

Source harus tersedia dalam ZIP atau di video/ dengan hash cocok. Importer membaca metadata menggunakan ffprobe; durasi mengikuti stream video pertama non-cover-art, dengan fallback durasi container jika stream tidak mencatat durasi. Width/height mengikuti orientasi tampilan; fps adalah avg_frame_rate. Toleransi pembulatan durasi 0.001 detik. Hash di manifest adalah SHA-256 file, bukan Git blob SHA-1.

`content_sha256` dihitung importer dari daftar path dan SHA-256 isi folder yang diurutkan, tanpa source.mp4. Identitas ini mengikat laporan, manifest dan semua media; manifest sudah mengikat hash sumber. Nilainya tersedia dalam registry dan hasil validate, untuk supersedes revisi berikutnya.

## Media dan asal bukti

| kind / nama | Ketentuan |
| --- | --- |
| area-overview / shot-XX/area-overview.jpg | Satu frame utuh yang paling jelas dan luas memperlihatkan area; biasanya awal untuk IN dan akhir untuk OUT |
| start, middle, end | Frame awal, pertengahan dan akhir setiap shot, disimpan terpisah |
| reveal / reveal-NN.jpg | Opsional untuk bagian area yang belum terwakili |
| detail / detail-NN.jpg | Opsional; dapat berupa crop detail dari sumber |
| storyboard / storyboard.jpg | Gabungan seluruh area-overview dalam urutan shot, disusun ke bawah, dengan label shot, area dan timestamp |

Frame utuh mempertahankan dimensi dan rasio tampilan sumber. Frame tidak diperluas generatif atau dijadikan panorama. Timestamp sumber memakai detik desimal dan harus berada di dalam interval shot [start_s, end_s). Boundary frame berada dalam sekitar satu frame awal dan dua frame sebelum akhir; middle berada dalam satu frame dari midpoint. VFR atau batas shot yang ambigu perlu dikalibrasi pada pilot; jangan mengklaim ketepatan frame asli hanya dari fps rata-rata.

Semua media selain storyboard memiliki shot_id dan timestamp_s. `derived_from` berupa daftar kosong, `crop` null. Khusus detail crop, crop adalah [x, y, width, height] dalam koordinat frame tampilan sumber pada timestamp terkait; dimensi JPEG sama dengan ukuran crop.

Storyboard mempunyai shot_id/timestamp_s/crop null dan derived_from berisi semua path area-overview dalam urutan shot. Asal, urutan dan integritas file diperiksa secara teknis; kesesuaian piksel dengan sumber, label gambar, keterbacaan dan kebenaran interpretasi diperiksa saat audit/pilot.

MD mencatat overview_role start/middle/end berdasarkan sepertiga awal/tengah/akhir shot, timestamp dan alasan pemilihan. Untuk Dolly-In murni biasanya start; Dolly-Out murni biasanya end. Pengecualian dijelaskan dalam overview_exception. Pan/orbit/gabungan dipilih dari cakupan nyata. Simpan posisi serta arah pandang kamera dan peran frame agar penggunaan untuk prompt gambar sesuai lintasan, termasuk pandangan serong/samping.

## Penerimaan dan revisi

Audit/koreksi isi selesai di chat sebelum ZIP dibangun dari keseluruhan revisi final. Upload menjadi penyerahan versi tersebut. Repo memeriksa struktur, integritas dan konsistensi; tidak mengaudit ulang kebenaran visual atau meminta review isi baru.

Replay ZIP identik menghasilkan unchanged tanpa commit baru. ZIP yang dikompresi ulang dengan isi revisi aktif identik juga unchanged. Perubahan isi dengan ID/revisi aktif yang sama ditolak. Revisi baru menyebut supersedes yang benar. Sumber aktif identik pada ID lain ditolak berdasarkan hash; kesamaan rumah pada video berbeda tidak disimpulkan.

Paket fixture ditolak di repo produksi. Tes memerlukan root berbeda dari repo tooling dan marker .homeku-fixture-root.


## Log pemeriksaan frame pada 1.1

`audit.frame_reviews` wajib dan berisi satu atau beberapa lintasan per shot. Gabungan lintasan harus mencakup seluruh shot tanpa gap pada minimal 10 FPS, atau seluruh frame native. Shot panjang boleh diperiksa dalam rentang terbatas; setiap rentang menyertakan frame asli pertama/terakhirnya. Helper selalu menyertakan frame asli pertama/terakhir dalam interval. Rentang pendalaman boleh tumpang tindih baseline; semuanya harus benar-benar diperiksa.

| Field record | Makna |
| --- | --- |
| shot_id | Shot yang diperiksa |
| start_s / end_s | Interval waktu sumber [start, end), dalam batas shot |
| mode | sampling atau frame-by-frame |
| sampling_fps | FPS target sampling (minimal 10); null pada mode frame-by-frame |
| selected_frame_indices | Indeks asli berbasis 0, berurutan, yang dipilih dari PTS sumber |
| viewed_frame_indices | Indeks yang benar-benar dilihat; seluruh pilihan harus selesai diperiksa sebelum paket diekspor |
| reason | Tujuan baseline atau alasan pendalaman, misalnya orbit/pan belum terpisah |

Jumlah frame adalah panjang daftar indeks, bukan estimasi durasi × FPS. FPS sumber ada dalam source.fps; timestamp tepat diperoleh dari PTS sumber. Mode native tidak membatasi ke 30 FPS. Sampel di atas FPS sumber menggunakan semua frame tersedia, tanpa duplikasi/interpolasi. Reviewed_ranges tetap mencatat cakupan metode keseluruhan, selaras dengan frame_reviews dan method/limitations.

Validasi memeriksa indeks terhadap video dan kelengkapan deklarasi, bukan membuktikan AI sungguh melihat atau benar menafsirkan frame. Helper sample mengisi viewed_frame_indices kosong; AI mengisinya hanya setelah melihat. Frame/log kerja sementara tidak disertakan sebagai file tambahan ZIP. Log ringkas masuk manifest, tanpa seluruh JPEG pemeriksaan.
