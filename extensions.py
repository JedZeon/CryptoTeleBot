import requests
import json
from config import keys_val


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты: {base}")

        try:
            base_ticker = keys_val[base]
        except KeyError:
            raise APIException(f'Не найдена валюта: {base}')

        try:
            quote_ticker = keys_val[quote]
        except KeyError:
            raise APIException(f'Не найдена валюта: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        data_val = json.loads(r.content)[keys_val[quote]]

        return data_val
