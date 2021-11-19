import requests
import json
from settings import API_KEY


class APIException(Exception):
    pass


class ErrorSameCurrency(APIException):
    def __str__(self):
        return 'Выберите разные валюты'


class ErrorCorrectData(APIException):
    def __str__(self):
        return 'Введите корректные данные в формате: <имя валюты> ' \
               '<в какую валюту перевести> <количество переводимой валюты>'


class AmountNotDigits(APIException):
    def __str__(self):
        return 'Количество должно быть числом'


class ErrorCurrencyCodes(APIException):
    def __str__(self):
        return 'Укажите верные коды валют'


class Currency:
    def __init__(self):
        self.params = {'access_key': API_KEY}
        self.url_latest = 'http://api.exchangeratesapi.io/v1/latest'
        self.url_all_curr = 'http://api.exchangeratesapi.io/v1/symbols'
        self.keys = {'евро': 'EUR',
                     'доллар': 'USD',
                     'золото': 'XAU',
                     'серебро': 'XAG',
                     'рубль': 'RUB',
                     'биткоин': 'BTC'}

    # @staticmethod
    def get_price(self, base, quote, amount):
        base, quote = self.keys.get(base.lower(), base), self.keys.get(quote.lower(), quote)
        params = self.params
        if base == 'EUR':
            params['symbols'] = f'{quote}'
            req = self.request(self.url_latest, params=params)
            if req.get('error', 0) != 0:
                raise ErrorCurrencyCodes()
            return req["rates"][quote] * int(amount)
        elif quote == 'EUR':
            params['symbols'] = f'{base}'
            req = self.request(self.url_latest, params=params)
            if req.get('error', 0) != 0:
                raise ErrorCurrencyCodes()
            return 1/req['rates'][base] * int(amount)
        else:
            params['symbols'] = f'{base},{quote}'
            req = self.request(self.url_latest, params=params)
            if req.get('error', 0) != 0:
                raise ErrorCurrencyCodes()
            return 1/req['rates'][base] * req['rates'][quote] * int(amount)


    def get_all_currencies(self):
        return self.request(url=self.url_all_curr, params=self.params)['symbols']

    def request(self, url, params):
        req = requests.get(url, params=params).content
        to_json = json.loads(req)
        print(to_json)
        return to_json


# all rates
# url = 'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&format=1'

# available rates
# url = f'http://api.exchangeratesapi.io/v1/symbols?access_key={API_KEY}&format=1'

# url = f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&symbols=USD,AUD,CAD,PLN,MXN&format=1'
# url = f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&symbols=USD,RUB&format=1'

#
# c = Currency()
# print(c.get_all_currencies())

# url = 'http://api.exchangeratesapi.io/v1/latest'
# params = {'access_key': API_KEY, 'symbols': 'USD,RUB'}
# req = requests.get(url, params=params).content
# to_json = json.loads(req)
# print(to_json)
