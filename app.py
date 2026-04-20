from flask import Flask, jsonify, send_from_directory
import yfinance as yf
import os

app = Flask(__name__, static_folder='static')

FX_PAIRS = {
    'EUR': 'EURDKK=X',
    'USD': 'USDDKK=X',
    'GBP': 'GBPDKK=X',
    'SEK': 'SEKDKK=X',
    'NOK': 'NOKDKK=X',
}

def get_price(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period='5d')
        if hist.empty:
            return None, None
        price = float(hist['Close'].dropna().iloc[-1])
        currency = (t.fast_info.currency or 'DKK').upper()
        return price, currency
    except:
        return None, None

def get_fx_rate(currency):
    if currency == 'DKK':
        return 1.0
    symbol = FX_PAIRS.get(currency.upper())
    if not symbol:
        return None
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period='5d')
        if hist.empty:
            return None
        return round(float(hist['Close'].dropna().iloc[-1]), 4)
    except:
        return None

@app.route('/api/quote/<ticker>')
def quote(ticker):
    try:
        price, currency = get_price(ticker)
        if price is None:
            return jsonify({'error': 'Kurs ikke fundet'}), 404

        if currency == 'GBP' and price > 500:
            price = price / 100

        fx_rate = get_fx_rate(currency)

        return jsonify({
            'ticker': ticker,
            'price': round(price, 2),
            'currency': currency,
            'rate_to_dkk': fx_rate,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
