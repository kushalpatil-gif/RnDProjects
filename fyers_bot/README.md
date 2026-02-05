# Fyers Bot (Auth Helper & Paper Demo)

This folder contains helper scripts to obtain a Fyers access token via OAuth and run a small paper-trade demo.

Steps:
1. Copy `fyers_config.example.py` to `fyers_config.py` and fill your credentials.
2. Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the auth helper to print the auth URL:
   ```bash
   python auth_helper.py
   ```
   Open the printed URL in your browser, complete login (enter OTP & PIN locally), then after redirect copy the full redirect URL from the address bar.
4. Run the paper demo and paste the redirect URL when prompted:
   ```bash
   python paper_demo.py
   ```

Files:
- auth_helper.py — prints the auth URL using your fyers login flow
- paper_demo.py — accepts the redirect URL, exchanges auth_code for access token, saves to access_token_path, fetches a quote
- fyers_config.example.py — example config file
- requirements.txt — dependencies

Security:
- Do not share OTPs or PINs in chat. Run the browser login locally.
- The script saves access token to the path you configure in `fyers_config.py`.

