import requests

API_KEY = "10f73b718e8240b2a8493911251504"  # Kendi API anahtarını buraya yapıştır

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no&lang=tr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_hourly_weather(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no&lang=tr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return data['forecast']['forecastday'][0]['hour']
        except (KeyError, IndexError):
            return None
    return None

def get_daily_forecast(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&lang=tr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['forecast']['forecastday']
    return None

def save_weather_to_csv(city, weather_data):
    import csv
    with open(f"{city}_weather.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Şehir", "Sıcaklık(°C)", "Hava Durumu", "Nem(%)", "Rüzgar(kmh)"])
        writer.writerow([
            weather_data['location']['name'],
            weather_data['current']['temp_c'],
            weather_data['current']['condition']['text'],
            weather_data['current']['humidity'],
            weather_data['current']['wind_kph']
        ])
