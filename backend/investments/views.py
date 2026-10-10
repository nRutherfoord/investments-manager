from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from investments.models import Investment
from investments.serializer import InvestmentsSerializer
from investments.services import get_instrumentId_fromTickerSymbol

# Create your views here.

class InvestmentViewSet (viewsets.ModelViewSet):
      queryset = Investment.objects.only("id", "stock_symbol", "value").all()
      serializer_class = InvestmentsSerializer
      
      @action(detail=True, methods=["get"])
      def get_investment(self, request, pk=None):
          instrument = get_instrumentId_fromTickerSymbol(pk)
          return Response({"instrument": instrument})