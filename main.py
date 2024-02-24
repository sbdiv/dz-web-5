import aiohttp
import asyncio
import argparse

async def fetch_currency_rates(days):
    base_url = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    currency_rates = []

    async with aiohttp.ClientSession() as session:
        for day in range(days):
            date = (datetime.datetime.now() - datetime.timedelta(days=day)).strftime("%d.%m.%Y")
            url = f"{base_url}{date}"

            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = {
                        'date': date,
                        'EUR': {
                            'sale': data['exchangeRate'][0]['saleRate'],
                            'purchase': data['exchangeRate'][0]['purchaseRate']
                        },
                        'USD': {
                            'sale': data['exchangeRate'][1]['saleRate'],
                            'purchase': data['exchangeRate'][1]['purchaseRate']
                        }
                    }
                    currency_rates.append(rates)

    return currency_rates

def print_currency_rates(currency_rates):
    print(currency_rates)

async def main():
    parser = argparse.ArgumentParser(description="Get currency rates from PrivatBank API")
    parser.add_argument("days", type=int, help="Number of days to retrieve currency rates")
    args = parser.parse_args()

    currency_rates = await fetch_currency_rates(args.days)
    print_currency_rates(currency_rates)

if __name__ == "__main__":
    import datetime
    asyncio.run(main())
