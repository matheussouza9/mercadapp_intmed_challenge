from django.contrib.auth.models import User
from .models import Market, Item, Cart, ItemCart
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


class CartSerializerInput(serializers.ModelSerializer):
    items_cart = ItemCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('market', 'items_cart')

    def validate(self, data):
        market = data['market']
        items_cart = data['items_cart']
        items_cart_to_save = []

        for item_cart in items_cart:
            item = item_cart['item']
            amount = item_cart['amount']

            # if item is not active, skip it
            if not item.active:
                raise serializers.ValidationError(
                    "Item {} doesn't exist in stock".format(item.id)
                )

            # it checks if item belongs to the market
            if item.market != market:
                raise serializers.ValidationError(
                    "Item {} - {} doesn't belong to {}".format(item.id, item.name, market.name)
                )

            # it checks if item amount is available in the market
            if amount > item.amount_available:
                raise serializers.ValidationError(
                    "Item {} - {} {} units are not available in stock. Only {} units".format(
                        item.id, amount, item.name, item.amount_available
                    )
                )

            items_cart_to_save.append(ItemCart(item=item, amount=amount))

        data['items_cart'] = items_cart_to_save
        return data

    def create(self, validated_data):
        request = self.context['request']
        market = validated_data['market']
        items_cart = validated_data['items_cart']

        cart = Cart.objects.create(market=market, user=request.user)
        cart.set_items_cart_list(items_cart=items_cart)
        cart.save()

        return cart

    def update(self, instance, validated_data):
        market = validated_data['market']
        items_cart = validated_data['items_cart']

        instance.market = market
        instance.set_items_cart_list(items_cart=items_cart)
        instance.save()

        return instance


class CartSerializerOutput(serializers.ModelSerializer):
    market = MarketSerializer()
    items_cart = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ('user', 'items', 'active')

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
