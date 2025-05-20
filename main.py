import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTextEdit
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import csv

API_KEY = "10f73b718e8240b2a8493911251504"  # Kendi API anahtarınızı buraya yapıştırın


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
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&aqi=no&alerts=no&lang=tr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return data['forecast']['forecastday']
        except KeyError:
            return None
    return None


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌤️ Hava Durumu Uygulaması")
        self.setFixedSize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Başlık
        title = QLabel("Hava Durumu Uygulaması")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00796B; margin-bottom: 20px;")
        layout.addWidget(title)

        # Şehir girişi
        city_layout = QHBoxLayout()
        city_label = QLabel("Şehir Adı:")
        city_label.setFont(QFont("Arial", 14))
        city_label.setStyleSheet("color: #004D40;")
        city_layout.addWidget(city_label)

        self.city_input = QLineEdit()
        self.city_input.setFont(QFont("Arial", 14))
        self.city_input.setStyleSheet("""
            padding: 6px;
            border: 2px solid #00796B;
            border-radius: 8px;
            background-color: #E0F2F1;
            color: #004D40;
        """)
        city_layout.addWidget(self.city_input)
        layout.addLayout(city_layout)

        # Butonlar
        button_layout = QHBoxLayout()
        button_style = """
            QPushButton {
                background-color: #00796B;
                color: white;
                border-radius: 12px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #004D40;
            }
            QPushButton:pressed {
                background-color: #00251A;
            }
        """

        self.btn_current = QPushButton("Güncel Hava Durumu")
        self.btn_current.setStyleSheet(button_style)
        self.btn_current.clicked.connect(self.show_current_weather)
        button_layout.addWidget(self.btn_current)

        self.btn_hourly = QPushButton("Saatlik Tahmin")
        self.btn_hourly.setStyleSheet(button_style)
        self.btn_hourly.clicked.connect(self.show_hourly_weather)
        button_layout.addWidget(self.btn_hourly)

        self.btn_daily = QPushButton("Günlük Tahmin")
        self.btn_daily.setStyleSheet(button_style)
        self.btn_daily.clicked.connect(self.show_daily_weather)
        button_layout.addWidget(self.btn_daily)

        self.btn_save_csv = QPushButton("CSV'ye Kaydet")
        self.btn_save_csv.setStyleSheet(button_style)
        self.btn_save_csv.clicked.connect(self.save_current_weather_csv)
        button_layout.addWidget(self.btn_save_csv)

        layout.addLayout(button_layout)

        # Hava durumu sonucu
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Arial", 12))
        self.result_text.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #B2DFDB;
            border-radius: 8px;
            padding: 10px;
            color: #004D40;
        """)
        layout.addWidget(self.result_text)

        # İkon için label
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("background-color: #ffffff; border-radius: 8px; padding: 10px; margin-top: 10px;")
        layout.addWidget(self.icon_label)

        # Pencere arka planı
        self.setStyleSheet("background-color: #E0F7FA;")

        self.setLayout(layout)

    def show_current_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Uyarı", "Lütfen şehir adı girin.")
            return

        data = get_weather(city)
        if not data:
            QMessageBox.critical(self, "Hata", "Hava durumu verisi alınamadı.")
            return

        current = data.get('current', {})
        location = data.get('location', {})
        condition = current.get('condition', {})

        text = (
            f"Şehir: {location.get('name', city)}\n"
            f"Sıcaklık: {current.get('temp_c', 'Bilinmiyor')} °C\n"
            f"Nem: {current.get('humidity', 'Bilinmiyor')} %\n"
            f"Rüzgar: {current.get('wind_kph', 'Bilinmiyor')} km/h\n"
            f"Hava Durumu: {condition.get('text', 'Bilinmiyor')}"
        )
        self.result_text.setText(text)
        self.load_icon(condition.get('icon'))

        # Son gösterilen veriyi CSV için sakla
        self.last_weather_data = {
            'Şehir': location.get('name', city),
            'Sıcaklık (°C)': current.get('temp_c', 'Bilinmiyor'),
            'Nem (%)': current.get('humidity', 'Bilinmiyor'),
            'Rüzgar (km/h)': current.get('wind_kph', 'Bilinmiyor'),
            'Hava Durumu': condition.get('text', 'Bilinmiyor')
        }

    def show_hourly_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Uyarı", "Lütfen şehir adı girin.")
            return

        hours = get_hourly_weather(city)
        if not hours:
            QMessageBox.critical(self, "Hata", "Saatlik hava durumu verisi alınamadı.")
            return

        text = f"Saatlik Hava Durumu - {city}\n\n"
        for hour in hours:
            time = hour.get('time', 'Bilinmiyor')
            temp = hour.get('temp_c', 'Bilinmiyor')
            condition = hour.get('condition', {}).get('text', 'Bilinmiyor')
            text += f"{time}: {temp} °C, {condition}\n"

        self.result_text.setText(text)
        self.icon_label.clear()

    def show_daily_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Uyarı", "Lütfen şehir adı girin.")
            return

        days = get_daily_forecast(city)
        if not days:
            QMessageBox.critical(self, "Hata", "Günlük hava durumu verisi alınamadı.")
            return

        text = f"Günlük Hava Durumu - {city}\n\n"
        for day in days:
            date = day.get('date', 'Bilinmiyor')
            day_cond = day.get('day', {})
            max_temp = day_cond.get('maxtemp_c', 'Bilinmiyor')
            min_temp = day_cond.get('mintemp_c', 'Bilinmiyor')
            condition = day_cond.get('condition', {}).get('text', 'Bilinmiyor')
            text += f"{date}: Maks {max_temp} °C, Min {min_temp} °C, {condition}\n"

        self.result_text.setText(text)
        self.icon_label.clear()

    def load_icon(self, icon_url):
        if not icon_url:
            self.icon_label.clear()
            return

        # WeatherAPI'den gelen ikon url'si küçük başında '//', bunu http: ile tamamla
        if icon_url.startswith("//"):
            icon_url = "http:" + icon_url

        pixmap = self.get_pixmap_from_url(icon_url)
        if pixmap:
            self.icon_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.icon_label.clear()

    def get_pixmap_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            from PyQt6.QtGui import QImage
            image = QImage()
            image.loadFromData(response.content)
            return QPixmap.fromImage(image)
        except Exception as e:
            print("İkon yüklenemedi:", e)
            return None

    def save_current_weather_csv(self):
        try:
            data = getattr(self, 'last_weather_data', None)
            if not data:
                QMessageBox.warning(self, "Uyarı", "Önce hava durumu verisini görüntüleyin.")
                return

            with open('weather_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                # Dosya boşsa başlık yaz
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)

            QMessageBox.information(self, "Başarılı", "Veri CSV dosyasına kaydedildi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"CSV kaydetme hatası: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
