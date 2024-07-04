import requests
import math


def get_exchange_rate(api_key):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/INR'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print("Error fetching exchange rate")
        return 0

    exchange_rate = data['conversion_rates']['USD']
    return exchange_rate


if __name__ == "__main__":
    api_key = '6d47f28acebd699f95158260'
    amount_inr = '8,237'  # Example amount in INR
    amount_inr = int(amount_inr.replace(',', ''))
    exchange_rate = get_exchange_rate(api_key)
    amount_usd = amount_inr * exchange_rate
    amount_usd = int(math.ceil(amount_usd))

    if amount_usd:
        print(f'{exchange_rate} INR is equal to {amount_usd:.2f} USD')
