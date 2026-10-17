from django.db import models


# TODO remove this model -> not needed anymore
class Investment(models.Model):
    stock_symbol = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.stock_symbol


class InvestmentPlatform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InvestmentPlatformAccount(models.Model):
    platform = models.ForeignKey(
        InvestmentPlatform,
        on_delete=models.CASCADE,
        related_name="investment_platform",
    )
    account_name = models.CharField(max_length=100)


class AccountEquitySnapshot(models.Model):
    account = models.ForeignKey(
        InvestmentPlatformAccount,
        on_delete=models.CASCADE,
        related_name="equity_snapshots",
    )
    available_cash = models.DecimalField(max_digits=18, decimal_places=2)
    total_invested = models.DecimalField(max_digits=18, decimal_places=2)
    unrealized_pnl = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    recorded_at = models.DateTimeField(auto_now_add=True)


class Trade(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    account = models.ForeignKey(
        InvestmentPlatformAccount, 
        on_delete=models.CASCADE, 
        related_name="trades"
    )
    external_id = models.CharField(max_length=128)

    symbol = models.CharField(max_length=32)
    side = models.CharField(
        max_length=8,
        choices=[("BUY", "Buy"), ("SELL", "Sell")],
    )

    quantity = models.DecimalField(max_digits=24, decimal_places=10)
    price = models.DecimalField(max_digits=24, decimal_places=10)
    currency = models.CharField(max_length=3)
    fees = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    executed_at = models.DateTimeField()
    closed_at = models.DateTimeField(blank=True, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)

    # Keep the original API record for debugging or future remapping
    raw_data = models.JSONField(default=dict, blank=True)
    trade_status = models.CharField(
        max_length=6,
        choices=Status.choices,
        default=Status.OPEN,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["external_id"],
                name="unique_trade_per_account",
            )
        ]
