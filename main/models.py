import uuid
from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return f'{self.name}-{self.id}'


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

    def display_image(self):
        try:
            image = ProductImages.objects.filter(product_id=self.id)[0]
        except Exception as e:
            raise Exception('no images yet')

        return image.image.url


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.product.name} image'


class BillingAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f'{self.user.username}\'billing address'


class Order(models.Model):
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.DO_NOTHING)
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
