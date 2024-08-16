from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
# from django.contrib import admin
# from .models import Customer  # Import the Customer model from the same app

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')

# admin.site.register(Customer, CustomerAdmin)

admin.site.register(Product)

admin.site.register(Cart)
admin.site.register(OrderPlaced)
admin.site.register(Payment)
# from django.contrib import admin
from .models import Payment  # Import the Payment model from the same app

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid')
    list_filter = ('paid',)

# admin.site.register(Payment, PaymentAdmin)

