# Hasil implementasi tahap 6–7

Implementasi 17 November 2026. Snapshot sumber pengetahuan: 2026-11-17-stage-6-7. Repo tetap menjadi pustaka desain; alur proyek dan prompt akhir berada pada plugin/master prompt mendatang.

## Tahap 6 — Pintu masuk dan bacaan

Jalur utama: README → pengetahuan inti → tema terkait → contoh relevan → bukti bila diperlukan. Data pendukung tetap berada pada path aslinya, sehingga hash dan tautan bukti tidak rusak. Tidak ada analisis ulang video pada tahap ini.

| Bacaan | Panjang saat diuji |
| --- | --- |
| README root | 228 kata |
| Peta bacaan | 326 kata |
| Pengetahuan inti | 788 kata |
| Profil individual | 493–722 kata |

Hitungan menggunakan pemisahan whitespace, bukan token model. Inti dapat dipahami tanpa mengambil gambar. Sembilan tema mencakup arsitektur, interior, lanskap, cahaya/palet, ruang, kontinuitas, sinematografi, kompatibilitas dan orisinalitas. Modul kontinuitas membedakan identitas tetap, perubahan pandangan, dunia luar jendela dan batas bukti temporal.

Direktori dikelompokkan menurut kebutuhan desain. Profil memberi deskripsi kalimat dari label tersimpan; deskripsi itu tidak menambahkan verifikasi fisik. Metadata hash ditempatkan sebagai pendukung. JSON, review, media temporal, manifest dan kemiripan tidak menjadi bacaan wajib.

## Publikasi kandidat

Kandidat tersedia pada [branch uji](https://github.com/milyarderpro/homeku/tree/codex/knowledge-stage-6-7).

Kedua jalur diuji pada commit yang sama: [217c63a473f5b6d9d967b1cb3372dae355ffed8b](https://github.com/milyarderpro/homeku/tree/217c63a473f5b6d9d967b1cb3372dae355ffed8b). Commit pengujian tersebut mengandung seluruh bacaan yang diuji. Commit laporan setelahnya mempertahankan fingerprint bacaan yang sama; perubahan laporan dan validator tidak dianggap pengujian ulang model.

Branch utama dan staging pengguna tidak diganti oleh proses publikasi kandidat. URL branch atau commit uji diperlukan untuk membaca kandidat sebelum perubahan ini diterbitkan pada branch default.

## Tahap 7 — Pengukuran yang dilakukan

Bank awal tetap 40 kasus: 24 development dan 16 heldout. Hash baseline tidak berubah. Kasus dipakai sebagai uji baca terpandu; jawaban acuan sudah diketahui evaluator. Label heldout pada bank tidak membuat pelaksanaan ini menjadi benchmark buta.

| Ukuran | Web | Konektor GitHub |
| --- | --- | --- |
| Percobaan mengambil teks | 34 | 32 |
| Respons teks berhasil | 33 | 32 |
| Path unik yang dibaca | 32 | 32 |
| Respons parsial | 1 manifest | 0 |
| Karakter teks dikembalikan | 323.932 | 269.712 |
| Kasus yang memiliki jawaban dan kutipan | 40 | 40 |
| Pemeriksaan mekanis lulus | 26/26 | 26/26 |
| Jawaban semantik tanpa skor independen | 14 | 14 |

Angka karakter adalah total satu batch 40 kasus, termasuk wrapper/navigasi alat dan pembacaan berulang. Itu bukan biaya satu konsep, token model, atau bacaan wajib. Semua pengambilan isi sumber dilakukan melalui alat remote pada commit uji; file lokal hanya dipakai oleh harness untuk menyimpan/menilai hasil dan membaca bank acuan yang memang diketahui.

Dua belas cek mekanis memeriksa akses ke contoh positif yang sudah ditentukan. Ini tidak mengukur precision/recall penemuan referensi secara independen. Empat belas cek lain membandingkan nilai hasil parsing anotasi yang benar-benar dikembalikan jalur tersebut. Empat belas jawaban unknown/kreatif ditulis oleh asisten ini dengan kutipan aktual dan tidak diberi skor mutu model.

Manifest web terpotong setelah baris 364 dari 411 baris. Hanya field release_id yang dikembalikan yang dipakai untuk memeriksa identitas snapshot. Laporan tidak mengklaim seluruh binding manifest dibaca melalui web. Anotasi yang dipakai untuk perbandingan nilai berhasil dikembalikan dan diekstrak. Pemeriksaan byte sumber lengkap tetap pengukuran lokal tersendiri.

## Temuan akses yang berpengaruh

- Pembaca web utama pada awal sesi menghasilkan cache miss. Pembaca web alternatif berhasil membuka halaman commit dan konten mentah secara langsung.
- Tombol Raw melalui URL github.com/raw ditolak alat web, sementara URL langsung raw.githubusercontent.com berhasil untuk teks. Keberhasilan satu bentuk URL tidak dianggap keberhasilan bentuk lainnya.
- Probe pencarian konektor tidak menemukan hasil untuk label uji. Probe pencarian web tidak menemukan repository target dalam hasil yang dikembalikan. Pembacaan path langsung berhasil; pencarian tidak dipakai untuk mengisi jawaban.
- Pencarian tersebut tidak dikunci ke commit kandidat, sehingga tidak dipakai sebagai ukuran kelengkapan snapshot atau performa retrieval.
- Konektor berhasil mengambil base64 gambar shot-02 edh060 dan gambar benar-benar ditampilkan. Pembaca web hanya mengembalikan penanda gambar tanpa piksel yang tersedia kepada evaluator; review visual melalui web tidak diklaim.
- Pemutaran video asli dan hasil generator tidak diuji pada tahap ini.

Hasil menggambarkan alat yang tersedia pada sesi ini. Keberhasilan pada alat tersebut tidak membuktikan semua konsumen AI atau pembaca web mempunyai kemampuan yang sama.

## Batas kesimpulan

Asisten evaluator sudah memiliki konteks repo dan mengetahui jawaban acuan. Uji akses, keberadaan kutipan dan parsing sumber ini bukan evaluasi model konsumen yang independen. consumer_model_accuracy tetap null. Tidak ada klaim bahwa kualitas konsep atau prompt akhir meningkat dengan persentase tertentu.

Sesuai pilihan pengguna pada sesi ini, tahap 7 saat ini dicukupkan pada uji akses. Benchmark AI independen ditunda dan tidak termasuk klaim penyelesaian pengujian saat ini.

Kriteria benchmark buta untuk pengujian lanjutan: AI baru mendapat hanya URL, pertanyaan dan satu jalur akses, tanpa konteks repo atau jawaban acuan. Jawaban, dukungan kutipan, unknown, kebebasan kreatif, keragaman referensi dan biaya bacaan perlu dinilai pada pelaksanaan tersebut. Pengujian prompt/generator akhir baru relevan setelah konsumen plugin/master prompt tersedia.

## Pemeliharaan

Audit memeriksa 4.147 tautan lokal, anggaran bacaan dan tautan sumber seluruh 57 profil. Fingerprint mengikat berkas bacaan dan snapshot. Validator menolak campuran route/commit, kutipan yang tidak ada, isi transkrip yang berubah, anotasi yang diisi dari teks lain, dan klaim akurasi independen pada format uji terpandu ini.

Perubahan sumber dipetakan ke profil, pemetaan, bukti, review/media terkait serta agregat bersama. Koreksi satu sumber tidak otomatis membuat semua review sumber lain usang. Perubahan kamus dan sumber yang bersamaan tetap memerlukan review sumber yang berubah. CI memeriksa hasil build dan rekaman akses tanpa membuat panggilan remote.

Sumber references/, video/ dan requests/ tetap dipertahankan. Review temporal 45 referensi yang sebelumnya pending tidak diubah menjadi selesai oleh pengujian akses ini.

[Pengetahuan inti](../knowledge/ai-knowledge.md) · [Peta bacaan](../knowledge/README.md) · [Audit dan rekaman evaluasi](../evaluations/stage7/README.md) · [Pemeliharaan](knowledge-maintenance.md)

## Validasi akhir

Seluruh 158 tes lulus. Pemeriksaan source integrity, knowledge library, design evidence, similarity dan knowledge access lulus. Seluruh video, anotasi asli serta requests tetap utuh. Bank evaluasi awal tidak diubah.

Perubahan dipublikasikan sebagai kandidat pada branch uji. Branch utama dan staging workspace tetap berada dalam kendali pengguna.
