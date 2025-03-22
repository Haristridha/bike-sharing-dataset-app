import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("day_clean.csv")
hour_df = pd.read_csv("hour_clean.csv")

# Mapping season values
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}

day_df["season_name"] = day_df["season"].map(season_mapping)
hour_df["season_name"] = hour_df["season"].map(season_mapping)

# Tambahkan pilihan "All Season"
season_options = ["Seluruh Musim"] + list(season_mapping.values())

# Sidebar
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim:", options=season_options)

# Filter data berdasarkan pilihan musim
if selected_season == "Seluruh Musim":
    filtered_day_df = day_df
    filtered_hour_df = hour_df
else:
    filtered_day_df = day_df[day_df['season_name'] == selected_season]
    filtered_hour_df = hour_df[hour_df['season_name'] == selected_season]

# 1️⃣ Tren Penyewaan Sepeda
# Ubah format tanggal ke datetime
filtered_day_df["dteday"] = pd.to_datetime(filtered_day_df["dteday"])

# Tambahkan kolom bulan
filtered_day_df["month"] = filtered_day_df["dteday"].dt.strftime('%Y-%m')

# Hitung total penyewaan per bulan
monthly_summary = filtered_day_df.groupby("month")["cnt"].sum().reset_index()

# Plot
st.subheader("📊 Tren Penyewaan Sepeda Per Bulan")
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(data=monthly_summary, x="month", y="cnt", ax=ax, palette="Blues_d")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig)

# 2️⃣ Pengaruh Cuaca & Musim
st.subheader(f"☀️ Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda selama {selected_season}")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=filtered_day_df, x='weathersit', y='cnt', palette='coolwarm')
ax.set_xlabel("Kondisi Cuaca (1=Cerah, 2=Berawan, 3=Hujan)")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# 3️⃣ Waktu Puncak Peminjaman Sepeda
st.subheader("⏰ Waktu Puncak Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=filtered_hour_df, x='hr', y='cnt', ax=ax, errorbar=None)
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_xticks(range(0, 24))  # Menampilkan semua label jam
ax.grid(False)  # Hanya grid horizontal agar lebih rapi

st.pyplot(fig)

# 4️⃣ Eksplorasi Penyewaan Sepeda Berdasarkan Jam
st.sidebar.header("Eksplorasi Data")
hour_range = st.sidebar.slider("Pilih Rentang Jam Penyewaan:", 0, 23, (0, 23))

# Filter data berdasarkan jam yang dipilih
filtered_hour_range = filtered_hour_df[(filtered_hour_df["hr"] >= hour_range[0]) & (filtered_hour_df["hr"] <= hour_range[1])]

# Visualisasi interaktif
st.subheader("🔍 Eksplorasi Penyewaan Sepeda Berdasarkan Rentang Jam")
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(data=filtered_hour_range, x="hr", y="cnt", marker="o", ax=ax)
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_xticks(range(hour_range[0], hour_range[1] + 1))
ax.grid(True)
st.pyplot(fig)

# Footer
st.markdown("---")
st.write("🚲 **Dashboard dibuat dengan Streamlit** | Data dari sistem penyewaan sepeda")
 
