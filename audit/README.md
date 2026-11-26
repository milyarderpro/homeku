# Audit HOMEKU 3.1 di ChatGPT atau Gemini

Lampirkan MP4 asli dan `homeku-audit-kit.zip`, satu video per chat. Gunakan [prompt mulai](prompts/01-audit.md).

Gunakan workspace yang dapat menjalankan Python dan FFmpeg, membuka frame hasil ekstraksi, serta menyediakan file ZIP. Catat provider dan model yang diketahui. Jika operasi gagal, sebutkan langkah dan error yang terjadi agar audit dapat dilanjutkan dari workspace yang sesuai.

Ekstrak kit, jalankan `python homeku_runtime.py --output .`, lalu ikuti [alur audit](authoring.md).

1. **Pemetaan shot.** Konfirmasi cut, jalankan `prepare`, dan siapkan baseline.
2. **Audit kamera.** Baca [metode visual](visual-audit.md) serta [kasus kamera](camera-cases.md). Periksa frame, catat gerakan serta tempo, lalu jalankan `check-camera`.
3. **Audit desain dan kurasi media.** Ikuti [panduan desain](design-audit.md) untuk melengkapi profil, detail area, framing, panel dan Overview.
4. **Validasi dan ekspor.** Jalankan `complete`, `check-input`, `draft`, `review`, lalu `export`. Laporan, media, dan ZIP final tersedia dalam chat yang sama.

Periksa hasil di chat dan unduh ZIP yang Anda pilih. Taruh di `incoming/`, simpan MP4 kanonis di `video/<id>.mp4`, dan jalankan `python tools/library.py ingest`.

## Susunan media

Shot biasa memakai tiga panel dari frame jernih. Jika ada Production Start, gunakan frame itu sebagai panel Start. Shot multi-area memakai panel sesuai momen visual dan muat hingga lima panel pada satu baris secara default. Jika lebih banyak, panel dibagi rata antarbaris. `draft --columns` dapat menentukan batas 1–6 untuk shot multi-area. Storyboard memakai lebar dan margin kiri yang sama pada setiap shot. Waktu shot berada di kanan, sementara waktu panel berada di bawah foto di samping caption. Overview menampilkan frame wide dalam satu baris.

[Prompt koreksi](prompts/02-correct.md) · [Prompt ekspor](prompts/03-export.md) · [Kontrak paket](contracts/package.md)
