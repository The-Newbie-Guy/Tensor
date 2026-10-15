import streamlit as st

st.set_page_config(
    page_title="Buku Kating — Kelompok 1 Tensor",
    page_icon="📖",
    layout="wide",
)

# Satu baris per anggota: (nama file tanpa .py, judul yang tampil di sidebar).
# Judul ditulis terpisah dari nama file karena tidak selalu sama, misalnya
# 104_Felisya Nabila Putri Nugroho.py -> "104 - Felisya Putri Nugroho".
ANGGOTA = [
    ("021_Favian Arkaanda", "021 - Favian Arkaanda"),
    ("031_Muhammad Razan Maulana Pratama", "031 - Muhammad Razan Maulana Pratama"),
    ("047_Muhammad Afdal Lutfi", "047 - Muhammad Afdal Lutfi"),
    ("054_Nazlah Auliya", "054 - Nazlah Auliya"),
    ("060_Andra Ilham Bintang", "060 - Andra Ilham Bintang"),
    ("067_Ghiyats Thabularasa Meardhy", "067 - Ghiyats Thabularasa Meardhy"),
    ("088_Elsa Sitorus", "088 - Elsa Sitorus"),
    ("091_Alya Ramadhanti", "091 - Alya Ramadhanti"),
    ("095_Della Ainisa Fitri", "095 - Della Ainisa Fitri"),
    ("096_Aisyah Khairunisa", "096 - Aisyah Khairunisa"),
    ("100_Rozak Ramdani", "100 - Rozak Ramdani"),
    ("104_Felisya Nabila Putri Nugroho", "104 - Felisya Putri Nugroho"),
]

pg = st.navigation(
    {
        "Halaman Utama": [
            st.Page("Halaman Utama/halaman_utama.py", title="Tensor", default=True)
        ],
        "Buku Kating": [
            st.Page(f"Buku Kating/{nama_file}.py", title=judul, icon=":material/person:")
            for nama_file, judul in ANGGOTA
        ],
        "Playground": [
            st.Page("tools/KREASI.py", title="Tebak Anggota", icon=":material/search:"),
            st.Page("tools/KREASII.py", title="Suara Nama", icon=":material/search:"),
        ],
    }
)

# Design system Tensor: navy sebagai kanvas, oranye hanya aksen 10%.
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Plus+Jakarta+Sans:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: "Plus Jakarta Sans", system-ui, -apple-system, sans-serif;
}
h1, h2, .tensor-display {
    font-family: "Space Grotesk", "Plus Jakarta Sans", sans-serif !important;
    letter-spacing: -0.02em;
}
code, .tensor-mono {
    font-family: "IBM Plex Mono", ui-monospace, monospace !important;
}

[data-testid="stSidebar"] {
    position: relative;
    background: #101B3C;
    color: #ffffff !important;
    overflow: hidden;
}

[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(255,111,0,0.55), rgba(16,27,60,0) 42%);
    opacity: 0.9;
    animation: tensorGlow 20s ease-in-out infinite;
    pointer-events: none;
}

@keyframes tensorGlow {
    0%, 100% { opacity: 0.55; }
    50% { opacity: 0.9; }
}

/* Perbaikan untuk link di sidebar */
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] .stNavLink,
[data-testid="stSidebar"] div[data-testid="stSidebarNav"] a,
[data-testid="stSidebar"] div[data-testid="stSidebarNav"] span {
    color: #ffffff !important;
    font-weight: 500;
    position: relative;
    z-index: 1;
    transition: color 0.2s ease, background 0.2s ease;
    border-radius: 8px;
}

/* Efek hover untuk link */
[data-testid="stSidebar"] a:hover,
[data-testid="stSidebar"] .stNavLink:hover,
[data-testid="stSidebar"] div[data-testid="stSidebarNav"] a:hover {
    color: #FFB37A !important;
}

/* Untuk teks biasa di sidebar */
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] p {
    color: #ffffff !important;
}

a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible,
textarea:focus-visible, [tabindex]:focus-visible {
    outline: 2px solid #00C2A8 !important;
    outline-offset: 2px;
    border-radius: 6px;
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stSidebar"]::before { animation: none; }
    * { scroll-behavior: auto !important; }
}
</style>
""",
    unsafe_allow_html=True,
)

pg.run()
