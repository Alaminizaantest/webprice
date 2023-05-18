from flask import Flask, render_template
import ccxt

app = Flask(__name__)

@app.route('/')
def index():
    gateio = ccxt.gateio()
    
    try:
        gateio_markets = gateio.load_markets()
        gateio_spot_markets = {symbol: market for symbol, market in gateio_markets.items() if market['spot'] and market['active']}
        gateio_tickers = gateio.fetch_tickers(list(gateio_spot_markets.keys()))
    except Exception as e:
        return f"Error retrieving data from Gate.io API: {e}"
    
    return render_template('index.html', gateio_tickers=gateio_tickers)

if __name__ == '__main__':
    app.run(debug=True)
