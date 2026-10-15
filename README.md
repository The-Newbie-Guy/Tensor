# Buku Kating — Kelompok 1 Tensor

Website Streamlit berisi buku kating anggota HMSD Adyatama ITERA 2024.

## Struktur folder

```
kating.py                  Kode view bersama: menu, ambil foto, render kartu.
                           dipakai oleh semua halaman Buku Kating + Halaman Utama.
main.py                    Halaman utama / router. Satu-satunya tempat daftar anggota.
Buku Kating/               Satu file .py per anggota.
Halaman Utama/             halaman_utama.py — landing page, Home, dan About Us.
tools/                     KREASI.py, KREASII.py (tugas kelompok) + smoke_test.py.
.streamlit/config.toml     Warna tema.
requirements.txt           Daftar library.
```

## Menjalankan di lokal

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt      # Windows
.venv\Scripts\python -m streamlit run main.py
```

## Menjalankan cek

```bash
.venv\Scripts\python tools\smoke_test.py
.venv\Scripts\python tools\about_us_check.py
```

`smoke_test.py` mengecek semua file bisa di-parse, semua seksi menu ada bloknya,
data lengkap, link foto hidup/mati ditangani, dan 3 halaman benar-benar dirender
tanpa error. Wagaan `WAGA` berarti masalah data yang harus diperbaiki pemilik
file, bukan bug kodenya.

`about_us_check.py` khusus mengecek halaman About Us, karena tidak bisa dicapai
lewat navigasi otomatis (`streamlit-option-menu` itu custom component).

## Menambah anggota

1. Salin file Buku Kating milik anggota yang sudah ada ke
   `Buku Kating/{NIM}_{Nama}.py`.
2. Tambah satu baris di `ANGGOTA` pada `main.py`:

   ```python
   ("123_Nama Lengkap", "123 - Nama Lengkap"),
   ```

   Kolom pertama adalah nama file tanpa `.py`, kolom kedua adalah judul yang
   tampil di sidebar. Keduanya tidak harus sama.

## Menambah orang ke dalam seksi

Hanya menyentuh bagian yang ditandai di file anggota:

```python
gambar_urls = [
    "https://drive.google.com/uc?export=view&id=ID_FOTO_1",   # orang ke-1
    "https://drive.google.com/uc?export=view&id=ID_FOTO_2",   # orang ke-2
]
data_list = [
    {"nama": "...", "nim": "...", "umur": "...", "asal": "...",
     "alamat": "...", "hobbi": "...", "sosmed": "...",
     "pesan": "..."},
]
```

`gambar_urls` dan `data_list` berpasangan urutan: link ke-N adalah foto orang
ke-N. Kalau satu link mati, hanya slot itu yang kosong — data orang lain tidak
bergeser. Format link foto:

```
https://drive.google.com/uc?export=view&id=<ID_FILE>
```

Cara mendapat `<ID_FILE>`: buka foto di Drive → Bagikan → "Salin tautan" →
ambil karakter setelah `id=`. Sebaiknya format JPG atau PNG. Foto dari iPhone
kadang berformat HEIC dan tidak bisa ditampilkan.

## Menambah seksi baru

1. Tambah label seksi ke `KATING_SECTIONS` di `kating.py`.
2. Tambah blok `if menu == "Labelbaru":` di file anggota yang relevan,
   dengan `gambar_urls`, `data_list`, lalu
   `render_profiles(gambar_urls, data_list, KATING_FIELDS)`.

## Isi halaman Halaman Utama

- Foto besar atas dan `FOTO_KELOMPOK` — variabel di bagian atas
  `halaman_utama.py`.
- Deskripsi kelompok dan `{NIM}` — blok `if menu == "Home"`.
- `gambar_urls` dan `data_list` di `elif menu == "About Us"` — 12 anggota
  kelompok, berurutan.
