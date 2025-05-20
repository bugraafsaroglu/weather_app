import matplotlib.pyplot as plt
from .api import get_hourly_weather, get_daily_forecast

def hourly_weather_graph(hours, temperatures):  # ✅ 2 ARGÜMAN ALACAK ŞEKİLDE GÜNCELLE
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))
    plt.plot(hours, temperatures, marker='o')
    plt.title("Saatlik Sıcaklık")
    plt.xlabel("Saat")
    plt.ylabel("Sıcaklık (°C)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def daily_forecast_graph(city):
    data = get_daily_forecast(city)
    if data:
        days = [day['date'] for day in data]
        temps = [day['day']['avgtemp_c'] for day in data]

        plt.figure(figsize=(8, 4))
        plt.bar(days, temps, color='orange')
        plt.title(f"{city} - 7 Günlük Ortalama Sıcaklık")
        plt.xlabel("Tarih")
        plt.ylabel("Ortalama Sıcaklık (°C)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Günlük tahmin alınamadı.")
