import os
import time

import openai
import random
from prompt.agent_prompt import *
from procoder.functional import format_prompt
from procoder.prompt import *
from utils import *


def random_init(stock_initial_price):
    stock, cash, debt_amount = 0.0, 0.0, 0.0
    while stock * stock_initial_price * 10 + cash < MIN_INITIAL_PROPERTY \
            or stock * stock_initial_price * 10 + cash > MAX_INITIAL_PROPERTY \
            or debt_amount > stock * stock_initial_price * 10 + cash:
        stock = random.uniform(0, MAX_INITIAL_PROPERTY / (stock_initial_price * 10))
        cash = random.uniform(0, MAX_INITIAL_PROPERTY)
        debt_amount = random.uniform(0, MAX_INITIAL_PROPERTY)
    debt = {"amount": debt_amount,
            "type": random.choice(LOAN_TYPE),
            "repayment_date": random.randint(1, TOTAL_DATE)
            }
    return stock, cash, debt


class Agent:
    def __init__(self, i, stock_a_price, secretary, model):
        self.order = i
        self.secretary = secretary
        self.model = model
        self.character = random.choice(["性格一", "性格二"])  # todo

        self.stock_a, self.cash, init_debt = random_init(stock_a_price)
        self.stock_b = 0  # stock 以手为单位存储，一手=10股，计算资产时*10
        self.init_proper = self.get_total_proper(stock_a_price, 0)  # 初始资产 后续借贷不超过初始资产

        self.action_history = [[] for _ in range(TOTAL_DATE)]
        self.chat_history = []
        self.loans = [init_debt]

    def run_api(self, prompt, temperature: float = 0):
        openai.api_key = OPENAI_API_KEY
        client = openai.OpenAI(api_key=openai.api_key)
        self.chat_history.append({"role": "user", "content": prompt})
        max_retry = 2
        retry = 0
        while retry < max_retry:
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=self.chat_history,
                    temperature=temperature,
                )
                self.chat_history.append(response.choices[0].message)
                resp = response.choices[0].message.content
                return resp
            except openai.OpenAIError as e:
                retry += 1
                print(e)
                time.sleep(1)

    def get_total_proper(self, stock_a_price, stock_b_price):
        return self.stock_a * stock_a_price * 10 + self.stock_b * stock_b_price * 10 + self.cash

    def get_total_loan(self):
        debt = 0
        for loan in self.loans:
            debt += loan["amount"]
        return debt

    def plan_loan(self, date, stock_a_price, stock_b_price, lastday_forum_message):
        # first day action : prompt with background
        if date == 1:
            prompt = Collection(BACKGROUND_PROMPT, LOAN_TYPE_PROMPT, DECIDE_IF_LOAN_PROMPT)
            assert self.init_proper > self.get_total_loan()
            max_loan = self.init_proper - self.get_total_loan()
            inputs = {
                "date": date,
                "character": self.character,
                "stock_a": self.stock_a,
                "stock_b": self.stock_b,
                "cash": self.cash,
                "debt": self.loans,
                "max_loan": max_loan
            }
        # other days action : prompt with last day forum message & stock price
        else:
            prompt = Collection(LASTDAY_FORUM_AND_STOCK_PROMPT, LOAN_TYPE_PROMPT, DECIDE_IF_LOAN_PROMPT)
            assert self.init_proper > self.get_total_loan()
            max_loan = self.init_proper - self.get_total_loan()
            inputs = {
                "date": date,
                "character": self.character,
                "stock_a": self.stock_a,
                "stock_b": self.stock_b,
                "cash": self.cash,
                "debt": self.loans,
                "max_loan": max_loan,
                "stock_a_price": stock_a_price,
                "stock_b_price": stock_b_price,
                "lastday_forum_message": lastday_forum_message
            }

        try_times = 0
        MAX_TRY_TIMES = 10
        resp = self.run_api(format_prompt(prompt, inputs))
        loan_format_check, fail_response, loan = self.secretary.check_loan(resp, max_loan)  # secretary check loan format
        while not loan_format_check:
            print("Loan format check failed because of these issues: {}".format(fail_response))
            try_times += 1
            if try_times > MAX_TRY_TIMES:
                print("Loan format try times > MAX_TRY_TIMES. Skip as no loan today.")
                loan = {"loan": "no"}
                break

            resp = self.run_api(format_prompt(LOAN_RETRY_PROMPT, {"fail_response": fail_response}), temperature=0)
            loan_format_check, fail_response, loan = self.secretary.check_loan(date, resp)

        if loan["loan"] == "yes":
            self.loans.append(loan)
            self.action_history[date].append(loan)
            self.cash += loan["amount"]

        def loan_repayment():
            # todo check是否贷款还款日，还款，破产检查

        def interest_payment():
            # todo 贷款付息日付息
