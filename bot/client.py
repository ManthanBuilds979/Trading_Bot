import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from bot.logging_config import setup_logger

logger = setup_logger()

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def post(self, endpoint: str, params: dict) -> dict:
        signed_params = self._sign(params)
        url = f"{BASE_URL}{endpoint}"

        logger.debug(f"POST {url} | Params: { {k: v for k, v in signed_params.items() if k != 'signature'} }")

        try:
            response = self.session.post(url, data=signed_params, timeout=10)
            data = response.json()
            logger.debug(f"Response [{response.status_code}]: {data}")

            if not response.ok:
                error_msg = data.get("msg", "Unknown API error")
                error_code = data.get("code", response.status_code)
                raise RuntimeError(f"API Error {error_code}: {error_msg}")

            return data

        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Network connection failed.")
            raise
        except RuntimeError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
