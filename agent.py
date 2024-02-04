import os
import openai
import random
from prompt.agent_prompt import *
from procoder.functional import format_prompt
from procoder.prompt import *
from utils import *

def random_init(stock_initial_price):
    stock, cash, debt = 0.0, 0.0, 0.0
    while stock * stock_initial_price + cash < MIN_INITIAL_PROPERTY \
            or stock * stock_initial_price + cash > MAX_INITIAL_PROPERTY\
            or debt > stock * stock_initial_price + cash:
        stock = random.uniform(0, MAX_INITIAL_PROPERTY / stock_initial_price)
        cash = random.uniform(0, MAX_INITIAL_PROPERTY)
        debt = random.uniform(0, MAX_INITIAL_PROPERTY)
    return stock, cash, debt



def run_api(model, prompt, temperature: float = 0):
    openai.api_key = ""
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    resp = response.choices[0].message.content
    return resp

class Agent:
    def __init__(self, i, stock_a_price, secretary, model):
        self.order = i
        self.secretary = secretary
        self.model = model
        self.character = random.choice(["性格一", "性格二"])  # todo
        self.stock_a, self.cash, self.debt = random_init(stock_a_price)
        self.stock_b = 0
        self.history = [[] for _ in range(TOTAL_DATE)]
        self.loans = []

    def plan_loan(self, date):
        # first day action
        if date == 1:
            prompt = Collection(BACKGROUND_PROMPT, LOAN_TYPE_PROMPT, DECIDE_IF_MOAN_PROMPT)
            inputs = {
                "date": date,
                "character": self.character,
                "stock_a": self.stock_a,
                "stock_b": self.stock_b,
                "cash": self.cash,
            }
        # other day action
        else:
            prompt = Collection(LOAN_TYPE_PROMPT, DECIDE_IF_MOAN_PROMPT)
            inputs = {
                "date": date,
                "character": self.character,
                "stock_a": self.stock_a,
                "stock_b": self.stock_b,
                "cash": self.cash,
            }
        resp = run_api(self.model, format_prompt(prompt, inputs), temperature=0)
        loan = self.secretary.check_moan(date, resp)
        self.loans.append(loan)
        self.history[date].append(loan)



