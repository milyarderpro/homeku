# Omni Flash R2V dan paket proyek

Gunakan setelah gambar area asli tersedia, dilihat dan disetujui/didelegasikan. Baca [kontrak](project-contract.md), [aturan](production-rules.yaml) dan [template R2V](../assets/prompt-template.md). Jika gambar bertentangan dengan desain, kembali ke [alur gambar](image-workflow.md); jangan menutupinya melalui morphing.

## Referensi area, bukan endpoint wajib

Satu shot memakai satu prompt R2V dan satu klip. Gambar menetapkan identitas visual area, bukan susunan piksel yang wajib menjadi frame pertama/terakhir. Posisi dan framing awal–akhir video tetap diuraikan dari rancangan.

Living-to-kitchen memakai gambar living dan kitchen. Exterior-to-living memakai exterior dan living. Kedua file menjelaskan dua area dalam satu rumah; bukan pilihan desain alternatif, kolase, dua shot atau kewajiban interpolasi antarframe.

Pada REFERENCE IMAGE ROLE, sebut setiap image_id sesuai reference_image_ids beserta fungsi/identitasnya. Jelaskan hubungan ruang dari design.connections, bukaan, lantai atau elemen lain yang memang dirancang. Jangan menciptakan pintu/jalur baru hanya agar dua gambar dapat disambungkan.

Fungsi terpadu lain memakai peta gambar yang disetujui. Format/jumlah input yang diterima aplikasi dibuktikan pada lingkungan pengguna; jangan mengarang nama tombol, parameter API atau kemampuan batch dari alat lain. Percobaan R2V satu gambar yang telah dilaporkan pengguna tidak diulang sebagai syarat. Kasus dua referensi diuji manual pada V2.

## Sembilan bagian prompt

Gunakan nama sections persis sesuai prompt_sections pada aturan, dengan isi lengkap yang konsisten:

1. OUTPUT SPECIFICATION: identitas shot, home tour, durasi shot dan video 9:16.
2. REFERENCE IMAGE ROLE: peran setiap ID gambar sebagai referensi area.
3. ARCHITECTURE AND DESIGN: struktur, plafon, furnitur, material, bukaan dan hubungan yang dipertahankan.
4. CAMERA START COMPOSITION: posisi/arah kamera, subjek, foreground/background.
5. CAMERA MOVEMENT: lintasan, perkiraan jarak/sudut, ritme dan simultan/sekuensial sesuai data kamera.
6. VISIBLE MOTION EVIDENCE: perubahan yang terlihat akibat gerak yang diminta.
7. ENDING COMPOSITION: pandangan akhir yang geometris sesuai lintasan, tanpa wajib menyalin gambar referensi.
8. VISUAL CONSISTENCY LOCK: struktur/objek tetap dan bagian yang tidak boleh berubah.
9. CONTINUITY AND AUDIO RULES: continuous shot, tanpa cut/morphing, ambient halus tanpa musik/narasi/dialog/efek dramatis.

Salin instruksi continuous dan audio dari prompt_constraints ke bagian terakhir. Tidak cukup hanya mencantumkan aturan pada ringkasan proyek. Baca seluruh prompt agar bagian lain tidak meminta musik/cut atau transformasi yang bertentangan.

Isi prompt.method R2V, revision aktif, duration_s dan reference_image_ids yang sama/berurutan seperti shot. sections adalah sumber tunggal teks; eksportir merender sembilan judul, bukan menulis isi kreatif atau menambahkan text kedua. Penanda template belum diisi tidak boleh diserahkan.

## Kamera sesuai 4/6 detik

Exterior dan dua penghubung 6 detik; area lain 4 detik. Jangan mengejar total referensi melalui pemangkasan atau menyamaratakan durasi.

Pan/orbit yang memang dipilih minimal 12°. Pan mengubah arah pandang; orbit memindahkan posisi mengitari fokus. Jangan menggantinya dengan roll, benda/rumah yang berputar atau zoom digital yang tidak diminta.

Hubungan waktu pada camera.components harus cocok dengan kalimat prompt. single/simultaneous berlangsung sepanjang durasi shot, sequential mempunyai fase tersambung dengan total tepat. Contoh bahasa: “move forward while panning” untuk simultan; “first move forward, then pan” untuk sekuensial. Arah/fase contoh tidak otomatis diterapkan ke semua shot.

Tentukan jarak dan kompleksitas yang masuk akal. Jangan meminta perjalanan panjang beberapa tahap dalam 4 detik sambil hanya menyebut slow. Kurangi jarak/kompleksitas dalam batas keputusan; perubahan material dikembalikan ke review rancangan.

Bukti visual memakai elemen yang ada: foreground membesar saat mendekat, perubahan perspektif orbit, atau sisi ruang/kitchen yang terungkap saat pan. Pastikan komponen gerak gabungan benar-benar terlihat. Angka sudut dalam prompt bukan pengukuran hasil video; pemeriksaan aktual dilakukan dari media.

## Ekspor dua jenis paket

~~~sh
python skills/produce-home-tour/scripts/build_production_package.py /path/to/project/project.json --output /path/to/delivery/project-r1
~~~

[Pembuat paket](../scripts/build_production_package.py) menerima dua stage:

| Stage | Keluaran |
| --- | --- |
| image_prompt_package | project.json, production-guide.md dan image-prompts/image-id.txt untuk seluruh rencana gambar; tidak mengklaim file dibuat atau siap R2V |
| prompt_package | Catatan/panduan, prompt gambar, seluruh gambar referensi asli dan video-prompts/shot-NN.txt dari sembilan bagian |

Nama project.json, production-guide.md, image-prompts/ dan video-prompts/ disediakan untuk keluaran; aset memakai folder gambar, misalnya images/. Folder tujuan harus baru. ID/revisi, keputusan, prompt dan file asli dipertahankan; salinan divalidasi ulang.

Panduan berisi rumah/plafon, shot/total, peta ID gambar–file–prompt, gerak, sumber, keputusan, batch dan revisi. Satu gambar boleh dirujuk sesuai peta, tanpa menggandakan file atau menambah shot pengungkapan area. Pustaka HOMEKU dan percobaan yang tidak terdaftar tidak disalin ke paket.

Serahkan panduan/catatan, prompt serta tautan setiap gambar individual lewat mekanisme host. ZIP proyek opsional tidak menggantikan file individual. Jika file atau alat tidak tersedia, jelaskan bagian yang belum selesai.

Pengguna memasang referensi pada mode R2V sesuai peta, memakai prompt/durasi shot, lalu menghasilkan satu klip. Cut antarklip dijelaskan terpisah, tanpa musik pada editing. Jangan mengirim seluruh total proyek sebagai durasi satu klip.

## Revisi dan sesi baru

Periksa hanya gambar/video yang dapat dibuka serta audio yang dapat didengar. Thumbnail/metadata tidak membuktikan geometri, plafon, ritme atau ambient. Catat pemeriksaan yang belum dilakukan.

Revisi penyebab masalah: kamera/timing pada rancangan/prompt; perubahan bentuk/plafon/material pada gambar bila perlu. Elemen tetap berubah berarti meninjau area dan shot terdampak. Jangan menambah bedroom, mengulang area, mengubah durasi atau menambah musik sebagai jalan pintas.

Naikkan revision ketika keputusan yang sudah disetujui berubah. Catat dasar peninjauan ulang aset/prompt/approval. Jangan mengubah nomor versi aset lama untuk menyamarkan data usang. Simpan hasil versi lama di luar catatan aktif; ekspor revisi baru ke folder baru.

Sesi baru membaca project.json, panduan dan gambar asli; pertahankan mode/keputusan yang masih berlaku dan minta hanya data yang hilang. Hasil produksi tidak otomatis menjadi pengetahuan sumber. Penyiapan paket tidak berarti video dibuat, dirangkai atau dipublikasikan.
