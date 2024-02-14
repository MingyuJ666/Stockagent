import math
import time
import openai
import tiktoken
import random

import utils
from log.custom_logger import log

from prompt.agent_prompt import *
from procoder.functional import format_prompt
from procoder.prompt import *



def random_init(stock_initial_price):
    stock, cash, debt_amount = 0.0, 0.0, 0.0
    while stock * stock_initial_price + cash < utils.MIN_INITIAL_PROPERTY \
            or stock * stock_initial_price + cash > utils.MAX_INITIAL_PROPERTY \
            or debt_amount > stock * stock_initial_price + cash:
        stock = int(random.uniform(0, utils.MAX_INITIAL_PROPERTY / stock_initial_price))
        cash = random.uniform(0, utils.MAX_INITIAL_PROPERTY)
        debt_amount = random.uniform(0, utils.MAX_INITIAL_PROPERTY)
    debt = {
        "loan": "yes",
        "amount": debt_amount,
        "loan_type": random.randint(0, len(utils.LOAN_TYPE)),
        "repayment_date": random.choice(utils.REPAYMENT_DAYS)
    }
    return stock, cash, debt


class Agent:
    def __init__(self, i, stock_a_price, secretary, model):
        self.order = i
        self.secretary = secretary
        self.model = model
        self.character = random.choice(["稳健型", "激进型"])

        self.stock_a_amount, self.cash, init_debt = random_init(stock_a_price)
        self.stock_b_amount = 0  # stock 以手为单位存储，一手=10股，股价其实是一手的价格
        self.init_proper = self.get_total_proper(stock_a_price, 0)  # 初始资产 后续借贷不超过初始资产

        self.action_history = [[] for _ in range(utils.TOTAL_DATE)]
        self.chat_history = []
        self.loans = [init_debt]
        self.is_bankrupt = False

    def run_api(self, prompt, temperature: float = 0):
        encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
        openai.api_key = utils.OPENAI_API_KEY
        client = openai.OpenAI(api_key=openai.api_key)
        self.chat_history.append({"role": "user", "content": prompt})
        max_retry = 2
        retry = 0

        # just cut off the overflow tokens
        # tokens = encoding.encode(self.chat_history)

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
                log.logger.warning("OpenAI api retry...{}".format(e))
                retry += 1
                time.sleep(1)
        log.logger.error("ERROR: OPENAI API FAILED. SKIP THIS INTERACTION.")
        return ""

    def get_total_proper(self, stock_a_price, stock_b_price):
        return self.stock_a_amount * stock_a_price + self.stock_b_amount * stock_b_price + self.cash

    def get_proper_cash_value(self, stock_a_price, stock_b_price):
        proper = self.stock_a_amount * stock_a_price + self.stock_b_amount * stock_b_price + self.cash
        a_value = self.stock_a_amount * stock_a_price
        b_value = self.stock_b_amount * stock_b_price
        return proper, self.cash, a_value, b_value

    def get_total_loan(self):
        debt = 0
        for loan in self.loans:
            debt += loan["amount"]
        return debt

    def plan_loan(self, date, stock_a_price, stock_b_price, lastday_forum_message):
        # first day action : prompt with background
        if date == 1:
            prompt = Collection(BACKGROUND_PROMPT,
                                LOAN_TYPE_PROMPT,
                                DECIDE_IF_LOAN_PROMPT).set_indexing_method(sharp2_indexing).set_sep("\n")
            assert self.init_proper >= self.get_total_loan()
            max_loan = self.init_proper - self.get_total_loan()
            inputs = {
                'date': date,
                'character': self.character,
                'stock_a': self.stock_a_amount,
                'stock_b': self.stock_b_amount,
                'cash': self.cash,
                'debt': self.loans,
                'max_loan': max_loan,
                'loan_rate1': utils.LOAN_RATE[0],
                'loan_rate2': utils.LOAN_RATE[1],
                'loan_rate3': utils.LOAN_RATE[2],
            }

        # other days action : prompt with last day forum message & stock price
        else:
            prompt = Collection(BACKGROUND_PROMPT,
                                LASTDAY_FORUM_AND_STOCK_PROMPT,
                                LOAN_TYPE_PROMPT,
                                DECIDE_IF_LOAN_PROMPT).set_indexing_method(sharp2_indexing).set_sep("\n")
            assert self.init_proper >= self.get_total_loan()
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
                "lastday_forum_message": lastday_forum_message,
                'loan_rate1': utils.LOAN_RATE[0],
                'loan_rate2': utils.LOAN_RATE[1],
                'loan_rate3': utils.LOAN_RATE[2],
            }
        if max_loan == 0:
            return {"loan": "no"}
        try_times = 0
        MAX_TRY_TIMES = 10
        resp = self.run_api(format_prompt(prompt, inputs))
        # print(resp)
        if resp == "":
            return {"loan": "no"}

        loan_format_check, fail_response, loan = self.secretary.check_loan(resp,
                                                                           max_loan)  # secretary check loan format
        while not loan_format_check:
            # log.logger.debug("WARNING: Loan format check failed because of these issues: {}".format(fail_response))
            try_times += 1
            if try_times > MAX_TRY_TIMES:
                log.logger.warning("WARNING: Loan format try times > MAX_TRY_TIMES. Skip as no loan today.")
                loan = {"loan": "no"}
                break

            resp = self.run_api(format_prompt(LOAN_RETRY_PROMPT, {"fail_response": fail_response}), temperature=0)
            if resp == "":
                return {"loan": "no"}
            loan_format_check, fail_response, loan = self.secretary.check_loan(date, resp)

        if loan["loan"] == "yes":
            loan["repayment_date"] = date + utils.LOAN_TYPE_DATE[loan["loan_type"]]  # add loan repayment_date
            self.loans.append(loan)
            self.action_history[date].append(loan)
            self.cash += loan["amount"]
            log.logger.info("INFO: Agent {} decide to loan: {}".format(self.order, loan))
        else:
            log.logger.info("INFO: Agent {} decide not to loan".format(self.order))
        return loan

    # date=交易日, time=当前交易时段
    def plan_stock(self, date, time, stock_a, stock_b, stock_a_deals, stock_b_deals):
        if date == 1:
            prompt = Collection(FIRST_DAY_FINANCIAL_REPORT,
                                DECIDE_BUY_STOCK_PROMPT).set_indexing_method(sharp2_indexing).set_sep("\n")
            inputs = {
                "date": date,
                "time": time,
                "stock_a": self.stock_a_amount,
                "stock_b": self.stock_b_amount,
                "stock_a_price": stock_a.get_price(),
                "stock_b_price": stock_b.get_price(),
                "stock_a_deals": stock_a_deals,
                "stock_b_deals": stock_b_deals,
                "cash": self.cash
            }
        elif date in utils.SEASON_REPORT_DAYS:
            index = utils.SEASON_REPORT_DAYS.index(date)
            prompt = Collection(SEASONAL_FINANCIAL_REPORT,
                                DECIDE_BUY_STOCK_PROMPT).set_indexing_method(sharp2_indexing).set_sep("\n")
            inputs = {
                "date": date,
                "time": time,
                "stock_a": self.stock_a_amount,
                "stock_b": self.stock_b_amount,
                "stock_a_price": stock_a.get_price(),
                "stock_b_price": stock_b.get_price(),
                "stock_a_deals": stock_a_deals,
                "stock_b_deals": stock_b_deals,
                "cash": self.cash,
                "stock_a_report": stock_a.gen_financial_report(index),
                "stock_b_report": stock_b.gen_financial_report(index)
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
                "stock_a_deals": stock_a_deals,
                "stock_b_deals": stock_b_deals,
                "cash": self.cash
            }
        try_times = 0
        MAX_TRY_TIMES = 10
        resp = self.run_api(format_prompt(prompt, inputs))
        # print(resp)
        if resp == "":
            return {"action_type": "no"}

        action_format_check, fail_response, action = self.secretary.check_action(
            resp, self.cash, self.stock_a_amount, self.stock_b_amount, stock_a.get_price(), stock_b.get_price())
        while not action_format_check:
            # log.logger.debug("Action format check failed because of these issues: {}".format(fail_response))
            try_times += 1
            if try_times > MAX_TRY_TIMES:
                log.logger.warning("WARNING: Action format try times > MAX_TRY_TIMES. Skip as no loan today.")
                action = {"action_type": "no"}
                break

            resp = self.run_api(format_prompt(BUY_STOCK_RETRY_PROMPT, {"fail_response": fail_response}), temperature=0)
            if resp == "":
                return {"action_type": "no"}
            action_format_check, fail_response, action = self.secretary.check_action(
                resp, self.cash, self.stock_a_amount, self.stock_b_amount, stock_a.get_price(), stock_b.get_price())

        if action["action_type"] == "buy":
            self.action_history[date].append(action)
            log.logger.info("INFO: Agent {} decide to action: {}".format(self.order, action))
            # if action["stock"] == "stock_a":
            #     self.stock_a_amount += action["amount"]
            #     self.cash -= action["amount"] * stock_a.get_price()
            # else:
            #     self.stock_b_amount += action["amount"]
            #     self.cash -= action["amount"] * stock_b.get_price()
            return action
        elif action["action_type"] == "sell":
            self.action_history[date].append(action)
            log.logger.info("INFO: Agent {} decide to action: {}".format(self.order, action))
            # if action["stock"] == "stock_a":
            #     self.stock_a_amount -= action["amount"]
            #     self.cash += action["amount"] * stock_a.get_price()
            # else:
            #     self.stock_b_amount -= action["amount"]
            #     self.cash += action["amount"] * stock_b.get_price()
            return action
        elif action["action_type"] == "no":
            log.logger.info("INFO: Agent {} decide not to action".format(self.order))
            return action

        log.logger.error("ERROR: WRONG ACTION: {}".format(action))
        return {"action_type": "no"}

    def buy_stock(self, stock_name, price, amount):
        self.cash -= price * amount
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
                self.cash -= loan["amount"] * (1 + utils.LOAN_RATE[loan["loan_type"]])
                to_del.append(idx)
        if self.cash < 0:
            self.is_bankrupt = True
        for idx in to_del:
            del self.loans[idx]

    def interest_payment(self):
        # 贷款付息日付息
        for loan in self.loans:
            self.cash -= loan["amount"] * utils.LOAN_RATE[loan["loan_type"]] / 4
            if self.cash < 0:
                self.is_bankrupt = True

    def bankrupt_process(self, stock_a_price, stock_b_price):
        total_value_of_stock = self.stock_a_amount * stock_a_price + self.stock_b_amount * stock_b_price
        if total_value_of_stock + self.cash < 0:
            log.logger.warning(f"Agent {self.order} bankrupt. Action history: " + str(self.action_history))
            return True
        if stock_a_price * self.stock_a_amount >= -self.cash:
            sell_a = math.ceil(-self.cash / stock_a_price)
            self.stock_a_amount -= sell_a
            self.cash += sell_a * stock_a_price
        else:
            self.cash += stock_a_price * self.stock_a_amount
            self.stock_a_amount = 0
            sell_b = math.ceil(-self.cash / stock_b_price)
            self.stock_b_amount -= sell_b
            self.cash += sell_b * stock_b_price

        if self.stock_a_amount < 0 or self.stock_b_amount < 0 or self.cash < 0:
            raise RuntimeError("ERROR: WRONG BANKRUPT PROCESS")

        return False

    def post_message(self):
        prompt = format_prompt(POST_MESSAGE_PROMPT, inputs={})
        resp = self.run_api(prompt)
        return resp

    def next_day_estimate(self):
        prompt = format_prompt(NEXT_DAY_ESTIMATE_PROMPT, inputs={})
        resp = self.run_api(prompt)
        if resp == "":
            return {"buy_A": "no", "buy_B": "no", "sell_A": "no", "sell_B": "no", "loan": "no"}
        format_check, fail_response, estimate = self.secretary.check_estimate(resp)
        try_times = 0
        MAX_TRY_TIMES = 10
        while not format_check:
            try_times += 1
            if try_times > MAX_TRY_TIMES:
                log.logger.warning("WARNING: Estimation format try times > MAX_TRY_TIMES. Skip as all 'no' today.")
                estimate = {"buy_A": "no", "buy_B": "no", "sell_A": "no", "sell_B": "no", "loan": "no"}
                break
            resp = self.run_api(format_prompt(NEXT_DAY_ESTIMATE_RETRY, {"fail_response": fail_response}), temperature=0)
            if resp == "":
                return {"buy_A": "no", "buy_B": "no", "sell_A": "no", "sell_B": "no", "loan": "no"}
            format_check, fail_response, estimate = self.secretary.check_estimate(resp)
        return estimate

# test
# secretary = Secretary("gpt-3.5-turbo")
# agent = Agent(1, 123, secretary, "gpt-3.5-turbo")
# stocka = Stock("a", 5, 100, [])
# stockb = Stock("b", 7, 100, [])
# agent.plan_stock(33, 1, stocka, stockb, "", "")


# plan = '{"action_type": "sell", "stock": "B", "amount": 10}'
# print(secretary.check_action(plan, 100, 0, 20, stocka.get_price(), stockb.get_price()))
