import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

path = Path(__file__).parent / "dashboard/main_data.csv"

# Baca dan Olah Data
bicycle_df_day = pd.read_csv(path) 
bicycle_df_day['dteday'] = pd.to_datetime(bicycle_df_day['dteday'])
bicycle_df_day['year_month'] = bicycle_df_day['dteday'].dt.to_period('M')
bicycle_df_day['season'] = bicycle_df_day['season'].map({1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'})

# Buat sidebar untuk memilih tanggal
min_date = bicycle_df_day["dteday"].min()
max_date = bicycle_df_day["dteday"].max()

st.sidebar.title("Pick the Date to Filter Data")
start_date, end_date = st.sidebar.date_input(label="Date Range", 
                                             min_value=min_date,
                                             max_value=max_date,
                                             value=[min_date, max_date]
                                             )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = bicycle_df_day[(bicycle_df_day['dteday'] >= start_date) & (bicycle_df_day['dteday'] <= end_date)]

def trend_df(df):
    monthly_users = df.groupby('year_month')[['casual', 'registered']].sum().reset_index()
    monthly_users['year_month'] = monthly_users['year_month'].astype(str)
    return monthly_users

def seasonal_df(df):
    return df.groupby('season')[['casual', 'registered']].sum().sort_values(by="registered", ascending=False)

def user_group(df):
    bins = [0, 2000, 4000, 6000, 8000, float('inf')]
    labels = ['<2000', '2000-4000', '4000-6000', '6000-8000', '>8000']
    filtered_df['cnt_group'] = pd.cut(filtered_df['cnt'], bins=bins, labels=labels, right=False)
    return filtered_df['cnt_group'].value_counts().sort_index()

st.header('Bike Sharing Dashboard - M Farrel Danendra Rachim')

# Tren Per Bulan Pengguna
monthly_users = trend_df(filtered_df)

st.subheader("Banyak Pengguna Bike Sharing dari Januari 2011 - Desember 2012")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_users['year_month'], monthly_users['casual'], label='Casual Users', marker='o')
ax.plot(monthly_users['year_month'], monthly_users['registered'], label='Registered Users', marker='o')
ax.set_xticks(range(len(monthly_users['year_month'])))
ax.set_xticklabels(monthly_users['year_month'], rotation=60)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Total users per season
total_users_per_season = seasonal_df(filtered_df)

st.subheader("Banyak Pengguna Bike Sharing Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 6))
total_users_per_season.plot(kind='bar', stacked=False, color=['blue', 'orange'], ax=ax)
ax.set_xlabel('')
ax.set_xticks(range(len(total_users_per_season.index)))
ax.set_xticklabels(total_users_per_season.index, rotation=0)
st.pyplot(fig)

# Manual Grouping Pengguna
user_group_counts = user_group(filtered_df)

st.subheader("Distribusi Pengguna Berdasarkan Jumlah Pengguna (Registered + Casual)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(user_group_counts.index, user_group_counts.values, color=['skyblue' if idx == user_group_counts.idxmax() else 'grey' for idx in user_group_counts.index])
ax.set_ylabel('Jumlah Hari', fontsize=12)
ax.set_xticks(range(len(user_group_counts.index)))
ax.set_xticklabels(user_group_counts.index, rotation=0)
st.pyplot(fig)


st.caption('Copyright © Farrel DR 2024')

