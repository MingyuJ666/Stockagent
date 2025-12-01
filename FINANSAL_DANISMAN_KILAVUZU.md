# 🤖 NVIDIA Otomatik Finansal Danışman

## 📋 Genel Bakış

Otomatik finansal danışman sistemi, NVIDIA hissesini **7/24 izler** ve günde **3 kez** (09:00, 13:00, 17:00) detaylı analiz yaparak size **alım/satım** sinyalleri verir.

---

## ✨ ÖZELLİKLER

### 🎯 Temel Özellikler

1. **📊 Otomatik Analiz**
   - Günde 3 kez (09:00, 13:00, 17:00) otomatik çalışır
   - 2 yıllık tarihsel veri üzerinden analiz
   - Gerçek zamanlı NASDAQ fiyat takibi

2. **📈 Teknik Analiz**
   - MA20, MA50, MA200 hareketli ortalamalar
   - Destek ve direnç seviyeleri
   - Volatilite hesaplama
   - Trend analizi

3. **🤖 AI Destekli Karar**
   - 10 bağımsız AI ajanı
   - Çoğunluk oylaması sistemi
   - Güven seviyesi hesaplama

4. **🎯 Akıllı Sinyaller**
   - ✅ **Alım Sinyalleri**: Fiyat giriş noktaları
   - ❌ **Satım Sinyalleri**: Kar realizasyon noktaları
   - 📊 **Hedef Fiyatlar**: Take-profit seviyeleri
   - 🛡️ **Stop-Loss**: Risk yönetimi

5. **💾 Otomatik Kayıt**
   - Her analiz JSON + TXT olarak kaydedilir
   - Tarihsel veri takibi
   - `advisor_results/` klasöründe

---

## 🚀 KULLANIM

### 1️⃣ Otomatik İzleme Modu (7/24)

```powershell
# Sürekli çalışır, günde 3 kez analiz yapar
python financial_advisor.py
```

**Çalışma Saatleri:**
- 🌅 **09:00** - Sabah analizi (piyasa açılışı)
- ☀️ **13:00** - Öğlen analizi
- 🌆 **17:00** - Akşam analizi (piyasa kapanış)

**Durdurmak için:** `Ctrl+C`

---

### 2️⃣ Tek Seferlik Analiz

```powershell
# Şimdi hemen bir analiz yap ve çık
python financial_advisor.py --once
```

**Ne zaman kullanılır?**
- Hemen bir karar almanız gerekiyorsa
- Sistemin düzgün çalıştığını test etmek için
- Zamanlanmış analizi beklemek istemiyorsanız

---

### 3️⃣ Özelleştirme

```powershell
# Daha fazla AI ajanı (daha hassas)
python financial_advisor.py --agents 20

# Farklı model
python financial_advisor.py --model gpt-4

# Tek analiz + fazla ajan
python financial_advisor.py --once --agents 15
```

---

## 📊 ÖRNEK ÇIKTI

```
======================================================================
  💰 NVIDIA (NVDA) - FİNANSAL DANIŞMAN RAPORU
======================================================================

💵 GÜNCEL FİYAT: $179.50

📊 TEKNİK GÖSTERGELER:
   • MA20:  $183.25 ❌
   • MA50:  $175.80 ✅
   • MA200: $125.30 ✅
   • Volatilite: $8.45
   • Kısa Vadeli Trend: -2.1%
   • Orta Vadeli Trend: +15.3%

🎯 DESTEK/DİRENÇ SEVİYELERİ:
   • Direnç 2: $207.04
   • Direnç 1: $200.15
   • Fiyat:    $179.50 ◄
   • Destek 1: $166.35
   • Destek 2: $175.80

🤖 AI AJANLARININ TAVSİYESİ:
   • Tavsiye: AL
   • Güven: Orta
   • AL: 6/10 (%60)
   • SAT: 3/10 (%30)
   • BEKLE: 1/10 (%10)

🟢 ALIM SİNYALLERİ (2 sinyal):

   1. 🟢 ALIM FIRSATI
      Sebep: Fiyat MA20 ($183.25) altında, AI %60 AL öneriyor
      Giriş: $179.50
      Hedef 1: $183.25 (+2.1%)
      Hedef 2: $200.15 (+11.5%)
      Stop-Loss: $166.35 (-7.3%)

   2. 🟡 DESTEK SEVİYESİ
      Sebep: Fiyat destek seviyesine ($166.35) yakın
      Giriş: $179.50
      Hedef 1: $183.25 (+2.1%)
      Hedef 2: $175.80 (-2.1%)
      Stop-Loss: $161.36 (-10.1%)

======================================================================
  💡 GENEL DEĞERLENDİRME
======================================================================

  🟢 ALIM FIRSATI VAR!
     2 farklı alım sinyali tespit edildi.
     Risk/Ödül oranınızı hesaplayın ve pozisyon açmayı düşünün.

======================================================================

💾 Rapor kaydedildi: analysis_20251201_210030.json
```

---

## 🎯 SİNYAL TİPLERİ

### 🟢 Alım Sinyalleri

| Sinyal | Açıklama | Ne Zaman? |
|--------|----------|-----------|
| 🟢 **ALIM FIRSATI** | Fiyat MA20 altında + AI AL diyor | Güçlü giriş noktası |
| 🟡 **DESTEK SEVİYESİ** | Fiyat destek seviyesine yakın | Teknik geri tepme |
| 🔥 **GÜÇLÜ AL SİNYALİ** | AI %70+ AL öneriyor | Yüksek konsensüs |
| ⭐ **TREND DEĞİŞİMİ** | Golden Cross potansiyeli | Uzun vadeli yükseliş |

### 🔴 Satım Sinyalleri

| Sinyal | Açıklama | Ne Zaman? |
|--------|----------|-----------|
| 🔴 **KAR REALIZASYONU** | Fiyat direnç seviyesinde | Kar al |
| ⚠️ **GÜÇLÜ SAT SİNYALİ** | AI %60+ SAT öneriyor | Pozisyon azalt |
| 📉 **TREND KIRILMASI** | MA20 altına düştü | Stop-loss kontrolü |

---

## 📁 DOSYA YAPISI

```
Stockagent/
├── financial_advisor.py      # Ana danışman sistemi
├── advisor_results/           # Analiz sonuçları
│   ├── analysis_20251201_090000.json
│   ├── report_20251201_090000.txt
│   ├── analysis_20251201_130000.json
│   └── ...
└── ...
```

---

## 💡 KULLANIM ÖNERİLERİ

### ✅ Yapmanız Gerekenler

1. **Sabah Analizi (09:00)**
   - Günlük stratejinizi belirleyin
   - Alım sinyalleri varsa hazır olun

2. **Öğlen Analizi (13:00)**
   - Piyasa ortasında durum değerlendirmesi
   - Stop-loss kontrolü

3. **Akşam Analizi (17:00)**
   - Günü değerlendirin
   - Yarın için plan yapın

4. **Sinyalleri Takip Edin**
   - Alım sinyali geldiğinde fiyatları takip edin
   - Hedef fiyatlara ulaşınca kısmi kar alın
   - Stop-loss'u mutlaka ayarlayın

### ❌ Yapmayın

1. ❌ **Körü körüne takip etmeyin**
   - Sistemi diğer analizlerle birleştirin
   - Kendi araştırmanızı yapın

2. ❌ **Her sinyalde işlem yapmayın**
   - Güven seviyesi "Yüksek" olanları tercih edin
   - 2+ sinyal birlikte geldiğinde güçlüdür

3. ❌ **Stop-loss'u ihmal etmeyin**
   - Her alımda mutlaka stop-loss ayarlayın
   - Önerilen seviyelere uyun

---

## 🔧 SORUN GİDERME

### Problem: "API anahtarı hatası"
**Çözüm:** `util.py` dosyasında `OPENAI_API_KEY` kontrol edin

### Problem: "Veri çekilemiyor"
**Çözüm:** İnternet bağlantınızı kontrol edin, VPN kapalı olsun

### Problem: "Yavaş çalışıyor"
**Çözüm:** Ajan sayısını azaltın: `--agents 5`

### Problem: "Zamanlama çalışmıyor"
**Çözüm:** 
- Bilgisayarın uyku moduna girmediğinden emin olun
- Saat dilimini kontrol edin

---

## 📊 PERFORMANS İPUÇLARI

### Hızlı Analiz
```powershell
python financial_advisor.py --once --agents 5
# Süre: ~5 dakika
```

### Dengeli Analiz (Önerilen)
```powershell
python financial_advisor.py --agents 10
# Süre: ~10 dakika per analiz
```

### Detaylı Analiz
```powershell
python financial_advisor.py --agents 20
# Süre: ~20 dakika per analiz
```

---

## 🎯 ÖRNEK SENARYOLAR

### Senaryo 1: Sabah Rutini

```powershell
# 1. Gece boyunca sistem çalışsın
python financial_advisor.py

# 2. Sabah 09:00'da otomatik analiz
# 3. Bildirim gelir, raporları kontrol edin
# 4. Alım sinyali varsa broker'a gidin
```

### Senaryo 2: Hızlı Karar

```powershell
# Hemen bir analiz yapın
python financial_advisor.py --once

# Sonucu görün ve karar verin
```

### Senaryo 3: Hafta Sonu Değerlendirme

```powershell
# Hafta sonu analiz yapın
python financial_advisor.py --once --agents 20

# Detaylı raporu inceleyin
# Gelecek hafta için strateji belirleyin
```

---

## ⚠️ YASAL UYARI

```
Bu sistem EĞİTİM ve ARAŞTIRMA amaçlıdır.

❌ FİNANSAL TAVSİYE DEĞİLDİR
❌ YATIRIM ÖNERİSİ DEĞİLDİR
❌ GARANTİ VERİLMEZ

✅ Profesyonel danışman ile konuşun
✅ Kendi araştırmanızı yapın
✅ Risk yönetimi uygulayın
✅ Kaybedebileceğinizden fazlasını yatırmayın
```

---

## 🆘 DESTEK

- **Loglar:** `log/` klasörü
- **Sonuçlar:** `advisor_results/` klasörü
- **Sistem Kontrolü:** `python check_setup.py`

---

## 🎉 BAŞARILAR!

Artık NVIDIA için otomatik finansal danışmanınız var!

**Başlatmak için:**
```powershell
python financial_advisor.py
```

**İyi yatırımlar! 🚀📈💰**
