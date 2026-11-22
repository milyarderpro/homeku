# Verifikasi perangkat Phase 2 dan pilot pertama

Catatan historis implementasi awal, 21 November 2026. Penyempurnaan berikutnya dicatat terpisah pada [verifikasi improvement](phase-2-improvement-verification.md).

Tanggal: 21 November 2026. Perangkat workflow telah diimplementasikan. Penyelesaian seluruh Phase 2 masih menunggu tinjauan pengguna atas edh001 serta enam audit di chat sehari-hari; kontrak belum dibekukan.

## Perangkat yang tersedia

- [Panduan pengguna](../audit/README.md) dengan kit input berulang, prompt audit, koreksi dan ekspor satu ZIP final.
- Protokol, rubrik desain/komposisi/kamera/tempo, kosakata, contoh notasi dan bahan kalibrasi.
- Helper chat untuk metadata/PTS asli, sampling sementara, frame pilihan, storyboard, manifest dan round-trip ZIP.
- Snapshot MD dikunci dengan SHA-256 pada ekspor setelah tinjauan chat; digest bukan bukti otomatis persetujuan manusia.
- Kit portabel berisi sembilan file tanpa video/audio, diuji di folder terisolasi tanpa repo lengkap. Tidak ada API AI berbayar.
- CI memeriksa kesegaran kit agar perubahan prompt/kontrak/runtime tidak tertinggal dari file ZIP yang dibagikan.

## Pengujian teknis

`python -m unittest discover -s tests -t . -v`: **34 pengujian lulus**, termasuk 23 pengujian fondasi dan 11 pengujian helper chat.

Regresi yang diuji mencakup timestamp integer/time_base pada 30 FPS, pemilihan stream yang sama dengan metadata, bukti sampling lama tidak dicampur, snapshot review yang berubah ditolak, extras usang dihapus saat regenerasi, file pengguna tidak ditimpa, dan kit yang dapat menjalankan ekspor mandiri.

Fondasi tetap lulus pada 300 referensi/600 shot sintetis, replay/revisi, konkurensi, pemulihan transaksi dan benturan push pada remote Git lokal sementara. Ini tidak dianggap sebagai run hosted GitHub atau pengujian akun Gemini/ChatGPT pengguna.

## Pilot nyata edh001

Sumber asli: video/edh001.mp4; SHA-256 3ccf8acf75ca46922025d39b3198e3cf460f9cb3c96c4dc670be0fa2d23c0de8. Stream video 18.4 s, 30 FPS, 720×1280, 552 frame; durasi container/audio sekitar 18.528 s.

Audit dilakukan di chat implementasi Codex. Pemeriksaan visual menggunakan 184 sampel setiap 0.1 s, 20 pilihan keyframe termasuk batas cut, serta pembesaran sepuluh frame awal/akhir. Sampel bertumpang tindih dan tidak dinyatakan sebagai semua 552 frame. Audio tidak diperiksa. Native PTS digunakan untuk pembuatan media.

[Laporan lengkap](../audit/pilots/edh001/analysis.md) memuat 5 shot, 127 fakta terstruktur dan 9 fase kamera. [Kandidat ZIP](../audit/pilots/packages/edh001-r0001.zip) memuat 21 JPEG, analysis.md dan manifest.json; MP4 tidak diduplikasi karena sumber kanonis tersedia dan cocok.

Gambaran area exterior/kitchen/bathroom dipilih pada awal IN; living/bedroom pada akhir OUT. Storyboard tersusun dari lima gambaran area. Interpretasi kamera diberi dasar dan ketidakpastian; minor pan/tracking/orbit dan percepatan fisik tidak dinyatakan sebagai hasil rekonstruksi pose.

Kandidat lolos validasi terhadap sumber kanonis. ZIP nyata di-ingest pada root sementara: 1 referensi/5 shot terbentuk tanpa edit manual, rebuild penuh cocok, fungsi bathroom/laundry dan fase fast tetap muncul dalam indeks/katalog. Root produksi tetap 0 referensi aktif; kandidat tidak ditaruh di incoming/.

## Yang belum dinyatakan selesai

- Tinjauan/koreksi isi edh001 oleh pengguna dan ekspor final sesudahnya.
- Audit edh058, edh013, edh033, edh049, edh056 dan dreamshome01 di lingkungan ChatGPT/Gemini pengguna.
- Evaluasi perbedaan lintas chat, koreksi rubrik berdasarkan hasil nyata dan pembekuan kontrak.
- Run hosted dan konfigurasi izin publikasi GitHub setelah implementasi dipush.

Daftar ini mengikuti [pembagian pilot](../audit/pilots/README.md) yang diminta pengguna. Tidak ada metadata run/review palsu dan tidak ada tahap review isi tambahan setelah penyerahan ZIP final ke repo.
