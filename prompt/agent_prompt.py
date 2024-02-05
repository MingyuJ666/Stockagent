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
    name="Lasyday Forum and Stock",
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
        贷款种类选择为{loan_type_prompt}。贷款金额不得超过{max_loan}。
        用json形式返回结果，例如：
        {{{{"loan": "yes", "loan_type": 3, "amount": 1000}}}}
        如果不需贷款，则返回：
        {{{{"loan" : "no"}}}}
    }
    """
)

LOAN_RETRY_PROMPT = NamedBlock(
    name="Instruction",
    content="""
        The following questions appeared in the loan format you last answered: {fail_response}.
        你应当用json形式返回结果，例如：
        {{{{"loan": "yes", "loan_type": "3", "amount": 1000}}}}
        如果不需贷款，则返回：
        {{{{"loan" : "no"}}}}
        Please answer again.
    """
)

