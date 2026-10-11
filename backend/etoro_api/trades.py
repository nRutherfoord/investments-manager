import requests

from etoro_api.doRequest import doRequest
import logging
OPEN_TRADES_ENDPOINT = "https://public-api.etoro.com/api/v1/trading/info/portfolio"
CLOSED_TRADES_ENDPOINT = "/api/v1/trading/info/trade/history"

logger = logging.getLogger(__name__)
def fetch_all_trades():
    try:
        try:
            response = doRequest(OPEN_TRADES_ENDPOINT)
            payload = response.json()
        except requests.RequestException as exc:
            logger.exception("Request to eToro failed")
            raise RuntimeError("Could not fetch account data from eToro") from exc
        except ValueError as exc:
            logger.exception("eToro returned invalid JSON")
            raise RuntimeError("eToro returned an invalid response") from exc
        
        open_positions = response.json()["clientPortfolio"]["positions"]

        return open_positions

    except:
        logging.exception("Failed to fetch or parse eToro trades")
        
