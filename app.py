from flask import Flask, render_template
import ccxt

app = Flask(__name__)

@app.route('/')
def index():
    gateio = ccxt.gateio()
    mexc_global = ccxt.mexc()

    try:
        gateio_markets = gateio.load_markets()
        gateio_spot_markets = {symbol: market for symbol, market in gateio_markets.items() if market['spot'] and market['active']}
        gateio_tickers = gateio.fetch_tickers(list(gateio_spot_markets.keys()))
        print("Gate.io data:", gateio_tickers)
    except Exception as e:
        print("Error retrieving data from Gate.io API:", e)
        gateio_tickers = {}

    return render_template('index.html', gateio_data=gateio_tickers)

if __name__ == '__main__':
    app.run(debug=True)
