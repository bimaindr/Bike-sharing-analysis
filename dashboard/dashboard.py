import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

# LOAD DATA 
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

all_df = load_data()

# SIDEBAR: FILTERING
with st.sidebar:
    st.image("https://share.google/TPsEJQmFh94HnTdoM")
    st.header("Filter Eksplorasi")
    
    # Filter Rentang Tanggal
    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()
    
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except:
        st.stop()

    # Filter Musim
    selected_season = st.multiselect(
        "Pilih Musim:",
        options=all_df['season_hour'].unique(),
        default=all_df['season_hour'].unique()
    )

# Filter Dataset Berdasarkan Input Sidebar
main_df = all_df[
    (all_df["dteday"] >= pd.to_datetime(start_date)) & 
    (all_df["dteday"] <= pd.to_datetime(end_date)) &
    (all_df["season_hour"].isin(selected_season))
]

# MAIN PAGE
st.title("Bicycle Rental Dashboard")

# Metriks Utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt_hour'].sum():,}")
with col2:
    st.metric("Rata-rata Sewa/Jam", value=f"{int(main_df['cnt_hour'].mean()):,}")
with col3:
    st.metric("Total Hari", value=f"{main_df['dteday'].nunique()}")

st.divider()

# PERTANYAAN 1: POLA JAM
st.subheader("1. Pola Waktu: Hari Kerja vs Akhir Pekan")
fig_hour, ax_hour = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=main_df, 
    x='hr', y='cnt_hour', hue='workingday_hour', 
    palette={'Weekend/Holiday': '#FFA500', 'Working Day': '#6A0DAD'},
    linewidth=2.5, marker='o', ax=ax_hour
)
ax_hour.set_xlabel("Jam")
ax_hour.set_ylabel("Jumlah Penyewa")
st.pyplot(fig_hour)

# PERTANYAAN 2: DAMPAK CUACA & MUSIM (HARIAN)
st.subheader("2. Dampak Kondisi Lingkungan (Harian)")
col_a, col_b = st.columns(2)

with col_a:
    st.write("Dampak Kondisi Cuaca (Harian)")
    fig_weather, ax_weather = plt.subplots()
    sns.barplot(
        data=main_df,
        x='weathersit_day', 
        y='cnt_day',
        palette='viridis',
        ax=ax_weather
    )
    ax_weather.set_xlabel('Kondisi Cuaca')
    ax_weather.set_ylabel('Rata-rata Sewa Harian')
    st.pyplot(fig_weather)

with col_b:
    # REVISI: Menggunakan Box Plot untuk Dampak Musim Harian
    st.write("Distribusi Penyewaan Harian per Musim")
    fig_season, ax_season = plt.subplots()
    sns.boxplot(
        data=main_df, 
        x='season_day', 
        y='cnt_day', 
        palette='magma', 
        ax=ax_season
    )
    ax_season.set_xlabel('Musim')
    ax_season.set_ylabel('Total Sewa Harian')
    st.pyplot(fig_season)

# ANALISIS LANJUTAN
st.divider()
st.subheader("3. Advanced Analysis: Demand Clustering")
fig_cluster, ax_cluster = plt.subplots(figsize=(12, 5))
sns.scatterplot(
    data=main_df,
    x='temp_hour', y='cnt_hour', hue='demand_cluster',
    palette={'Low Demand': 'red', 'Medium Demand': 'orange', 'High Demand': 'green'},
    ax=ax_cluster
)
st.pyplot(fig_cluster)

st.caption(f"Copyright © 2026 - Bima Indra Sakti | Terakhir diperbarui pada {pd.Timestamp.now().strftime('%Y-%m-%d')}")



