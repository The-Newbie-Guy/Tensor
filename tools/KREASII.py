"""KREASII — Suara Nama Tensor.

Ketik nama, tiap huruf menjadi satu nada di tangga C mayor dua oktaf.
Dengarkan melodinya, lihat kontur nada dan spektrumnya.
"""
import io

import numpy as np
import streamlit as st
from scipy.io import wavfile

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

BASE_FREQ = 261.63  # C4
PATTERN = [0, 2, 4, 5, 7, 9, 11]
NOTE_NAMES = ["C", "D", "E", "F", "G", "A", "B"]
SAMPLE_RATE = 8000

st.title("🎹 Suara Nama Tensor")
st.caption("Setiap huruf = satu nada. Nama yang sama selalu berbunyi sama — seperti NIM yang bisa dinyanyikan.")

nama = st.text_input("Ketik nama:", value="Tensor", max_chars=24, placeholder="mis. Razan")
durasi = st.slider("Durasi per nada (detik)", 0.15, 0.8, 0.35, 0.05)
volume = st.slider("Volume", 0.1, 1.0, 0.8, 0.05)

huruf = [c for c in nama.upper() if "A" <= c <= "Z"]
if not huruf:
    st.info("Ketik minimal satu huruf A–Z untuk membunyikan nama.")
    st.stop()

notasi = []
for c in huruf:
    idx = ord(c) - ord("A")
    offset = 12 * ((idx // 7) % 2) + PATTERN[idx % 7]
    freq = BASE_FREQ * (2 ** (offset / 12))
    not_name = f"{NOTE_NAMES[idx % 7]}{4 + ((idx // 7) % 2)}"
    notasi.append({"huruf": c, "nada": not_name, "frekuensi": round(freq, 1)})

st.dataframe(notasi, use_container_width=True, hide_index=True)

n_sample = int(SAMPLE_RATE * durasi)
t_note = np.linspace(0, durasi, n_sample, endpoint=False)
attack = max(1, int(0.01 * SAMPLE_RATE))
envelope = np.ones(n_sample)
envelope[:attack] = np.linspace(0, 1, attack)
envelope[-attack:] = np.linspace(1, 0, attack)

melodi = np.concatenate([
    np.sin(2 * np.pi * n["frekuensi"] * t_note) * envelope for n in notasi
])
melodi = (melodi / max(1e-9, np.max(np.abs(melodi))) * 32767 * volume).astype(np.int16)

buf = io.BytesIO()
wavfile.write(buf, SAMPLE_RATE, melodi)
buf.seek(0)
st.subheader("🔊 Dengarkan namamu")
st.audio(buf, format="audio/wav")
st.download_button(
    "⬇ Unduh melodi (WAV)",
    data=buf.getvalue(),
    file_name=f"suara_nama_{''.join(huruf).lower()}.wav",
    mime="audio/wav",
)

c1, c2, c3 = st.columns(3)
c1.metric("Jumlah nada", f"{len(notasi)}")
c2.metric("Durasi total", f"{len(notasi) * durasi:.1f} dtk")
tertinggi = max(notasi, key=lambda n: n["frekuensi"])
c3.metric("Nada tertinggi", f"{tertinggi['nada']} ({tertinggi['huruf']})")

freqs = [n["frekuensi"] for n in notasi]
labels = [f"{n['huruf']}·{n['nada']}" for n in notasi]

st.subheader("Kontur nada")
if HAS_PLOTLY:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=labels, y=freqs, mode="lines+markers",
        line=dict(color="#00C2A8", width=2),
        marker=dict(color="#101B3C", size=8), name="Frekuensi",
    ))
    fig1.update_layout(
        xaxis_title="Huruf · Nada", yaxis_title="Frekuensi (Hz)",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif"),
        margin=dict(l=40, r=20, t=30, b=40),
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.line_chart(freqs)

st.subheader("Spektrum melodi (FFT)")
y = melodi.astype(float) / 32768.0
N = len(y)
yf = np.fft.fft(y)
xf = np.fft.fftfreq(N, 1 / SAMPLE_RATE)
half = N // 2
if HAS_PLOTLY:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=xf[:half], y=np.abs(yf[:half]) / N, mode="lines",
        line=dict(color="#FF6F00", width=2), name="Magnitudo",
    ))
    fig2.update_layout(
        xaxis_title="Frekuensi (Hz)", yaxis_title="Magnitudo",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif"),
        margin=dict(l=40, r=20, t=30, b=40),
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.line_chart(np.abs(yf[:half]) / N)
