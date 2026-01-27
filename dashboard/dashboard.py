import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

def load_data():
    return pd.read_csv("main_data.csv")

main_data = load_data()

with st.sidebar:
    st.image("https://share.google/TPsEJQmFh94HnTdoM")
    st.header("Filter Eksplorasi")
    
    # Filter Musim
    selected_season = st.multiselect(
        "Pilih Musim:",
        options=main_data['season_hour'].unique(),
        default=main_data['season_hour'].unique()
    )

main_df = main_data[main_data['season_hour'].isin(selected_season)]

st.title("Bicycle Rental Dashboard")
st.markdown("Dashboard ini menampilkan analisis perilaku penyewa sepeda berdasarkan pola waktu dan kondisi lingkungan.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{main_df['cnt_hour'].sum():,}")
with col2:
    st.metric("Rata-rata Sewa/Jam", f"{int(main_df['cnt_hour'].mean()):,}")
with col3:
    st.metric("Suhu Rata-rata", f"{main_df['temp_hour'].mean():.2f}°C")

st.divider()

st.subheader("1. Pola Waktu: Hari Kerja vs Akhir Pekan")
fig_hour, ax_hour = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=main_df, 
    x='hr', 
    y='cnt_hour', 
    hue='workingday_hour', 
    palette={'Weekend/Holiday': 'orange', 'Working Day': 'blue'},
    marker='o', ax=ax_hour
)
ax_hour.set_title("Rata-rata Penyewaan Sepeda per Jam")
ax_hour.set_xlabel("Jam (0-23)")
ax_hour.set_ylabel("Jumlah Penyewa")
st.pyplot(fig_hour)

st.subheader("2. Dampak Faktor Eksternal")
c1, c2 = st.columns(2)

with c1:
    fig_s, ax_s = plt.subplots()
    sns.barplot(data=main_df, x='season_day', y='cnt_day', palette='viridis', ax=ax_s)
    ax_s.set_title("Berdasarkan Musim")
    st.pyplot(fig_s)

with c2:
    fig_w, ax_w = plt.subplots()
    sns.barplot(data=main_df, x='weathersit_hour', y='cnt_hour', palette='magma', ax=ax_w)
    ax_w.set_title("Berdasarkan Kondisi Cuaca")
    st.pyplot(fig_w)
    
st.subheader("3. Advanced Analysis: Demand Clustering (Suhu vs Total Sewa)")
fig_cluster, ax_cluster = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    data=main_df,
    x='temp_hour', 
    y='cnt_hour', 
    hue='demand_cluster',
    palette={'Low Demand': 'red', 'Medium Demand': 'orange', 'High Demand': 'green'},
    alpha=0.6, ax=ax_cluster
)
ax_cluster.set_title("Kluster Kategori Permintaan")
st.pyplot(fig_cluster)


st.caption("Copyright © 2026 - Bima Indra Sakti")
