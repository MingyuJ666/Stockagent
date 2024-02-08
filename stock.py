import json
import os

class Stock:
    def __init__(self, name, initial_price, initial_stock, is_new=False):
        self.name = name
        self.price = initial_price
        self.ideal_price = 0
        self.initial_stock = initial_stock
        self.history = {}   # {date: session_deal}
        self.session_deal = [] # [{"price", "amount"}]

    def gen_financial_report(self):
        # todo 生成季度财报
        return {
            "name": self.name,
            "price": self.price,
            "history": self.history
        }

    """
    {{{{"action_type":"buy"|"sell", "stock":"A"|"B", amount: 100}}}}
    """
    def get_new_price(self, action_list):
        # todo 根据交易时段的交易情况（json列表），更新价格
        for action in action_list:
            if not action["stock"] == self.name:
                continue
            if action["action_type"] == "buy":
                self.price = 0
            elif action["action_type"] == "sell":
                self.price = 0

    def add_session_deal(self, price_and_amount):
        self.session_deal.append(price_and_amount)

    def update_price(self, date):
        self.price = self.session_deal[-1]["price"]
        self.history[date] = self.session_deal
        self.session_deal.clear()

    def get_price(self):
        return self.price


