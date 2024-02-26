"""
DONT FORGET TO DELETE!!!
"""
OPENAI_API_KEY = ""
GOOGLE_API_KEY = ""

# 基础设置
AGENTS_NUM = 50  # 交易员数量
TOTAL_DATE = 264   # 模拟时长
TOTAL_SESSION = 3   # 每日交易次数

# 股票初始价格
STOCK_A_INITIAL_PRICE = 30
STOCK_B_INITIAL_PRICE = 40
# STOCK_B_PUBLISH = 100   # 股票B发行数量

# agent初始财产
MAX_INITIAL_PROPERTY = 5000000.0
MIN_INITIAL_PROPERTY = 100000.0


# 贷款
LOAN_TYPE = ["one-month", "two-month", "three-month"]
LOAN_TYPE_DATE = [22, 44, 66]  # 贷款时长
LOAN_RATE = [0.027, 0.03, 0.033] # 贷款利率

REPAYMENT_DAYS = [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264]  # 付息日

# 财报
SEASONAL_DAYS = 66 # 一季度的时间
SEASON_REPORT_DAYS = [12, 78, 144, 210] # 财报发布时间
FINANCIAL_REPORT_A = ["Last quarter's financial report of Company A. Revenue growth rate (YoY): 9.49%, Revenue million: 4483.99, Gross margin: 41.05%, Income Tax as a percentage of Revenue: 11.31%, Selling Expense Rate:6.83%, Management Expense Rate: 3.83%, Net profit million: 856.6705, Depreciation and Amortization: 0.91%, Capital Expenditures: 2.30%, Changes in working capital: 0.82%, Cash Flow(million): 756.7537",
                      "Last quarter's financial report of Company A. Revenue growth rate (YoY): 7.38%, Revenue million: 4417.79, Gross margin: 35.68%, Income Tax as a percentage of Revenue: 11.75%, Selling Expense Rate:8.13%, Management Expense Rate: 4.62%, Net profit million: 493.9451, Depreciation and Amortization: 1.34%, Capital Expenditures: 2.68%, Changes in working capital: 0.86%, Cash Flow(million): 396.5329",
                      "Last quarter's financial report of Company A. Revenue growth rate (YoY): 8.70%, Revenue million: 4041.30, Gross margin: 37.45%, Income Tax as a percentage of Revenue: 9.34%, Selling Expense Rate:6.79%, Management Expense Rate: 3.41%, Net profit million: 724.3648, Depreciation and Amortization: 1.27%, Capital Expenditures: 2.44%, Changes in working capital: 0.94%, Cash Flow(million): 639.5329",
                      "Last quarter's financial report of Company A. Revenue growth rate (YoY): 7.75%, Revenue million: 5024.04, Gross margin: 42.47%, Income Tax as a percentage of Revenue: 10.67%, Selling Expense Rate:6.56%, Management Expense Rate: 4.72%, Net profit million: 1031.214, Depreciation and Amortization: 1.08%, Capital Expenditures: 2.71%, Changes in working capital: 0.08%, Cash Flow(million): 945.5034"] # 各个季度的财报
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