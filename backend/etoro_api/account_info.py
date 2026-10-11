import requests
import logging
from etoro_api.doRequest import doRequest

logger = logging.getLogger(__name__)
def get_total_invested():
    print("Getting total invested...")
    try:
        response = doRequest("https://public-api.etoro.com/api/v1/trading/info/real/pnl")
        payload = response.json()
    except requests.RequestException as exc:
        logger.exception("Request to eToro failed")
        raise RuntimeError("Could not fetch account data from eToro") from exc
    except ValueError as exc:
        logger.exception("eToro returned invalid JSON")
        raise RuntimeError("eToro returned an invalid response") from exc
  
    if response.status_code == 200:
        try:
            data = response.json()["clientPortfolio"]

            # Sum all position amounts
            positions_amount = sum(pos["amount"] for pos in data["positions"])
            # Sum all mirror position amounts and adjusted available amounts
            mirrors_positions_amount = sum(
                pos["amount"]
                for mirror in data["mirrors"]
                for pos in mirror["positions"]
            )
            mirrors_adjusted_amount = sum(
                mirror["availableAmount"] - mirror["closedPositionsNetProfit"]
                for mirror in data["mirrors"]
            )

            # Sum manual pending orders (mirrorID = 0)
            orders_for_open_amount = sum(
                order["amount"]
                for order in data["ordersForOpen"]
                if order["mirrorID"] == 0
            )

            # Sum all orders
            orders_amount = sum(order["amount"] for order in data["orders"])

            # Sum external costs for manual pending orders
            external_costs = sum(
                order["totalExternalCosts"]
                for order in data["ordersForOpen"]
                if order["mirrorID"] == 0
            )

            total_invested = (
                positions_amount
                + mirrors_positions_amount
                + mirrors_adjusted_amount
                + orders_for_open_amount
                + orders_amount
                + external_costs
            )

            print(f"Total Invested: {total_invested}")

            return total_invested

        except Exception as e:
            error_type = type(e).__name__
            print("An exception occured", error_type)

    else:
        print(f"Error: {response.status_code}")
