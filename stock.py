import utils

class Stock:
    def __init__(self, name, initial_price, initial_stock, is_new=False):
        self.name = name
        self.price = initial_price
        self.ideal_price = 0
        self.initial_stock = initial_stock
        self.history = {}   # {date: session_deal}
        self.session_deal = [] # [{"price", "amount"}]

    def gen_financial_report(self, index):
        if self.name == "A":
            return utils.FINANCIAL_REPORT_A[index]
        elif self.name == "B":
            return utils.FINANCIAL_REPORT_B[index]

    def add_session_deal(self, price_and_amount):
        self.session_deal.append(price_and_amount)

    def update_price(self, date):
        if len(self.session_deal) == 0:
            return
        self.price = self.session_deal[-1]["price"]
        self.history[date] = self.session_deal
        self.session_deal.clear()

    def get_price(self):
        return self.price


