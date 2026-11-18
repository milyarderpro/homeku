# Template prompt video per shot

Gunakan setelah melihat dua frame final dan membaca [panduan Omni Flash](../references/omni-flash.md). Ini kerangka penulisan, bukan prompt siap pakai. Isi berdasarkan gambar dan rancangan aktif; jangan menambahkan ruang atau gerak baru.

Salin instruksi wajib dari prompt_constraints pada [aturan produksi](../references/production-rules.yaml) ke CONTINUOUS_INSTRUCTION dan AUDIO_INSTRUCTION. Isi DURATION_S dari shot yang sama. START_FILE dan END_FILE harus cocok dengan aset yang ditunjuk prompt.start_asset_id/end_asset_id. Ganti semua penanda kurung kurawal sebelum menyimpan text.

~~~text
Use the supplied {{START_FILE}} as the first frame and {{END_FILE}} as the last frame of the same house.
Duration: {{DURATION_S}} seconds.
{{SUBJECT_LIGHT_AND_ENVIRONMENT}}
Begin at {{START_FRAMING}}.
{{CAMERA_PATH_SPEED_AND_REVEAL}}
Finish at {{END_FRAMING}}, matching the supplied end frame.
Preserve {{FIXED_ELEMENTS_AND_SPATIAL_RELATIONSHIPS}} throughout the movement.
{{CONTINUOUS_INSTRUCTION}}
No jump cuts, sudden viewpoint changes, teleportation, or morphing of the house, openings, furniture, or surroundings.
{{AUDIO_INSTRUCTION}}
~~~

Untuk CAMERA_PATH_SPEED_AND_REVEAL:

| Rancangan | Bentuk instruksi |
| --- | --- |
| single | Uraikan satu gerak, lintasan dan pengungkapan yang dirancang |
| simultaneous | Tegaskan gerak berjalan bersamaan: “Move forward while panning right throughout the movement.” |
| sequential | Tegaskan pergantian fase: “First move forward, then pan right after reaching the planned turning point.” |

Dua contoh gerak terakhir hanya memperlihatkan perbedaan waktu. Gunakan arah, fase dan lintasan proyek yang sebenarnya; jangan menerapkannya ke semua shot atau menganggapnya kutipan sumber. Bila pembagian waktu sumber belum pasti, nyatakan pilihan tersebut sebagai adaptasi proyek pada catatan desain/gerak.

Jelaskan lintasan yang memungkinkan dua frame tersambung dalam 6/4 detik. Jangan memakai transformasi ruang, cut internal, perpindahan menembus dinding atau pergantian sudut sebagai pengganti gerak kamera. Cut ke shot berikutnya dicatat di panduan perangkaian, bukan di dalam prompt klip ini.
