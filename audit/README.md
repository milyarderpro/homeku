# Audit referensi di Gemini/ChatGPT

## Mulai dari sini

1. Buka chat baru, lampirkan MP4 asli dan [homeku-audit-kit.zip](homeku-audit-kit.zip). MP4 dilampirkan terpisah dari kit.
2. Salin [prompt mulai audit](prompts/01-audit.md). AI memeriksa video, menyusun laporan 1.1 yang nyaman dibaca beserta kartu tiap shot, mengambil gambar dan membuat kandidat di chat. Anda memeriksa kartu bergambar terutama desain, posisi kamera, arah/fase dan tempo; MD lengkap tetap tersedia tanpa mewajibkan membaca tabel teknis.
3. Bila perlu, gunakan [prompt koreksi](prompts/02-correct.md). Setelah isi sesuai, kirim [prompt ekspor final](prompts/03-export.md), unduh satu ZIP hasil dan unggah ke incoming/ repo.

Kit adalah perangkat input yang dipakai berulang, bukan paket referensi. ZIP hasil audit hanya memuat laporan, manifest, media pilihan dan MP4 bila sumber belum tersedia. Anda tidak perlu menata file satu per satu atau memeriksa isi lagi setelah ingest.

Kit berisi sembilan file tanpa video/audio. README di dalamnya sudah menggabungkan protokol, rubrik, kosakata, prompt dan kontrak, serta helper portabel yang mengambil frame dan memvalidasi ZIP. Helper tidak memakai API AI berbayar. [Panduan lingkungan chat](providers.md) menjelaskan input file dan batas pembuktian.

## Isi laporan dan gambar

- [Protokol lengkap](protocol.md), [rubrik desain/kamera/tempo](rubric.md), dan [kosakata](vocabulary.md).
- [Template analysis.md](template-analysis.md), [kontrak laporan](../docs/contracts/analysis-v1.md), dan [kontrak paket](../docs/contracts/package-v1.md).
- [Contoh notasi dan bahan kalibrasi](calibration.md).

Setiap shot mempunyai satu frame asli area-overview.jpg, biasanya awal untuk IN dan akhir untuk OUT, serta start/middle/end. Detail/reveal ditambahkan sesuai kebutuhan. Storyboard menggabungkan area-overview seluruh shot. Tidak ada motion/ atau seluruh frame dalam paket. Laporan menjelaskan posisi, arah pandang dan peran frame agar referensi gambar sesuai lintasan kamera.

## Pilot dan status

[Pilot edh001](pilots/edh001/analysis.md) sudah diaudit ulang dengan format 1.1, disetujui pengguna, [diekspor final](pilots/packages/edh001-r0001.zip) dan [di-ingest ke pustaka lokal](../references/edh001/analysis.md); [kartu tinjauan](pilots/edh001-review.md) tetap mengacu snapshot yang sama. [Daftar pilot](pilots/README.md) mencatat enam video berikutnya yang akan Anda audit di ChatGPT/Gemini. Belum ada klaim bahwa keenam chat tersebut sudah dijalankan; persetujuan edh001 tercatat pada [catatan audit ulang](../docs/edh001-re-audit.md).

Perangkat workflow 1.1 dan tooling sudah tersedia; edh001 sudah menjadi referensi aktif lokal, sedangkan enam pilot lain belum dijalankan. Kontrak tetap provisional sampai pengalaman pilot nyata selesai. Fixture sintetis hanya menguji tooling, bukan contoh kebenaran desain/gerakan.

## Pemeliharaan teknis

Regenerasi kit setelah mengubah prompt/kontrak/helper: `python tools/build_audit_kit.py`. Pemeriksaan kesegaran: `python tools/build_audit_kit.py --check`. Seluruh perintah audit dalam kit dijalankan AI di workspace chat; pengguna cukup meninjau, mengunduh dan mengunggah hasil.


Audit memakai 10 FPS sepanjang setiap shot, frame asli pertama/terakhir, lalu pendalaman semua frame native sesuai kebutuhan. Lihat frame yang dipilih dan catat pemeriksaan aktual. Helper review menghasilkan kartu dari snapshot laporan yang sama. JSON pembaca AI dihasilkan repo setelah ingest; Anda tetap mengunduh satu ZIP saja. Tidak ada tugas pengujian manfaat melalui konsep/gambar baru.
