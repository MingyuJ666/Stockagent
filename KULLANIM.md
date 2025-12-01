# NVIDIA Finansal Danışman

Otomatik NVIDIA hisse analizi ve Telegram bildirimleri.

## Hızlı Başlangıç

```powershell
# Tek analiz (önerilen başlangıç)
python financial_advisor.py --once --agents 5

# 7/24 otomatik (günde 3 analiz: 09:00, 13:00, 17:00)
python financial_advisor.py --agents 7

# Telegram bildirimlerini kapat
python financial_advisor.py --once --no-telegram
```

## Maliyet Hesabı

| Ajan Sayısı | 1 Analiz | Günlük (3×) | Aylık |
|-------------|----------|-------------|--------|
| 5 ajan      | $0.003   | $0.009      | $0.27  |
| 7 ajan ⭐   | $0.004   | $0.012      | $0.36  |
| 10 ajan     | $0.006   | $0.018      | $0.54  |

**Önerilen:** `--agents 7` (kalite/fiyat dengesi)

## Çıktılar

- **Konsol:** Özet rapor
- **Telegram:** Detaylı bildirim (emoji ile)
- **Dosyalar:** `advisor_results/` klasörü
  - `analysis_YYYYMMDD_HHMMSS.json` (tam veri)
  - `report_YYYYMMDD_HHMMSS.txt` (özet)

## Ayarlar

`util.py` dosyasında:
- `OPENAI_API_KEY` - OpenAI API anahtarı
- `TELEGRAM_BOT_TOKEN` - Bot token
- `TELEGRAM_CHAT_ID` - Chat ID (otomatik ayarlanır)

## Notlar

- İlk çalıştırmada bot'a Telegram'dan `/start` gönderin
- Chat ID otomatik kaydedilir
- SSL hatası olursa alternatif API devreye girer
- Her analiz 5-10 dakika sürer
