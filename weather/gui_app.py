import tkinter as tk
from tkinter import messagebox
from weather.utils import get_weather
from weather.visual import save_weather_to_csv

def get_weather_info():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Uyarı", "Lütfen şehir adı girin.")
        return
    
    data = get_weather(city)
    if data:
        # Örnek: data sözlük ise daha okunaklı gösterelim
        display_text = (
            f"Şehir: {city}\n"
            f"Sıcaklık: {data.get('temperature', 'Bilinmiyor')} °C\n"
            f"Nem: {data.get('humidity', 'Bilinmiyor')} %\n"
            f"Hava Durumu: {data.get('description', 'Bilinmiyor')}"
        )
        result_text.set(display_text)
        # Hava durumu ikonunu güncelle (eğer ekleyeceksen)
    else:
        messagebox.showerror("Hata", "Veri alınamadı.")

def save_csv_data():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Uyarı", "Lütfen şehir adı girin.")
        return
    
    data = get_weather(city)
    if data:
        save_weather_to_csv(city, data)
        messagebox.showinfo("Başarılı", f"{city} verisi CSV'ye kaydedildi.")
    else:
        messagebox.showerror("Hata", "Veri alınamadı.")

# Pencere oluşturma
root = tk.Tk()
root.title("🟡 Hava Durumu Uygulaması")
root.geometry("800x800")
root.config(bg="#87ceeb")  # Gökyüzü mavisi arka plan

# Başlık
title_label = tk.Label(root, text="Hava Durumu Uygulaması", font=("Helvetica", 18, "bold"), bg="#87ceeb", fg="white")
title_label.pack(pady=10)

# Şehir girişi çerçevesi
input_frame = tk.Frame(root, bg="#87ceeb")
input_frame.pack(pady=10)

city_label = tk.Label(input_frame, text="Şehir Adı:", font=("Helvetica", 14), bg="#87ceeb", fg="white")
city_label.pack(side="left", padx=5)

city_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=25)
city_entry.pack(side="left")

# Butonlar çerçevesi
button_frame = tk.Frame(root, bg="#87ceeb")
button_frame.pack(pady=10)

show_button = tk.Button(button_frame, text="Hava Durumunu Göster", font=("Helvetica", 12), bg="#007acc", fg="white", activebackground="#005f99", command=get_weather_info)
show_button.pack(side="left", padx=10)

save_button = tk.Button(button_frame, text="CSV'ye Kaydet", font=("Helvetica", 12), bg="#28a745", fg="white", activebackground="#1e7e34", command=save_csv_data)
save_button.pack(side="left", padx=10)

# Sonuç göstergesi
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Helvetica", 14), bg="#87ceeb", fg="white", justify="left", wraplength=400)
result_label.pack(pady=20)

root.mainloop()
