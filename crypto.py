import requests
import json


class CoinApi:
    url = 'https://rest.coinapi.io/v1/exchangerate/{0}/{1}'
    api_key = 'E77D7AF4-98F7-4C99-BDE3-48A983C2473D'
    coins = ('BTC', 'ETH', 'XRP', 'BCH', 'XLM', 'EOS', 'LTC', 'ADA', 'XMR', 'TRX', 'MIOTA', 'DASH', 'ETC')

    def __init__(self, crypto='BTC', currency='UAH'):
        self.crypto = crypto
        self.currency = currency

    def get(self):
        url = self.url.format(self.crypto, self.currency)
        response = requests.get(url, headers={'X-CoinAPI-Key': self.api_key})
        if response.status_code == 200:
            data = json.loads(response.text)
            return data.get('rate')
        return None
