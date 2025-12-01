"""
NVIDIA Otomatik Finansal Danışman
Gunluk analiz ve Telegram bildirimleri
"""

import schedule
import time
import util
from datetime import datetime
from stock import Stock
from agent import Agent
from secretary import Secretary
from pathlib import Path
import json
import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError

class NvidiaFinancialAdvisor:
    def __init__(self, model="gpt-4o-mini", num_agents=10, enable_telegram=True):
        self.model = model
        self.num_agents = num_agents
        self.secretary = Secretary(model)
        self.analysis_history = []
        self.results_dir = Path("advisor_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Telegram ayarları
        self.enable_telegram = enable_telegram
        self.telegram_bot = None
        self.chat_id = None
        
        if self.enable_telegram:
            self._initialize_telegram()
        
        print("\n" + "="*70)
        print("  NVIDIA Finansal Danışman")
        print("="*70)
        print(f"  Model: {model}")
        print(f"  Ajanlar: {num_agents}")
        print(f"  Telegram: {'Aktif' if self.enable_telegram else 'Kapali'}")
        print("="*70 + "\n")
    
    def _initialize_telegram(self):
        """Telegram bot'u başlat"""
        try:
            if not util.TELEGRAM_BOT_TOKEN:
                print("Telegram bot token bulunamadi")
                self.enable_telegram = False
                return
            
            self.telegram_bot = Bot(token=util.TELEGRAM_BOT_TOKEN)
            
            # Chat ID'yi al (eğer ayarlanmışsa)
            if util.TELEGRAM_CHAT_ID:
                self.chat_id = util.TELEGRAM_CHAT_ID
                print(f"Telegram bot hazir (Chat ID: {self.chat_id})")
            else:
                print("TELEGRAM_CHAT_ID ayarlanmamis")
                self._get_chat_id()
                
        except Exception as e:
            print(f"Telegram hatasi: {e}")
            self.enable_telegram = False
    
    def _get_chat_id(self):
        """Chat ID'yi otomatik al"""
        try:
            print("Chat ID aliniyor...")
            
            for i in range(30):  # 30 saniye bekle
                updates = asyncio.run(self.telegram_bot.get_updates())
                if updates:
                    self.chat_id = str(updates[-1].message.chat_id)
                    print(f"Chat ID: {self.chat_id}")
                    
                    # util.py'ye kaydet
                    self._save_chat_id_to_config(self.chat_id)
                    return
                time.sleep(1)
            
            print("Chat ID alinamadi")
            
        except Exception as e:
            print(f"Chat ID hatasi: {e}")
    
    def _save_chat_id_to_config(self, chat_id):
        """Chat ID'yi util.py'ye kaydet"""
        try:
            with open('util.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace(
                'TELEGRAM_CHAT_ID = ""',
                f'TELEGRAM_CHAT_ID = "{chat_id}"'
            )
            
            with open('util.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("Chat ID kaydedildi")
            
        except Exception as e:
            print(f"Kayit hatasi: {e}")
    
    async def _send_telegram_message(self, message, parse_mode=None):
        """Telegram mesajı gönder"""
        if not self.enable_telegram or not self.telegram_bot or not self.chat_id:
            return False
        
        try:
            await self.telegram_bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
            return True
        except TelegramError as e:
            print(f"Telegram mesaj hatasi: {e}")
            return False
    
    def send_telegram_notification(self, result):
        """Analiz sonucunu Telegram'a gönder"""
        if not self.enable_telegram:
            return
        
        try:
            tech = result['technical']
            ai = result['ai_recommendation']
            buy_sigs = result['buy_signals']
            sell_sigs = result['sell_signals']
            timestamp = datetime.fromisoformat(result['timestamp'])
            
            # Mesajı oluştur
            message = f"📊 *NVIDIA Finansal Danışman Raporu*\n"
            message += f"🕐 {timestamp.strftime('%d/%m/%Y %H:%M')}\n"
            message += f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Fiyat bilgisi
            message += f"💰 *Güncel Fiyat:* ${tech['current_price']:.2f}\n\n"
            
            # Trend
            trend_emoji = "📈" if tech['recent_trend'] > 0 else "📉"
            message += f"{trend_emoji} *Trend:* {tech['recent_trend']:+.2f}%\n"
            
            # MA durumu
            ma20_status = "✅" if tech['price_above_ma20'] else "❌"
            ma50_status = "✅" if tech['price_above_ma50'] else "❌"
            message += f"MA20 {ma20_status} | MA50 {ma50_status}\n\n"
            
            # AI Tavsiyesi
            rec_emoji = "🟢" if "AL" in ai['recommendation'] else "🔴" if "SAT" in ai['recommendation'] else "🟡"
            message += f"{rec_emoji} *AI Tavsiyesi:* {ai['recommendation']}\n"
            message += f"💪 *Güven:* {ai['confidence']}\n"
            message += f"AL: {ai['buy_pct']:.0f}% | SAT: {ai['sell_pct']:.0f}%\n\n"
            
            # Alım Sinyalleri
            if buy_sigs:
                message += f"🟢 *ALIM SİNYALLERİ* ({len(buy_sigs)})\n"
                for i, sig in enumerate(buy_sigs[:2], 1):  # İlk 2 sinyal
                    message += f"{i}. {sig['type']}\n"
                    message += f"   Giriş: ${sig['entry_price']:.2f}\n"
                    message += f"   Hedef: ${sig['target_1']:.2f}\n"
                if len(buy_sigs) > 2:
                    message += f"   +{len(buy_sigs)-2} sinyal daha\n"
                message += "\n"
            
            # Satım Sinyalleri
            if sell_sigs:
                message += f"🔴 *SATIM SİNYALLERİ* ({len(sell_sigs)})\n"
                for i, sig in enumerate(sell_sigs[:2], 1):  # İlk 2 sinyal
                    message += f"{i}. {sig['type']}\n"
                    message += f"   {sig['reason'][:60]}...\n"
                if len(sell_sigs) > 2:
                    message += f"   +{len(sell_sigs)-2} sinyal daha\n"
                message += "\n"
            
            # Genel değerlendirme
            if buy_sigs and len(buy_sigs) >= 2:
                message += "💡 *ALIM FIRSATI VAR!*\n"
            elif sell_sigs and len(sell_sigs) >= 2:
                message += "⚠️ *DİKKATLİ OLUN!*\n"
            elif ai['recommendation'] in ['GÜÇLÜ AL', 'AL']:
                message += "🟡 *POZİSYON AÇMA FIRSATI*\n"
            else:
                message += "⚪ *BEKLE MODU*\n"
            
            message += f"\n📝 Detaylı rapor kaydedildi."
            
            # Mesajı gönder
            asyncio.run(self._send_telegram_message(message, parse_mode='Markdown'))
            
        except Exception as e:
            print(f"Telegram bildirim hatasi: {e}")
    
    def get_current_price_and_data(self):
        """Güncel NVIDIA fiyatını ve 2 yıllık veriyi çek"""
        stock = Stock("NVDA", util.STOCK_A_INITIAL_PRICE, 0, is_new=False, symbol="NVDA")
        return stock
    
    def analyze_price_levels(self, stock):
        """Teknik analiz - Destek/Direnç seviyeleri"""
        if not stock.real_prices or len(stock.real_prices) < 20:
            return None
        
        prices = stock.real_prices
        current_price = stock.price
        
        # Son 20, 50, 200 günlük ortalamalar
        ma_20 = sum(prices[-20:]) / 20
        ma_50 = sum(prices[-50:]) / 50 if len(prices) >= 50 else ma_20
        ma_200 = sum(prices[-200:]) / 200 if len(prices) >= 200 else ma_50
        
        # Volatilite (son 30 gün standart sapma)
        recent_prices = prices[-30:]
        avg = sum(recent_prices) / len(recent_prices)
        variance = sum((x - avg) ** 2 for x in recent_prices) / len(recent_prices)
        volatility = variance ** 0.5
        
        # Destek ve direnç seviyeleri
        support_1 = ma_20 - (volatility * 2)
        support_2 = ma_50
        resistance_1 = ma_20 + (volatility * 2)
        resistance_2 = max(prices[-30:])
        
        # Trend analizi
        recent_trend = (prices[-1] - prices[-20]) / prices[-20] * 100
        mid_trend = (prices[-1] - prices[-50]) / prices[-50] * 100 if len(prices) >= 50 else recent_trend
        
        return {
            'current_price': current_price,
            'ma_20': ma_20,
            'ma_50': ma_50,
            'ma_200': ma_200,
            'volatility': volatility,
            'support_1': support_1,
            'support_2': support_2,
            'resistance_1': resistance_1,
            'resistance_2': resistance_2,
            'recent_trend': recent_trend,
            'mid_trend': mid_trend,
            'price_above_ma20': current_price > ma_20,
            'price_above_ma50': current_price > ma_50,
            'price_above_ma200': current_price > ma_200
        }
    
    def get_ai_recommendation(self, stock):
        """AI ajanlarından tavsiye al"""
        agents = []
        for i in range(self.num_agents):
            agent = Agent(i, stock.get_price(), 0, self.secretary, self.model)
            agents.append(agent)
        
        buy_votes = 0
        sell_votes = 0
        hold_votes = 0
        
        stock_deals = {"sell": [], "buy": []}
        
        for agent in agents:
            action = agent.plan_stock(
                date=1,
                time=1,
                stock_a=stock,
                stock_b=Stock("B", 0, 0, is_new=False, symbol=None),
                stock_a_deals=stock_deals,
                stock_b_deals={"sell": [], "buy": []}
            )
            
            if action["action_type"] == "buy":
                buy_votes += 1
            elif action["action_type"] == "sell":
                sell_votes += 1
            else:
                hold_votes += 1
        
        total = self.num_agents
        buy_pct = (buy_votes / total) * 100
        sell_pct = (sell_votes / total) * 100
        hold_pct = (hold_votes / total) * 100
        
        # Tavsiye belirleme
        if buy_pct >= 60:
            recommendation = "GÜÇLÜ AL"
            confidence = "Yüksek"
        elif buy_pct >= 50:
            recommendation = "AL"
            confidence = "Orta"
        elif sell_pct >= 60:
            recommendation = "GÜÇLÜ SAT"
            confidence = "Yüksek"
        elif sell_pct >= 50:
            recommendation = "SAT"
            confidence = "Orta"
        else:
            recommendation = "BEKLE"
            confidence = "Düşük"
        
        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'buy_votes': buy_votes,
            'sell_votes': sell_votes,
            'hold_votes': hold_votes,
            'buy_pct': buy_pct,
            'sell_pct': sell_pct,
            'hold_pct': hold_pct
        }
    
    def generate_buy_signals(self, technical, ai_recommendation):
        """Alım sinyalleri üret"""
        signals = []
        current_price = technical['current_price']
        
        # Sinyal 1: Fiyat MA20'nin altında ve AI AL diyor
        if current_price < technical['ma_20'] and ai_recommendation['buy_pct'] >= 50:
            signals.append({
                'type': '🟢 ALIM FİRSATI',
                'reason': f'Fiyat MA20 (${technical["ma_20"]:.2f}) altında, AI %{ai_recommendation["buy_pct"]:.0f} AL öneriyor',
                'entry_price': current_price,
                'target_1': technical['ma_20'],
                'target_2': technical['resistance_1'],
                'stop_loss': technical['support_1']
            })
        
        # Sinyal 2: Fiyat destek seviyesine yakın
        if current_price <= technical['support_1'] * 1.02:
            signals.append({
                'type': '🟡 DESTEK SEVİYESİ',
                'reason': f'Fiyat destek seviyesine (${technical["support_1"]:.2f}) çok yakın',
                'entry_price': current_price,
                'target_1': technical['ma_20'],
                'target_2': technical['ma_50'],
                'stop_loss': technical['support_1'] * 0.97
            })
        
        # Sinyal 3: Güçlü AI AL sinyali
        if ai_recommendation['buy_pct'] >= 70:
            signals.append({
                'type': '🔥 GÜÇLÜ AL SİNYALİ',
                'reason': f'AI ajanlarının %{ai_recommendation["buy_pct"]:.0f}\'i AL öneriyor (Yüksek konsensüs)',
                'entry_price': current_price,
                'target_1': current_price * 1.05,
                'target_2': technical['resistance_1'],
                'stop_loss': current_price * 0.95
            })
        
        # Sinyal 4: MA50 üzerinde golden cross potansiyeli
        if technical['price_above_ma50'] and technical['ma_20'] > technical['ma_50'] * 0.98:
            signals.append({
                'type': '⭐ TREND DEĞİŞİMİ',
                'reason': 'MA20 MA50\'yi geçmek üzere (Golden Cross potansiyeli)',
                'entry_price': current_price,
                'target_1': technical['ma_50'] * 1.05,
                'target_2': technical['resistance_2'],
                'stop_loss': technical['ma_50']
            })
        
        return signals
    
    def generate_sell_signals(self, technical, ai_recommendation):
        """Satım sinyalleri üret"""
        signals = []
        current_price = technical['current_price']
        
        # Satış sinyali 1: Direnç seviyesinde
        if current_price >= technical['resistance_1'] * 0.98:
            signals.append({
                'type': '🔴 KAR REALIZASYONU',
                'reason': f'Fiyat direnç seviyesine (${technical["resistance_1"]:.2f}) ulaştı',
                'action': 'Kısmi satış yapılabilir'
            })
        
        # Satış sinyali 2: AI SAT diyor
        if ai_recommendation['sell_pct'] >= 60:
            signals.append({
                'type': '⚠️ GÜÇLÜ SAT SİNYALİ',
                'reason': f'AI ajanlarının %{ai_recommendation["sell_pct"]:.0f}\'i SAT öneriyor',
                'action': 'Pozisyon azaltılabilir'
            })
        
        # Satış sinyali 3: MA20'nin altına düştü
        if current_price < technical['ma_20'] and technical['recent_trend'] < -5:
            signals.append({
                'type': '📉 TREND KIRILMASI',
                'reason': 'Fiyat MA20 altına düştü ve trend negatif',
                'action': 'Stop-loss kontrolü yapın'
            })
        
        return signals
    
    def perform_analysis(self):
        """Tam analiz yap"""
        timestamp = datetime.now()
        print(f"\nAnaliz basladi - {timestamp.strftime('%d/%m/%Y %H:%M')}")
        
        # 1. Veri çek
        stock = self.get_current_price_and_data()
        
        if not stock.real_prices:
            print("Veri cekilemedi, analiz iptal.")
            return None
        
        # 2. Teknik analiz
        technical = self.analyze_price_levels(stock)
        
        # 3. AI tavsiyesi
        print(f"AI ajanlari analiz ediyor ({self.num_agents} ajan)...")
        ai_rec = self.get_ai_recommendation(stock)
        
        # 4. Alım/Satım sinyalleri
        buy_signals = self.generate_buy_signals(technical, ai_rec)
        sell_signals = self.generate_sell_signals(technical, ai_rec)
        
        # Sonuçları hazırla
        result = {
            'timestamp': timestamp.isoformat(),
            'price': technical['current_price'],
            'technical': technical,
            'ai_recommendation': ai_rec,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals
        }
        
        # Geçmişe kaydet
        self.analysis_history.append(result)
        
        # Rapor göster
        self.display_report(result)
        
        # Dosyaya kaydet
        self.save_report(result)
        
        # Telegram bildirimi gönder
        self.send_telegram_notification(result)
        
        return result
    
    def display_report(self, result):
        """Analiz raporunu ekrana yazdir"""
        tech = result['technical']
        ai = result['ai_recommendation']
        buy_sigs = result['buy_signals']
        sell_sigs = result['sell_signals']
        
        print(f"\n{'='*70}")
        print(f"NVIDIA (NVDA) Rapor")
        print(f"{'='*70}")
        
        print(f"\nFiyat: ${tech['current_price']:.2f}")
        print(f"MA20: ${tech['ma_20']:.2f} | MA50: ${tech['ma_50']:.2f} | MA200: ${tech['ma_200']:.2f}")
        print(f"Trend: {tech['recent_trend']:+.2f}% (kisa) | {tech['mid_trend']:+.2f}% (orta)")
        
        print(f"\nAI Tavsiye: {ai['recommendation']} (Guven: {ai['confidence']})")
        print(f"AL: {ai['buy_pct']:.0f}% | SAT: {ai['sell_pct']:.0f}% | BEKLE: {ai['hold_pct']:.0f}%")
        
        if buy_sigs:
            print(f"\nAlim Sinyalleri: {len(buy_sigs)}")
            for i, sig in enumerate(buy_sigs[:2], 1):
                print(f"  {i}. Giris: ${sig['entry_price']:.2f} -> Hedef: ${sig['target_1']:.2f}")
        
        if sell_sigs:
            print(f"\nSatim Sinyalleri: {len(sell_sigs)}")
            for i, sig in enumerate(sell_sigs[:2], 1):
                print(f"  {i}. {sig['type']}")
        
        print(f"\n{'='*70}\n")
    
    def save_report(self, result):
        """Raporu JSON ve TXT olarak kaydet"""
        timestamp = datetime.fromisoformat(result['timestamp'])
        filename = timestamp.strftime('%Y%m%d_%H%M%S')
        
        # JSON kaydet
        json_file = self.results_dir / f"analysis_{filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # TXT özet kaydet
        txt_file = self.results_dir / f"report_{filename}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"NVIDIA Rapor - {timestamp.strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"Fiyat: ${result['price']:.2f}\n")
            f.write(f"AI: {result['ai_recommendation']['recommendation']}\n")
            f.write(f"Alım Sinyalleri: {len(result['buy_signals'])}\n")
            f.write(f"Satım Sinyalleri: {len(result['sell_signals'])}\n\n")
            
            if result['buy_signals']:
                f.write("🟢 ALIM SİNYALLERİ:\n")
                for sig in result['buy_signals']:
                    f.write(f"  - {sig['type']}: {sig['reason']}\n")
            
            if result['sell_signals']:
                f.write("\nSatim Sinyalleri:\n")
                for sig in result['sell_signals']:
                    f.write(f"  - {sig['type']}\n")
    
    def run_scheduled_analysis(self):
        """Zamanlanmis analiz"""
        print(f"\nZamanlanmis analiz - {datetime.now().strftime('%H:%M')}")
        try:
            self.perform_analysis()
        except Exception as e:
            print(f"Analiz hatasi: {e}")
    
    def start_monitoring(self):
        """7/24 izleme baslat"""
        print("\nOtomatik izleme baslatiliyor...")
        
        # İlk analizi hemen yap
        self.perform_analysis()
        
        # Başlangıç bildirimi
        if self.enable_telegram and self.chat_id:
            startup_msg = "🤖 *NVIDIA Finansal Danışman Başlatıldı*\n\n"
            startup_msg += f"✅ Sistem aktif\n"
            startup_msg += f"⏰ Analiz saatleri: 09:00, 13:00, 17:00\n"
            startup_msg += f"📊 {self.num_agents} AI ajanı hazır\n\n"
            startup_msg += f"İyi yatırımlar! 🚀"
            asyncio.run(self._send_telegram_message(startup_msg, parse_mode='Markdown'))
        
        # Zamanlamaları ayarla (09:00, 13:00, 17:00)
        schedule.every().day.at("09:00").do(self.run_scheduled_analysis)
        schedule.every().day.at("13:00").do(self.run_scheduled_analysis)
        schedule.every().day.at("17:00").do(self.run_scheduled_analysis)
        
        print("\nZamanlayici aktif: 09:00, 13:00, 17:00")
        print("Durdurmak icin Ctrl+C\n")
        
        # Sonsuz döngü
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nIzleme durduruldu\n")
            
            # Kapatma bildirimi
            if self.enable_telegram and self.chat_id:
                shutdown_msg = "🛑 *NVIDIA Finansal Danışman Durduruldu*\n\n"
                shutdown_msg += "Sistem kapatıldı. Tekrar görüşmek üzere! 👋"
                asyncio.run(self._send_telegram_message(shutdown_msg, parse_mode='Markdown'))


def main():
    """Ana fonksiyon"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NVIDIA Finansal Danışman")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="AI model")
    parser.add_argument("--agents", type=int, default=10, help="Ajan sayisi")
    parser.add_argument("--once", action="store_true", help="Tek analiz")
    parser.add_argument("--no-telegram", action="store_true", help="Telegram kapat")
    args = parser.parse_args()
    
    # API kontrolü
    if not util.OPENAI_API_KEY or len(util.OPENAI_API_KEY) < 10:
        print("\nHATA: OpenAI API anahtari ayarlanmamis!")
        print("util.py dosyasinda OPENAI_API_KEY doldurun.\n")
        return
    
    advisor = NvidiaFinancialAdvisor(
        model=args.model, 
        num_agents=args.agents,
        enable_telegram=not args.no_telegram
    )
    
    if args.once:
        advisor.perform_analysis()
    else:
        advisor.start_monitoring()


if __name__ == "__main__":
    main()
