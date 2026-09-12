from procoder.prompt import *


BACKGROUND_PROMPT = NamedBlock(
    name="Background",
    content="""
    You are a stock trader, and you will simulate your interactions with other traders in the market.
    There are two stocks in the market, named A and B, where B is the newly listed stock.
    Next, follow the instructions to complete your trading actions.
    """
)


LASTDAY_FORUM_AND_STOCK_PROMPT = NamedBlock(
    name="Last Day Forum and Stock",
    content="""
    After the close of trading yesterday, the stock prices of Company A and Company B
    were {stock_a_price} dollars per share and {stock_b_price} dollars per share,
    respectively. Posts by other traders on the forum are as follows:
    {lastday_forum_message}
    """
)


LOAN_TYPE_PROMPT = NamedVariable(
    refname="loan_type_prompt",
    name="Loan Type",
    content="""
    [0]. 1 year, the benchmark interest rate {loan_rate1}.
    [1]. 2 years, the benchmark interest rate {loan_rate2}.
    [2]. 3 years, the benchmark interest rate {loan_rate3}.
    """
)


DECIDE_IF_LOAN_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    It is the {date} day, and your current character is {character}.
    You hold {stock_a} shares of Company A and {stock_b} shares of Company B.
    You have {cash} dollars in cash and {debt} in your loan situation.
    You need to decide whether to continue the loan and the amount of the loan.
    The alternative type is {loan_type_prompt}, and you should use the number to select a loan type.
    The loan amount shall not exceed {max_loan}.

    Return the result as json, for example:
    {{"loan": "yes", "loan_type": 3, "amount": 1000}}

    If no loan is required, return:
    {{"loan" : "no"}}
    """
)


LOAN_RETRY_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    The following questions appeared in the loan format you last answered:
    {fail_response}.
    You should return the results as json, for example:
    {{"loan": "yes", "loan_type": 2, "amount": 1000}}
    If no loan is required, return:
    {{"loan" : "no"}}
    Please answer again.
    """
)


DECIDE_BUY_STOCK_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    It is the {time} trading session on the {date} day. After the previous session,
    the stock price of Company A is {stock_a_price}, and the stock price of Company B is
    {stock_b_price}.
    In the current session, the buy and sell order of stock A is {stock_a_deals},
    and the buy and sell order of stock B is {stock_b_deals}.
    You currently hold {stock_a} shares of Company A, {stock_b} shares of Company B,
    and {cash} dollars in cash.
    You need to decide whether to buy or sell shares of Company A or Company B,
    and how much to buy/sell and at what price.
    You can refer to the current share price and the market to determine the price yourself,
    not the current share price. The quantity must be an integer.
    We encourage you to buy and sell more. You can only answer one json action.
    Return the result as json, for example:
    {{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100, price : 30.1}}
    If neither buy nor sell, return:
    {{"action_type" : "no"}}
    """
)


BUY_STOCK_RETRY_PROMPT = NamedBlock(
    name="Instruction",
    content="""
    The following questions appeared in the action format you last answered:
    {fail_response}.
    You should return the result as json, for example:
    {{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100, price: 30.1}}
    If neither buy nor sell, return:
    {{"action_type" : "no"}}
    Please answer again. You can only answer one json action.
    """
)


FIRST_DAY_FINANCIAL_REPORT = NamedVariable(
    refname="first_day_financial_prompt",
    name="The last 3 years financial report of Stock A, B, C and D",
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
    Stock C:
    Revenue million: 35015.73, 36595.79, 35484.08, 36814.05, 37134.12, 38902.45, 37654.89, 39201.33, 40123.56, 41867.90, 40567.12, 42234.78
    Net profit million: 8939.515869, 9485.9947259, 8554.1471656, 8977.474233, 9876.321456, 10423.567891, 9123.456789, 9589.012345, 10789.654321, 11234.567890, 9876.543210, 10345.678901
    Cash flow million: 8456.298795, 8915.1004019, 8380.2751736, 9106.323408, 9321.456789, 9876.543210, 8567.890123, 9012.345678, 10123.456789, 10678.901234, 9324.567890, 9789.012345
    Stock D:
    Revenue million: 17925.22, 17725.45, 17714.92, 17732.90, 17845.67, 17689.34, 17654.88, 17701.23, 17989.45, 17834.56, 17789.01, 17845.67
    Net profit million: 1444.772732, 1745.956825, 1679.374416, 1478.923860, 1589.456321, 1890.123456, 1812.345678, 1601.234567, 1723.456789, 2015.678901, 1934.567890, 1712.345678
    Cash flow million: 1193.819652, 1830.1527125, 1709.489780, 1382.279555, 1487.654321, 1789.012345, 1712.345678, 1490.123456, 1612.345678, 1901.234567, 1823.456789, 1601.234567
    """
)


FIRST_DAY_BACKGROUND_KNOWLEDGE = NamedBlock(
    name="The initial financial situation of Stock A, B, C and D",
    content="""
    Company A has been listed for 10 years, deeply rooted in the chemical industry. However, the company's operations
    have encountered bottlenecks, with revenues declining over the past three years.
    Although Company A's performance has declined over the past five years, the overall trend is stable.

    Company B, as a technology company, has just been listed for three years and is in a period of business growth.
    Last year, its revenue declined due to the overall tech environment, but the company's operations remain robust.

    Please infer and update your beliefs based on the financial reports and evolving market information.
    """
)


SEASONAL_FINANCIAL_REPORT = NamedVariable(
    refname="seasonal_financial_report",
    name="The Seasonal financial report of Stock A and B",
    content="""
    Stock A: {stock_a_report}
    Stock B: {stock_b_report}
    """
)


POST_MESSAGE_PROMPT = NamedBlock(
    refname="post_message",
    name="Instruction",
    content="""
    The current trading day is over, please briefly post your trading tips on the forum and post them on the forum.
    What you post will be publicly visible to all traders. The responses contain only what needs to be posted.
    """
)


NEXT_DAY_ESTIMATE_PROMPT = NamedBlock(
    refname="next_day_estimate",
    name="Instruction",
    content="""
    Based on the market information and forum information of the current trading day, please estimate whether you
    will buy or sell stock A and stock B tomorrow and whether you will choose a loan.
    Actions that are expected to take place are marked yes, and actions that will not take place are marked no.
    Return the result in JSON format, for example:
    {{"buy_A":"yes", "buy_B":"no", "sell_A":"yes", "sell_B":"no", "loan":"yes"}}
    """
)


NEXT_DAY_ESTIMATE_RETRY = NamedBlock(
    refname="next_day_estimate_retry",
    name="Instruction",
    content="""
    The following questions appeared in the JSON format you last answered:
    {fail_response}.
    Return the result in JSON format, for example:
    {{"buy_A":"yes", "buy_B":"no", "sell_A":"yes", "sell_B":"no", "loan":"yes"}}
    """
)
