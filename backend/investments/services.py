from investments.models import Trade
from etoro_api.trades import fetch_all_open_trades, fetch_closed_trades



def get_open_trades():
    print("Attempting to sync etoro with local db....")
    etoro_trades = fetch_all_open_trades()
    created_count = 0 
    for item in etoro_trades:
        _, created = Trade.objects.get_or_create(
            # account=account,
            external_id=item["positionID"],
            defaults={
                "symbol": item["instrumentID"],
                "side": "BUY" if item["isBuy"] else "SELL",
                "quantity": item["units"],
                "price": item["openRate"],
                "currency": "USD",
                "fees": item.get("totalFees", 0),
                "executed_at": item["openDateTime"],
                "raw_data": item,
                "trade_status": Trade.Status.OPEN
            },
        )
        
    created_count += created
    return {"fetched": len(etoro_trades), "created": created_count}



def get_trading_history():
    print("Attempting to sync etoro with local db for trading history....")
    etoro_trades = fetch_closed_trades("2025-11-07T00:00:00Z")
    created_count = 0 
    for item in etoro_trades:
        _, created = Trade.objects.get_or_create(
            # account=account,
            external_id=item["positionId"],
            defaults={
                "symbol": item["instrumentId"],
                "side": "BUY" if item["isBuy"] else "SELL",
                "quantity": item["units"],
                "price": item["openRate"],
                "currency": "USD",
                "fees": item.get("totalFees", 0),
                "executed_at": item["openTimestamp"],
                "closed_at" : item.get("closeTimestamp"),
                "trade_status" : Trade.Status.CLOSED if item.get("closeTimestamp") else Trade.Status.OPEN,
                "raw_data": item,
            },
        )
        
    created_count += created
    return {"fetched": len(etoro_trades), "created": created_count}
