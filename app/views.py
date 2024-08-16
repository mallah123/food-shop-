from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay
from django.conf import settings
from django.core.mail import send_mail





# @method_decorator(login_required, name='dispatch')
class ProductView(View):
    def get(self, request):
        totalitem = 0
        Breakfast = Product.objects.filter(category='B')
        Lunch = Product.objects.filter(category='L')
        EveningNasta = Product.objects.filter(category='EN')
        Dinner = Product.objects.filter(category='D')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        context = {'Breakfast': Breakfast,
                   'Lunch': Lunch, 'EveningNasta': EveningNasta, 'Dinner':Dinner, 'totalitem': totalitem}
        return render(request, 'app/home.html', context)


# @method_decorator(login_required, name='dispatch')
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(id=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('showcart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        # list-comprehension
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem': totalitem})
        else:
            return render(request, 'app/emptycart.html', {'totalitem': totalitem})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']

        # using get to extract single object
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        # list-comprehension
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
    
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        try:
            # Using get to extract single object
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            
            if c.quantity > 1:
                c.quantity -= 1
                c.save()

                amount = 0.0
                shipping_amount = 70.0

                # Fetch the updated cart products for the user
                cart_products = Cart.objects.filter(user=request.user)

                for p in cart_products:
                    tempamount = p.quantity * p.product.discounted_price
                    amount += tempamount

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': amount + shipping_amount
                }
            else:
                data = {
                    'quantity': c.quantity,
                    'amount': 0.0,
                    'totalamount': 0.0
                }
        except Cart.DoesNotExist:
            data = {
                'error': 'Product not found in cart'
            }

        return JsonResponse(data)



from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def removeFromCart(request, cid):
    try:
        Cart.objects.get(id=cid).delete()
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart item does not exist'}, status=404)
    return redirect("/viewcart")

# def buy_now(request):
#     return render(request, 'app/buynow.html')


def buy_now(request):
    return render(request, 'app/buynow.html')


# def profile(request):
#     return render(request, 'app/profile.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


@login_required
def lunch(request, data=None):
    if data == None:
        lunch = Product.objects.filter(category='l')
    elif data == 'panner' or data == 'chicken':
        lunch = Product.objects.filter(category='l').filter(brand=data)
    elif data == 'above':
        lunch = Product.objects.filter(
            category='l').filter(discounted_price__gt=50000)
    elif data == 'below':
        lunch = Product.objects.filter(
            category='l').filter(discounted_price__lt=50000)

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/lunch.html', {'lunch': lunch, 'totalitem': totalitem})


@login_required
def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.all().filter(category='M')
    elif data == 'Apple' or data == 'Oppo':
        mobile = Product.objects.all().filter(category='M').filter(brand=data)
    elif data == 'above':
        mobile = Product.objects.all().filter(
            category='M').filter(discounted_price__gte=50000)
    elif data == 'below':
        mobile = Product.objects.all().filter(
            category='M').filter(discounted_price__lt=50000)

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/mobile.html', {'mobile': mobile, 'totalitem': totalitem})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product:
        for p in cart_product:
            tempamount = int (p.quantity * p.product.discounted_price)
            amount += tempamount

        totalamount = amount + int(shipping_amount)
    # this new line 
        # client = razorpay.client(auth = (settings.KEY, settings.SECRET))
        # Payment = client.order.create({'amount':Cart.objects})
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        
        Payment = client.order.create({'amount' : totalamount ,'currency': 'INR', 'payment_capture': 1 })
        # # context = {'add':Cart.objects,'curreny'}
        # Cart.objects.razor_pay_order_id= Payment['id']
        # Cart.objects.save()
        # print('*******')
        print(Payment)
        # print('*******')

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem, 'Payment': Payment})
    


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulations Profile Updated Successfully!!')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})


def search(request):
    # here 'search' is name in input tag in base.html
    data = request.GET['search']
    
    if (data.lower()) == 'mobile':
        return redirect('mobile')
    elif data.lower() == 'laptop':
        return redirect('laptop')
    else:
        return redirect('home')        



# views.py

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def custom_logout(request):
    # Additional logic you want to perform before logging out
    messages.success(request, 'You have been successfully logged out.')  # Example: Display a logout message
    logout(request)
    # Your custom logic here, if needed
    return redirect('login')  # Redirect to the 'login' URL after logout





# from decimal import Decimal

# def checkout(request):
#     # Retrieve user's orders
#     orders = Order.objects.filter(uid=request.user.id)
#     total_amount = Decimal(0)

#     # Calculate the total amount
#     for order_item in orders:
#         total_amount += Decimal(order_item.pid.price) * order_item.quantity

#     # Multiply by 100 outside the loop
#     total_amount *= 100

#     # Create Razorpay payment order
#     client = razorpay.Client(auth=("rzp_test_96Z24vMDhZdMqV", "4jYsYDnTLb14giLL9PB7foGm"))
#     data = {"amount": int(total_amount), "currency": "INR", "receipt": order_item.order_id}

#     try:
#         payment = client.order.create(data=data)

#         # Clear the user's cart after successful payment
#         for order_item in orders:
#             order_item.delete()

#         context = {"payment": payment}
#         return render(request, "pay.html", context)

#     except Exception as e:
#         # Handle the exception, log it, and inform the user
#         print(f"Error creating Razorpay payment: {e}")
#         # Redirect to an error page
#         return redirect("error_page")
#     return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem, 'Payment': Payment})


# from django.shortcuts import render
# from django.conf import settings
# from .models import Customer, Cart
# import razorpay

# @login_required
# def checkout(request):
#     user = request.user
#     add = Customer.objects.filter(user=user)
#     cart_items = Cart.objects.filter(user=user)
#     amount = 0.0
#     shipping_amount = 70.0
#     totalamount = 0.0
#     totalitem = 0
#     razorpay_order_id = None

#     cart_product = Cart.objects.filter(user=request.user)

#     if cart_product.exists():
#         for p in cart_product:
#             tempamount = p.quantity * p.product.discounted_price
#             amount += tempamount

#         totalamount = amount + shipping_amount
#         totalitem = len(cart_product)

#         client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
#         payment_data = {
#             'amount': int(totalamount * 100),  # Razorpay amount is in paisa, so multiply by 100
#             'currency': 'INR',
#             'payment_capture': 1,
#         }

#         payment = client.order.create(data=payment_data)

#         razorpay_order_id = payment['id']
#         for item in cart_product:
#             item.razorpay_order_id = razorpay_order_id
#             item.save()

#     return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem, 'razorpay_order_id': razorpay_order_id})



# app/views.py

# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Customer, Cart
# from django.conf import settings
# import razorpay

# @login_required
# def checkout(request):
#     user = request.user

#     try:
#         add = get_object_or_404(Customer, user=user)
#     except Customer.DoesNotExist:
#         add = None  # Handle the case where the customer does not exist

#     cart_items = Cart.objects.filter(user=user)
#     amount = 0.0
#     shipping_amount = 70.0
#     totalamount = 0.0
#     totalitem = 0
#     razorpay_order_id = None

#     cart_product = Cart.objects.filter(user=request.user)

#     if cart_product.exists():
#         for p in cart_product:
#             tempamount = p.quantity * p.product.discounted_price
#             amount += tempamount

#         totalamount = amount + shipping_amount
#         totalitem = len(cart_product)

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
#         payment_data = {
#             'amount': int(totalamount * 100),
#             'currency': 'INR',
#             'payment_capture': 1,
#         }

#         payment = client.order.create(data=payment_data)

#         razorpay_order_id = payment['id']
#         for item in cart_product:
#             item.razorpay_order_id = razorpay_order_id
#             item.save()

#     return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem, 'razorpay_order_id': razorpay_order_id})

   

                
# def pay(request):
#     order = order.objects.filter(uid = request.user.id)
#     sum = 0
#     for i in order:
#         sum=sum+i.pid.price*i.quantity
#         oid = i.order_id

#     # sum=sum*100

#     client = razorpay.Client(auth=("rzp_test_w6zCvVY3Omwuwl", "jqrfoaHf126PYrL8JYuIJvbI"))
#     data = { "amount": sum, "currency": "INR", "receipt": oid }
#     payment = client.order.create(data=data)
#     print(payment)
#     context={}
#     context['payment']=payment
#     return render(request,"pay.html",context)
           
         
    
def sendusermail(request):
    msg = "Order placed successfully"
    send_mail(
    "Ekart Order",
    msg,
    "mallahnilesh123@gmail.com",
    ["mallahnilesh123@gmail.com"],
    fail_silently=False,
    )
    return redirect("/")  

        