"""Kode view bersama untuk halaman Buku Kating.

Data orang tetap tinggal di file masing-masing di `Buku Kating/`.
Yang dikumpulkan di sini hanya bagian yang sama berulang: menu, pengambilan
foto, dan render kartu.
"""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import base64
import html
import re
import urllib.parse

import requests
import streamlit as st
from PIL import Image, ImageOps
from streamlit_option_menu import option_menu

# (koneksi, baca) dalam detik. Tanpa timeout, satu link Drive yang
# menggantung akan menggantungkan seluruh halaman tanpa batas.
TIMEOUT = (5, 20)

# Label Departemen/Badan, urutan kiri ke kanan. Entri baru berarti menambah
# label di sini DAN menambah blok `if menu == "..."` di file anggota.
KATING_SECTIONS = (
    "Kesekjenan",
    "Baleg",
    "Senator",
    "Departemen PSDA",
    "Departemen MIKFES",
    "Departemen Eksternal",
    "Departemen Internal",
    "Departemen SSD",
    "Departemen Medkraf",
)

# Pasangan (key di data_list, label yang tampil).
KATING_FIELDS = (
    ("nama", "Nama"),
    ("nim", "NIM"),
    ("umur", "Umur"),
    ("asal", "Asal"),
    ("alamat", "Alamat"),
    ("hobbi", "Hobbi"),
    ("sosmed", "Sosial Media"),
    ("kesan", "Kesan"),
    ("pesan", "Pesan"),
)

ABOUT_FIELDS = (
    ("nama", "Nama"),
    ("sebagai", "Sebagai"),
    ("nim", "NIM"),
    ("fun_fact", "Fun Fact"),
    ("motto_hidup", "Motto Hidup"),
)

MENU_STYLE = {
    "container": {"padding": "0!important", "background-color": "#ffffff"},
    "icon": {"color": "#101B3C", "font-size": "19px"},
    "nav-link": {
        "font-size": "15px",
        "text-align": "left",
        "margin": "0px",
        "--hover-color": "#E8F5F1",
    },
    "nav-link-selected": {"background-color": "#FF6F00"},
}

# Opsi B: thumbnail Drive sebagai fallback. `sz=w1000` cukup untuk kartu,
# tetap tajam di layar retina tanpa mengunduh file asli yang besar.
DRIVE_THUMBNAIL_SZ = "w1000"


def _drive_id(url: str):
    """Ambil ID file Drive dari URL `uc?export=view&id=...` atau bentuk lain."""
    if not url or "drive.google" not in url:
        return None
    try:
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        if qs.get("id"):
            return qs["id"][0]
    except Exception:
        pass
    m = re.search(r"id=([A-Za-z0-9_-]{10,})", url)
    if m:
        return m.group(1)
    return None


def _thumbnail_url(drive_id: str, sz: str = DRIVE_THUMBNAIL_SZ) -> str:
    return f"https://drive.google.com/thumbnail?id={drive_id}&sz={sz}"


def _fetch_bytes(url: str):
    """GET satu URL, kembalikan bytes atau None.

    HTML ditolak eksplisit: halaman virus-scan Drive dan halaman error
    thumbnail mati mengembalikan 200 text/html berukuran besar.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        return None
    blob = response.content
    if not blob or len(blob) < 500:
        return None
    content_type = (response.headers.get("Content-Type") or "").lower()
    if "text/html" in content_type:
        return None
    if blob.lstrip()[:15].startswith(b"<"):
        return None
    return blob


@st.cache_data(show_spinner=False, max_entries=2048)
def fetch_photo(url: str):
    """Bytes mentah satu foto, atau None kalau tidak bisa diambil.

    Opsi B: coba URL asli dulu, fallback ke thumbnail hanya saat asli
    gagal atau mengembalikan HTML (kasus virus-scan file besar).

    Urutan ini disengaja agar cek `smoke_test.py` tetap hijau:
    - link mati `uc?export=view` (404) + thumbnail-nya (200 HTML) -> None.
    - HEIC asli (octet-stream) dikembalikan apa adanya -> `open_photo`
      yang menolaknya, bukan thumbnail JPEG hasil konversi server.
    """
    if not url:
        return None
    if "drive.google.com/thumbnail" in url:
        return _fetch_bytes(url)
    blob = _fetch_bytes(url)
    if blob is not None:
        return blob
    drive_id = _drive_id(url)
    if not drive_id:
        return None
    thumb = _fetch_bytes(_thumbnail_url(drive_id))
    if thumb is None:
        return None
    if (
        thumb[:2] == b"\xff\xd8"
        or thumb[:8].startswith(b"\x89PNG")
        or thumb[:4] == b"RIFF"
        or thumb[:3] in (b"GIF",)
    ):
        return thumb
    return None


def open_photo(blob):
    """Bytes -> gambar RGB siap tampil, atau None kalau bukan gambar.

    `convert("RGB")` sengaja dipanggil: `Image.open` hanya membaca header,
    jadi errordecode baru muncul saat piksel benar-benar dibuka. `convert()`
    memaksa decode di sini, di tempat kita masih bisa menangkapnya.
    """
    if not blob:
        return None
    try:
        with Image.open(BytesIO(blob)) as img:
            return ImageOps.exif_transpose(img).convert("RGB")
    except Exception:
        # Blob dari internet bisa HEIC, HTML, atau apa pun. Apa pun itu,
        # satu foto rusak tidak boleh menjatuhkan seluruh halaman.
        return None


def fetch_all(urls):
    """Ambil banyak foto sekaligus.

    `st.cache_data` memakai lock per key, bukan lock global, jadi pemanggilan
    dari beberapa thread tetap paralel dan URL yang sama tidak diunduh dua kali.
    """
    with ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(fetch_photo, urls))


def _ensure_card_css():
    # Disuntik TANPA syarat tiap run: Streamlit membangun ulang DOM dari nol
    # setiap rerun, jadi guard session_state justru menghilangkan <style>.
    st.markdown(
        """
<style>
.tensor-badge {
  display: inline-block;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.06em;
  background: #101B3C;
  color: #fff;
  border-radius: 999px;
  padding: 0.15rem 0.6rem;
  margin-bottom: 0.4rem;
}
.tflip {
  background: transparent;
  perspective: 1200px;
  margin-bottom: 1rem;
}
.tflip-inner {
  position: relative;
  width: 100%;
  height: 420px;
  transition: transform 0.55s ease;
  transform-style: preserve-3d;
  -webkit-transform-style: preserve-3d;
}
.tflip:hover .tflip-inner,
.tflip:focus-within .tflip-inner {
  transform: rotateY(180deg);
}
.tflip-face {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  background: #ffffff;
  border: 1px solid #E5E0D5;
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.tflip-front img {
  width: 100%;
  height: 290px;
  object-fit: contain;
  object-position: center;
  display: block;
  flex-shrink: 0;
  background: #F6F3EB;
  filter: saturate(0.85);
}
.tflip-front-body { padding: 0.6rem 0.75rem 0.8rem 0.75rem; }
.tflip-name { font-weight: 700; color: #101B3C; }
.tflip-back {
  transform: rotateY(180deg);
  -webkit-transform: rotateY(180deg);
  background: #101B3C;
  color: #F6F3EB;
  padding: 0.8rem 0.85rem;
  overflow-y: auto;
}
.tflip-back dt {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #7FE3D0;
  margin-top: 0.55rem;
}
.tflip-back dd { margin: 0.1rem 0 0 0; font-size: 0.88rem; }
.tflip-hint { font-size: 0.72rem; color: #6B7280; margin-top: 0.35rem; }
.tflip-missing {
  height: 290px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F6F3EB;
  color: #6B7280;
  font-size: 0.85rem;
}
@media (prefers-reduced-motion: reduce) {
  .tflip-inner { transition: none; }
  .tflip:hover .tflip-inner,
  .tflip:focus-within .tflip-inner { transform: none; }
  .tflip-face { position: static; height: auto; }
  .tflip-back { transform: none; -webkit-transform: none; }
  .tflip-inner { height: auto; }
}
</style>
""",
        unsafe_allow_html=True,
    )


def _photo_to_data_uri(blob, max_side=600):
    """Bytes foto -> data URI JPEG kecil, atau None kalau gagal dibuka."""
    gambar = open_photo(blob)
    if gambar is None:
        return None
    gambar.thumbnail((max_side, max_side))
    buf = BytesIO()
    gambar.save(buf, format="JPEG", quality=72)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def render_photo(url, width=None):
    """Satu foto di tengah halaman."""
    _ensure_card_css()
    _, kolom, _ = st.columns([1, 2, 1])
    with kolom:
        gambar = open_photo(fetch_photo(url)) if url else None
        if gambar is None:
            st.warning("Foto gagal dimuat — cek link Google Drive-nya.")
        else:
            st.image(gambar, width=width)


def _flip_card_html(orang, fields, data_uri):
    """Satu kartu flip sebagai HTML: depan foto, belakang detail."""
    nama = str(orang.get("nama", "?"))
    nim = str(orang.get("nim", "?"))
    if data_uri is None:
        depan_media = "<div class='tflip-missing'>Foto gagal dimuat.</div>"
    else:
        depan_media = (
            f"<img src=\"{data_uri}\" alt=\"Foto {html.escape(nama, quote=True)}\" />"
        )
    baris_belakang = []
    for key, label in fields:
        if key in ("nama", "nim"):
            continue
        nilai = html.escape(str(orang.get(key, "-")))
        baris_belakang.append(f"<dt>{html.escape(label)}</dt><dd>{nilai}</dd>")
    return f"""
<div class='tflip' tabindex='0' aria-label='Kartu {html.escape(nama, quote=True)}'>
  <div class='tflip-inner'>
    <div class='tflip-face tflip-front'>
      {depan_media}
      <div class='tflip-front-body'>
        <div class='tflip-name'>{html.escape(nama)}</div>
        <div class='tflip-hint'>Hover / ketuk untuk detail</div>
      </div>
    </div>
    <div class='tflip-face tflip-back'>
      <div class='tflip-name' style='color:#F6F3EB;'>{html.escape(nama)}</div>
      <dl>{''.join(baris_belakang)}</dl>
    </div>
  </div>
</div>
"""


def render_profiles(gambar_urls, data_list, fields, *, columns=3, flip=False):
    """Grid kartu anggota.

    `flip=False` (default, dipakai 12 halaman Buku Kating): kartu klasik,
    foto via `st.image`, semua field sebagai teks biasa.
    `flip=True` (dipakai About Us): kartu flip, depan foto, belakang detail
    saat hover/ketuk. Nama selalu dirender sebagai teks agar
    `tools/about_us_check.py` tetap menemukan semua nama.
    """
    _ensure_card_css()
    if len(gambar_urls) != len(data_list):
        st.warning(
            f"Jumlah foto ({len(gambar_urls)}) dan jumlah data ({len(data_list)}) "
            "tidak sama. Foto berlebih disembunyikan supaya tidak salah pasang."
        )

    pairs = list(zip(data_list, gambar_urls))
    if flip:
        st.caption(
            f"{len(pairs)} kartu · arahkan kursor atau ketuk kartu untuk melihat detail."
        )
    if not pairs:
        st.info("Belum ada data di Departemen/Badan ini.")
        return

    with st.spinner(f"Memuat {len(pairs)} foto..."):
        blobs = fetch_all([url for _, url in pairs])

    gagal = []
    for i in range(0, len(pairs), columns):
        chunk = pairs[i:i + columns]
        chunk_blobs = blobs[i:i + columns]
        cols = st.columns(columns)
        for col, (orang, _url), blob in zip(cols, chunk, chunk_blobs):
            nama = str(orang.get("nama", "?"))
            with col:
                if flip:
                    data_uri = _photo_to_data_uri(blob)
                    if data_uri is None:
                        gagal.append(nama)
                    st.markdown(
                        _flip_card_html(orang, fields, data_uri),
                        unsafe_allow_html=True,
                    )
                else:
                    with st.container(border=True):
                        gambar = open_photo(blob)
                        if gambar is None:
                            st.warning("Foto gagal dimuat.")
                            gagal.append(nama)
                        else:
                            st.image(gambar, use_container_width=True)
                        st.markdown(f"**{nama}**")
                        for key, label in fields:
                            if key in ("nama", "nim"):
                                continue
                            st.write(f"**{label}:** {orang.get(key, '-')}")

    st.write(f"Menampilkan {len(pairs)} dari {len(data_list)} orang.")
    if gagal:
        st.error(
            f"{len(gagal)} foto gagal dimuat, atas nama: {', '.join(gagal)}. "
            "Link-nya sudah tidak aktif di Google Drive - silakan unggah ulang."
        )


def kating_header(title="BUKU KATING"):
    st.markdown(
        """<style>.centered-title { text-align: center; }</style>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h1 class='centered-title'>{title}</h1>", unsafe_allow_html=True
    )


def kating_menu(sections=KATING_SECTIONS, icons=None):
    return option_menu(
        menu_title=None,
        options=list(sections),
        icons=["people-fill"] * len(sections) if icons is None else icons,
        default_index=0,
        orientation="horizontal",
        styles=MENU_STYLE,
    )
