from investments.models import Trade
from etoro_api.trades import fetch_all_trades



def sync_etoro_trades():
    print("Attempting to sync etoro with local db....")
    etoro_trades = fetch_all_trades()
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
            },
        )
        
    created_count += created
    return {"fetched": len(etoro_trades), "created": created_count}
