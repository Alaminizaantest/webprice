from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = [
        {'symbol': 'BTC', 'gateio_price': 50000, 'mexc_price': 51000},
        {'symbol': 'ETH', 'gateio_price': 3000, 'mexc_price': 3200},
        {'symbol': 'LTC', 'gateio_price': 150, 'mexc_price': 160}
    ]
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
