# Homeku — Library Analisis Video Rumah

Homeku menyimpan hasil **analisis visual video desain rumah** sebagai YAML schema 2.1 dan laporan Markdown bergambar. Tidak termasuk audio, ide konten, maupun prompt generatif.

## Struktur

    video/                        # MP4 asli, unggah manual ke branch main
    references/VID-XXX/            # Paket hasil satu video
      analysis.yaml                # sumber data terstruktur
      analysis.md                  # laporan inline storyboard + gambar shot
      storyboard.jpg               # gabungan semua shot
      shot-01.jpg, shot-02.jpg...  # satu keyframe per shot
    requests/save.json             # satu request teks, awalnya idle
    requests/result.json           # hasil penyimpanan terakhir (cek request_id)
    .github/workflows/save-analysis.yml
    scripts/save_analysis_action.py
    scripts/validate_analysis.py
    rules/workflow-analysis.md
    rules/analysis.md
    templates/video-analysis.yaml
    templates/analysis.md
    docs/github-actions-save.md

## Alur v1.2 (sequential, no parallel save)

1. Unggah MP4 ke **main/video/<file>.mp4** sebelum meminta analisis.
2. Unggah video yang sama ke ChatGPT. ChatGPT membaca rules dan template, memverifikasi file di main/video/, menganalisis seluruh shot dan menampilkan hasil. Sampai tahap review/revisi, GitHub **READ ONLY**.
3. Hanya ketika pengguna mengirim pesan tersendiri **save now**, ChatGPT memakai konektor GitHub untuk memperbarui **requests/save.json** dengan YAML lengkap, path & Git blob SHA MP4, satu timestamp keyframe tiap shot, dan request_id stabil.
4. Push request memicu GitHub Actions. Runner membaca MP4 yang sudah ada di repo, menghasilkan JPG, storyboard, YAML dan Markdown, memvalidasi lalu membuat **satu commit** ke references/VID-XXX/ serta requests/result.json.
5. ChatGPT memeriksa status Actions, request_id, semua file dan commit sebelum menyatakan **Saved**. Simpan satu video hingga selesai sebelum video selanjutnya.

**Tidak ada lagi transport Base64 JPEG melalui konektor GitHub.** Runner melakukan ekstraksi JPG langsung dari video di repository yang sama. Source MP4 tidak dihapus sesudah save.

## Sumber aturan

- [Workflow v1.2](rules/workflow-analysis.md)
- [Standar analisis visual](rules/analysis.md)
- [Template YAML schema 2.1](templates/video-analysis.yaml)
- [Template laporan Markdown](templates/analysis.md)
- [Dokumentasi integrasi Actions](docs/github-actions-save.md)
- [Contoh VID-001](references/VID-001/analysis.md)

Luas bangunan disimpan sebagai perkiraan visual (rentang m² dan confidence), bukan ukuran terukur. YAML adalah satu-satunya sumber fakta; Markdown dibentuk dari YAML. Setiap shot punya satu JPG dan storyboard merangkum semuanya.

## Project Instructions ChatGPT

Agar berlaku konsisten di semua chat dalam Project Homeku, tambahkan instruksi berikut ke konfigurasi proyek ChatGPT:

> Untuk video yang diunggah, baca versi terbaru rules/workflow-analysis.md, rules/analysis.md, templates/video-analysis.yaml, dan templates/analysis.md dari GitHub milyarderpro/homeku. Cari MP4 yang sama di main/video/; lakukan ANALYZE dan REVIEW tanpa write GitHub. Hanya pesan pengguna tersendiri save now yang mengizinkan update requests/save.json via konektor GitHub. Tunggu GitHub Actions memproses request, cek requests/result.json, status run dan semua file di references/ sebelum menyatakan Saved. Jangan menyimpan paralel.

**Catatan:** Dokumen GitHub tidak otomatis mengeksekusi tool di ChatGPT. Request harus dibuat ChatGPT melalui konektor ketika pengguna sudah memberi izin yang sah.
