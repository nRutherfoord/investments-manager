import requests
import logging
from etoro_api.doRequest import doRequest

logger = logging.getLogger(__name__)


def get_calculate_equity():
    url = "https://public-api.etoro.com/api/v1/trading/info/real/pnl"
    try:
        response = doRequest(url)
        payload = response.json()
    except ValueError as exc:
        logger.exception("eToro returned invalid account equity JSON")
        raise RuntimeError("eToro returned an invalid account equity response") from exc
    except requests.RequestException as exc:
        logger.exception("Request to eToro for account equity failed")
        raise RuntimeError("Could not fetch account equity from eToro") from exc

    try:
        data = payload['clientPortfolio']
        # Calculate Available Cash

        credits = data['credit']
        orders_for_open_amount = sum(
            order['amount'] for order in data['ordersForOpen']
            if order['mirrorID'] == 0
        )
        orders_amount = sum(order['amount'] for order in data['orders'])
        available_cash = credits - (orders_for_open_amount + orders_amount)

        # Calculate Total Invested
        positions_amount = sum(pos['amount'] for pos in data['positions'])
        mirrors_positions_amount = sum(
            pos['amount']
            for mirror in data['mirrors']
            for pos in mirror['positions']
        )
        mirrors_adjusted_amount = sum(
            mirror['availableAmount'] - mirror['closedPositionsNetProfit']
            for mirror in data['mirrors']
        )
        external_costs = sum(
            order['totalExternalCosts']
            for order in data['ordersForOpen']
            if order['mirrorID'] == 0
        )
        total_invested = (
            positions_amount + mirrors_positions_amount + mirrors_adjusted_amount
            + orders_for_open_amount + orders_amount + external_costs
        )
        # Calculate Unrealized PnL
        positions_pnl = sum(pos['unrealizedPnL']['pnL'] for pos in data['positions'])
        mirrors_pnl = sum(
            pos['unrealizedPnL']['pnL']
            for mirror in data['mirrors']
            for pos in mirror['positions']
        )

        closed_positions_profit = sum(
            mirror['closedPositionsNetProfit']
            for mirror in data['mirrors']
        )
        unrealized_pnl = positions_pnl + mirrors_pnl + closed_positions_profit
        
        return available_cash, total_invested, unrealized_pnl
    except (KeyError, TypeError) as exc:
        logger.exception("eToro returned malformed account equity data")
        raise RuntimeError("eToro returned an invalid account equity response") from exc


def get_total_invested():
    print("Getting total invested...")
    url = "https://public-api.etoro.com/api/v1/trading/info/real/pnl"
    try:
        response = doRequest(url)
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
