from django.db import models
from django.contrib.auth.models import User


class Market(models.Model):
    name = models.CharField(max_length=250)
    active = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.active = False
        super().save()

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField()
    amount_available = models.IntegerField(default=0)
    market = models.ForeignKey(Market, related_name='items', on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.active = False
        super().save()

    def __str__(self):
        return '{} - {}'.format(self.name, self.market)


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='carts', on_delete=models.DO_NOTHING)
    market = models.ForeignKey(Market, related_name='carts', on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(Item, through='ItemCart', blank=True)
    is_open = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    total = models.FloatField(default=0)

    def __str__(self):
        return '#{} - Owner: {} - Market: {} - Is open: {} - Active: {}'.format(
            self.id, self.user, self.market, self.is_open, self.active
        )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total = self.calculate_total()
        super().save()

    def delete(self, using=None, keep_parents=False):
        self.active = False
        super().save()

    def close(self):
        if self.is_open:
            self.is_open = False
            self.save()

    def calculate_total(self):
        total = 0
        for itemCart in self.itemcart_set.all():
            total += itemCart.item.price * itemCart.amount

        return total

    def set_items_cart_list(self, items_cart):
        # items_cart is a list of ItemCart objects

        # deleting all previous item_cart from this cart
        self.itemcart_set.all().delete()

        for item_cart in items_cart:
            item_cart.cart = self
            item_cart.save()


class ItemCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()


class Order(models.Model):
    market = models.ForeignKey(Market, related_name='orders', on_delete=models.DO_NOTHING)
    cart = models.OneToOneField(Cart, related_name='order', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.DO_NOTHING)
    delivery_address = models.CharField(max_length=500)
    delivery_appointment = models.DateTimeField()
    payment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '#{} - Owner: {} - Market: {} - Paid at {}'.format(
            self.id, self.user, self.market, self.payment_date
        )

    @property
    def total(self):
        return self.cart.total
