from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL,null=True)
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collections =models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
        ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email =models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_day = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default='B')

    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]

class Order(models.Model):
    PATMENT_STATUS_PENDING='P'
    PATMENT_STATUS_COMPLETE='C'
    PATMENT_STATUS_FAILED='F'
    PAYMENT_STATUS_CHOICES =[
        (PATMENT_STATUS_PENDING,'Pending'),
        (PATMENT_STATUS_COMPLETE,'Complete'),
        (PATMENT_STATUS_FAILED,'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PATMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
