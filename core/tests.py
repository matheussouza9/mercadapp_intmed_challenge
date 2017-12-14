import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Market, Item, Cart, Order
from .serializers import MarketSerializer, ItemSerializer, CartSerializerOutput


class CoreTests(APITestCase):
    def setUp(self):
        user1 = User(username='user1')
        user1.set_password('user1')
        user1.save()

        user2 = User(username='user2')
        user2.set_password('user2')
        user2.save()

        market1 = Market.objects.create(name='Skina')
        litrao = Item.objects.create(name='Litrão', market=market1, amount_available=200, price=6.99)
        _600 = Item.objects.create(name='600', market=market1, amount_available=300, price=4.99)
        _300 = Item.objects.create(name='300', market=market1, amount_available=250, price=2.99, active=False)

        market2 = Market.objects.create(name='Dinal')
        arroz = Item.objects.create(name='Arroz', market=market2, amount_available=55, price=3.5)
        feijao = Item.objects.create(name='Feijão', market=market2, amount_available=60, price=3.9)

        market3 = Market.objects.create(name='Pinheiro')
        sushi = Item.objects.create(name='Sushi combo', market=market3, amount_available=15, price=29.99)
        shoyu = Item.objects.create(name='Molho shoyu', market=market3, amount_available=40, price=4.2)

        self.cart_valid_payload = {
            'market': market1.id,
            'items_cart': [
                {
                    'item': litrao.id,
                    'amount': 5
                },
                {
                    'item': _600.id,
                    'amount': 10
                }
            ]
        }

        self.cart_inactive_item = {
            'market': market1.id,
            'items_cart': [
                {
                    'item': litrao.id,
                    'amount': 5
                },
                {
                    'item': _300.id,
                    'amount': 10
                }
            ]
        }

        self.cart_item_amount_exceeded = {
            'market': market1.id,
            'items_cart': [
                {
                    'item': litrao.id,
                    'amount': 300
                },
                {
                    'item': _600.id,
                    'amount': 10
                }
            ]
        }

        self.cart_item_from_another_market = {
            'market': market2.id,
            'items_cart': [
                {
                    'item': litrao.id,
                    'amount': 5
                },
                {
                    'item': _600.id,
                    'amount': 10
                }
            ]
        }

    def test_list_markets(self):
        markets = Market.objects.filter(active=True)
        serializer = MarketSerializer(markets, many=True)

        self.client.login(username='user1', password='user1')
        url = reverse('markets-list')

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_not_list_inactive_markets(self):
        Market.objects.create(name='Zé do Amâncio', active=False)
        active_markets = Market.objects.filter(active=True)
        serializer = MarketSerializer(active_markets, many=True)

        self.client.login(username='user1', password='user1')
        url = reverse('markets-list')

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_list_items_from_market(self):
        market = Market.objects.get(name='Dinal')
        items = market.items.filter(active=True)
        serializer = ItemSerializer(items, many=True)

        self.client.login(username='user1', password='user1')
        url = "/api/markets/{}/items/".format(market.id)

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_not_list_inactive_items_from_market(self):
        market = Market.objects.get(name='Skina')
        active_items = market.items.filter(active=True)
        serializer = ItemSerializer(active_items, many=True)

        self.client.login(username='user1', password='user1')
        url = "/api/markets/{}/items/".format(market.id)

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_create_valid_cart(self):
        self.client.login(username='user1', password='user1')
        url = '/api/carts/'

        response = self.client.post(url, json.dumps(self.cart_valid_payload), content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        cart = Cart.objects.get(pk=response.data['id'])
        serializer = CartSerializerOutput(cart)

        self.assertEquals(response.data, serializer.data)

    def test_create_cart_item_amount_exceeded(self):
        self.client.login(username='user1', password='user1')
        url = '/api/carts/'

        response = self.client.post(url, json.dumps(self.cart_item_amount_exceeded), content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cart_item_from_another_market(self):
        self.client.login(username='user1', password='user1')
        url = '/api/carts/'

        response = self.client.post(url, json.dumps(self.cart_item_from_another_market), content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cart_inactive_item(self):
        self.client.login(username='user1', password='user1')
        url = '/api/carts/'

        response = self.client.post(url, json.dumps(self.cart_inactive_item), content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
