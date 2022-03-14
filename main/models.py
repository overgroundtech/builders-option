import uuid
from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    categories = models.ManyToManyField(Category)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField()
    in_stock = models.IntegerField()
    details = models.TextField()
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return f'{self.name}-{self.id}'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.product.name} image'


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_id = models.CharField(default=uuid.uuid4(), max_length=100)
    total_price = models.FloatField()
    payment = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    made_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.FloatField()
    total_price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product} order item'
