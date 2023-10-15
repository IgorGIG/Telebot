import requests
import json
from config import CURRENCY_NAMES
class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price (quote: str, base: str, amount: str):
        try:
            quote_ticker = CURRENCY_NAMES[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта {quote} отсутствует в списке доступных валют.')

        try:
            base_ticker = CURRENCY_NAMES[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} отсутствует в списке доступных валют.')

        if quote_ticker == base_ticker:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote} и {base}.')

        try:
            amount_num = float(amount)
        except ValueError:
            raise APIException(f'Неверное количество {amount}.')

        r = requests.get('https://www.cbr-xml-daily.ru/latest.js')
        rates = json.loads(r.content)['rates']
        print(rates)
        if quote_ticker == 'RUB':
            rate = rates[base_ticker]
        elif base_ticker == 'RUB':
            rate = 1 / rates[quote_ticker]
        else:
            rate = rates[base_ticker] / rates[quote_ticker]
        print(amount, quote_ticker, '=', amount_num * rate, base_ticker)
        return amount_num * rate
