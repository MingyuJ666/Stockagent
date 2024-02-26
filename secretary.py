import json
import os
import openai
from log.custom_logger import log


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


class Secretary:
    def __init__(self, model):
        self.model = model

    def get_response(self, prompt):
        return run_api(self.model, prompt)

    """
        用json形式返回结果，例如：
        {{{{"loan": "yes", "loan_type": 3, "amount": 1000}}}}
        如果不需贷款，则返回：
        {{{{"loan" : "no"}}}}
        :returns: loan_format_check, fail_response, loan
    """

    def check_loan(self, resp, max_loan) -> (bool, str, dict):
        # format check
        if isinstance(resp, str) and resp.count('{') == 1 and resp.count('}') == 1:
            start_idx = resp.index('{')
            end_idx = resp.index('}')
        else:
            log.logger.debug("Wrong json content in response: {}".format(resp))
            fail_response = "Wrong json format, there is no {} or more than one {} in response."
            return False, fail_response, None

        action_json = resp[start_idx: end_idx + 1]
        action_json = action_json.replace("\n", "").replace(" ", "")
        try:
            parsed_json = json.loads(action_json)
        except json.JSONDecodeError as e:
            print(e)
            log.logger.debug("Illegal json content in response: {}".format(resp))
            fail_response = "Illegal json format."
            return False, fail_response, None

        # content check
        try:
            if "loan" not in parsed_json:
                log.logger.debug("Wrong json content in response: {}".format(resp))
                fail_response = "Key 'loan' not in response."
                return False, fail_response, None

            if parsed_json["loan"].lower() not in ["yes", "no"]:
                log.logger.debug("Wrong json content in response: {}".format(resp))
                fail_response = "Value of key 'loan' should be yes or no."
                return False, fail_response, None

            if parsed_json["loan"].lower() == "no":
                if "loan_type" in parsed_json or "amount" in parsed_json:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = "Don't include loan_type or amount in response if value of key 'loan' is no."
                    return False, fail_response, None
                else:
                    return True, "", parsed_json

            if parsed_json["loan"].lower() == "yes":
                if "loan_type" not in parsed_json or "amount" not in parsed_json:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = "Should include loan_type and amount in response if value of key 'loan' is yes."
                    return False, fail_response, None
                if parsed_json["loan_type"] not in [0, 1, 2]:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = "Value of key 'loan_type' should be 0, 1 or 2."
                    return False, fail_response, None
                if parsed_json["amount"] <= 0 or parsed_json["amount"] > max_loan:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = f"Value of key 'amount' should be positive and less than {max_loan}"
                    return False, fail_response, None
                return True, "", parsed_json

            log.logger.error("UNSOLVED LOAN JSON RESPONSE:{}".format(parsed_json))
            return False, "", None
        except Exception as e:
            log.logger.error("UNSOLVED LOAN JSON RESPONSE:{}".format(parsed_json))
            return False, "", None

    def check_action(self, resp, cash, stock_a_amount,
                     stock_b_amount, stock_a_price, stock_b_price) -> (bool, str, dict):
        # format check
        if isinstance(resp, str) and resp.count('{') == 1 and resp.count('}') == 1:
            start_idx = resp.index('{')
            end_idx = resp.index('}')
        else:
            log.logger.debug("Wrong json content in response: {}".format(resp))
            fail_response = "Wrong json format, there is no {} or more than one {} in response."
            return False, fail_response, None

        action_json = resp[start_idx: end_idx + 1]
        action_json = action_json.replace("\n", "").replace(" ", "")
        try:
            parsed_json = json.loads(action_json)
        except json.JSONDecodeError as e:
            print(e)
            log.logger.debug("Illegal json content in response: {}".format(resp))
            fail_response = "Illegal json format."
            return False, fail_response, None

        # content check
        try:
            prices = {"A": stock_a_price, "B": stock_b_price}
            holds = {"A": stock_a_amount, "B": stock_b_amount}
            if "action_type" not in parsed_json:
                log.logger.debug("Wrong json content in response: {}".format(resp))
                fail_response = "Key 'action_type' not in response."
                return False, fail_response, None

            if parsed_json["action_type"].lower() not in ["buy", "sell", "no"]:
                log.logger.debug("Wrong json content in response: {}".format(resp))
                fail_response = "Value of key 'action_type' should be 'buy', 'sell' or 'no'."
                return False, fail_response, None

            if parsed_json["action_type"].lower() == "no":
                if "stock" in parsed_json or "amount" in parsed_json:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = "Don't include stock or amount in response if value of key 'action_type' is no."
                    return False, fail_response, None
                else:
                    return True, "", parsed_json
            else:
                if "stock" not in parsed_json or "amount" not in parsed_json or "price" not in parsed_json:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = "Should include stock, amount and price in response " \
                                    "if value of key 'action_type' is buy or sell."
                    return False, fail_response, None
                if parsed_json["stock"] not in ['A', 'B']:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = "Value of key 'stock' should be 'A' or 'B'."
                    return False, fail_response, None
                if parsed_json["price"] <= 0:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = f"Value of key 'price' should be positive."
                    return False, fail_response, None
                if not isinstance(parsed_json["amount"], int):
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = f"Value of key 'amount' should be integer."
                    return False, fail_response, None

                # buy more than cash or sell more than hold amount
                # price = prices[parsed_json["stock"]]
                price = parsed_json["price"]
                if parsed_json["action_type"].lower() == "buy":
                    if parsed_json["amount"] <= 0 or parsed_json["amount"] * price > cash:
                        log.logger.debug("Buy more than cash: {}".format(resp))
                        fail_response = f"The cash you have now is {cash}, " \
                                        f"the value of 'amount' * 'price'  " \
                                        f"should be positive and not exceed cash."
                        return False, fail_response, None

                hold_amount = holds[parsed_json["stock"]]
                if parsed_json["action_type"].lower() == "sell":
                    if parsed_json["amount"] <= 0 or parsed_json["amount"] > hold_amount:
                        log.logger.debug("Sell more than hold: {}".format(resp))
                        fail_response = f"The amount of stock you hold is {hold_amount}, " \
                                        f"the value of 'amount' should be positive and not exceed the " \
                                        f"amount of stock you hold."
                        return False, fail_response, None
                return True, "", parsed_json

        except Exception as e:
            log.logger.error("UNSOLVED ACTION JSON RESPONSE:{}".format(parsed_json))
            return False, "", None

    def check_estimate(self, resp):
        # format check
        if isinstance(resp, str) and resp.count('{') == 1 and resp.count('}') == 1:
            start_idx = resp.index('{')
            end_idx = resp.index('}')
        else:
            log.logger.debug("Wrong json content in response: {}".format(resp))
            fail_response = "Wrong json format, there is no {} or more than one {} in response."
            return False, fail_response, None

        action_json = resp[start_idx: end_idx + 1]
        action_json = action_json.replace("\n", "").replace(" ", "")
        try:
            parsed_json = json.loads(action_json)
        except json.JSONDecodeError as e:
            print(e)
            log.logger.debug("Illegal json content in response: {}".format(resp))
            fail_response = "Illegal json format."
            return False, fail_response, None

        # content check
        try:
            if "buy_A" not in parsed_json or "buy_B" not in parsed_json \
                    or "sell_A" not in parsed_json or "sell_B" not in parsed_json \
                    or "loan" not in parsed_json:
                log.logger.debug("Wrong json content in response: {}".format(resp))
                fail_response = "Key 'buy_A', 'buy_B', 'sell_A', 'sell_B' and 'loan' should in response."
                return False, fail_response, None

            for key, item in parsed_json.items():
                if item not in ['yes', 'no']:
                    log.logger.debug("Wrong json content in response: {}".format(resp))
                    fail_response = "Value of all keys should be 'yes' or 'no'."
                    return False, fail_response, None
            return True, "", parsed_json

        except Exception as e:
            log.logger.error("UNSOLVED ESTIMATE JSON RESPONSE:{}".format(parsed_json))
            return False, "", None
