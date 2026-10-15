import streamlit as st

from kating import (
    ABOUT_FIELDS,
    KATING_SECTIONS,
    fetch_all,
    kating_menu,
    open_photo,
    render_profiles,
)

FOTO_UTAMA = [
    "https://drive.google.com/uc?export=view&id=12cQ4T8NkVvVPVNX6zBQC4sviFcc4cDWx",
    "https://drive.google.com/uc?export=view&id=12RBvQdMiqqqph-Q1QqLb0zvvIPnBjCYb",
]

FOTO_KELOMPOK = "https://drive.google.com/uc?export=view&id=1_04qOrTrYwchG0l_31HVqCvU9QwfBLei"

YEL_LINES = [
    "go tensor",
    "go go go",
    "we are the one one tensor one",
    "we are the go go tensor go",
    "we are the one one one",
    "we are the go go go",
]


def _ensure_home_css():
    # Tanpa guard session_state: tiap rerun Streamlit membangun ulang DOM,
    # jadi <style> harus dikirim ulang setiap kali.
    st.markdown(
        """
<style>
.tensor-eyebrow {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  color: #6B7280;
  margin-bottom: 0.2rem;
}
.tensor-hero {
  background-image:
    linear-gradient(rgba(16,27,60,0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(16,27,60,0.07) 1px, transparent 1px);
  background-size: 28px 28px;
  border: 1px solid #E5E0D5;
  border-radius: 16px;
  padding: 1.4rem 1.5rem;
  margin-bottom: 1rem;
}
.tensor-hero h1 {
  font-size: clamp(2rem, 5vw, 3.4rem);
  line-height: 1.05;
  margin: 0 0 0.4rem 0;
  color: #101B3C;
}
.tensor-hero p { color: #3A3A40; max-width: 62ch; }
.yel-full {
  text-align: center;
  border-top: 1px solid #E5E0D5;
  border-bottom: 1px solid #E5E0D5;
  padding: 0.9rem 0.5rem;
  margin: 1rem 0;
  color: #101B3C;
  font-weight: 600;
  line-height: 1.7;
}
</style>
""",
        unsafe_allow_html=True,
    )


_ensure_home_css()

st.markdown(
    """
    <div class='tensor-hero'>
      <div class='tensor-eyebrow'>KELOMPOK 1 · TENSOR · HMSD ADYATAMA ITERA 2024</div>
      <h1>Buku Kating Tensor</h1>
      <p>Arsip kakak tingkat + dua playground interaktif: operasi tensor dan gelombang suara. Cari orang dalam hitungan detik, bukan scroll tanpa akhir.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3 = st.columns(3)
m1.metric("Anggota Tensor", "12")
m2.metric("Departemen/Badan", f"{len(KATING_SECTIONS)}")
m3.metric("Playground", "2")

menu = kating_menu(("Home", "About Us"), icons=("house-door", "hand-index"))

if menu == "Home":
    st.markdown("<h2 style='text-align:center;'>Meja Tensor</h2>", unsafe_allow_html=True)
    with st.spinner("Memuat foto utama..."):
        blobs = fetch_all(FOTO_UTAMA)
    foto_col1, foto_col2 = st.columns(2)
    for col, blob in zip((foto_col1, foto_col2), blobs):
        with col:
            gambar = open_photo(blob)
            if gambar is None:
                st.warning("Foto utama gagal dimuat — cek link Google Drive-nya.")
            else:
                st.image(gambar, use_container_width=True)

    st.markdown(
        "<div class='yel-full'>" + "<br>".join(YEL_LINES) + "<br>We are the, Tensor</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<h2 style='text-align:center;'>Deskripsi Kelompok</h2>", unsafe_allow_html=True)
    with st.spinner("Memuat foto kelompok..."):
        blobs_kel = fetch_all([FOTO_KELOMPOK])
    gambar_kel = open_photo(blobs_kel[0]) if blobs_kel else None
    if gambar_kel is None:
        st.warning("Foto kelompok gagal dimuat — cek link Google Drive-nya.")
    else:
        st.image(gambar_kel, use_container_width=True, caption="Kelompok 1 Tensor")
    st.markdown(
        """<div style="text-align: justify;">Kelompok 1 Tensor bukan hanya sekelompok nama, kami adalah simpul keakraban dan keharmonian.
        Nama Tensor sendiri melambangkan kekuatan yang menyatukan berbagai elemen, dan itulah yang kami lakukan. Di sini, setiap individu dihargai,
        dan suasana yang tercipta terasa hangat—seperti keluarga kedua tempat setiap anggota bebas bercerita, tertawa, dan tumbuh bersama tanpa rasa
        canggung. Kami percaya bahwa kaderisasi terbaik lahir dari kebersamaan yang solid. Kami belajar, berdiskusi, dan berproses dengan semangat
        saling dukung dan gotong royong. Kelompok Tensor adalah bukti nyata bahwa ketika kita selaras, proses belajar pun terasa ringan dan
        penuh makna.</div>""",
        unsafe_allow_html=True,
    )

elif menu == "About Us":
    st.markdown(
        """<style>.centered-title { text-align: center; }</style>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 class='centered-title'>About Us</h1>", unsafe_allow_html=True
    )
    st.caption("12 anggota Kelompok 1 Tensor — arahkan kursor atau ketuk foto untuk melihat detail.")

    gambar_urls = [
        "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_",  # Andra
        "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_",  # Aisyah
        "https://drive.google.com/uc?export=view&id=1YeKupUCs6_H_DuShkwH-t6lDo0BWOM22",  # Aliya
        "https://drive.google.com/uc?export=view&id=1cH_4xLVVySDkjafokPLl4c7OCslSFOK7",  # Della
        "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_",  # Elsa
        "https://drive.google.com/uc?export=view&id=1-8b-WLrqBEMIkPIYROpuPfILcIgii7zG",  # Favian
        "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_",  # Felisya
        "https://drive.google.com/uc?export=view&id=19rya7Zkzck08XZf82EBAN4lWtMBxhA_f",  # Ghiyat
        "https://drive.google.com/uc?export=view&id=1gX1RV6SsMhWp1XVrI2-K71MKNRCHhlDd",  # Lutfi
        "https://drive.google.com/uc?export=view&id=1STo9XNgWn-WbbwlvaipBo79sf-GZtEX-",  # Nazlah
        "https://drive.google.com/uc?export=view&id=15CBRRE1N-puql9vHfJRm27UoCoGYGp9E",  # Razan
        "https://drive.google.com/uc?export=view&id=1tBo0l5pxH4N8o3rNk-Iupet4c12OATy_",  # Rozak
    ]
    data_list = [
        {
            "nama": "Andra",
            "sebagai": "Pak Lurah",
            "nim": "122450016",
            "fun_fact": "suka makan pedes, tapi ga suka efeknya",
            "motto_hidup": "new semester new me",
        },
        {
            "nama": "Aisyah",
            "sebagai": "Bu Lurah",
            "nim": "122450000",
            "fun_fact": "nyemilin es bata",
            "motto_hidup": "Ya apa ya",
        },
        {
            "nama": "Alya",
            "sebagai": "Anggota",
            "nim": "122450091",
            "fun_fact": "takut kucing tapi suka liat nya",
            "motto_hidup": "Setap hari adalah kesempatan baru untuk lebih baik",
        },
        {
            "nama": "Della",
            "sebagai": "Anggotaa",
            "nim": "122450000",
            "fun_fact": "suka membayangkan domba lompat pager kalo mau tidur ,biar cepet tidur",
            "motto_hidup": "jalanin yang membuatmu bahagia dengan sebaik-baiknya",
        },
        {
            "nama": "Elsa",
            "sebagai": "Anggotaa",
            "nim": "122450088",
            "fun_fact": "Makan sayur tapi, ga makan tangkainya",
            "motto_hidup": "Untuk segala sesuatu ada masanya, untuk apa pun di bawah langit ada waktunya.",
        },
        {
            "nama": "Favian",
            "sebagai": "Anggotaa paling cool abiezzz",
            "nim": "124450021",
            "fun_fact": "Suka berdialog sama diri sendiri",
            "motto_hidup": "anything that happens to you, tetaplah jadi manusia yang baik",
        },
        {
            "nama": "Felisya",
            "sebagai": "Anggotaa",
            "nim": "122450100",
            "fun_fact": "nyemilin es bata, kiko",
            "motto_hidup": "jalanin dulu keles",
        },
        {
            "nama": "Ghiyats",
            "sebagai": "Anggotaa",
            "nim": "122450110",
            "fun_fact": "apapun game yang dimainin pasti bagus",
            "motto_hidup": "yang penting hidup dulu",
        },
        {
            "nama": "Lutfi",
            "sebagai": "Anggotaa",
            "nim": "124450047",
            "fun_fact": "Makan sayur hanya daunnya saja tidak dengan tangkainya",
            "motto_hidup": "Man Jadda Wa Jadda",
        },
        {
            "nama": "Nazlah Auliya",
            "sebagai": "Anggotaa",
            "nim": "124450054",
            "fun_fact": "susah hapalin nama orang baru",
            "motto_hidup": "tebarkan kebaikan maka ia akan kembali padamu",
        },
        {
            "nama": "Razan",
            "sebagai": "Anggotaa",
            "nim": "124450031",
            "fun_fact": "Sudah pernah main salju",
            "motto_hidup": "Tidak semua bisa dimiliki, tapi semuanya bisa di syukuri",
        },
        {
            "nama": "Rozak",
            "sebagai": "Anggotaa",
            "nim": "122450110",
            "fun_fact": "nyemilin es bata, kiko",
            "motto_hidup": "jalanin dulu keles",
        },
    ]
    render_profiles(gambar_urls, data_list, ABOUT_FIELDS, flip=True)
