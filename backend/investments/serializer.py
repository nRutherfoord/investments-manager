from rest_framework import serializers

from investments.models import Investment


class InvestmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ["id", "stock_symbol", "value"]