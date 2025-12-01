# 🎯 NVIDIA Al-Sat Tavsiye Sistemi

AI destekli NVIDIA hisse analiz ve al-sat tavsiye sistemi. Gerçek piyasa verilerini kullanarak yapay zeka ajanları ile analiz yapar.

## ⚡ Hızlı Başlangıç

### 1. Paketleri Yükle
```powershell
pip install -r requirements.txt
```

### 2. API Anahtarı Ayarla

`util.py` dosyasını aç ve API anahtarını ekle:

```python
GOOGLE_API_KEY = "buraya-api-anahtarini-yaz"  # Ücretsiz: https://makersuite.google.com/app/apikey
```

### 3. Sistemi Test Et
```powershell
python check_setup.py
```

### 4. NVIDIA Tavsiyesi Al
```powershell
python nvidia_advisor.py
```

## 📖 Detaylı Kullanım

Tüm detaylar için **[NVIDIA_KULLANIM.md](NVIDIA_KULLANIM.md)** dosyasına bakın.

## 🎯 Özellikler

- ✅ Gerçek NVIDIA (NVDA) hisse fiyatları
- ✅ 10-20 bağımsız AI ajanı ile analiz
- ✅ AL/SAT/BEKLE tavsiyesi
- ✅ Güven seviyesi gösterimi
- ✅ Son 90 günlük fiyat geçmişi
- ✅ NVIDIA mali raporları ile analiz

## 🚀 Kullanım Modları

### 🟢 Hızlı Tavsiye (Önerilen)
```powershell
python nvidia_advisor.py
```
**Süre:** 2-5 dakika | **Çıktı:** AL/SAT/BEKLE tavsiyesi

### 🟡 Detaylı Analiz
```powershell
python nvidia_advisor.py --agents 20
```
**Süre:** 5-10 dakika | **Çıktı:** Daha hassas tavsiye

### 🔴 Tam Simülasyon
```powershell
python main.py --model gemini-pro
```
**Süre:** 30-60 dakika | **Çıktı:** 60 günlük detaylı simülasyon

## 📊 Örnek Çıktı

```
==============================================================
  📊 NVIDIA (NVDA) ANALİZ RAPORU
==============================================================

💰 Güncel Fiyat: $142.35
📈 Son 90 Gün: $118.42 - $148.88 (Ort: $135.60)

🧠 AI Ajanları Analiz Ediyor...
  ✅ AL oyları: 7/10 (70%)
  ❌ SAT oyları: 1/10 (10%)
  ⏸️ BEKLE oyları: 2/10 (20%)

  🎯 TAVSİYE: 🟢 AL TAVSİYESİ
  💪 Güven: Yüksek
```

## 🛠️ Gereksinimler

- Python 3.9+
- Gemini API (ücretsiz) veya OpenAI API (ücretli)
- İnternet bağlantısı

## ⚠️ Yasal Uyarı

Bu yazılım **eğitim amaçlıdır**. Finansal tavsiye değildir. Yatırım kararlarınızın sorumluluğu size aittir.

## 📞 Yardım

Sorun yaşıyorsan:
1. `python check_setup.py` - Kurulumu kontrol et
2. `NVIDIA_KULLANIM.md` - Detaylı kılavuzu oku
3. `log/` klasöründeki hata loglarına bak

## 🌟 İpuçları

- **Gemini kullan:** Ücretsiz ve hızlı
- **10-15 ajan yeterli:** Daha fazla = daha yavaş
- **Günde 1-2 kez çalıştır:** Sık kontrol etmeye gerek yok
- **Başka hisseler:** `util.py`'de `STOCK_SYMBOL` değiştir

---

**Made with ❤️ using AI Agents**
