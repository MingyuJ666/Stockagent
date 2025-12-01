import util
import yfinance as yf
from datetime import datetime, timedelta
import ssl
import requests
import json

class Stock:
    def __init__(self, name, initial_price, initial_stock, is_new=False, symbol=None):
        self.name = name
        self.price = initial_price
        self.ideal_price = 0
        self.initial_stock = initial_stock
        self.history = {}   # {date: session_deal}
        self.session_deal = [] # [{"price", "amount"}]
        self.symbol = symbol  # Ticker symbol (e.g., "NVDA")
        self.real_prices = []  # Gerçek fiyat geçmişi
        
        # Eğer gerçek veri kullanılacaksa, fiyatları çek
        if util.USE_REAL_DATA and symbol:
            self._fetch_real_prices()

    def _fetch_real_prices(self):
        """NVIDIA icin gercek NASDAQ fiyatlarini cek (son 2 yil)"""
        print(f"{self.symbol} icin son 2 yillik veri cekiliyor...")
        
        # Önce Yahoo Finance API'yi dene
        success = self._fetch_from_yahoo()
        
        # Başarısızsa alternatif kaynak dene
        if not success:
            print("Yahoo Finance basarisiz, alternatif kaynak deneniyor...")
            success = self._fetch_from_alternative()
        
        if not success:
            print(f"Canli veri cekilemedi, baslangic fiyati: ${self.price:.2f}")
    
    def _fetch_from_yahoo(self):
        """Yahoo Finance'den veri çek"""
        try:
            # SSL sertifika kontrolünü atla
            ssl._create_default_https_context = ssl._create_unverified_context
            
            ticker = yf.Ticker(self.symbol)
            
            # Son 2 yıllık veri (730 gün)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=730)
            
            hist = ticker.history(start=start_date, end=end_date)
            
            if not hist.empty and len(hist) > 0:
                self.real_prices = hist['Close'].tolist()
                self.price = self.real_prices[-1]  # En son fiyatla başla (bugünkü)
                
                print(f"Yahoo Finance: {len(self.real_prices)} gunluk veri")
                print(f"Guncel Fiyat: ${self.price:.2f}")
                print(f"Aralik: ${min(self.real_prices):.2f} - ${max(self.real_prices):.2f}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Yahoo Finance hatasi: {str(e)[:100]}")
            return False
    
    def _fetch_from_alternative(self):
        """Alternatif kaynaklardan veri çek"""
        try:
            # Yahoo Finance Query API (alternatif endpoint)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.symbol}"
            params = {
                'range': '2y',
                'interval': '1d'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'chart' in data and 'result' in data['chart']:
                    result = data['chart']['result'][0]
                    
                    # Fiyat verilerini al
                    closes = result['indicators']['quote'][0]['close']
                    self.real_prices = [p for p in closes if p is not None]
                    
                    if self.real_prices:
                        self.price = self.real_prices[-1]  # En son fiyat
                        
                        print(f"Alternatif API: {len(self.real_prices)} gunluk veri")
                        print(f"Guncel Fiyat: ${self.price:.2f}")
                        print(f"Aralik: ${min(self.real_prices):.2f} - ${max(self.real_prices):.2f}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"Alternatif API hatasi: {str(e)[:100]}")
            return False
    
    def gen_financial_report(self, index):
        if self.name == "A":
            return util.FINANCIAL_REPORT_A[index]
        elif self.name == "B":
            return util.FINANCIAL_REPORT_B[index] if hasattr(util, 'FINANCIAL_REPORT_B') else ""

    def add_session_deal(self, price_and_amount):
        self.session_deal.append(price_and_amount)

    def update_price(self, date):
        # Gerçek veri kullanılıyorsa ve mevcutsa
        if util.USE_REAL_DATA and self.real_prices and date <= len(self.real_prices):
            self.price = self.real_prices[date - 1]
        # Simülasyon verisi kullanılıyorsa
        elif len(self.session_deal) > 0:
            self.price = self.session_deal[-1]["price"]
        
        self.history[date] = self.session_deal.copy()
        self.session_deal.clear()

    def get_price(self):
        return self.price
