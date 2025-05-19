import json
import ssl
from functools import lru_cache

import aiohttp
import certifi
import toml

from config import BALANCE_ID, PROFILE_ID, WISE_HOST, WISE_TOKEN


async def payment_requests(currency: str, amount: int):
    # You can customize the SSL context as needed
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    url = f"{WISE_HOST}/v1/profiles/{PROFILE_ID}/acquiring/payment-requests"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WISE_TOKEN}",
    }
    payload = json.dumps(
        {
            "amount": {"currency": currency, "value": amount},
            "balanceId": BALANCE_ID,
            "message": "321",
            "selectedPaymentMethods": ["WISE_ACCOUNT", "ACCOUNT_DETAILS"],
        }
    )

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context), headers=headers
    ) as session:
        async with session.post(url, data=payload) as resp:
            response = await resp.json()
            payment_request_id = response["id"]

        url = f"{WISE_HOST}/v1/profiles/{PROFILE_ID}/acquiring/payment-requests/{payment_request_id}/status"
        payload = json.dumps({"status": "PUBLISHED"})
        async with session.put(url, data=payload) as resp:
            response = await resp.json()
            return response["link"]


async def rates(source, target: str):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context),
        headers={"Authorization": f"Bearer {WISE_TOKEN}"},
    ) as session:
        async with session.get(
            f"{WISE_HOST}/v1/rates?source={source}&target={target}"
        ) as resp:
            rates = await resp.json()
            return rates[0]["rate"]


@lru_cache(maxsize=1)
def get_pyproject_version():
    try:
        with open("pyproject.toml", "r") as file:
            pyproject_data = toml.load(file)
            version = pyproject_data["project"]["version"]
            return version
    except FileNotFoundError:
        print("pyproject.toml file not found.")
    except KeyError:
        print("Version not found in pyproject.toml.")


# Example usage
pyproject_version = get_pyproject_version()
