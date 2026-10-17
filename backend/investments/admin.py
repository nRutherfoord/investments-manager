from django.contrib import admin
from investments.models import AccountEquitySnapshot, Investment, InvestmentPlatform, InvestmentPlatformAccount, Trade

admin.site.register(Investment)
admin.site.register(InvestmentPlatform)
admin.site.register(InvestmentPlatformAccount)
admin.site.register(AccountEquitySnapshot)
admin.site.register(Trade)
