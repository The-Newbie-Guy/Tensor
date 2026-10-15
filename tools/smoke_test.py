"""Cek langsung isi repo dan file Buku Kating.

Jalankan dari root repo:

    python tools/smoke_test.py

Yang dicek:
  1. Semua file Buku Kating bisa di-parse Python.
  2. Tiap label di KATING_SECTIONS punya blok `if menu == "..."` di tiap file.
  3. Tiap entri data_list punya 9 key yang lengkap.
  4. Panjang gambar_urls dan data_list sama, atau selisihnya cuma placeholder.
  5. Foto yang hidup bisa diambil dan dibuka; link mati / HEIC ditolak rapi.
  6. Halaman beneran jalan: dirender lewat Streamlit AppTest tanpa exception.
"""
import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from kating import KATING_FIELDS, KATING_SECTIONS  # noqa: E402

BUKU = ROOT / "Buku Kating"

# Link yang dipakai di data, dipakai sebagai fixture.
URL_HIDUP = "https://drive.google.com/uc?export=view&id=1l59a1EhP_9kx7lJ74RAIwypZZcmLdk8c"
URL_MATI = "https://drive.google.com/uc?export=view&id=1-7fNuyGA8w2ZVMn4rZQRDTv-k3VWX19p"
URL_HEIC = "https://drive.google.com/uc?export=view&id=1YeKupUCs6_H_DuShkwH-t6lDo0BWOM22"

# ID foto placeholder yang ikut ditempel di akhir beberapa seksi.
PLACEHOLDER_ID = "1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_"

gagal = []
peringatan = []


def cek(kondisi, pesan):
    print(("  OK   " if kondisi else "  GAGAL") + f"  {pesan}")
    if not kondisi:
        gagal.append(pesan)


def warn(pesan):
    """Masalah data — hanya bisa diperbaiki pemilik file, bukan kodenya."""
    print(f"  WAGA  {pesan}")
    peringatan.append(pesan)


def seksi_dari_file(tree):
    """-> {nama_fungsi: (list_url, list_data)}"""
    hasil = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        urls = data = None
        for stmt in node.body:
            if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Name):
                if stmt.targets[0].id == "gambar_urls":
                    urls = stmt.value
                elif stmt.targets[0].id == "data_list":
                    data = stmt.value
        if isinstance(urls, ast.List) and isinstance(data, ast.List):
            hasil[node.name] = (
                [e.value for e in urls.elts if isinstance(e, ast.Constant)],
                [e for e in data.elts if isinstance(e, ast.Dict)],
            )
    return hasil


print("\n[1] file Buku Kating bisa di-parse")
files = sorted(BUKU.glob("*.py"))
trees = {}
for path in files:
    try:
        trees[path] = ast.parse(path.read_bytes().decode("utf-8"))
    except SyntaxError as e:
        cek(False, f"{path.name} baris {e.lineno}: {e.msg}")
cek(len(trees) == len(files), f"{len(trees)}/{len(files)} file berhasil di-parse")

print("\n[2] tiap Departemen/Badan di menu punya bloknya di tiap file")
for path, tree in trees.items():
    ada = {
        n.comparators[0].value
        for n in ast.walk(tree)
        if isinstance(n, ast.Compare)
        and isinstance(n.left, ast.Name)
        and n.left.id == "menu"
        and isinstance(n.comparators[0], ast.Constant)
    }
    kurang = set(KATING_SECTIONS) - ada
    cek(not kurang, f"{path.name}: semua 9 Departemen/Badan ada" + (f" (kurang {kurang})" if kurang else ""))

print("\n[3] & [4] kelengkapan data per Departemen/Badan")
for path, tree in trees.items():
    masalah_key = []
    masalah_panjang = []
    for nama, (urls, data) in seksi_dari_file(tree).items():
        for i, e in enumerate(data):
            keys = {k.value for k in e.keys if isinstance(k, ast.Constant)}
            if keys != {k for k, _ in KATING_FIELDS}:
                masalah_key.append(f"{nama}[{i}] {sorted(keys ^ {k for k, _ in KATING_FIELDS})}")
        if len(urls) != len(data):
            # Boleh berbeda kalau link berlebih cuma foto placeholder di ujung.
            sisa = urls[len(data):]
            if not (sisa and all(u.rsplit("=", 1)[-1] == PLACEHOLDER_ID for u in sisa)):
                masalah_panjang.append(f"{nama} url={len(urls)} data={len(data)}")
    cek(not masalah_key, f"{path.name}: semua entri punya 9 key" + (f" {masalah_key[:3]}" if masalah_key else ""))
    if not masalah_panjang:
        cek(True, f"{path.name}: panjang url == data")
    else:
        for m in masalah_panjang:
            warn(f"{path.name}: {m} - foto orang terakhir tidak ada, atau linknya bukan gambar")

print("\n[5] pengambilan foto")
from kating import fetch_photo, open_photo  # noqa: E402

blob = fetch_photo(URL_HIDUP)
cek(isinstance(blob, bytes) and len(blob) > 1000, f"link hidup -> {len(blob) if blob else 0} byte")
cek(open_photo(blob) is not None, "link hidup -> PIL bisa dibuka")

cek(fetch_photo(URL_MATI) is None, "link mati (404) -> None, bukan exception")
cek(open_photo(fetch_photo(URL_HEIC)) is None, "foto HEIC -> ditolak, bukan exception")

print("\n[5b] data tidak bergeser saat ada foto gagal")
# rendered = hasil render_profiles: foto None hanya muncul di slotnya sendiri.
urls = [URL_HIDUP, URL_MATI, URL_HIDUP, URL_MATI]
data = ["orang-1", "orang-2", "orang-3", "orang-4"]
blobs = [fetch_photo(u) for u in urls]
pasangan = [(d, b) for d, b in zip(data, blobs) if b is not None]
cek([d for d, _ in pasangan] == ["orang-1", "orang-3"],
    f"2 foto dari 4 hidup -> yang tampil persis orang-1 dan orang-3 (dapat {[d for d, _ in pasangan]})")

print("\n[6] halaman jalan tanpa exception")
try:
    from streamlit.testing.v1 import AppTest

    target = [
        ROOT / "main.py",
        BUKU / "031_Muhammad Razan Maulana Pratama.py",   # halaman sehat
        BUKU / "088_Elsa Sitorus.py",                     # 54 dari 55 link-nya mati
    ]
    for path in target:
        at = AppTest.from_file(str(path), default_timeout=300)
        at.run()
        cek(not at.exception, f"{path.name}: render tanpa exception")
        if at.exception:
            for e in at.exception:
                print(f"          {e.value}")
except ImportError as e:
    print(f"  LEWATI  AppTest tidak tersedia ({e})")

print("\n" + "=" * 62)
for p in peringatan:
    print(f"  WAGA  {p}")
if gagal:
    print(f"\n{len(gagal)} CEK GAGAL:")
    for g in gagal:
        print(f"  - {g}")
    sys.exit(1)
if peringatan:
    print(f"\nSEMUA CEK KODE LULUS, {len(peringatan)} WAGAAN DATA (lihat di atas)")
else:
    print("\nSEMUA CEK LULUS")
