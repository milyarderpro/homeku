# Verifikasi Tahap 1 V2

Tanggal: 22 November 2026. **Status: Tahap 1 selesai; Tahap 2 belum dijalankan.**

**Pembaruan berikutnya:** [koreksi tampilan 2.1.2](v2-stage-1-media-verification.md) sudah selesai: nama gaya bahasa Inggris, judul lebih kecil, header hanya judul/rentang/durasi, serta label dan timestamp kecil di bawah tiap foto. Catatan fondasi 2.0.0 di bawah dipertahankan sebagai riwayat; hasil verifikasi terbaru ada pada dokumen tersebut.

Fondasi V2 telah diimplementasikan mengikuti urutan 1.1–1.12 pada [plan](improvement-v2-plan.md). Seluruh pengujian V2 memakai data sintetis di root terisolasi. Referensi aktif tetap edh001 r0001 berformat 1.1, lima shot; tidak ada audit ulang, persetujuan isi V2, ZIP r0002 atau pilot baru.

## Hasil per langkah

| Langkah | Hasil yang tersedia |
| --- | --- |
| 1.1 | Empat schema V2, kontrak paket/laporan/reader dan v2-field-map; versi source 2.0, reader/index 2.0, renderer/media 2.0.0, generator 3 |
| 1.2 | Baseline 51 tes dan hash aktif; fixture normal, multi area, fungsi gabungan, interval overlap/reentry serta input gagal |
| 1.3 | Model JSON V2 dan adapter legacy; helper video native/PTS dipisahkan tanpa mengubah metode 10 FPS/native |
| 1.4 | Kolase normal 3 panel, multi dinamis, storyboard satu baris; font DejaVu Sans beserta lisensi dibundel; bbox foto dan asal frame tersedia |
| 1.5 | MD lima bagian, kartu A/B/C, narasi desain lengkap, kamera sederhana/teknis, tempo dan luas wajib tanpa catatan tambahan |
| 1.6 | Dispatch kontrak eksplisit, JSON/hash/MD/media/PTS/log/interval/scope diperiksa; paket legacy tetap valid |
| 1.7 | Kandidat lengkap, kartu/receipt di luar payload, digest seluruh snapshot, ekspor byte yang sama dan validasi ZIP dibuka ulang |
| 1.8 | Proyeksi/index 2.0, inventaris bukti bersama, scope area, facet tempo eksplisit, hubungan gaya terpisah dari alias; denominator shot unik |
| 1.9 | CLI search/read/panel: batas hasil, identitas/shot/area, konteks kontinuitas dan ekstraksi foto sementara |
| 1.10 | Registry V2 menambah versi/hash audit.json, koleksi campuran, replay/revisi/supersedes/cache dan turunan usang diuji; storage/actions tetap dipertahankan |
| 1.11 | AGENTS, README, operasi/pembaca dan CI selaras; kit legacy diperluas menjadi 18 file agar dependensi bersama lengkap |
| 1.12 | Tes penuh, check pustaka, check kit, kapasitas dan perbandingan hash lulus; hasil aktual dicatat di sini |

## Pemeriksaan aktual

| Pemeriksaan | Hasil |
| --- | --- |
| Baseline sebelum perubahan | 51 tes lulus; library check dan kit check lulus |
| `python -m unittest discover -s tests -t . -v` | **86 tes lulus**, 121,536 detik pada putaran akhir |
| Regresi tambahan pada metode beberapa fase/area sama | Lulus; membedakan dua fase satu shot dari dua cut pada area fisik yang sama |
| `python tools/library.py check` | Lulus: 1 referensi, 5 shot |
| `python tools/build_audit_kit.py --check` | Lulus: 18 file, 450.339 byte |
| `git diff --check` | Lulus |
| Bandingkan baseline edh001 | Seluruh 28 file yang dicatat sama; inventaris references/edh001 juga sama |

Lingkungan lokal: Python 3.12.3, FFmpeg 6.1.1, Pillow 12.2.0, jsonschema 4.26.0. Pengujian portabel menjalankan helper melalui subprocess dari kit yang dibuka pada workspace kosong; tidak menggunakan repo penuh atau API provider. Jalur legacy draft/export tetap lulus; jalur teknis V2 draft → review → export juga lulus. Ini bukan pelaksanaan pilot pada layanan ChatGPT/Gemini.

Regresi V2 mencakup bukti kolektif lintas panel (satu fase tidak perlu menampilkan semua area dalam satu gambar), area terlihat tanpa dimasuki, satu fase lintas area, beberapa fase satu area, fungsi laundry dalam satu bathroom, kemunculan berulang, frame native yang tidak masuk kolase, panel dinamis 4/6/8 dan kolase beberapa baris. Perubahan salah satu JSON/MD/manifest/gambar membatalkan digest. Export tidak memanggil encoder media atau mengubah snapshot. MD manual berbeda, bbox/pointer/scope salah, log belum selesai dan file kerja dalam ZIP ditolak.

Tes kapasitas lama benar-benar meng-ingest 300 paket sintetis legacy/600 shot pada root sementara. Tes V2 membangun keluaran deterministik dari 300 model, memeriksa denominator unik serta indeks di bawah 4 MB. Pencarian 300 entri diuji dengan batas/paginasi; pembacaan identitas/shot tidak membawa frame_reviews. Ini tidak diklaim sebagai audit atau ingest 300 video V2 nyata.

## Keutuhan referensi aktif dan ukuran aktual

- Registry tetap satu edh001 r0001; file registry identik dengan baseline.
- Content SHA-256: `6664a56c09c428c24c30ac00bfb4c8a973647bd8269d0f661eca719197b59c96`.
- Source SHA-256: `3ccf8acf75ca46922025d39b3198e3cf460f9cb3c96c4dc670be0fa2d23c0de8`.
- ZIP r0001: `8d2795ee808c88fa6285bb84e542fe4b4fd6041c007e54011fe34e719bf03b7f`.
- Kedua salinan ZIP penyerahan, MD, manifest, 22 JPEG dan video sama byte dengan sebelum implementasi. Tidak ada fixture dalam registry produksi.

Generator membangun ulang keluaran yang berubah; fakta sumber tidak diedit. JSON pembaca edh001 memakai envelope 2.0 tetapi format sumber tetap 1.1 dan paths.audit null. Ukuran proyeksi berubah dari **255.070 menjadi 199.129 byte**; indeks dari **30.437 menjadi 32.411 byte** karena facet/konteks tambahan. Kit menjadi **450.339 byte**, terutama karena font portabel. Jumlah file media lebih sedikit tidak diklaim otomatis menghemat byte.

Preview media sintetis diperiksa pada sumber native 96×160 dan 720×1280: foto mempertahankan rasio/detail, caption di luar foto, urutan panel jelas dan storyboard satu baris. Preview berada di workspace sementara, bukan referensi aktif. Ukuran media edh001 V2 baru dapat dibandingkan setelah audit ulang Tahap 2.

## Penyerahan ke Tahap 2

Siap: kontrak, model, renderer/media, kandidat/ekspor, validator, ingest, reader serta kit teknis yang kompatibel. Panduan workflow chat yang sudah berlaku tetap 1.1; template audit JSON, protokol/prompt V2 lengkap dan pengalaman review provider diselesaikan pada langkah 2.1–2.7.

Berikutnya: audit ulang nyata seluruh lima shot edh001, tinjauan/koreksi pengguna dan persetujuan kandidat lengkap sebelum r0002. Setelah itu pengguna menjalankan enam pilot sesuai plan. Log audit r0001 tidak diperlakukan sebagai pemeriksaan V2 baru. Tidak ada pengujian konsep/gambar, plugin produksi, watcher lokal, klaim ketepatan visual atau penutupan tujuh pilot pada Tahap 1.
