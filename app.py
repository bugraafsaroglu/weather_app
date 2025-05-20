from flask import Flask, render_template, request
from weather.api import get_weather, get_multiple_city_weather, get_hourly_weather, get_daily_forecast, save_weather_to_csv
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

API_KEY = "10f73b718e8240b2a8493911251504"  # API key

# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html')

# Birden fazla şehir için hava durumu
@app.route('/multiple', methods=['POST'])
def multiple_weather():
    cities = request.form['cities'].split(',')
    weather_data = get_multiple_city_weather(cities)
    return render_template('multiple_weather.html', weather_data=weather_data)

# Saatlik hava durumu grafiği
@app.route('/hourly', methods=['POST'])
def hourly_weather():
    city = request.form['city']
    hourly_data = get_hourly_weather(city)

    if hourly_data:
        hours = [str(hour['time'].split(' ')[1]) for hour in hourly_data]
        temps = [hour['temp_c'] for hour in hourly_data]

        # Grafik oluşturma
        plt.plot(hours, temps)
        plt.title(f"{city} Saatlik Sıcaklık Değerleri")
        plt.xlabel("Saat")
        plt.ylabel("Sıcaklık (°C)")
        plt.xticks(rotation=45)

        # Grafik görselini base64 formatında al
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode('utf-8')
        return render_template('hourly_weather.html', graph_url=graph_url)
    else:
        return "Hata: Saatlik hava durumu verisi alınamadı."

# Günlük hava durumu tahmini
@app.route('/daily', methods=['POST'])
def daily_weather():
    city = request.form['city']
    daily_data = get_daily_forecast(city)

    return render_template('daily_weather.html', daily_data=daily_data)

# Hava durumu verisini CSV'ye kaydet
@app.route('/save_csv', methods=['POST'])
def save_csv():
    city = request.form['city']
    weather_data = get_weather(city)

    if weather_data:
        save_weather_to_csv(city, weather_data)
        return f"{city} hava durumu verisi CSV dosyasına kaydedildi."
    else:
        return "Hata: API'den veri alınamadı."

if __name__ == '__main__':
    app.run(debug=True)
