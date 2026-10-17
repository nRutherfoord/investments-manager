from etoro_api.account_info import get_total_invested
from investments.services import get_trading_history, get_open_trades, get_account_equity
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from investments.models import Investment, InvestmentPlatform, InvestmentPlatformAccount, Trade
from investments.serializer import InvestmentPlatformAccountSerializer, InvestmentPlatformSerializer, InvestmentsSerializer, TradeSerializer

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
      

class InvestmentPlatformAccountViewSet(viewsets.ModelViewSet):
      queryset = InvestmentPlatformAccount.objects.only("account_name").all()
      serializer_class = InvestmentPlatformAccountSerializer
      
      @action(detail=True, methods=["get"])
      def sync_account_equity(self,request, pk=None):
            account = self.get_object()
            equity = get_account_equity(account)
            return Response({"equity": equity})
      
      
class TradeViewSet(viewsets.ViewSet):
      queryset = Trade.objects.all()
      serializer_class = TradeSerializer
      @action(detail=False, methods=["get"])
      def syncOpen(self, request):
            result = get_open_trades()
            return Response(result)
      
      @action(detail=False, methods=["get"])
      def syncHistoricalTrades(self, request):
            result = get_trading_history()
            return Response(result)
            