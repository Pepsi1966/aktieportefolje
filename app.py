from flask import Flask, jsonify, send_from_directory
import yfinance as yf
import os

app = Flask(__name__, static_folder='static')

# Valutakurser til DKK (hentes live fra Yahoo Finance)
FX_PAIRS = {
    'EUR': 'EURDKK=X',
    'USD': 'USDDKK=X',
    'GBP': 'GBPDKK=X',
    'SEK': 'SEKDKK=X',
    'NOK': 'NOKDKK=X',
}

def get_fx_rate(currency):
    if currency == 'DKK':
        return 1.0
    symbol = FX_PAIRS.get(currency.upper())
    if not symbol:
        return None
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.last_price
        return round(price, 4) if price else None
    except:
        return None

@app.route('/api/quote/<ticker>')
def quote(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.fast_info
        price = info.last_price
        currency = getattr(info, 'currency', 'DKK') or 'DKK'
        currency = currency.upper()

        # GBp (pence) → GBP
        if currency == 'GBP' and price and price > 500:
            price = price / 100

        fx_rate = get_fx_rate(currency)

        return jsonify({
            'ticker': ticker,
            'price': round(price, 2) if price else None,
            'currency': currency,
            'rate_to_dkk': fx_rate,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quotes')
def quotes_bulk():
    """Hent kurser for alle tre fonde på én gang"""
    tickers = ['MAJVAA.CO', 'STIIAM.CO', 'JREG.DE']
    result = {}
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            info = t.fast_info
            price = info.last_price
            currency = (getattr(info, 'currency', 'DKK') or 'DKK').upper()
            if currency == 'GBP' and price and price > 500:
                price = price / 100
            fx_rate = get_fx_rate(currency)
            result[ticker] = {
                'price': round(price, 2) if price else None,
                'currency': currency,
                'rate_to_dkk': fx_rate,
            }
        except Exception as e:
            result[ticker] = {'error': str(e)}
    return jsonify(result)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
