# Fixture sintetis HOMEKU 3.1

Factory membuat MP4 pola uji dengan FFmpeg, lalu mengisi audit dengan contoh sintetis normal atau multi area. Contoh normal memuat satu bathroom yang juga berfungsi sebagai laundry. Contoh multi memuat satu lintasan living–kitchen, visibilitas tumpang tindih dan perubahan tempo pada satu fase gerak. Golden laporan ada di `reports/normal.md` dan `reports/multi.md`.

Jalankan perintah berikut untuk membuat dua ZIP fixture dan MP4 terpisah pada root kosong.

~~~sh
python tools/make_test_packages.py --output /tmp/homeku-fixtures
python tools/library.py --root /tmp/homeku-fixtures validate /tmp/homeku-fixtures/incoming/fixture-normal-r0001.zip
~~~

Tes integrasi memakai root sementara bertanda `.homeku-fixture-root`. Paket ditandai `purpose: fixture`, dan deklarasi viewed di sini menguji pipeline teknis. Jalankan pilot dengan MP4 referensi asli di chat.
