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

LOAN_TYPE_PROMPT = NamedVariable(
    refname="loan_type_prompt",
    name="Loan Type",
    content="""
        1. 1年期，基准利率...
        2. 
        3. 
    """
)

DECIDE_IF_MOAN_PROMPT = NamedBlock(
    name="Instruction",
    content="""
        现在是第{date}天，你当前的性格是{character}，持有{stock_a}股A公司股票，持有{stock_b}股B公司股票，
        现在你有{cash}元现金，{debt}元负债
        你需要决定是否贷款和贷款金额。
        贷款种类选择为{loan_type_prompt}，还款日在[65, 130, 195, 260]中决定。
        用json形式返回结果，例如：
        {{{{"loan": "yes", "loan_type": "3", "closing_date": 130, "amount": 1000}}}}
        如果不需贷款，则返回：
        {{{{"loan" : "no"}}}}
    }
    """
)

