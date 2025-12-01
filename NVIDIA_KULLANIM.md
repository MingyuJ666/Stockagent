# 🚀 NVIDIA Al-Sat Tavsiye Sistemi - Kullanım Kılavuzu

## 📋 Hızlı Başlangıç

### 1️⃣ Kurulum

```powershell
# Gerekli paketleri yükle
pip install -r requirements.txt
```

### 2️⃣ API Key Ayarla

`util.py` dosyasını aç ve API anahtarını ekle:

```python
# Gemini kullanacaksan (ÜCRETSİZ):
GOOGLE_API_KEY = "buraya-gemini-api-anahtarini-yaz"

# veya GPT-4 kullanacaksan (ÜCRETLÜ):
OPENAI_API_KEY = "buraya-openai-api-anahtarini-yaz"
```

**🆓 Gemini API Anahtarı Nasıl Alınır?**
1. https://makersuite.google.com/app/apikey adresine git
2. "Create API Key" butonuna tıkla
3. Anahtarı kopyala ve `util.py`'ye yapıştır

### 3️⃣ NVIDIA Tavsiyesi Al

```powershell
# Basit kullanım (Gemini ile):
python nvidia_advisor.py

# GPT-4 ile kullanım:
python nvidia_advisor.py --model gpt-4

# Daha fazla AI ajanı ile (daha hassas analiz):
python nvidia_advisor.py --agents 20
```

---

## 📊 Sistem Nasıl Çalışır?

1. **📈 Gerçek Veri Çekimi**: yfinance ile NVIDIA'nın son 90 günlük fiyat geçmişini çeker
2. **🤖 AI Ajanları**: 10-20 bağımsız AI ajanı piyasayı analiz eder
3. **🧠 Karar Mekanizması**: Her ajan AL/SAT/BEKLE kararı verir
4. **🎯 Tavsiye**: Çoğunluk oyuna göre size tavsiye verilir

---

## 💡 Örnek Çıktı

```
==============================================================
  📊 NVIDIA (NVDA) ANALİZ RAPORU
  Tarih: 01/12/2025 14:30
==============================================================

💰 Güncel Fiyat: $142.35
📈 Son 90 Gün:
   • En Düşük: $118.42
   • En Yüksek: $148.88
   • Ortalama: $135.60
   • Durum: 📈 Ortalamadan YÜKSEK

🧠 AI Ajanları Analiz Ediyor...
  Ajan 1: ✅ AL - Fiyat: $142, Miktar: 10
  Ajan 2: ⏸️ BEKLE
  Ajan 3: ✅ AL - Fiyat: $141, Miktar: 15
  ...

==============================================================
  📊 SONUÇ ÖZETI
==============================================================
  ✅ AL oyları: 7/10 (70.0%)
  ❌ SAT oyları: 1/10 (10.0%)
  ⏸️ BEKLE oyları: 2/10 (20.0%)
==============================================================

  🎯 TAVSİYE: 🟢 AL TAVSİYESİ
  📝 Açıklama: AI ajanlarının çoğunluğu alım yapılmasını öneriyor.
  💪 Güven Seviyesi: Yüksek

⚠️ UYARI: Bu tavsiye yalnızca AI simülasyonuna dayalıdır.
```

---

## ⚙️ Gelişmiş Kullanım

### Tam Simülasyon Çalıştırma

```powershell
# 60 günlük detaylı simülasyon (daha uzun sürer):
python main.py --model gemini-pro
```

Bu mod:
- 20 AI ajanının 60 gün boyunca işlem yapmasını simüle eder
- Her günün sonunda ajanlar forum'da fikirlerini paylaşır
- Mali raporlar ve ekonomik olaylar simüle edilir
- Sonuçlar Excel dosyalarına kaydedilir

### Parametreleri Özelleştirme

`util.py` dosyasında şunları değiştirebilirsin:

```python
AGENTS_NUM = 20          # Ajan sayısı (daha fazla = daha yavaş ama daha hassas)
TOTAL_DATE = 60          # Simülasyon süresi (gün)
TOTAL_SESSION = 2        # Günlük işlem seans sayısı
STOCK_A_INITIAL_PRICE = 140  # NVIDIA başlangıç fiyatı
```

---

## 🎯 Hangi Modu Kullanmalıyım?

| Durum | Önerilen Komut | Süre |
|-------|---------------|------|
| **Hızlı tavsiye istiyorum** | `python nvidia_advisor.py` | ~2-5 dakika |
| **Daha hassas analiz** | `python nvidia_advisor.py --agents 20` | ~5-10 dakika |
| **Detaylı simülasyon** | `python main.py --model gemini-pro` | ~30-60 dakika |

---

## ❓ Sık Sorulan Sorular

**S: API anahtarı ücretsiz mi?**
A: Gemini API ücretsiz kotası var. GPT-4 ücretli.

**S: Tavsiyeler ne kadar güvenilir?**
A: AI simülasyonudur, %100 doğru değildir. Profesyonel danışman ile konuşun.

**S: Başka hisseler için kullanabilir miyim?**
A: Evet! `util.py`'de `STOCK_SYMBOL = "NVDA"` kısmını değiştir (örn: "TSLA", "AAPL")

**S: İnternet gerekli mi?**
A: Evet, hem API hem de hisse fiyatları için internet gerekli.

**S: Hatalar alıyorum?**
A: 
- API anahtarının doğru girildiğinden emin ol
- `pip install -r requirements.txt` komutunu çalıştırdığından emin ol
- İnternet bağlantını kontrol et

---

## 🔧 Sorun Giderme

### "ModuleNotFoundError: No module named 'yfinance'"
```powershell
pip install yfinance
```

### "API Key hatası"
`util.py` dosyasında API anahtarını kontrol et.

### "Rate limit exceeded"
API kotanız doldu. Birkaç dakika bekleyin veya farklı API kullanın.

---

## 📞 Destek

Sorun yaşarsan:
1. Hata mesajını oku
2. `log/` klasöründeki log dosyalarını kontrol et
3. API anahtarını ve internet bağlantını kontrol et

---

## ⚠️ YASAL UYARI

Bu yazılım yalnızca eğitim ve araştırma amaçlıdır. 
- Finansal tavsiye değildir
- Yatırım kararlarınızın sorumluluğu size aittir
- Geçmiş performans gelecek getiriyi garanti etmez
- Profesyonel finansal danışmanlık alın

**Kullanmadan önce risk toleransınızı değerlendirin!**
