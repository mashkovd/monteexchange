import ssl
import certifi
import json
import aiohttp
from config import WISE_HOST, WISE_TOKEN, PROFILE_ID, BALANCE_ID


async def payment_requests(currency: str, amount: str):
    # You can customize the SSL context as needed
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    url = f"{WISE_HOST}/v1/profiles/{PROFILE_ID}/acquiring/payment-requests"

    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {WISE_TOKEN}'}
    payload = json.dumps({
        "amount": {
            "currency": currency,
            "value": amount
        },
        "balanceId": BALANCE_ID,
        "message": "321",
        "selectedPaymentMethods": [
            "WISE_ACCOUNT",
            "ACCOUNT_DETAILS"
        ]
    })

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context),
            headers=headers) as session:
        async with session.post(url, data=payload) as resp:
            response = await resp.json()
            payment_request_id = response['id']

        url = f"{WISE_HOST}/v1/profiles/{PROFILE_ID}/acquiring/payment-requests/{payment_request_id}/status"
        payload = json.dumps({"status": "PUBLISHED"})
        async with session.put(url, data=payload) as resp:
            response = await resp.json()
            return response['link']


async def rates(source, target: str):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context),
                                     headers={'Authorization': f'Bearer {WISE_TOKEN}'}) as session:
        async with session.get(f'{WISE_HOST}/v1/rates?source={source}&target={target}') as resp:
            rates = await resp.json()
            return rates[0]['rate']

