# Pemeriksaan akhir audit HOMEKU

Metode pengamatan dipelihara hanya di [visual-audit.md](visual-audit.md). Rubrik ini memeriksa hasil sebelum pengguna melihat kandidat.

| Pemeriksaan | Harus terpenuhi |
| --- | --- |
| Shot/area | Cut nyata, timeline utuh; satu take multi area tidak dipecah menjadi shot rekaan; visible berbeda dari dilalui |
| Kamera | Depth diperiksa sebelum Pan-only; translation dan rotation juga diperiksa. Gabungan/arah/fase dijelaskan oleh bukti dan alternatif yang relevan |
| Estimasi | ~×/~° visual tersedia; bila diukur, objek/dimensi utuh yang sama, piksel resolusi sumber dan rasio cocok. Sudut diusahakan; alasan khusus bila belum dapat diperkirakan |
| Tempo | Sesuai sumber dan interval setara. Semua moderate boleh; smooth bukan slow; pembesaran perspektif bukan otomatis percepatan fisik |
| Desain | Bentuk/proporsi, bukaan, layout, penyimpanan, furnitur/properti/orientasi dan lingkungan yang terlihat konkret; bukan isi ruang generik |
| Fakta | Narasi penting terwakili fact_coverage dan facts; facet_roles eksplisit. Status, negasi, label baru, basis/uncertainty dan evidence dipertahankan |
| Identitas | Nama gaya English, primary/interior/influence cocok profile; luas lantai wajib rentang positif, MD hanya angka m² |
| Komposisi | Camera Start awal sumber, Overview wide terpilih; akhir OUT tidak disebut awal. Tiap Overview menjelaskan posisi/arah/sudut/tinggi/cakupan/kedalaman/cahaya |
| Pemeriksaan | Baseline2.3=6FPS/native, short<1s native;10/native untuk pertanyaan belum jelas. Source2.2 tetap10FPS. Bukti/panel benar-benar viewed |
| Laporan | Renderer2.2.2, enam bagian dan A/B/C sesuai template. MD tidak diedit manual; data proses tetap JSON |
| Media | N+2 JPEG dengan layout/font2.2.0 terdaftar. Seluruh Overview/Storyboard/kolase ditampilkan dan caption terbaca; tidak menimpa foto |
| Ekspor | Seluruh snapshot terbaru disetujui, receipt di luar ZIP, byte sama; tanpa MP4/frame kerja |

Periksa ulang detail rawan salah: lampu kaca vs anyaman, bench vs footboard, opening/shutter, crop anchor dan tampilan material vs kepastian material fisik. Tidak ada kuota fakta atau distribusi tempo. High tidak diberikan hanya karena formulir lengkap. Jika bukti belum cukup, perdalam atau simpan batasnya.

Default quality91, scale1, columns4. Batas60M piksel/gambar, sisi65000px,95MiB/file,256MiB paket/ekstraksi. Perubahan skala/quality/kolom eksplisit sebelum review lengkap; jangan mengganti font/layout versi lama. Tooling lulus tidak berarti audit visual benar atau kandidat disetujui.

## Sumber2.4

Estimasi visual ~×/~° sah tanpa kalibrasi atau sumber eksternal; pengukuran piksel opsional. Jangan menghilangkan sudut pada gerak jelas hanya karena lensa tidak diketahui. Jika pengukuran diisi, nilai/bukti/rasio diperiksa. Camera checks tetap singkat dan lengkap. Runtime resmi memakai preflight sebelum render dan cache yang terikat sumber; seluruh isi/narasi/media tetap ditinjau.
