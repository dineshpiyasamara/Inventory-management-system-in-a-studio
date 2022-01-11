from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=[(
        'MALE', 'MALE'), ('FEMALE', 'FEMALE')], null=True, blank=True)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    product_code = models.CharField(primary_key=True, max_length=30)
    category = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.product_code, self.category)


class SellingPrice(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.item, self.selling_price)


class Suppliers(models.Model):
    organization = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.organization


class Purchases(models.Model):
    date = models.DateField(auto_now_add=True)
    qty = models.IntegerField()
    supplier_id = models.ForeignKey(Suppliers, on_delete=CASCADE)
    product_code = models.ForeignKey(Item, on_delete=CASCADE)
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}'.format(self.product_code.product_code, self.supplier_id.organization, self.employee_id.username)


class Customers(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Sales(models.Model):
    date = models.DateField(auto_now_add=True)
    qty = models.IntegerField()
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product_code = models.ForeignKey(Item, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.product_code.product_code, self.employee_id.username)
