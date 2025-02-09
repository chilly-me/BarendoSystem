import base64
import json
import requests


def generate_access_token():
    consumer_key = "hnXn07KKDO9cOzigeuADtvu14uexicrOPS7maxIJRGq8jaDF"
    consumer_secret = "01ajWccXJ8OTAEA5uv3ByJMijdFrnsE9C6D94PocLNDcEZJ7f34o1Z4WZsdbX1b1"

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        encoded_credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers).json()

        if 'access_token' in response:
            return response['access_token']
        else:
            raise Exception("Failed to get access token: " + response['error_description'])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e))