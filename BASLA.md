# 🎯 NVIDIA AL-SAT SİSTEMİ - HIZLI BAŞLANGIÇ

## ⚡ 3 ADIMDA BAŞLA

### 1️⃣ Hızlı Kurulum
```powershell
python hizli_basla.py
```
Bu script sizin için her şeyi yapacak!

### 2️⃣ Manuel Kurulum (İsterseniz)

**a) API Anahtarı Al:**
- Gemini (ÜCRETSİZ): https://makersuite.google.com/app/apikey

**b) `util.py` dosyasını aç ve ekle:**
```python
GOOGLE_API_KEY = "buraya-api-anahtarini-yaz"
```

**c) Test et:**
```powershell
python check_setup.py
```

### 3️⃣ Analizi Çalıştır
```powershell
python nvidia_advisor.py
```

---

## 📊 NE BEKLEMELİSİN?

Sistem size şunu söyleyecek:
- 🟢 **AL** - NVIDIA almayı düşün
- 🔴 **SAT** - NVIDIA satmayı düşün  
- 🟡 **BEKLE** - Şimdi işlem yapma

Her tavsiyeyle birlikte:
- Güven seviyesi (Yüksek/Orta/Düşük)
- AI ajanlarının oy dağılımı
- Son 90 günlük fiyat analizi

---

## 🎮 KULLANIM MODLARİ

| Komut | Ne Yapar? | Süre |
|-------|-----------|------|
| `python nvidia_advisor.py` | Hızlı tavsiye | 2-5 dk |
| `python nvidia_advisor.py --agents 20` | Hassas tavsiye | 5-10 dk |
| `python main.py --model gemini-pro` | Tam simülasyon | 30-60 dk |

---

## 💡 İPUÇLARI

✅ **YAP:**
- Gemini kullan (ücretsiz ve hızlı)
- Günde 1-2 kez kontrol et
- Tavsiyeleri diğer analizlerle birleştir

❌ **YAPMA:**
- Sadece AI'ya güvenme
- Her saatte kontrol etme
- API kotanı tüketme

---

## ⚠️ ÖNEMLİ UYARI

Bu sistem **eğitim amaçlıdır**:
- Finansal tavsiye DEĞİLDİR
- Profesyonel danışman ile konuş
- Kaybedebileceğinden fazlasını yatırma
- Geçmiş performans gelecek getiri değildir

---

## 🆘 SORUN MU VAR?

```powershell
# Kurulumu kontrol et
python check_setup.py

# Logları kontrol et
dir log\
```

**Sık Sorunlar:**
- API anahtarı yok → `util.py` dosyasını düzenle
- Paket eksik → `pip install -r requirements.txt`
- İnternet hatası → VPN kapat, bağlantı kontrol et

---

## 📖 DAHA FAZLA BİLGİ

- **Detaylı Kılavuz:** `NVIDIA_KULLANIM.md`
- **Türkçe README:** `README_TURKISH.md`
- **Orijinal Proje:** `README.md`

---

## 🎉 HAZIRSIN!

```powershell
# Şimdi başla:
python nvidia_advisor.py
```

**Başarılar! 🚀**

---

Made with ❤️ for NVIDIA investors
