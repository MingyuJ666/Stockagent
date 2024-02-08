from procoder.prompt import *
from utils import *

BACKGROUND_PROMPT = NamedBlock(
    name="Background",
    content="""
        背景设定
        任务描述
        COT？
    """
)

LASTDAY_FORUM_AND_STOCK_PROMPT = NamedBlock(
    name="Last Day Forum and Stock",
    content="""
        昨天交易截止后，A公司股票和B公司股票的股价分别是{stock_a_price}元/股和{stock_b_price}元/股。
        其他交易员在论坛上发布的帖子如下：
        {lastday_forum_message}
    """
)

LOAN_TYPE_PROMPT = NamedVariable(
    refname="loan_type_prompt",
    name="Loan Type",
    content="""
        1. 1年期，基准利率...
        2. 
        3. 
    """
)

DECIDE_IF_LOAN_PROMPT = NamedBlock(
    name="Instruction",
    content="""
        现在是第{date}天，你当前的性格是{character}，持有{stock_a}股A公司股票，持有{stock_b}股B公司股票，
        现在你有{cash}元现金，贷款情况为{debt}。
        你需要决定是否继续贷款和贷款金额。
        可供选择的种类为{loan_type_prompt}，你应当用编号选择一个贷款种类。贷款金额不得超过{max_loan}。
        用json形式返回结果，例如：
        {{{{"loan": "yes", "loan_type": 3, "amount": 1000}}}}
        如果不需贷款，则返回：
        {{{{"loan" : "no"}}}}
    """
)

LOAN_RETRY_PROMPT = NamedBlock(
    name="Instruction",
    content="""
        The following questions appeared in the loan format you last answered: {fail_response}.
        你应当用json形式返回结果，例如：
        {{{{"loan": "yes", "loan_type": 3, "amount": 1000}}}}
        如果不需贷款，则返回：
        {{{{"loan" : "no"}}}}
        Please answer again.
    """
)

DECIDE_BUY_STOCK_PROMPT = NamedBlock(
    name="Instruction",
    content="""
        现在是第{date}天的{time}交易时段，A公司的股票股价为{stock_a_price}，B公司的股票股价为{stock_b_price}。
        你当前持有{stock_a}股A公司股票，持有{stock_b}股B公司股票，{cash}元现金。
        你需要决定是否购买/卖出A公司或B公司的股票，以及购买/卖出的数量与价格。 
        用json形式返回结果，例如：
        {{{{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100, price : 30}}}}
        如果既不购买也不卖出，则返回：
        {{{{"action_type" : "no"}}}}
    """
)

BUY_STOCK_RETRY_PROMPT = NamedBlock(
    name="Instruction",
    content="""
        The following questions appeared in the action format you last answered: {fail_response}.
        你应当用json形式返回结果，例如：
        {{{{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100}}}}
        如果既不购买也不卖出，则返回：
        {{{{"action_type" : "no"}}}}
        Please answer again.
    """
)

FIRST_DAY_FINANCIAL_REPORT = NamedVariable(
    refname="first_day_financial_report",
    name="The initial financial situation of Stock A and B",
    content="""
        第一天需要给交易员告知的股票A和B的数据
        ●公司A：给定公司A过去五年的财务数据、股价变动和公司B上市当日的前一个交易日的股价	（扒现实公司数据）
        ●公司B：公司根据FCFF发对自身市值进行估值，得到公司总市值，公司总市值减债务现值得到股权现值
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