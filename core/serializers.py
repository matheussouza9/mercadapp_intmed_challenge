from django.contrib.auth.models import User
from .models import Market, Item, Cart, ItemCart
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'amount_available')


class ItemCartSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.filter(active=True))

    class Meta:
        model = ItemCart
        fields = ('item', 'amount')


class CartSerializerPost(serializers.ModelSerializer):
    items = ItemCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('market', 'items')

    def validate(self, data):
        market = data['market']
        items = data['items']
        items_to_save = []

        for itemCart in items:
            item = itemCart['item']
            amount = itemCart['amount']

            # it checks if item belongs to the market
            if item.market != market:
                raise serializers.ValidationError(
                    "{} doesn't belong to {}".format(item.name, market.name)
                )

            # it checks if item amount is available in the market
            if amount > item.amount_available:
                raise serializers.ValidationError(
                    "{} {} unit are not available in stock. Only {} unit".format(amount, item.name, item.amount_available)
                )

            items_to_save.append(ItemCart(item=item, amount=amount))

        data['items'] = items_to_save
        return data

    def create(self, validated_data):
        request = self.context['request']
        market = validated_data['market']
        items = validated_data['items']

        cart = Cart.objects.create(market=market, user=request.user)

        for itemCart in items:
            itemCart.cart = cart
            itemCart.save()

        cart.save()

        return cart


class CartSerializerGet(serializers.ModelSerializer):
    market = MarketSerializer()
    items_cart = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ('user', 'items')

    def get_items_cart(self, cart):
        response_obj = []
        for itemCart in cart.itemcart_set.all():
            total_price = itemCart.amount * itemCart.item.price
            response_obj.append({
                'item_cart_id': itemCart.id,
                'item_id': itemCart.item.id,
                'name': itemCart.item.name,
                'unit_price': itemCart.item.price,
                'amount': itemCart.amount,
                'total_price': float(format(total_price, '.2f'))
            })

        return response_obj
