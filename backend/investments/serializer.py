from rest_framework import serializers

from investments.models import Investment, InvestmentPlatform, Trade


class InvestmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ["id", "stock_symbol", "value"] # noqa: RUF012
        
        
class InvestmentPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlatform
        fields = ["id", "name", "accountValue"]  # noqa: RUF012


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        