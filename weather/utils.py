import csv
from colorama import Fore, Style
from .api import get_weather

def save_weather_to_csv(city, weather_data):
    with open(f'{city}_weather.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Şehir", "Sıcaklık(°C)", "Hava Durumu", "Nem(%)", "Rüzgar(kmh)"])
        writer.writerow([
            weather_data['location']['name'],
            weather_data['current']['temp_c'],
            weather_data['current']['condition']['text'],
            weather_data['current']['humidity'],
            weather_data['current']['wind_kph']
        ])

def get_multiple_city_weather(cities):
    for city in cities:
        data = get_weather(city.strip())
        if data:
            print(f"{Fore.CYAN}🌆 Şehir: {data['location']['name']}")
            print(f"🌡️ Sıcaklık: {data['current']['temp_c']}°C")
            print(f"🌤️ Hava Durumu: {data['current']['condition']['text']}")
            print(f"💧 Nem: {data['current']['humidity']}%")
            print(f"🌬️ Rüzgar: {data['current']['wind_kph']} km/h{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Hata: {city.strip()} için veri alınamadı.{Style.RESET_ALL}\n")
