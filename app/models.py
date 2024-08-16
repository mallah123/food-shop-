from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andra Pradesh', 'Andra Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('U.P', 'U.P'),
    ('M.P', 'M.P'),
    ('Delhi', 'Delhi'),
    ('Maharastra','Maharastra')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices = STATE_CHOICES, max_length=200)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('EN', 'EveningNasta'),
    ('D', 'Dinner')
)   

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=200)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to = 'productimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_signature = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return str(self.id)

    # helps in model template relationship
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price        

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)  

# cfrom django.db import models
# from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    # razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    # razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    # razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    # paid = models.BooleanField(default=False)



class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')


    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price        




