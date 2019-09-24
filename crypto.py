import requests
import json
import tokens


class CoinApi:
    url = 'https://rest.coinapi.io/v1/exchangerate/{0}/{1}'

    coins = ('BTC', 'ETH', 'XRP', 'BCH', 'XLM', 'EOS', 'LTC',
             'ADA', 'XMR', 'TRX', 'MIOTA', 'DASH', 'ETC')

    def __init__(self, crypto='BTC', currency='UAH'):
        self.crypto = crypto
        self.currency = currency

    def get(self):
        url = self.url.format(self.crypto, self.currency)
        response = requests.get(url, headers={'X-CoinAPI-Key': tokens.coinapi})
        if response.status_code == 200:
            data = json.loads(response.text)
            return data.get('rate')
        return None
