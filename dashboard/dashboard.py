import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

sns.set(style='white')

# Menyiapkan data day_df
day_df = pd.read_csv("main_data.csv")

day_df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather',
    'hum': 'humidity',
    'cnt': 'count'
}, inplace=True)

day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

day_df['year'] = day_df['year'].map({0: '2011', 1: '2012'})

day_df['month'] = day_df['month'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Des'})

day_df['weekday'] = day_df['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})

day_df['weather'] = day_df['weather'].map({1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain'})

day_df.head()

# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather').agg({
        'count': 'sum'
    })
    return weather_rent_df

# Membuat komponen filter
min_date = pd.to_datetime(day_df['date']).dt.date.min()
max_date = pd.to_datetime(day_df['date']).dt.date.max()

with st.sidebar:
    st.image('https://i.pinimg.com/564x/22/3b/74/223b74ef5162b74938fc76adecd39e36.jpg')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['date'] >= str(start_date)) & 
                (day_df['date'] <= str(end_date))]

# Menyiapkan berbagai dataframe
season_rent_df = create_season_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Membuat judul dashboard
st.header('Dashboard Penyewaan Sepeda')

# Visualizations
years = main_df['year'].unique()
casual_usage = main_df.groupby('year')['casual'].sum()
registered_usage = main_df.groupby('year')['registered'].sum()
bar_positions = np.arange(len(years))
bar_width = 0.35

st.header("Penyewa Sepeda pada Tahun 2011 dan 2012")
fig_yearly_usage = plt.figure()
plt.bar(bar_positions, casual_usage, width=bar_width, label='Casual')
plt.bar(bar_positions + bar_width, registered_usage, width=bar_width, label='Registered')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Penyewa')
plt.title('Tren Penyewaan Sepeda Berdasarkan Tahun')
plt.xticks(bar_positions + bar_width / 2, years)
plt.legend()
st.pyplot(fig_yearly_usage)

st.header("Penyewa Sepeda Berdasarkan Musim")
seasonal_usage = day_df.groupby('season')[['count']].sum().reset_index()
seasons = seasonal_usage['season']
registered = seasonal_usage['count']
colors = ['#4169E1', '#FF8C00', '#228B22', '#B22222']
fig_seasonal_usage = plt.figure(figsize=(8, 8))
plt.pie(registered, labels=seasons, autopct='%1.1f%%', colors=colors, startangle=90, counterclock=False)
plt.title('Persentase Penyewa Sepeda Berdasarkan Musim')
st.pyplot(fig_seasonal_usage)

st.header("Penyewa Sepeda Berdasarkan Hari Libur, Hari Biasa, dan Hari Kerja")
fig_days_usage, axes_days = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))
sns.barplot(x='holiday', y='count', data=day_df, ax=axes_days[0])
axes_days[0].set_title('Jumlah Penyewa Sepeda Pada Hari Libur')
axes_days[0].set_xlabel('Hari Libur')
axes_days[0].set_ylabel('Jumlah Penyewa Sepeda')

sns.barplot(x='weekday', y='count', data=day_df, ax=axes_days[1])
axes_days[1].set_title('Jumlah Penyewa Sepeda Pada Hari Biasa')
axes_days[1].set_xlabel('Hari Biasa')
axes_days[1].set_ylabel('Jumlah Penyewa Sepeda')

sns.barplot(x='workingday', y='count', data=day_df, ax=axes_days[2])
axes_days[2].set_title('Jumlah Penyewa Sepeda Pada Hari Kerja')
axes_days[2].set_xlabel('Hari Kerja')
axes_days[2].set_ylabel('Jumlah Penyewa Sepeda')

plt.tight_layout()
st.pyplot(fig_days_usage)

st.header("Hubungan Temp, Atemp, Humidity, Windspeed dengan Jumlah Penyewa")
usage = day_df.groupby('count')[['temp', 'atemp', 'humidity', 'windspeed']].sum().reset_index()
fig_weather_relationship = plt.figure(figsize=(10, 6))
plt.scatter(usage['temp'], usage['count'], label='Temp', marker='o')
plt.scatter(usage['atemp'], usage['count'], label='Atemp', marker='o')
plt.scatter(usage['humidity'], usage['count'], label='Humidity', marker='o')
plt.scatter(usage['windspeed'], usage['count'], label='Windspeed', marker='o')
plt.xlabel('Nilai Pengukuran')
plt.ylabel('Jumlah Penyewa')
plt.legend()
st.pyplot(fig_weather_relationship)
