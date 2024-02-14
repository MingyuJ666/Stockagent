"""
DONT FORGET TO DELETE!!!
"""
OPENAI_API_KEY = ""

# 基础设置
AGENTS_NUM = 5
TOTAL_DATE = 260
#TOTAL_SESSION = 12
TOTAL_SESSION = 5

# 股票初始
STOCK_A_INITIAL_PRICE = 10
STOCK_B_INITIAL_PRICE = 6
STOCK_B_PUBLISH = 100   # 股票B发行数量

# agent初始财产
MAX_INITIAL_PROPERTY = 10000.0 # agent
MIN_INITIAL_PROPERTY = 1000.0


# 贷款
LOAN_TYPE = ["one-year", "one2five-year", "five-year"]
LOAN_TYPE_DATE = [100, 200, 300] # todo 确定可选的贷款时长
LOAN_RATE = [0.042, 0.045, 0.047]

REPAYMENT_DAYS = [65, 130, 195, 260] # 付息日

# 财报
SEASONAL_DAYS = 65 # 一季度的时间
SEASON_REPORT_DAYS = [33, 98, 163, 228]
FINANCIAL_REPORT_A = ["Q1", "Q2", "Q3", "Q4"] # 财报放在这里，和season_report_days一一对应
FINANCIAL_REPORT_B = ["Q1", "Q2", "Q3", "Q4"]

# 特殊事件
EVENT_1_DAY = 131
EVENT_1_MESSAGE = "放在论坛里的事件信息"
EVENT_1_LOAN_RATE = [0.040, 0.043, 0.045] # 降准后的利率放在这里

EVENT_2_DAY = 391
EVENT_2_MESSAGE = "放在论坛里的事件信息"
EVENT_A_LOAN_RATE = [0.045, 0.048, 0.050]