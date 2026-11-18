---
name: produce-home-tour
description: Susun atau revisi brief, konsep desain rumah, dan daftar continuous shot home tour berbasis pustaka HOMEKU. Gunakan saat pengguna memulai atau melanjutkan praproduksi video rumah; permintaan analisis referensi saja tidak memulai produksi lengkap.
---

# Praproduksi home tour

Bantu pengguna menetapkan satu rumah dan cara mengungkapnya mengikuti DNA desain serta video referensi. Keluaran aktif skill ini sampai rancangan shot yang siap diteruskan ke produksi gambar. Kolase, pemotongan dan paket prompt video lengkap ditambahkan pada tahap implementasi berikutnya; jangan mengklaim aset tersebut sudah dibuat.

## Sumber kerja

- Baca [aturan produksi](references/production-rules.yaml) saat membuat atau merevisi proyek. Ini sumber durasi, jenis/cakupan shot, audio dan batas area.
- Baca bagian tahap/revisi pada [kontrak proyek](references/project-contract.md) sebelum mengisi catatan proyek. [Template](assets/project-template.json) dipakai saat proyek baru; [schema](assets/project.schema.json) membantu mengoreksi data bila diperlukan.
- Saat mengambil pengetahuan, gunakan [akses repo](references/repo-access.md). Pustaka dibaca melalui URL web atau konektor GitHub; tidak memerlukan clone, indeks lokal atau API pencarian khusus.
- Saat menyusun konsep dan shot, baca [panduan praproduksi](references/preproduction.md). Muat rincian sesuai tugas, bukan semua file repo sekaligus.

## Memulai atau melanjutkan

Pahami permintaan saat ini dan batas pekerjaan yang sudah diizinkan. Jika pengguna hanya meminta brief, pilihan konsep atau revisi shot, kerjakan bagian itu. Untuk analisis sumber saja, jawab analisis tanpa membuat proyek produksi.

Pada proyek baru, rangkum brief dan hal penting yang belum diketahui. Tanyakan hanya keputusan yang mengubah arah hasil; pilihan rutin dapat diajukan sebagai asumsi yang terlihat. Jangan menambah ruang, jumlah kamar atau pola shot yang tidak memiliki contoh sumber.

Pada kelanjutan, baca catatan proyek dan keputusan percakapan yang tersedia. Pertahankan konsep serta persetujuan yang masih berlaku. Minta hanya catatan/aset yang diperlukan tetapi belum tersedia; nama file bukan bukti file dapat dibuka. Jangan mengulang pertanyaan yang sudah dijawab atau meminta persetujuan ulang atas langkah yang telah didelegasikan.

Arahan eksplisit terbaru pengguna menjadi pegangan. Bila arahan mengubah aturan baku, catat perubahan secara jelas dan sesuaikan kontraknya dalam cakupan yang diminta; jangan menyembunyikan pelanggaran dengan catatan sumber palsu atau menghapus error validator.

## Dari referensi ke rancangan

1. Ambil pengetahuan inti dan contoh yang relevan melalui jalur akses yang tersedia. Catat hanya isi yang benar-benar dikembalikan alat. Referensi yang gagal dibaca belum boleh mendukung klaim atau shot.
2. Pilih referensi utama untuk bahasa video serta pendukung desain yang kompatibel. Jelaskan bentuk, tata ruang, material, lighting, lingkungan, framing, gerak dan urutan yang diadaptasi. Confidence sumber membatasi klaim fisik, bukan kebebasan memilih bahan baru.
3. Tawarkan arah konsep yang cukup untuk membantu keputusan, misalnya tiga opsi bila pengguna masih menjelajah. Jangan memperbanyak opsi ketika konsep sudah dipilih. Catat konsep terpilih setelah pengguna memilih atau memberi delegasi.
4. Tetapkan spesifikasi satu rumah dan elemen tetapnya. Bedakan fakta sumber dengan keputusan desain proyek; urutan edit tidak membuktikan denah atau adjacency.
5. Susun daftar shot kontinu tanpa cut dari pola yang didukung sumber. Catat area yang sudah tercakup setelah setiap shot. Living-to-kitchen mencakup keduanya; exterior-to-living mencakup exterior dan living. Jangan menambah pengungkapan area yang sama, bedroom lain, atau cut hanya karena label ruang berganti.
6. Isi framing awal–akhir dan gerak dengan jelas. Bedakan maju sambil pan dari maju lalu pan; daftar label kamera belum memastikan urutan waktunya. Pertahankan proporsi, cahaya, dunia luar jendela dan lintasan yang masuk akal.
7. Terapkan durasi dan audio dari aturan. Tampilkan total hasil penjumlahan; jangan mempercepat atau memangkas otomatis untuk mengejar durasi referensi.

## Keputusan dan penyerahan

Dua keputusan aktif praproduksi adalah pilihan konsep dan persetujuan desain beserta daftar shot. Keputusan ketiga, persetujuan visual final, berlangsung setelah produksi gambar tersedia. Catat persetujuan hanya dari instruksi pengguna atau delegasi yang benar-benar diberikan.

Simpan catatan proyek sesuai kontrak: tahap brief atau concept selama pilihan masih dikembangkan; shot_plan saat rancangan lengkap. Pada tahap ini assets tetap kosong, frames setiap shot null, dan prompt null. Jangan menambahkan field bebas untuk menghindari aturan.

Jalankan [validator](scripts/validate_project.py) pada project.json dengan lingkungan pemrosesan yang tersedia; [dependensi](scripts/requirements.txt) menjelaskan kebutuhan alat. Jika tidak dapat menjalankannya, nyatakan pemeriksaan otomatis belum dilakukan dan jangan mengarang hasil lulus.

Serahkan ringkasan rumah, asal DNA, daftar shot, cakupan area, durasi dan total, serta catatan proyek yang bisa diunduh bila alat file tersedia. Jelaskan keputusan yang masih menunggu pengguna. Keluaran valid secara struktural belum membuktikan mutu geometri atau kepastian sumber.

Saat diminta melanjutkan ke gambar atau prompt akhir, pertahankan rancangan dan jelaskan batas komponen yang sudah tersedia. Tahap ini tidak mengirim tugas ke Omni Flash, merangkai video atau memublikasikan Facebook.
