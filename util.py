"""
API Keys Configuration
"""
import os
from dotenv import load_dotenv

# .env dosyasından yükle
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# 基础设置 - NVIDIA için optimize edildi
AGENTS_NUM = 20  # 交易员数量 (NVIDIA için azaltıldı)
TOTAL_DATE = 60   # 模拟时长 (yaklaşık 3 ay)
TOTAL_SESSION = 2   # 每日交易次数

# NVIDIA Hisse Ayarları
USE_REAL_DATA = True  # Gerçek NVDA verisi kullan
STOCK_SYMBOL = "NVDA"  # NASDAQ: NVIDIA
STOCK_A_INITIAL_PRICE = 140  # NVIDIA yaklaşık fiyatı (sistem başlangıcı)
STOCK_B_INITIAL_PRICE = 40  # İkinci hisse (kullanılmayacak)
# STOCK_B_PUBLISH = 100   # 股票B发行数量

# agent初始财产
MAX_INITIAL_PROPERTY = 5000000.0
MIN_INITIAL_PROPERTY = 100000.0


# 贷款
LOAN_TYPE = ["one-month", "two-month", "three-month"]
LOAN_TYPE_DATE = [22, 44, 66]  # 贷款时长
LOAN_RATE = [0.027, 0.03, 0.033] # 贷款利率

REPAYMENT_DAYS = [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264]  # 付息日

# 财报 - NVIDIA Gerçek Verileri (FY2025 Q1-Q3)
SEASONAL_DAYS = 22 # 一季度的时间 (yaklaşık 1 ay)
SEASON_REPORT_DAYS = [15, 35, 55] # 财报发布时间 (her ay)
FINANCIAL_REPORT_A = [
    "NVIDIA Q1 FY2025 Financial Report (Apr 2024): Revenue growth rate (YoY): 262%, Revenue million: 26,044, Gross margin: 78.4%, Data Center Revenue: $22.6B (+427% YoY), Gaming Revenue: $2.6B (+18% YoY), Professional Visualization: $427M (-27% YoY), Automotive: $329M (+11% YoY), Net profit margin: 57.1%, Operating Income: $16,909M, EPS (diluted): $6.12, Cash and equivalents: $31.4B, Key highlights: Strong AI/datacenter demand, Hopper GPU architecture dominance, Blackwell architecture announced.",
    "NVIDIA Q2 FY2025 Financial Report (Jul 2024): Revenue growth rate (YoY): 122%, Revenue million: 30,040, Gross margin: 75.7%, Data Center Revenue: $26.3B (+154% YoY), Gaming Revenue: $2.9B (+16% YoY), Professional Visualization: $454M (+20% YoY), Automotive: $346M (+37% YoY), Net profit margin: 55.3%, Operating Income: $18,642M, EPS (diluted): $0.68, Key highlights: Record datacenter revenue, AI inference growth, Enterprise AI adoption accelerating.",
    "NVIDIA Q3 FY2025 Financial Report (Oct 2024): Revenue growth rate (YoY): 94%, Revenue million: 35,082, Gross margin: 75.0%, Data Center Revenue: $30.8B (+112% YoY), Gaming Revenue: $3.3B (+15% YoY), Professional Visualization: $486M (+17% YoY), Automotive: $449M (+30% YoY), Net profit margin: 54.8%, Operating Income: $21,869M, EPS (diluted): $0.81, Key highlights: Blackwell production ramping, Sovereign AI expansion, Record quarterly revenue.",
    "NVIDIA Outlook FY2025: Strong AI infrastructure demand continues, Blackwell architecture production scaling, Expected revenue growth 70-90% YoY, Gross margins expected 73-75%, Data center segment driving growth, Automotive and gaming segments stable, Key risks: Supply chain constraints, Competition from AMD/Intel, Geopolitical tensions affecting China sales, Market concerns: High valuation multiples, Potential demand saturation."                      
]
FINANCIAL_REPORT_B = ["Last quarter's financial report of Company B. Revenue growth rate (YoY): 19.96%, Revenue million: 1319.94, Gross margin: 31.21%, Income Tax as a percentage of Revenue: 0.70%, Selling Expense Rate:4.69%, Management Expense Rate: 8.78%, Net profit million: 224.9179, Depreciation and Amortization: 1.13%, Capital Expenditures: 1.77%, Changes in working capital: 0.59%, Cash Flow(million): 208.7266",
                      "Last quarter's financial report of Company B. Revenue growth rate (YoY): 19.86%, Revenue million: 1096.70, Gross margin: 31.26%, Income Tax as a percentage of Revenue: 0.71%, Selling Expense Rate:3.62%, Management Expense Rate: 9.90%, Net profit million: 186.7678, Depreciation and Amortization: 0.67%, Capital Expenditures: 1.44%, Changes in working capital: -0.31%, Cash Flow(million): 181.6862",
                      "Last quarter's financial report of Company B. Revenue growth rate (YoY): 18.21%, Revenue million: 1676.70, Gross margin: 31.58%, Income Tax as a percentage of Revenue: 0.92%, Selling Expense Rate:3.78%, Management Expense Rate: 10.27%, Net profit million: 278.3327, Depreciation and Amortization: 0.77%, Capital Expenditures: 1.56%, Changes in working capital: -0.06%, Cash Flow(million): 266.1486",
                      "Last quarter's financial report of Company B. Revenue growth rate (YoY): 15.98%, Revenue million: 1075.13, Gross margin: 32.41%, Income Tax as a percentage of Revenue: 1.08%, Selling Expense Rate:3.79%, Management Expense Rate: 10.70%, Net profit million: 181.1602, Depreciation and Amortization: 1.09%, Capital Expenditures: 2.28%, Changes in working capital: 0.67%, Cash Flow(million): 161.1985"]

# 特殊事件

EVENT_1_DAY = 78
EVENT_1_MESSAGE = "The government has announced a reduction in the reserve requirement ratio. " \
                  "The lending interest rates have been lowered."
EVENT_1_LOAN_RATE = [0.024, 0.027, 0.030] # 降准后的利率放在这里

EVENT_2_DAY = 144
EVENT_2_MESSAGE = "The government has announced an increase in interest rates."
EVENT_2_LOAN_RATE = [0.0255, 0.0285, 0.0315]