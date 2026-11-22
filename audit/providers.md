# Menggunakan ChatGPT dan Gemini

Gunakan chat baru per video agar sumber, revisi dan koreksi mudah diikuti. Lampirkan MP4 secara terpisah dan homeku-audit-kit.zip, lalu kirim prompt mulai audit. Kit tidak mengandung video atau audio dan berisi empat file input: README, bootstrap runtime, template audit dan template log. `python homeku_runtime.py --output .` memulihkan semua modul/schema/font/lisensi dari payload lokal; tidak ada dependensi runtime yang dibuang.

Pilih lingkungan chat yang dapat memeriksa video/frame, menjalankan helper dan menghasilkan file unduhan. Jalankan operasi yang diperlukan langsung; jangan menyimpulkan kemampuan hanya dari nama model. Jika suatu operasi benar-benar gagal, catat operasi/error tersebut dan pulihkan di chat tanpa membuat metadata palsu.

Pada ChatGPT, buktikan kemampuan menerima sumber dan menjalankan inspect/sample di workspace yang dipakai; dokumentasi file tidak menjamin FFmpeg/code execution tersedia di semua permukaan. Tampilkan hasil dan minta koreksi terarah sebelum file final diunduh. Panduan resmi menjelaskan alur sumber/format/kriteria review dan revisi file: [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer?surface=app).

Pada Gemini, jangan menyamakan kemampuan menonton video dengan ketersediaan Python/FFmpeg untuk ekspor. Jika workspace terpilih tidak dapat menjalankan bootstrap/helper, laporkan operasi yang gagal dan gunakan workspace beralat yang sesuai sebelum membuat ZIP; jangan mengarang hasil helper. Video diunggah sendiri, di luar ZIP kit. Panduan resminya menyatakan ZIP input tidak memuat video/audio dan dibatasi sampai 10 file di dalam ZIP, ukuran ZIP 100 MB. MP4 tidak dikemas di kit input; ketersediaan akun dapat berbeda. [Attach and analyze files](https://support.google.com/gemini/answer/14903178?hl=en).

Dokumentasi tersebut mendukung cara memasukkan/meninjau file; bukan bukti bahwa pilot HOMEKU telah dijalankan pada akun/model tertentu. Model/build yang tidak diketahui tetap unknown/null. Tidak ada asumsi frame rate internal model atau jaminan bahwa Gemini dan ChatGPT memberi jawaban identik.

Sisa enam pilot dibagi di antara kedua lingkungan agar keduanya diuji. Tidak wajib mengaudit setiap video dua kali. Pengguna menilai isi di chat dan mengunduh ZIP final setelah koreksi; importer repo tidak menambahkan review isi kedua.
