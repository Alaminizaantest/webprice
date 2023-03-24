from flask import Flask, render_template
import requests
import math

app = Flask(__name__)

@app.route('/')
def binance_data():
    # API endpoint for ticker prices
    ticker_url = 'https://api.binance.com/api/v3/ticker/price'
    # API endpoint for spot exchange information
    info_url = 'https://api.binance.com/api/v3/exchangeInfo'
    # Trading fee as decimal
    trading_fee = 0.001

    # Make the API requests
    ticker_response = requests.get(ticker_url).json()
    info_response = requests.get(info_url).json()

    # Fetch USDT price
    usdt_price = 1.0
    for item in ticker_response:
        if item['symbol'] == 'USDTBUSD':
            usdt_price = float(item['price'])
            break

    # Create a dictionary of asset names for spot trading
    asset_names = {}
    for asset in info_response['symbols']:
        if asset['status'] != 'TRADING':
            continue
        asset_names[asset['symbol']] = {
            'base': asset['baseAsset'],
            'quote': asset['quoteAsset']
        }

    # Create a dictionary to hold the data for each coin
    coins = {}
    for item in ticker_response:
        symbol = item['symbol']
        if symbol not in asset_names:
            continue
        base_asset = asset_names[symbol]['base']
        quote_asset = asset_names[symbol]['quote']
        price = float(item['price'])
        if base_asset not in coins:
            coins[base_asset] = {}
        coins[base_asset][quote_asset] = price

    # Find triangular arbitrage opportunities
    opportunities = []
    for base_asset in coins:
        for quote_asset_1 in coins[base_asset]:
            if quote_asset_1 not in coins:
                continue
            for quote_asset_2 in coins[quote_asset_1]:
                if quote_asset_2 not in coins:
                    continue
                if base_asset in coins[quote_asset_2]:
                    rate_1 = coins[base_asset][quote_asset_1] * (1 - trading_fee)
                    rate_2 = coins[quote_asset_1][quote_asset_2] * (1 - trading_fee)
                    rate_3 = coins[quote_asset_2][base_asset] * (1 - trading_fee)
                    potential_profit = rate_1 * rate_2 * rate_3 - 1
                    opportunity = {
                        'base_asset': base_asset,
                        'quote_asset_1': quote_asset_1,
                        'quote_asset_2': quote_asset_2,
                        'rate_1': rate_1,
                        'rate_2': rate_2,
                        'rate_3': rate_3,
                        'potential_profit': round(potential_profit, 4),
                        'potential_profit_usdt': round(potential_profit * usdt_price, 4)
                    }
                    opportunities.append(opportunity)

    # Sort the opportunities by potential profit
    opportunities = sorted(opportunities, key=lambda x: x['potential_profit'], reverse=True)

    # Find the highest and lowest potential profits
    if opportunities:
        max_profit = opportunities[0]['potential_profit']
    else:
        max_profit = 0
    if opportunities:
        min_profit = opportunities[-1]['potential_profit']
    else:
        min_profit=-10
    # Calculate the number of nearest opportunities to display
    num_opportunities = 10
    if max_profit <= 0:
        num_opportunities = min(num_opportunities, len(opportunities))

    # Create a list of opportunities to display
    display_opportunities = []
    for i in range(num_opportunities):
        opportunity = opportunities[i]
        display_opportunity = {
            'base_asset': opportunity['base_asset'],
            'quote_asset_1': opportunity['quote_asset_1'],
            'quote_asset_2': opportunity['quote_asset_2'],
            'potential_profit': opportunity['potential_profit'],
            'potential_profit_usdt': opportunity['potential_profit_usdt']
        }
        display_opportunities.append(display_opportunity)

    # Render the HTML template with the data
    return render_template('index.html', opportunities=display_opportunities, usdt_price=usdt_price)

if __name__ == '__main__':
    app.run(debug=True)





