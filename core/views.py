from .models import Market, Cart
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .serializers import MarketSerializer, ItemSerializer, CartSerializerInput, CartSerializerOutput


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
    serializer_class = CartSerializerOutput
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        user = request.user
        carts = user.carts.filter(is_open=True, active=True)
        serializer = CartSerializerOutput(carts, many=True)

        return Response(data=serializer.data)

    def retrieve(self, request, pk=None):
        user = request.user
        cart = user.carts.filter(pk=pk, is_open=True, active=True).get()
        if not cart:
            raise NotFound()

        serializer = CartSerializerOutput(cart)

        return Response(data=serializer.data)

    def create(self, request):
        serializer = CartSerializerInput(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors)

        my_new_cart = serializer.save()
        response_serializer = CartSerializerOutput(my_new_cart)

        return Response(data=response_serializer.data)

    def update(self, request, pk=None):
        user = request.user
        cart = user.carts.filter(pk=pk, is_open=True, active=True).get()
        if not cart:
            raise NotFound()

        serializer = CartSerializerInput(instance=cart, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors)

        my_updated_cart = serializer.save()
        response_serializer = CartSerializerOutput(my_updated_cart)

        return Response(data=response_serializer.data)

    def partial_update(self, request, pk=None):
        raise MethodNotAllowed(request.method)

    def destroy(self, request, pk=None):
        user = request.user
        cart = user.carts.filter(pk=pk, is_open=True, active=True).get()
        if not cart:
            raise NotFound()

        cart.delete()
        serializer = CartSerializerOutput(cart)

        return Response(data=serializer.data)
