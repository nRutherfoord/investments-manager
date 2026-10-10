from django.db import models

# Create your models here.

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