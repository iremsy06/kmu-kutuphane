import pandas as pd
import os

# --- 1. SENİN MEVCUT KİTAPLARINI OKUYALIM ---
# Eğer dosyan varsa okuyoruz, yoksa boş sayfa açıyoruz.
eski_veri = pd.DataFrame()
if os.path.exists("kitaplar.csv"):
    try:
        eski_veri = pd.read_csv("kitaplar.csv")
        print("✅ Senin eski kitapların bulundu ve hafızaya alındı.")
    except:
        print("⚠️ Eski dosya okunamadı ama sorun değil, devam ediyoruz.")

# --- 2. BENİM EKLEYECEĞİM YENİ KİTAPLAR ---
yeni_kitaplar = [
    {"Kitap Adi": "Nutuk", "Yazar": "Mustafa Kemal Atatürk", "Yayin Yili": 1927, "Durum": "Mevcut"},
    {"Kitap Adi": "Geometri", "Yazar": "Mustafa Kemal Atatürk", "Yayin Yili": 1937, "Durum": "Mevcut"},
    {"Kitap Adi": "Çalıkuşu", "Yazar": "Reşat Nuri Güntekin", "Yayin Yili": 1922, "Durum": "Mevcut"},
    {"Kitap Adi": "İnce Memed 1", "Yazar": "Yaşar Kemal", "Yayin Yili": 1955, "Durum": "Mevcut"},
    {"Kitap Adi": "Tutunamayanlar", "Yazar": "Oğuz Atay", "Yayin Yili": 1972, "Durum": "Mevcut"},
    {"Kitap Adi": "Saatleri Ayarlama Enstitüsü", "Yazar": "Ahmet Hamdi Tanpınar", "Yayin Yili": 1961, "Durum": "Mevcut"},
    {"Kitap Adi": "Kürk Mantolu Madonna", "Yazar": "Sabahattin Ali", "Yayin Yili": 1943, "Durum": "Mevcut"},
    {"Kitap Adi": "Aşk-ı Memnu", "Yazar": "Halid Ziya Uşaklıgil", "Yayin Yili": 1900, "Durum": "Mevcut"},
    {"Kitap Adi": "Yaban", "Yazar": "Yakup Kadri Karaosmanoğlu", "Yayin Yili": 1932, "Durum": "Mevcut"},
    {"Kitap Adi": "Sinekli Bakkal", "Yazar": "Halide Edib Adıvar", "Yayin Yili": 1936, "Durum": "Mevcut"},
    {"Kitap Adi": "Dokuzuncu Hariciye Koğuşu", "Yazar": "Peyami Safa", "Yayin Yili": 1930, "Durum": "Mevcut"},
    {"Kitap Adi": "Aylak Adam", "Yazar": "Yusuf Atılgan", "Yayin Yili": 1959, "Durum": "Mevcut"},
    {"Kitap Adi": "Bereketli Topraklar Üzerinde", "Yazar": "Orhan Kemal", "Yayin Yili": 1954, "Durum": "Mevcut"},
    {"Kitap Adi": "Devlet Ana", "Yazar": "Kemal Tahir", "Yayin Yili": 1967, "Durum": "Mevcut"},
    {"Kitap Adi": "Eylül", "Yazar": "Mehmet Rauf", "Yayin Yili": 1901, "Durum": "Mevcut"},
    {"Kitap Adi": "Araba Sevdası", "Yazar": "Recaizade Mahmut Ekrem", "Yayin Yili": 1896, "Durum": "Mevcut"},
    {"Kitap Adi": "Şimdiki Çocuklar Harika", "Yazar": "Aziz Nesin", "Yayin Yili": 1967, "Durum": "Mevcut"},
    {"Kitap Adi": "Semaver", "Yazar": "Sait Faik Abasıyanık", "Yayin Yili": 1936, "Durum": "Mevcut"},
    {"Kitap Adi": "Safahat", "Yazar": "Mehmet Akif Ersoy", "Yayin Yili": 1911, "Durum": "Mevcut"},
    {"Kitap Adi": "Kendi Gök Kubbemiz", "Yazar": "Yahya Kemal Beyatlı", "Yayin Yili": 1961, "Durum": "Mevcut"}
]

# --- 3. BİRLEŞTİRME İŞLEMİ ---
# Yeni kitapları tabloya çevir
df_yeni = pd.DataFrame(yeni_kitaplar)

# Eskilerle yenileri alt alta yapıştır
toplam_veri = pd.concat([eski_veri, df_yeni], ignore_index=True)

# --- 4. TEMİZLİK (AYNI KİTAPLARI SİL) ---
# Eğer 'Nutuk' sende varsa, bir daha ekleyip 2 tane yapmasın diye temizliyoruz.
toplam_veri.drop_duplicates(subset=["Kitap Adi"], keep="first", inplace=True)

# --- 5. KAYDETME ---
toplam_veri.to_csv("kitaplar.csv", index=False)

print("\n🎉 HARİKA! İşlem bitti.")
print(f"Toplam Kitap Sayısı: {len(toplam_veri)} oldu.")
print("Şimdi ana programını çalıştırabilirsin.")