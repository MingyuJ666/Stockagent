import os
import time
import openai
import random

from colorama import Fore, Style

from prompt.agent_prompt import *
from procoder.functional import format_prompt
from procoder.prompt import *
from utils import *
from secretary import Secretary
from stock import Stock


def random_init(stock_initial_price):
    stock, cash, debt_amount = 0.0, 0.0, 0.0
    while stock * stock_initial_price + cash < MIN_INITIAL_PROPERTY \
            or stock * stock_initial_price + cash > MAX_INITIAL_PROPERTY \
            or debt_amount > stock * stock_initial_price + cash:
        stock = random.uniform(0, MAX_INITIAL_PROPERTY / stock_initial_price)
        cash = random.uniform(0, MAX_INITIAL_PROPERTY)
        debt_amount = random.uniform(0, MAX_INITIAL_PROPERTY)
    debt = {
            "loan": "yes",
            "amount": debt_amount,
            "loan_type": random.randint(1, len(LOAN_TYPE)),
            "repayment_date": random.choice(REPAYMENT_DAYS)
            }
    return stock, cash, debt


class Agent:
    def __init__(self, i, stock_a_price, secretary, model):
        self.order = i
        self.secretary = secretary
        self.model = model
        self.character = random.choice(["性格一", "性格二"])  # todo

        self.stock_a_amount, self.cash, init_debt = random_init(stock_a_price)
        self.stock_b_amount = 0  # stock 以手为单位存储，一手=10股，股价其实是一手的价格
        self.init_proper = self.get_total_proper(stock_a_price, 0)  # 初始资产 后续借贷不超过初始资产

        self.action_history = [[] for _ in range(TOTAL_DATE)]
        self.chat_history = []
        self.loans = [init_debt]
        self.is_bankrupt = False

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
        return self.stock_a_amount * stock_a_price + self.stock_b_amount * stock_b_price + self.cash

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
                'date': date,
                'character': self.character,
                'stock_a': self.stock_a_amount,
                'stock_b': self.stock_b_amount,
                'cash': self.cash,
                'debt': self.loans,
                'max_loan': max_loan
            }

        # other days action : prompt with last day forum message & stock price
        else:
            prompt = Collection(LASTDAY_FORUM_AND_STOCK_PROMPT, LOAN_TYPE_PROMPT, DECIDE_IF_LOAN_PROMPT)
            assert self.init_proper > self.get_total_loan()
            max_loan = self.init_proper - self.get_total_loan()
            inputs = {
                "date": date,
                "character": self.character,
                "stock_a": self.stock_a_amount,
                "stock_b": self.stock_b_amount,
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
            loan["repayment_date"] = date + LOAN_TYPE_DATE[loan["loan_type"]]      # add loan repayment_date
            self.loans.append(loan)
            self.action_history[date].append(loan)
            self.cash += loan["amount"]

    # date=交易日, time=当前交易时段
    def plan_stock(self, date, time, stock_a, stock_b):
        if date == 1:
            prompt = Collection(FIRST_DAY_FINANCIAL_REPORT, DECIDE_BUY_STOCK_PROMPT)
            inputs = {
                "date": date,
                "time": time,
                "stock_a": self.stock_a_amount,
                "stock_b": self.stock_b_amount,
                "stock_a_price": stock_a.get_price(),
                "stock_b_price": stock_b.get_price(),
                "cash": self.cash
            }
        elif date in SEASON_REPORT_DAYS:
            prompt = Collection(SEASONAL_FINANCIAL_REPORT, DECIDE_BUY_STOCK_PROMPT)
            inputs = {
                "date": date,
                "time": time,
                "stock_a": self.stock_a_amount,
                "stock_b": self.stock_b_amount,
                "stock_a_price": stock_a.get_price(),
                "stock_b_price": stock_b.get_price(),
                "cash": self.cash,
                "stock_a_report": stock_a.gen_financial_report(),
                "stock_b_report": stock_b.gen_financial_report()
            }
        else:
            prompt = DECIDE_BUY_STOCK_PROMPT
            inputs = {
                "date": date,
                "time": time,
                "stock_a": self.stock_a_amount,
                "stock_b": self.stock_b_amount,
                "stock_a_price": stock_a.get_price(),
                "stock_b_price": stock_b.get_price(),
                "cash": self.cash
            }
        try_times = 0
        MAX_TRY_TIMES = 10
        resp = self.run_api(format_prompt(prompt, inputs))
        action_format_check, fail_response, action = self.secretary.check_action(
            resp, self.cash, self.stock_a_amount, self.stock_b_amount, stock_a.get_price(), stock_b.get_price())
        while not action_format_check:
            print("Action format check failed because of these issues: {}".format(fail_response))
            try_times += 1
            if try_times > MAX_TRY_TIMES:
                print("Action format try times > MAX_TRY_TIMES. Skip as no loan today.")
                action = {"action_type": "no"}
                break

            resp = self.run_api(format_prompt(BUY_STOCK_RETRY_PROMPT, {"fail_response": fail_response}), temperature=0)
            action_format_check, fail_response, action = self.secretary.check_action(
                resp, self.cash, self.stock_a_amount, self.stock_b_amount, stock_a.get_price(), stock_b.get_price())

        if action["action_type"] == "buy":
            self.action_history[date].append(action)
            # if action["stock"] == "stock_a":
            #     self.stock_a_amount += action["amount"]
            #     self.cash -= action["amount"] * stock_a.get_price()
            # else:
            #     self.stock_b_amount += action["amount"]
            #     self.cash -= action["amount"] * stock_b.get_price()
        elif action["action_type"] == "sell":
            self.action_history[date].append(action)
            # if action["stock"] == "stock_a":
            #     self.stock_a_amount -= action["amount"]
            #     self.cash += action["amount"] * stock_a.get_price()
            # else:
            #     self.stock_b_amount -= action["amount"]
            #     self.cash += action["amount"] * stock_b.get_price()
        elif action["action_type"] == "no":
            return action

        print("WRONG ACTION: {}".format(action))
        return None

    def buy_stock(self, stock_name, price, amount):
        self.cash -= price*amount
        if self.cash < 0 or stock_name not in ['A', 'B']:
            raise RuntimeError("ERROR: ILLEGAL STOCK BUY BEHAVIOR")
        if stock_name == 'A':
            self.stock_a_amount += amount
        elif stock_name == 'B':
            self.stock_b_amount += amount

    def sell_stock(self, stock_name, price, amount):
        if stock_name == 'A':
            self.stock_a_amount -= amount
        elif stock_name == 'B':
            self.stock_b_amount -= amount
        if self.stock_b_amount < 0 or self.stock_a_amount < 0:
            raise RuntimeError("ERROR: ILLEGAL STOCK SELL BEHAVIOR")
        self.cash += price * amount


    def loan_repayment(self, date):
        # check是否贷款还款日，还款，破产检查
        to_del = []
        for idx, loan in enumerate(self.loans):
            if loan["repayment_date"] == date:
                self.cash -= loan["amount"] * (1 + LOAN_RATE[loan["loan_type"]])
                to_del.append(idx)
        if self.cash < 0:
            self.bankrupt()
        for idx in to_del:
            del self.loans[idx]

    def interest_payment(self):
        # 贷款付息日付息
        for loan in self.loans:
            self.cash -= loan["amount"] * LOAN_RATE[loan["loan_type"]] / 4
            if self.cash < 0:
                self.bankrupt()

    def bankrupt(self):
        # todo cash<0，强制卖股票，股票卖完了破产，agent is_bankrupt=true
        return

    def is_bankrupt(self):
        return self.is_bankrupt
# test
# secretary = Secretary("gpt-3.5-turbo")
# agent = Agent(1, 123, secretary, "gpt-3.5-turbo")
# agent.plan_loan(1, 100, 100, "prompt")

# stocka = Stock("a", 5, 100, [])
# stockb = Stock("b", 7, 100, [])
# plan = '{"action_type": "sell", "stock": "B", "amount": 10}'
# print(secretary.check_action(plan, 100, 0, 20, stocka.get_price(), stockb.get_price()))