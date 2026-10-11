from django.contrib import admin
from investments.models import Investment, InvestmentPlatform, Trade

admin.site.register(Investment)
admin.site.register(InvestmentPlatform)
admin.site.register(Trade)
