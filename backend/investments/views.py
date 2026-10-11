from etoro_api.account_info import get_total_invested
from investments.services import sync_etoro_trades
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from investments.models import Investment, InvestmentPlatform, Trade
from investments.serializer import InvestmentPlatformSerializer, InvestmentsSerializer, TradeSerializer

# Create your views here.

class InvestmentViewSet (viewsets.ModelViewSet):
      queryset = Investment.objects.only("id", "stock_symbol", "value").all()
      serializer_class = InvestmentsSerializer


class InvestmentPlatformViewSet(viewsets.ViewSet):
      queryset = InvestmentPlatform.objects.only("id", "stock_symbol", "value").all()
      serializer_class = InvestmentPlatformSerializer
      
      @action(detail=False, methods=["get"])
      def getEtoroValue(self,request):
            return Response({"total_invested": get_total_invested()})
      

class TradeViewSet(viewsets.ViewSet):
      queryset = Trade.objects.all()
      serializer_class = TradeSerializer
      @action(detail=False, methods=["get"])
      def sync(self, request):
            result = sync_etoro_trades()
            return Response(result)
            