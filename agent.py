import os
import openai
import random
from prompt.agent_prompt import *
from procoder.functional import format_prompt
from procoder.prompt import *


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
    def __init__(self, i, secretary, model):
        self.order = i
        self.secretary = secretary
        self.model = model
        self.character = random.choice(["性格一", "性格二"])
        self.stock_a = ?
        self.stock_b = 0
        self.cash = ?

    def plan_loan(self, date):
        prompt = Collection(LOAN_TYPE_PROMPT, DECIDE_IF_MOAN_PROMPT)
        inputs = {
            "date": date,
            "character": self.character,
            "stock_a": self.stock_a,
            "stock_b": self.stock_b,
            "cash": self.cash,
        }
        resp = run_api(self.model, format_prompt(prompt, inputs), temperature=0)


