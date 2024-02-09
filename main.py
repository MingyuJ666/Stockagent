import argparse
import random
from colorama import Fore, Style

from utils import *
from agent import Agent
from secretary import Secretary
from stock import Stock


def handle_action(action, stock_deals, all_agents, stock):
    # action = JSON{"agent": 1, "action_type": "buy"|"sell", "stock": "A"|"B", "amount": 10, "price": 10}
    if action["action_type"] == "buy":
        for sell_action in stock_deals["sell"][:]:
            if action["price"] == sell_action["price"]:
                # 交易成交
                close_amount = min(action["amount"], sell_action["amount"])
                all_agents[action["agent"]].buy_stock(stock.name, close_amount, action["price"])
                all_agents[sell_action["agent"]].sell_stock(stock.name, close_amount, action["price"])
                stock.add_session_deal({"price": action["price"], "amount": close_amount})

                if action["amount"] >= close_amount:  # 买单未结束，卖单结束，继续循环
                    stock_deals["sell"].remove(sell_action)
                    action["amount"] -= close_amount
                else:  # 卖单未结束，买单结束
                    sell_action["amount"] -= close_amount
                    return
        # 遍历卖单后仍然有剩余
        stock_deals["buy"].append(action)

    else:
        for buy_action in stock_deals["buy"][:]:
            if action["price"] == buy_action["price"]:
                # 交易成交
                close_amount = min(action["amount"], buy_action["amount"])
                all_agents[action["agent"]].sell_stock(stock.name, close_amount, action["price"])
                all_agents[buy_action["agent"]].buy_stock(stock.name, close_amount, action["price"])
                stock.add_session_deal({"price": action["price"], "amount": close_amount})

                if action["amount"] >= close_amount:  # 卖单未结束，买单结束，继续循环
                    stock_deals["buy"].remove(buy_action)
                    action["amount"] -= close_amount
                else:  # 买单未结束，卖单结束
                    buy_action["amount"] -= close_amount
                    return
        stock_deals["sell"].append(action)


def simulation(args):
    # init
    secretary = Secretary(args.model)
    stock_a = Stock("A", STOCK_A_INITIAL_PRICE, 0, is_new=False)
    stock_b = Stock("B", STOCK_B_INITIAL_PRICE, STOCK_B_PUBLISH, is_new=True)
    all_agents = []
    for i in range(1, AGENTS_NUM + 1):  # agents start from 1, 0 refers to stock_b
        agent = Agent(i, stock_a.get_price(), secretary, args.model)
        all_agents.append(agent)

    # start simulation
    last_day_forum_message = []
    stock_a_deals = {"sell": [], "buy": []}
    stock_b_deals = {"sell": [], "buy": []}
    # stock b publish
    stock_b_deals["sell"].append({"agent": 0, "amount": STOCK_B_PUBLISH, "price": STOCK_B_INITIAL_PRICE})

    print(Fore.GREEN + "--------Simulation Start!--------" + Style.RESET_ALL)
    for date in range(1, TOTAL_DATE + 1):

        print(Fore.GREEN + f"--------DAY {date}---------" + Style.RESET_ALL)
        # 除b发行外，删除前一天的所有交易
        stock_a_deals["sell"].clear()
        stock_a_deals["buy"].clear()
        stock_b_deals["buy"].clear()

        tmp_action = next((action for action in stock_b_deals["sell"] if action["agent"] == 0), None)
        stock_b_deals["sell"].clear()
        if tmp_action:
            tmp_action["price"] *= 0.9  # B发行折价
            if tmp_action["price"] < 1:
                print(Fore.RED + "WARNING: STOCK B WITHDRAW FROM MARKET!!!" + Style.RESET_ALL)
            stock_b_deals["sell"].append(tmp_action)

        # check if an agent needs to repay loans
        for agent in all_agents[:]:
            agent.loan_repayment(date)
            if agent.is_bankrupt():
                all_agents.remove(agent)

        # repayment days
        if date in REPAYMENT_DAYS:
            for agent in all_agents[:]:
                agent.interest_payment()
                if agent.is_bankrupt():
                    all_agents.remove(agent)

        # seasonal report release days
        if date in SEASON_REPORT_DAYS:
            report_a = stock_a.gen_financial_report()
            report_b = stock_b.gen_financial_report()
            # todo 理想股价更新？

        # todo if date in 特定事件日（预先定义）

        # agent decide whether to loan
        for agent in all_agents:
            agent.plan_loan(date, stock_a.get_price(), stock_b.get_price(), last_day_forum_message)

        for session in range(1, TOTAL_SESSION + 1):
            print(Fore.GREEN + f"SESSION {session}" + Style.RESET_ALL)
            # 随机定义交易顺序
            sequence = list(range(len(all_agents)))
            random.shuffle(sequence)
            for i in sequence:
                agent = all_agents[i]
                action = agent.plan_stock(date, session, stock_a, stock_b, stock_a_deals, stock_b_deals)
                action["agent"] = agent.order
                if not action["action_type"] == "no":
                    if action["stock"] == 'A':
                        handle_action(action, stock_a_deals, all_agents, stock_a)
                    else:
                        handle_action(action, stock_b_deals, all_agents, stock_b)

            # 交易时段结束，更新股票价格
            stock_a.update_price(date)
            stock_b.update_price(date)

        # 交易日结束，论坛信息更新
        last_day_forum_message.clear()
        for agent in all_agents:
            message = agent.post_message()
            last_day_forum_message.append({"name": agent.order, "message": message})

    print(Fore.GREEN + "--------Simulation finished!--------" + Style.RESET_ALL)
    print(Fore.GREEN + "--------Agents action history--------" + Style.RESET_ALL)
    for agent in all_agents:
        print(f"Agent {agent.order} action history:")
        print(agent.action_history)
    print(Fore.GREEN + "--------Stock deal history--------" + Style.RESET_ALL)
    for stock in [stock_a, stock_b]:
        print(f"Stock {stock.name} deal history:")
        print(stock.history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="model name")
    args = parser.parse_args()
    simulation(args)
