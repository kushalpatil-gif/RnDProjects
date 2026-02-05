import json
from fyers_apiv3 import fyersModel
import fyers_config
import os

cfg = fyers_config.config
access_path = cfg['access_token_path']

def exchange_and_save(redirect_url):
    session = fyersModel.SessionModel(client_id=cfg['API_client_id'], redirect_uri=cfg['redirect_uri'], response_type=cfg['response_type'], state='state', secret_key=cfg['API_secret_key'], grant_type=cfg['grant_type'])
    auth_code = redirect_url[redirect_url.index('auth_code=') + 10:redirect_url.index('&state')]
    session.set_token(auth_code)
    token = session.generate_token()
    access_token = token.get('access_token')
    if access_token:
        info = {'date': __import__('datetime').datetime.today().strftime('%Y-%m-%d'), 'access_token': access_token}
        with open(access_path, 'w') as f:
            json.dump(info, f)
        print('Access token saved to', access_path)
    else:
        print('Failed to obtain access token:', token)

def fetch_quote(symbol):
    if not os.path.exists(access_path):
        print('Access token missing. Run auth flow first.')
        return
    with open(access_path) as f:
        info = json.load(f)
    token = info['access_token']
    client = fyersModel.FyersModel(client_id=cfg['API_client_id'], token=token)
    data = {"symbols": symbol}
    res = client.quotes(data)
    print('Quote response:', res)

if __name__ == '__main__':
    redirect = input('Paste the full redirected URL after login (or leave empty to just fetch quote if token exists): ').strip()
    if redirect:
        exchange_and_save(redirect)
    # demo fetch
    sym = input('Enter symbol to fetch (e.g., NSE:SBIN-EQ) [default NSE:SBIN-EQ]: ').strip() or 'NSE:SBIN-EQ'
    fetch_quote(sym)
