# Audit Record Authoring

## Purpose

Mengurangi penulisan struktur JSON berulang sambil menjaga isi audit dan rujukan bukti yang dinyatakan auditor.

## ADDED Requirements

### Requirement: Pengisian dan koreksi per entri audit

Kit SHALL menyediakan operasi terarah untuk menambah atau mengoreksi satu fase kamera atau satu fakta area pada `audit.json` kerja yang terikat sesi. Auditor SHALL dapat memilih shot dan target di dalam shot serta memberikan struktur yang diperlukan untuk entri tersebut saja. Pemilihan dengan indeks entri atau blok desain SHALL menyertakan SHA-256 dari audit kerja yang dibaca untuk memilih indeks.

#### Scenario: Koreksi satu fase kamera
- **WHEN** auditor menargetkan satu fase dan mengganti notasi atau buktinya
- **THEN** kit menyimpan perubahan pada fase yang dipilih tanpa meminta seluruh array fase
- **AND** kit menandai hasil pemeriksaan kamera shot tersebut perlu diperbarui ketika digesti isi kamera berubah

#### Scenario: Tambah fakta pada kategori area
- **WHEN** auditor memilih shot, blok desain, dan kategori lalu memasukkan fakta yang valid
- **THEN** kit menambahkan fakta di lokasi yang dipilih serta mempertahankan entri lain dan narasi kategori

#### Scenario: Urutan entri atau blok desain berubah
- **WHEN** auditor mengirim perubahan dengan hash audit dari sebelum perubahan urutan
- **THEN** kit meminta auditor membaca ulang audit dan memeriksa indeks sebelum mencoba lagi, serta menjaga audit kerja saat ini

### Requirement: Klaim dan bukti eksplisit

Operasi authoring SHALL mempertahankan narasi, nilai, state, negasi, bukti, dan field opsional yang dinyatakan. Kit SHALL menolak target atau perubahan yang tidak valid sebelum menyimpan dan mempertahankan ID serta batas shot yang terikat sesi. Bukti fase dan override SHALL mengikuti cakupan area serta interval frame yang berlaku.

#### Scenario: Fakta memakai label baru dan state negatif
- **WHEN** auditor memasukkan label yang valid bersama state `not-present` dan bukti yang disediakan
- **THEN** label, state, dan bukti tersimpan sesuai input
- **AND** provenance dapat menunjuk entri sumber pada `audit.json`

#### Scenario: Bukti wajib atau target entri belum valid
- **WHEN** operasi memperkenalkan fakta tanpa bukti yang diwajibkan oleh state atau target berada di luar scope shot
- **THEN** kit menunjukkan lokasi masalah dan mempertahankan versi kerja sebelum operasi

#### Scenario: Koreksi notasi menggeser rujukan override
- **WHEN** perubahan notasi memindahkan komponen yang dirujuk override
- **THEN** kit meminta pembaruan override yang eksplisit sebelum menyimpan koreksi

#### Scenario: Override memakai bukti di luar area fase
- **WHEN** visibilitas area fase sudah tercatat dan bukti eksplisit override berada di luar area tersebut
- **THEN** perubahan terarah dan pemeriksaan kamera yang terdampak melaporkan bukti yang salah sebelum menyimpan perubahan atau checkpoint
