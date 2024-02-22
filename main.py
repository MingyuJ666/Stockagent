import argparse
import random
import pandas as pd
import openai
import tiktoken

import util
from agent import Agent
from secretary import Secretary
from stock import Stock
from log.custom_logger import log
from record import create_stock_record, create_trade_record, AgentRecordDaily, create_agentses_record


def handle_action(action, stock_deals, all_agents, stock, session):
    # action = JSON{"agent": 1, "action_type": "buy"|"sell", "stock": "A"|"B", "amount": 10, "price": 10}
    if action["action_type"] == "buy":
        for sell_action in stock_deals["sell"][:]:
            if action["price"] == sell_action["price"]:
                # 交易成交
                close_amount = min(action["amount"], sell_action["amount"])
                all_agents[action["agent"]].buy_stock(stock.name, close_amount, action["price"])
                if not sell_action["agent"] == -1:  # B发行
                    all_agents[sell_action["agent"]].sell_stock(stock.name, close_amount, action["price"])
                stock.add_session_deal({"price": action["price"], "amount": close_amount})
                create_trade_record(action["date"], session, stock.name, action["agent"], sell_action["agent"],
                                    close_amount, action["price"])

                if action["amount"] > close_amount:  # 买单未结束，卖单结束，继续循环
                    log.logger.info(f"ACTION - BUY:{action['agent']}, SELL:{sell_action['agent']}, "
                                    f"STOCK:{stock.name}, PRICE:{action['price']}, AMOUNT:{close_amount}")
                    stock_deals["sell"].remove(sell_action)
                    action["amount"] -= close_amount
                else:  # 卖单未结束，买单结束
                    log.logger.info(f"ACTION - BUY:{action['agent']}, SELL:{sell_action['agent']}, "
                                    f"STOCK:{stock.name}, PRICE:{action['price']}, AMOUNT:{close_amount}")
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
                create_trade_record(action["date"], session, stock.name, buy_action["agent"], action["agent"],
                                    close_amount, action["price"])

                if action["amount"] > close_amount:  # 卖单未结束，买单结束，继续循环
                    log.logger.info(f"ACTION - BUY:{buy_action['agent']}, SELL:{action['agent']}, "
                                    f"STOCK:{stock.name}, PRICE:{action['price']}, AMOUNT:{close_amount}")
                    stock_deals["buy"].remove(buy_action)
                    action["amount"] -= close_amount
                else:  # 买单未结束，卖单结束
                    log.logger.info(f"ACTION - BUY:{buy_action['agent']}, SELL:{action['agent']}, "
                                    f"STOCK:{stock.name}, PRICE:{action['price']}, AMOUNT:{close_amount}")
                    buy_action["amount"] -= close_amount
                    return
        stock_deals["sell"].append(action)


def simulation(args):
    # init
    secretary = Secretary(args.model)
    stock_a = Stock("A", util.STOCK_A_INITIAL_PRICE, 0, is_new=False)
    stock_b = Stock("B", util.STOCK_B_INITIAL_PRICE, util.STOCK_B_PUBLISH, is_new=True)
    all_agents = []
    log.logger.debug("Agents initial...")
    for i in range(0, util.AGENTS_NUM):  # agents start from 0, -1 refers to stock_b
        agent = Agent(i, stock_a.get_price(), secretary, args.model)
        all_agents.append(agent)
        log.logger.debug("cash: {}, stock a: {}, debt: {}".format(agent.cash, agent.stock_a_amount, agent.loans))

    # start simulation
    last_day_forum_message = []
    stock_a_deals = {"sell": [], "buy": []}
    stock_b_deals = {"sell": [], "buy": []}
    # stock b publish
    stock_b_deals["sell"].append({"agent": -1, "amount": util.STOCK_B_PUBLISH, "price": util.STOCK_B_INITIAL_PRICE})

    log.logger.debug("--------Simulation Start!--------")
    for date in range(1, util.TOTAL_DATE + 1):

        log.logger.debug(f"--------DAY {date}---------")
        # 除b发行外，删除前一天的所有交易
        stock_a_deals["sell"].clear()
        stock_a_deals["buy"].clear()
        stock_b_deals["buy"].clear()

        tmp_action = next((action for action in stock_b_deals["sell"] if action["agent"] == 0), None)
        stock_b_deals["sell"].clear()
        if tmp_action:
            tmp_action["price"] *= 0.9  # B发行折价
            if tmp_action["price"] < 1:
                log.logger.warning("WARNING: STOCK B WITHDRAW FROM MARKET!!!")
            stock_b_deals["sell"].append(tmp_action)

        # check if an agent needs to repay loans
        for agent in all_agents[:]:
            agent.chat_history.clear()  # 只保存当天的聊天记录
            agent.loan_repayment(date)

        # repayment days
        if date in util.REPAYMENT_DAYS:
            for agent in all_agents[:]:
                agent.interest_payment()

        # special events
        if date == util.EVENT_1_DAY:
            util.LOAN_RATE = util.EVENT_1_LOAN_RATE
            last_day_forum_message.append({"name": -1, "message": util.EVENT_1_MESSAGE})
        if date == util.EVENT_2_DAY:
            util.LOAN_RATE = util.EVENT_2_LOAN_RATE
            last_day_forum_message.append({"name": -1, "message": util.EVENT_2_MESSAGE})

        # agent decide whether to loan
        daily_agent_records = []
        for agent in all_agents:
            loan = agent.plan_loan(date, stock_a.get_price(), stock_b.get_price(), last_day_forum_message)
            daily_agent_records.append(AgentRecordDaily(date, agent.order, loan))

        for session in range(1, util.TOTAL_SESSION + 1):
            log.logger.debug(f"SESSION {session}")
            # 随机定义交易顺序
            sequence = list(range(len(all_agents)))
            random.shuffle(sequence)
            for i in sequence:
                agent = all_agents[i]
                if agent.is_bankrupt:  # cash<0的当天停止交易，交易时段结束后贩卖股票
                    continue

                action = agent.plan_stock(date, session, stock_a, stock_b, stock_a_deals, stock_b_deals)
                proper, cash, valua_a, value_b = agent.get_proper_cash_value(stock_a.get_price(), stock_b.get_price())
                create_agentses_record(agent.order, date, session, proper, cash, valua_a, value_b, action)
                action["agent"] = agent.order
                if not action["action_type"] == "no":
                    if action["stock"] == 'A':
                        handle_action(action, stock_a_deals, all_agents, stock_a, session)
                    else:
                        handle_action(action, stock_b_deals, all_agents, stock_b, session)

            # 交易时段结束，更新股票价格
            stock_a.update_price(date)
            stock_b.update_price(date)
            create_stock_record(date, session, stock_a.get_price(), stock_b.get_price())

        # deal with cash<0 agents
        for agent in all_agents[:]:
            quit_sig = agent.bankrupt_process(stock_a.get_price(), stock_b.get_price())
            if quit_sig:
                all_agents.remove(agent)

        # agent预测明天行动
        for idx, agent in enumerate(all_agents):
            estimation = agent.next_day_estimate()
            daily_agent_records[idx].add_estimate(estimation)
            daily_agent_records[idx].write_to_excel()
        daily_agent_records.clear()

        # 交易日结束，论坛信息更新
        last_day_forum_message.clear()
        log.logger.debug(f"DAY {date} ends, display forum messages...")
        for agent in all_agents:
            chat_history = agent.chat_history
            message = agent.post_message()
            log.logger.info("Agent {} says: {}".format(agent.order, message))
            last_day_forum_message.append({"name": agent.order, "message": message})



    log.logger.debug("--------Simulation finished!--------")
    log.logger.debug("--------Agents action history--------")
    # for agent in all_agents:
    #     log.logger.debug(f"Agent {agent.order} action history:")
    #     log.logger.info(agent.action_history)
    # log.logger.debug("--------Stock deal history--------")
    # for stock in [stock_a, stock_b]:
    #     log.logger.debug(f"Stock {stock.name} deal history:")
    #     log.logger.info(stock.history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="model name")
    args = parser.parse_args()
    simulation(args)
