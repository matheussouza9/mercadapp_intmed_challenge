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
    user = models.ForeignKey(User, related_name='cart', on_delete=models.DO_NOTHING)
    market = models.ForeignKey(Market, related_name='cart', on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(Item, through='ItemCart', blank=True)
    is_open = models.BooleanField(default=True)
    partial_total = models.FloatField(default=0)

    def close(self):
        if self.is_open:
            self.is_open = False
            self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.partial_total = self.calculate_total()
        super().save()

    def calculate_total(self):
        total = 0
        for itemCart in self.itemcart_set.all():
            total += itemCart.item.price * itemCart.amount

        return total


class ItemCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.DO_NOTHING)
    delivery_address = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def total(self):
        return self.cart.partial_total
