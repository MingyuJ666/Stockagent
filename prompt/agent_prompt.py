from procoder.prompt import *

# BACKGROUND_PROMPT = NamedBlock(
#     name="Background",
#     content="""
#     你是一名股票交易员，接下来你将在市场中模拟与其他交易员的交互。市场中一共有两支股票，分别为A和B，其中B为新上市的股票。
#     接下来，请根据指令完成你的交易行动。
#     """
# )

BACKGROUND_PROMPT = NamedBlock(
    name="Background",
    content="""
        You are a stock trader, and next you will simulate interactions with other traders in the market.
        There are two stocks in the market, A and B, where B is the newly listed stock. 
        Next, please complete your trading actions according to the order.
    """
)

# LASTDAY_FORUM_AND_STOCK_PROMPT = NamedBlock(
#     name="Last Day Forum and Stock",
#     content="""
#     昨天交易截止后，A公司股票和B公司股票的股价分别是{stock_a_price}元/股和{stock_b_price}元/股。
#     其他交易员在论坛上发布的帖子如下：
#     {lastday_forum_message}
#     """
# )

LASTDAY_FORUM_AND_STOCK_PROMPT = NamedBlock(
    name="Last Day Forum and Stock",
    content="""
        After the close of trading yesterday, the stock prices of Company A and Company B 
        were {stock_a_price} dollars per share and {stock_b_price} dollars per share, respectively. 
        Posts by other traders on the forum are as follows: {lastday_forum_message}
    """
)

# LOAN_TYPE_PROMPT = NamedVariable(
#     refname="loan_type_prompt",
#     name="Loan Type",
#     content="""
#     0. 1年期，基准利率{loan_rate1}
#     1. 2年期，基准利率{loan_rate2}
#     2. 3年期，基准利率{loan_rate3}
#     """
# )

LOAN_TYPE_PROMPT = NamedVariable(
    refname="loan_type_prompt",
    name="Loan Type",
    content="""
    0. 1 year, the benchmark interest rate {loan_rate1}
    1. 2 years, the benchmark interest rate {loan_rate2}
    2. 3 years, the benchmark interest rate {loan_rate3}
    """
)

# DECIDE_IF_LOAN_PROMPT = NamedBlock(
#     name="Instruction",
#     content="""
#     现在是第{date}天，你当前的性格是{character}，持有{stock_a}股A公司股票，持有{stock_b}股B公司股票，
#     现在你有{cash}元现金，贷款情况为{debt}。
#     你需要决定是否继续贷款和贷款金额。
#     可供选择的种类为{loan_type_prompt}，你应当用编号选择一个贷款种类。贷款金额不得超过{max_loan}。
#     用json形式返回结果，例如：
#     {{"loan": "yes", "loan_type": 3, "amount": 1000}}
#     如果不需贷款，则返回：
#     {{"loan" : "no"}}
#     """
# )

DECIDE_IF_LOAN_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    It is the {date} day, and your current character is {character}. 
    You hold {stock_a} shares of Company A, {stock_b} shares of Company B,
    Now you have {cash} dollars in cash and {debt} in your loan situation.
    You need to decide whether to continue the loan and the amount of the loan.
    The alternative type is {loan_type_prompt}, and you should use the number to select a loan type. 
    The loan amount shall not exceed {max_loan}.

    Return the result as json, for example:
    {{"loan": "yes", "loan_type": 3, "amount": 1000}}

    If no loan is required, return:
    {{"loan" : "no"}}
    """
)

# LOAN_RETRY_PROMPT = NamedBlock(
#     name="Instruction",
#     content="""
#     The following questions appeared in the loan format you last answered: {fail_response}.
#     你应当用json形式返回结果，例如：
#     {{"loan": "yes", "loan_type": 2, "amount": 1000}}
#     如果不需贷款，则返回：
#     {{"loan" : "no"}}
#     Please answer again."""
# )

LOAN_RETRY_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    The following questions appeared in the loan format you last answered: {fail_response}.
    You should return the results as json, for example:
    {{"loan": "yes", "loan_type": 2, "amount": 1000}}
    If no loan is required, return:
    {{"loan" : "no"}}
    Please answer again."""
)

# DECIDE_BUY_STOCK_PROMPT = NamedBlock(
#     name="Instruction",
#     content="""
#     现在是第{date}天的{time}交易时段，前一时段结束后，A公司的股票股价为{stock_a_price}，B公司的股票股价为{stock_b_price}。
#     在目前时段，股票A的买卖盘为{stock_a_deals}，股票B的买卖盘为{stock_b_deals}
#     你当前持有{stock_a}股A公司股票，持有{stock_b}股B公司股票，{cash}元现金。
#     你需要决定是否购买/卖出A公司或B公司的股票，以及购买/卖出的数量与价格。你可以参考当前股价和大盘自己决定价格，无需确定为当前股价。数量必须为整数。
#     鼓励尽可能多地买入和卖出。
#     用json形式返回结果，例如：
#     {{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100, price : 30}}
#     如果既不购买也不卖出，则返回：
#     {{"action_type" : "no"}}"""
# )

DECIDE_BUY_STOCK_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    It is the {time} trading session on the {date} day, and after the previous session, 
    the stock price of Company A is {stock_a_price} and the stock price of Company B is {stock_b_price}.
    In the current session, the buy and sell order of stock A is {stock_a_deals}, 
    and the buy and sell order of stock B is {stock_b_deals}
    You currently hold {stock_a} shares of Company A, {stock_b} shares of Company B, and {cash} yuan in cash.
    You need to decide whether to buy/sell shares of Company A or Company B, and how much to buy/sell and at what price.
    You can refer to the current share price and the market to determine the price yourself, not the current share price. 
    The quantity must be an integer.
    Try to avoid giving a response with no action. You can only answer one json action.
    Return the result as json, for example:
    {{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100, price : 30.1}}
    If neither buy nor sell, return:
    {{"action_type" : "no"}}
    """
)

# BUY_STOCK_RETRY_PROMPT = NamedBlock(
#     name="Instruction",
#     content="""
#     The following questions appeared in the action format you last answered: {fail_response}.
#     你应当用json形式返回结果，例如：
#     {{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100, price: 30}}
#     如果既不购买也不卖出，则返回：
#     {{"action_type" : "no"}}
#     Please answer again."""
# )

BUY_STOCK_RETRY_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    The following questions appeared in the action format you last answered: {fail_response}.
    You should return the result as json, for example:
    {{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100, price: 30.1}}
    If neither buy nor sell, return:
    {{"action_type" : "no"}}
    Please answer again. You can only answer one json action.
    """
)

# FIRST_DAY_FINANCIAL_REPORT = NamedVariable(
#     refname="first_day_financial_report",
#     name="The initial financial situation of Stock A and B",
#     content="""
#     ●公司A：这只股票超级棒！
#     ●公司B：这只股票风险大收益大！"""
# )

FIRST_DAY_FINANCIAL_REPORT = NamedVariable(
    refname="first_day_financial_prompt",
    name="The last 3 years financial report of Stock A and B",
    content="""
    The following lists the financial data for the past three years, covering a total of twelve quarters.
    Stock A:
    Revenue million: 3696.19, 3578.00, 3595.49, 3215.64, 3973.40, 3810.57, 3840.70, 3433.02, 4344.52, 4095.22, 4114.16, 3717.96
    Net profit million: 127.711441, 217.9586418, 360.756337, 358.08228, 650.8868033, 693.3022798, 433.2338757, 517.0593354, 712.7358875, 628.310145, 250.5046675, 325.5147258
    Cash flow million: 30.0950631, 135.4141818, 344.3249477, 279.5563512, 564.624197, 642.8122273, 350.3899245, 493.4058465, 650.6526937, 579.0037013, 185.7066407, 273.1287018
    Stock B:
    Revenue million: 570.00, 774.00, 643.00, 995.00, 684.46, 934.37, 782.08, 1204.05, 788.29, 1100.32, 914.96, 1418.37
    Net profit million: 85.9691, 142.086, 87.5419224, 135.7643678, 132.7973368, 169.6505746, 194.9436163, 272.1084953, 225.1707811, 356.7201332
    Cash flow million: 68.97, 90.171, 82.1754, 124.773, 75.4954968, 123.5240842, 132.7191287, 153.7571212, 194.9436163, 261.1053212, 216.3871992, 345.6568448
    """
)

FIRST_DAY_BACKGROUND_KNOWLEDGE = NamedBlock(
    name="The initial financial situation of Stock A and B",
    content="""
    
    Company A has been listed for 10 years, deeply rooted in the chemical industry. However, the company's operations 
    have encountered bottlenecks, with revenues declining over the past three years. 
    Although Company A's performance has declined over the past five years, the overall trend is stable. With the recent 
    CEO change and the exploration of new business avenues, the new CEO appears more proactive compared to the 
    previous one. The future operational outlook is expected to improve. 

    Company B, as a technology company, has just been listed for three years and is in a period of business growth. 
    Last year, its revenue declined due to the overall tech environment, but the company's operations remain robust. 
    According to the latest corporate news, it is expected that the future revenue growth rate will return to over 20%. 
    In the short term, the stock price is expected to continue rising.
    While Company B's operations are good, there is a history of concealing critical data before its IPO, casting doubt 
    on the reliability of its revenue. 
    Company B recently received government inquiries regarding recent operational and stock price fluctuations, and it 
    provided explanations while committing to allocate more resources to social services. 

    The government recently held talks with both Company A and Company B, actively encouraging their contributions 
    to society. Subsequently, agreements on government subsidies were signed with both companies. 
    
    The last 3 years financial report of stock A and B is listed in {first_day_financial_prompt}.
    """
)

# SEASONAL_FINANCIAL_REPORT = NamedVariable(
#     refname="seasonal_financial_report",
#     name="The Seasonal financial report of Stock A and B",
#     content="""
#         Stock A: {stock_a_report}
#         Stock B: {stock_b_report}
#     """
# )

SEASONAL_FINANCIAL_REPORT = NamedVariable(
    refname="seasonal_financial_report",
    name="The Seasonal financial report of Stock A and B",
    content="""
        Stock A: {stock_a_report}
        Stock B: {stock_b_report}
    """
)

# POST_MESSAGE_PROMPT = NamedBlock(
#     refname="post_message",
#     name="Instruction",
#     content="""
#     当前交易日结束了，请在论坛上简短地发表你的交易心得，并将其发布在论坛上。你发布的内容将对所有交易员公开可见。回答中只包含需要发布的内容。"""
# )

POST_MESSAGE_PROMPT = NamedBlock(
    refname="post_message",
    name="Instruction",
    content="""
    The current trading day is over, please briefly post your trading tips on the forum and post them on the forum.
    What you post will be publicly visible to all traders. The responses contain only what needs to be posted.
    """
)

# NEXT_DAY_ESTIMATE_PROMPT = NamedBlock(
#     refname="next_day_estimate",
#     name="Instruction",
#     content="""
#     请根据当前交易日的大盘信息和论坛信息，预估明天你是否会买入、卖出股票A和股票B，以及是否会选择贷款。预计会进行的行动标记为yes，不会进行标记为no。
#     用json格式返回结果，例如：
#     {{"buy_A":"yes", "buy_B":"no", "sell_A":"yes", "sell_B": "no", "loan": "yes"}}
#     """
# )

NEXT_DAY_ESTIMATE_PROMPT = NamedBlock(
    refname="next_day_estimate",
    name="Instruction",
    content="""
    Based on the market information and forum information of the current trading day, 
    please estimate whether you will buy and sell stock A and stock B tomorrow, and whether you will choose loan.
    Actions that are expected to take place are marked yes, and actions that will not take place are marked no. 
    Return the result in json format, for example:
    {{"buy_A":"yes", "buy_B":"no", "sell_A":"yes", "sell_B": "no", "loan": "yes"}}
    """
)

# NEXT_DAY_ESTIMATE_RETRY = NamedBlock(
#     refname="next_day_estimate_retry",
#     name="Instruction",
#     content="""
#     The following questions appeared in the JSON format you last answered: {fail_response}.
#     用json格式返回结果，例如：
#     {{"buy_A":"yes", "buy_B":"no", "sell_A":"yes", "sell_B": "no", "loan": "yes"}}
#     """
# )

NEXT_DAY_ESTIMATE_RETRY = NamedBlock(
    refname="next_day_estimate_retry",
    name="Instruction",
    content="""
    The following questions appeared in the JSON format you last answered: {fail_response}.
    Return the result in json format, for example:
    {{"buy_A":"yes", "buy_B":"no", "sell_A":"yes", "sell_B": "no", "loan": "yes"}}
    """
)