from django.db import models

PAYMENT_BANK = 0
PAYMENT_CHECK = 1
PAYMENT_PAYPAL = 2

PAYMENT_CHOICES = [
    (PAYMENT_BANK, 'Direct Bank Payment'),
    (PAYMENT_CHECK, 'Check Payment'),
    (PAYMENT_PAYPAL, 'Paypal'),
]


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=80)
    price = models.IntegerField()
    description = models.CharField(max_length=280)

    def __str__(self):
        return self.name


# List of pick-up Points of Orders
class Point(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=280)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey('auth.User', null=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=10, null=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=150, null=True)
    point = models.ForeignKey(Point, null=True, on_delete=models.CASCADE)
    notes = models.TextField(max_length=500, null=True)
    active = models.BooleanField(default=True)
    order_date = models.DateField(null=True)
    payment_type = models.IntegerField(choices=PAYMENT_CHOICES, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null=True)


def __str__(self):
    return str(self.order_id)


class OrderItem(models.Model):
    #product = models.ManyToManyField(Product)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)


def __str__(self):
    return str(self.id)



