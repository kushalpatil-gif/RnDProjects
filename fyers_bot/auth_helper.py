from fyers_apiv3 import fyersModel
import fyers_config

def main():
    cfg = fyers_config.config
    session = fyersModel.SessionModel(client_id=cfg['API_client_id'], redirect_uri=cfg['redirect_uri'], response_type=cfg['response_type'], state='state', secret_key=cfg['API_secret_key'], grant_type=cfg['grant_type'])
    url = session.generate_authcode()
    print('OPEN THIS URL IN YOUR BROWSER:')
    print(url)
    print('\nAfter login and OTP/PIN, you will be redirected to a URL. Copy the full redirected URL and run `python paper_demo.py` and paste it when prompted.')

if __name__ == '__main__':
    main()
