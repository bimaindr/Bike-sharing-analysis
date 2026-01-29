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

# SIDEBAR FILTER
with st.sidebar:
    st.image("https://share.google/TPsEJQmFh94HnTdoM")
    
    # Filter Rentang Tanggal
    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Filter Kategori Musim
    selected_season = st.multiselect(
        label="Filter Musim",
        options=all_df["season_hour"].unique(),
        default=all_df["season_hour"].unique()
    )

# Menerapkan Filter ke Dataframe utama
main_df = all_df[
    (all_df["dteday"] >= pd.to_datetime(start_date)) & 
    (all_df["dteday"] <= pd.to_datetime(end_date)) &
    (all_df["season_hour"].isin(selected_season))
]

# MAIN PAGE
st.title("Bike Sharing Analysis Dashboard")

# Metriks Utama yang Berubah Sesuai Filter
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt_hour'].sum():,}")
with col2:
    st.metric("Rata-rata Sewa/Jam", value=f"{int(main_df['cnt_hour'].mean())}")
with col3:
    st.metric("Hari Unik", value=f"{main_df['dteday'].nunique()}")

st.divider()

# Row 2: Visualisasi Pertanyaan 1 (Pola Jam)
st.subheader("Pola Penyewaan: Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    data=main_df, 
    x='hr', 
    y='cnt_hour', 
    hue='workingday_hour', 
    palette="viridis",
    marker='o',
    ax=ax
)
ax.set_title(f"Tren per Jam ({start_date} s/d {end_date})", fontsize=20)
st.pyplot(fig)

# Row 3: Visualisasi Pertanyaan 2 & Clustering
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Pengaruh Kondisi Cuaca")
    fig2, ax2 = plt.subplots()
    sns.barplot(data=main_df, x='weathersit_hour', y='cnt_hour', palette='magma', ax=ax2)
    st.pyplot(fig2)

with col_b:
    st.subheader("Demand Clustering (Suhu)")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(
        data=main_df, 
        x='temp_hour', y='cnt_hour', 
        hue='demand_cluster', 
        palette={'Low Demand': 'red', 'Medium Demand': 'orange', 'High Demand': 'green'},
        ax=ax3
    )
    st.pyplot(fig3)

st.caption(f"Copyright © 2026 | Analisis oleh Bima Indra Sakti")


