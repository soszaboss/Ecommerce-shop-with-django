import json
from base64 import urlsafe_b64encode, b64encode
import environ
import requests
env = environ.Env()
environ.Env.read_env()

PAYPAL_CLIENT_ID = env("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = env("PAYPAL_CLIENT_SECRET")

def base64url(string):
    import json
    url = json.dumps(string).encode('utf-8')
    return str(urlsafe_b64encode(url), encoding='utf-8')

def get_auth_assertion_value(client_id, seller_payer_id):
    HEADER = {
        "alg": "none"
    }
    PAYLOAD = {
        "iss": client_id,
        "payer_id": seller_payer_id
    }
    encodedHeader = base64url(HEADER)
    encodedPayload = base64url(PAYLOAD)

    return f'{encodedHeader}.{encodedPayload}.'

#######################################################################server.js###################################################################################

BASE = "https://api-m.sandbox.paypal.com"
BN_CODE = env('BN_CODE')
def generate_access_token(client_id=PAYPAL_CLIENT_ID, client_secret=PAYPAL_CLIENT_ID):
    try:
        if (not client_id or not client_secret):
            raise ("MISSING_API_CREDENTIALS")
        AUTH = b64encode((f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}").encode()).decode()
        headers = {
            'Authorization' : f'Basic {AUTH}',
        }
        RESPONSE = requests.post(f"{BASE}/v1/oauth2/token", headers=headers, data={'grant_type': 'client_credentials'})
        if RESPONSE.status_code == 200:
            DATA = RESPONSE.json()
            return DATA['access_token']
        else:
            raise Exception(RESPONSE.text)
    except Exception as e:
        raise Exception(e)


# print(generate_access_token())

def handle_response(response):
    try:
        response.raise_for_status()  # Cela lèvera une exception pour les codes d'état HTTP 4xx/5xx
        json_response = response.json()
        return {
          'response': json_response,
          'http_status_code': response.status_code
        }
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6+
        print(response.text)  # Affiche le corps de la réponse qui peut contenir des détails sur l'erreur
    except Exception as e:
        print(f"An error occurred: {e}")


def create_order():
    print(f"shopping cart information passed from the frontend createOrder() callback")#: {cart}")
    clt_id="ATT2-zxtv5TV68k6fnXyxTAK4_wgdywE85Hnj6gYfbYsNBLRQhZBaNW_-k_R9LQRoq8yZ-Dvtm_cWJmG"
    clt_scrt="ECkBAR_WyeTq2BAA2YsecRFuihQ1_r_h6r-2aYJB70LyroLcYSz3sLt-DNEjcIM1hRua-0s5VHvQG4CO"
    accessToken = generate_access_token(client_id=clt_id, client_secret=clt_scrt)
    # iss = "ATT2-zxtv5TV68k6fnXyxTAK4_wgdywE85Hnj6gYfbYsNBLRQhZBaNW_-k_R9LQRoq8yZ-Dvtm_cWJmG"
    # payer_id = "LKRKDQ7MRWZ8C"
    # jwt = get_auth_assertion_value(client_id=iss, seller_payer_id=payer_id)
    url = f"{BASE}/v2/checkout/orders"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}',
        # 'PayPal-Request-Id': 'LKRKDQ7MRWZ8C',
        # 'PayPal - Partner - Attribution - Id': BN_CODE,
        # 'PayPal - Auth - Assertion': jwt,
    }

    # data = '{ "intent": "CAPTURE", "purchase_units": [ { "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b", "amount": { "currency_code": "USD", "value": "100.00" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "shipping_preference": "SET_PROVIDED_ADDRESS", "user_action": "PAY_NOW", "return_url": "https://example.com/returnUrl", "cancel_url": "https://example.com/cancelUrl" } } } }'
    payload = json.dumps({"intent": "CAPTURE","purchase_units": [{"amount":{"currency_code": "USD","value": "100.00", },}, ], })
    response = requests.post(url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)
    return handle_response(response)

def capture_order(order_id):
    accessToken = generate_access_token()
    url = f"{BASE}/v2/checkout/orders/{order_id}/capture"  # Removed the trailing apostrophe
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}',
    }
    response = requests.post(url, headers=headers)
    print(response)
    return handle_response(response)

# order_id = create_order()['response']['id']
# print(order_id)
print(capture_order("5PR019385M3167048"))
