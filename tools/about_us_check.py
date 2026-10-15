"""Uji jalur 'About Us' yang tidak bisa dijangkau lewat AppTest.

streamlit-option_menu 0.4.0 adalah custom component, jadi AppTest tidak bisa
mengganti pilihannya ke "About Us". Script ini mengambil `gambar_urls` dan
`data_list` apa adanya dari halaman_utama.py, lalu merendernya lewat
`render_profiles` yang sama persis dengan yang dipakai halaman aslinya.

Jalankan:  .venv\\Scripts\\python tools\\about_us_check.py
"""
import ast
import collections
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "Halaman Utama" / "halaman_utama.py"

tree = ast.parse(SRC.read_bytes().decode("utf-8"))
assigns = {}
for node in ast.walk(tree):
    if not isinstance(node, ast.If):
        continue
    for stmt in node.body:
        if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Name):
            if stmt.targets[0].id in ("gambar_urls", "data_list"):
                assigns[stmt.targets[0].id] = ast.literal_eval(stmt.value)
gambar_urls, data_list = assigns["gambar_urls"], assigns["data_list"]
print(f"About Us: {len(gambar_urls)} foto, {len(data_list)} orang")

PAGE = '''
import streamlit as st
from kating import ABOUT_FIELDS, render_profiles
gambar_urls = {urls!r}
data_list = {data!r}
render_profiles(gambar_urls, data_list, ABOUT_FIELDS)
st.write("SENTINEL-SELESAI")
'''.format(urls=gambar_urls, data=data_list)

with tempfile.TemporaryDirectory() as tmp:
    page = pathlib.Path(tmp) / "about_us_probe.py"
    page.write_text(
        "import sys; sys.path.insert(0, %r)\n" % str(ROOT) + PAGE,
        encoding="utf-8",
    )
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(page), default_timeout=600)
    at.run()

    exc = [e.value for e in at.exception]
    print(f"exception : {len(exc)}" + (f"  {exc[:1]}" if exc else "  (bersih)"))

    acc = collections.Counter()

    def walk(n):
        acc[n.type] += 1
        for c in getattr(n, "children", {}).values():
            for x in c:
                walk(x)

    walk(at._tree)
    print(f"img tampil : {acc['imgs']}  (12 foto, 3.8 KB placeholder dihitung juga)")
    for w in at.warning:
        print(f"  warning: {w.value}")
    for e in at.error:
        print(f"  error  : {e.value[:160]}")

    teks = "\n".join(m.value for m in at.markdown)
    hilang = [d["nama"] for d in data_list if d["nama"] not in teks]
    print(f"nama yang hilang : {hilang or 'tidak ada'}")

    sys.exit(1 if exc or hilang else 0)
