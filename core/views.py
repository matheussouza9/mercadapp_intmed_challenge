from .models import Market, Cart
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .serializers import MarketSerializer, ItemSerializer, CartSerializerPost, CartSerializerGet


class MarketViewSet(ReadOnlyModelViewSet):
    queryset = Market.objects.filter(active=True)
    serializer_class = MarketSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @detail_route(url_path='items', methods=['get'])
    def items(self, request, pk=None):
        market = self.get_object()
        items = market.items.filter(active=True)
        serializer = ItemSerializer(items, many=True)

        return Response(data=serializer.data)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializerGet
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = request.user.cart.filter(is_open=True)
        serializer = CartSerializerGet(queryset, many=True)

        return Response(data=serializer.data)

    def retrieve(self, request, pk=None):
        queryset = request.user.cart.filter(pk=pk, is_open=True)
        if not queryset.exists():
            raise NotFound()

        serializer = CartSerializerGet(queryset, many=True)

        return Response(data=serializer.data)

    def create(self, request):
        serializer = CartSerializerPost(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors)

        my_new_cart = serializer.save()

        response_serializer = CartSerializerGet(my_new_cart)

        return Response(data=response_serializer.data)
