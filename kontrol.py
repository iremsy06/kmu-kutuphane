import os
import pandas as pd

print("\n" + "="*40)
print("🔍 DEDEKTİF MODU BAŞLADI")
print("="*40)

# 1. Python şu an hangi klasörde çalışıyor?
klasor = os.getcwd()
print(f"📂 Python şu an bu klasöre bakıyor:\n{klasor}")

# 2. Bu klasörde 'books.csv' var mı?
dosya_adi = "books.csv"
dosya_yolu = os.path.join(klasor, dosya_adi)

if os.path.exists(dosya_yolu):
    print(f"\n✅ EVET! '{dosya_adi}' dosyası burada bulundu.")
    
    # 3. Dosyayı okumayı deneyelim
    print("⏳ Dosya okunmaya çalışılıyor...")
    try:
        # Önce virgülle ayrılmış mı diye bakıyoruz
        df = pd.read_csv(dosya_yolu, nrows=5)
        print("✅ BAŞARILI! Dosya okundu.")
        print("-" * 20)
        print("SÜTUN İSİMLERİ (Bunları bana söylemelisin):")
        print(list(df.columns))
        print("-" * 20)
    except Exception as e:
        print(f"❌ Dosya var ama okurken hata verdi: {e}")
        print("Belki noktalı virgül (;) kullanılmıştır veya dosya bozuktur.")
else:
    print(f"\n❌ HAYIR! Python '{dosya_adi}' dosyasını bulamadı.")
    print("🤔 Acaba dosyanın adı farklı olabilir mi?")
    print("\n📂 Bu klasördeki diğer dosyalar şunlar:")
    for d in os.listdir():
        print(f" - {d}")

print("="*40 + "\n")