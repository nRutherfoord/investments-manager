from django.db import models

# TODO remove this model -> not needed anymore
class Investment(models.Model):
    stock_symbol = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.stock_symbol
    
class InvestmentPlatform(models.Model):
    name = models.CharField(max_length=100)
    accountValue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Trade(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"
    # account = models.ForeignKey("InvestmentAccount", on_delete=models.PROTECT)
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
    closed_at = models.DateTimeField(blank=True,null=True)
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