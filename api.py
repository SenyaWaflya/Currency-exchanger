import requests

url = 'https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/'


def get_exchangerate(banknote, banknote2):
    new_url = url + banknote
    result = requests.get(new_url)
    data = result.json()['conversion_rates'][banknote2]
    return data
