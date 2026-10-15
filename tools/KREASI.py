"""KREASI 1 — Kuis Tebak Anggota Tensor.

Tebak siapa dari fun fact + motto-nya. Skor dan streak tersimpan di sesi.
Foto dibuka sebagai hadiah setelah menjawab.
"""
import random

import streamlit as st

from kating import fetch_photo, open_photo

ANGGOTA = [
    {"nama": "Andra", "sebagai": "Pak Lurah", "nim": "122450016",
     "fun_fact": "suka makan pedes, tapi ga suka efeknya",
     "motto_hidup": "new semester new me",
     "foto": "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_"},
    {"nama": "Aisyah", "sebagai": "Bu Lurah", "nim": "122450000",
     "fun_fact": "nyemilin es bata",
     "motto_hidup": "Ya apa ya",
     "foto": "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_"},
    {"nama": "Alya", "sebagai": "Anggota", "nim": "122450091",
     "fun_fact": "takut kucing tapi suka liat nya",
     "motto_hidup": "Setap hari adalah kesempatan baru untuk lebih baik",
     "foto": "https://drive.google.com/uc?export=view&id=1YeKupUCs6_H_DuShkwH-t6lDo0BWOM22"},
    {"nama": "Della", "sebagai": "Anggotaa", "nim": "122450000",
     "fun_fact": "suka membayangkan domba lompat pager kalo mau tidur, biar cepet tidur",
     "motto_hidup": "jalanin yang membuatmu bahagia dengan sebaik-baiknya",
     "foto": "https://drive.google.com/uc?export=view&id=1cH_4xLVVySDkjafokPLl4c7OCslSFOK7"},
    {"nama": "Elsa", "sebagai": "Anggotaa", "nim": "122450088",
     "fun_fact": "Makan sayur tapi, ga makan tangkainya",
     "motto_hidup": "Untuk segala sesuatu ada masanya, untuk apa pun di bawah langit ada waktunya.",
     "foto": "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_"},
    {"nama": "Favian", "sebagai": "Anggotaa paling cool abiezzz", "nim": "124450021",
     "fun_fact": "Suka berdialog sama diri sendiri",
     "motto_hidup": "anything that happens to you, tetaplah jadi manusia yang baik",
     "foto": "https://drive.google.com/uc?export=view&id=1-8b-WLrqBEMIkPIYROpuPfILcIgii7zG"},
    {"nama": "Felisya", "sebagai": "Anggotaa", "nim": "122450100",
     "fun_fact": "nyemilin es bata, kiko",
     "motto_hidup": "jalanin dulu keles",
     "foto": "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_"},
    {"nama": "Ghiyats", "sebagai": "Anggotaa", "nim": "122450110",
     "fun_fact": "apapun game yang dimainin pasti bagus",
     "motto_hidup": "yang penting hidup dulu",
     "foto": "https://drive.google.com/uc?export=view&id=19rya7Zkzck08XZf82EBAN4lWtMBxhA_f"},
    {"nama": "Lutfi", "sebagai": "Anggotaa", "nim": "124450047",
     "fun_fact": "Makan sayur hanya daunnya saja tidak dengan tangkainya",
     "motto_hidup": "Man Jadda Wa Jadda",
     "foto": "https://drive.google.com/uc?export=view&id=1gX1RV6SsMhWp1XVrI2-K71MKNRCHhlDd"},
    {"nama": "Nazlah Auliya", "sebagai": "Anggotaa", "nim": "124450054",
     "fun_fact": "susah hapalin nama orang baru",
     "motto_hidup": "tebarkan kebaikan maka ia akan kembali padamu",
     "foto": "https://drive.google.com/uc?export=view&id=1STo9XNgWn-WbbwlvaipBo79sf-GZtEX-"},
    {"nama": "Razan", "sebagai": "Anggotaa", "nim": "124450031",
     "fun_fact": "Sudah pernah main salju",
     "motto_hidup": "Tidak semua bisa dimiliki, tapi semuanya bisa di syukuri",
     "foto": "https://drive.google.com/uc?export=view&id=15CBRRE1N-puql9vHfJRm27UoCoGYGp9E"},
    {"nama": "Rozak", "sebagai": "Anggotaa", "nim": "122450110",
     "fun_fact": "nyemilin es bata, kiko",
     "motto_hidup": "jalanin dulu keles",
     "foto": "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_"},
]

TOTAL = len(ANGGOTA)


def _reset():
    order = list(range(TOTAL))
    random.shuffle(order)
    st.session_state["quiz_order"] = order
    st.session_state["quiz_pos"] = 0
    st.session_state["quiz_skor"] = 0
    st.session_state["quiz_streak"] = 0
    st.session_state["quiz_best"] = st.session_state.get("quiz_best", 0)
    st.session_state["quiz_answered"] = False
    st.session_state["quiz_pick"] = None
    st.session_state["quiz_options"] = []


if "quiz_order" not in st.session_state:
    _reset()

st.title("🕵️ Tebak Anggota Tensor")
st.caption("Satu fun fact + satu motto. Siapa dia? 12 soal, tanpa pengulangan.")

pos = st.session_state["quiz_pos"]
if pos >= TOTAL:
    st.success(
        f"Selesai! Skor akhir {st.session_state['quiz_skor']} dari {TOTAL} "
        f"· streak terbaik {st.session_state.get('quiz_best', 0)}."
    )
    if st.button("🔁 Main lagi", use_container_width=True):
        _reset()
        st.rerun()
    st.stop()

order = st.session_state["quiz_order"]
benar = ANGGOTA[order[pos]]

if not st.session_state.get("quiz_options"):
    lawan = random.sample([a for a in ANGGOTA if a["nama"] != benar["nama"]], 3)
    opsi = lawan + [benar]
    random.shuffle(opsi)
    st.session_state["quiz_options"] = [o["nama"] for o in opsi]

c1, c2, c3 = st.columns(3)
c1.metric("Soal", f"{pos + 1}/{TOTAL}")
c2.metric("Skor", f"{st.session_state['quiz_skor']}")
c3.metric("Streak", f"{st.session_state['quiz_streak']}")

with st.container(border=True):
    st.markdown(f"**Fun fact:** {benar['fun_fact']}")
    st.markdown(f"**Motto:** _{benar['motto_hidup']}_")

if not st.session_state["quiz_answered"]:
    qcols = st.columns(2)
    for i, nama in enumerate(st.session_state["quiz_options"]):
        with qcols[i % 2]:
            if st.button(nama, key=f"quiz_opt_{pos}_{i}", use_container_width=True):
                st.session_state["quiz_pick"] = nama
                st.session_state["quiz_answered"] = True
                if nama == benar["nama"]:
                    st.session_state["quiz_skor"] += 1
                    st.session_state["quiz_streak"] += 1
                    st.session_state["quiz_best"] = max(
                        st.session_state.get("quiz_best", 0),
                        st.session_state["quiz_streak"],
                    )
                else:
                    st.session_state["quiz_streak"] = 0
                st.rerun()
else:
    pick = st.session_state["quiz_pick"]
    if pick == benar["nama"]:
        st.success(f"Benar! Itu **{benar['nama']}** ({benar['sebagai']}).")
    else:
        st.error(f"Kurang tepat — yang benar **{benar['nama']}** ({benar['sebagai']}).")
    with st.spinner("Membuka foto..."):
        gambar = open_photo(fetch_photo(benar["foto"]))
    if gambar is None:
        st.warning("Foto hadiah gagal dimuat — link Drive-nya mati.")
    else:
        st.image(gambar, caption=f"{benar['nama']} ({benar['sebagai']})", width=280)
    if st.button("Soal berikutnya ➜", use_container_width=True):
        st.session_state["quiz_pos"] += 1
        st.session_state["quiz_answered"] = False
        st.session_state["quiz_pick"] = None
        st.session_state["quiz_options"] = []
        st.rerun()

if st.button("Reset skor", type="secondary"):
    _reset()
    st.rerun()
