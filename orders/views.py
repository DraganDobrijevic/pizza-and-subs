from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from  .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Regular_Pizza, Sicilian_Pizza, Topping, Sub, Subs_Extra, Pasta, Salad, Dinner_Platter, Cart, All_Order
from django.db.models import Sum
import datetime


def index(request):
    return render(request, "orders/home.html")

    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "orders/home.html", context)

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login {username} :)')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'orders/register.html', {'form': form})
   

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "orders/login.html", {"message": "Please enter a correct username and password. Note that both fields may be case-sensitive."})
    else:
        return render(request, "orders/login.html")

def logout_view(request):
    logout(request)
    return render(request, "orders/home.html", {"message": "You have been logged out."})

def home(request):
    return render(request, "orders/home.html")

@login_required
def orders(request):
    all_orders = All_Order.objects.all()
    context = {
        "all_orders": all_orders
    }
    return render(request, "orders/orders.html", context)

@login_required
def my_orders(request):
    my_orders = All_Order.objects.all().filter(buyer_name=request.user.username)
    context = {
        "my_orders": my_orders
    }
    return render(request, "orders/my_orders.html", context)

@login_required
def menu(request):
    context = {
        "r_pizza": Regular_Pizza.objects.all(),
        "s_pizza": Sicilian_Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Subs_Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_Platter.objects.all(),
        "hide": False
    }
    return render(request, "orders/menu.html", context)

@login_required
def cart(request):
    if request.method == 'POST':
        name = request.session.get('name')
        if name == "Regular Pizza" or name == "Sicilian Pizza":
            click_id = request.session.get('click_id')
            type_p = request.session.get('type')
            size = request.POST.get('size')
            topp_num = request.session.get('topp_num')
            toppings = request.POST.getlist('toppings')
            if (topp_num != len(toppings)) or size == None:
                context = {
                    "r_pizza": Regular_Pizza.objects.all(),
                    "s_pizza": Sicilian_Pizza.objects.all(),
                    "toppings": Topping.objects.all(),
                    "subs": Sub.objects.all(),
                    "extras": Subs_Extra.objects.all(),
                    "pastas": Pasta.objects.all(),
                    "salads": Salad.objects.all(),
                    "platters": Dinner_Platter.objects.all(),
                    "message": f"Select size and { topp_num } toppings!",
                    "hide": False
                }
                return render(request, "orders/menu.html", context)
            if name == "Regular Pizza":
                row = Regular_Pizza.objects.get(pk=click_id)
                if size == "small":
                    price = row.small
                else:
                    price = row.large
            if name == "Sicilian Pizza":
                row = Sicilian_Pizza.objects.get(pk=click_id)
                if size == "small":
                    price = row.small
                else:
                    price = row.large

            cart_obj = Cart(buyer_name=request.user.username, name=name, type_p=type_p, size=size, toppings=", ".join(toppings), price=price)
            cart_obj.save()

            get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
            total = Cart.objects.all().filter(buyer_name=request.user.username).aggregate(Sum('price'))
            total = round(total['price__sum'], 2)
            
            context = {
                "name": name,
                "type_p": type_p,
                "size": size,
                "toppings": toppings,
                "price": price,
                "obj": get_obj,
                "total": total    
            }

            return render(request, "orders/cart.html", context)

        elif name == "Sub":
            click_id = request.session.get('click_id')
            type_p = request.session.get('type')
            one_size = request.session.get('one_size')
            if one_size == True:
                size = "large"
            else:
                size = request.POST.get('size')
            toppings = request.POST.getlist('extra')
            if size == None:
                context = {
                    "r_pizza": Regular_Pizza.objects.all(),
                    "s_pizza": Sicilian_Pizza.objects.all(),
                    "toppings": Topping.objects.all(),
                    "subs": Sub.objects.all(),
                    "extras": Subs_Extra.objects.all(),
                    "pastas": Pasta.objects.all(),
                    "salads": Salad.objects.all(),
                    "platters": Dinner_Platter.objects.all(),
                    "message": "Select size!",
                    "hide": False
                }

                return render(request, "orders/menu.html", context)
                
            row = Sub.objects.get(pk=click_id)
            if size == "small":
                price = row.small
            else:
                price = row.large

            for topping in toppings:
                print(topping)
                topp_obj = Subs_Extra.objects.get(name=topping)
                topp_price = topp_obj.price
                price = price + topp_price

            cart_obj = Cart(buyer_name=request.user.username, name=name, type_p=type_p, size=size, toppings=", ".join(toppings), price=price)
            cart_obj.save()

            get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
            total = Cart.objects.all().filter(buyer_name=request.user.username).aggregate(Sum('price'))
            total = round(total['price__sum'], 2)

            context = {
                "name": name,
                "type_p": type_p,
                "size": size,
                "toppings": toppings,
                "price": price,
                "obj": get_obj,
                "total": total    
            }

            return render(request, "orders/cart.html", context)

        elif name == "Pasta" or name == "Salad":
            click_id = request.session.get('click_id')
            type_p = request.session.get('type')
                
            if name == "Pasta":
                row = Pasta.objects.get(pk=click_id)
                price = row.price
            else:
                row = Salad.objects.get(pk=click_id)
                price = row.price

            cart_obj = Cart(buyer_name=request.user.username, name=name, type_p=type_p, price=price)
            cart_obj.save()

            get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
            total = Cart.objects.all().filter(buyer_name=request.user.username).aggregate(Sum('price'))
            total = round(total['price__sum'], 2)
            
            context = {
                "name": name,
                "type_p": type_p,
                "price": price,
                "obj": get_obj,
                "total": total   
            }

            return render(request, "orders/cart.html", context)

        elif name == "Dinner Platter":
            click_id = request.session.get('click_id')
            type_p = request.session.get('type')
            size = request.POST.get('size')

            if size == None:
                context = {
                    "r_pizza": Regular_Pizza.objects.all(),
                    "s_pizza": Sicilian_Pizza.objects.all(),
                    "toppings": Topping.objects.all(),
                    "subs": Sub.objects.all(),
                    "extras": Subs_Extra.objects.all(),
                    "pastas": Pasta.objects.all(),
                    "salads": Salad.objects.all(),
                    "platters": Dinner_Platter.objects.all(),
                    "message": "Select size!",
                    "hide": False
                }

                return render(request, "orders/menu.html", context)
                
            row = Dinner_Platter.objects.get(pk=click_id)
            if size == "small":
                price = row.small
            else:
                price = row.large

            cart_obj = Cart(buyer_name=request.user.username, name=name, type_p=type_p, size=size, price=price)
            cart_obj.save()
            
            get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
            total = Cart.objects.all().filter(buyer_name=request.user.username).aggregate(Sum('price'))
            total = round(total['price__sum'], 2)
            
            context = {
                "name": name,
                "type_p": type_p,
                "size": size,
                "price": price,  
                "obj": get_obj,
                "total": total  
            }

            return render(request, "orders/cart.html", context)

    else:
        get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
        n = len(get_obj)
        name = []
        type_p = []
        size = []
        toppings = []
        price = []

        for i in range(n):
            name.append(get_obj[i].name)
            type_p.append(get_obj[i].type_p)
            size.append(get_obj[i].size)
            toppings.append(get_obj[i].toppings)
            price.append(get_obj[i].price)

        total = Cart.objects.all().filter(buyer_name=request.user.username).aggregate(Sum('price'))
        if total['price__sum'] is None:
            total = 0.0
        else:
            total = round(total['price__sum'], 2)
        
        context = {
                "name": name,
                "type_p": type_p,
                "size": size,
                "toppings": toppings,
                "price": price,  
                "x": range(n),
                "obj": get_obj,
                "total": total
            }

        return render(request, "orders/cart.html", context) 
    
@login_required
def regular_pizza(request, pizza_id):
    try:
        name = Regular_Pizza.objects.get(pk=pizza_id)
        if name:
            request.session['click_id'] = name.id
            request.session['name'] = "Regular Pizza"
            request.session['type'] = name.name
            request.session['topp_num'] = name.topp_num
    except Regular_Pizza.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No pizza"})

    context = {
        "r_pizza": Regular_Pizza.objects.all(),
        "s_pizza": Sicilian_Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Subs_Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_Platter.objects.all(),
        "click": name,
        "food": 'pizza',
        "pizza": 'regular',
        "hide": True,
        "topp_num": name.topp_num
    }

    return render(request, "orders/menu.html", context)


@login_required
def sicilian_pizza(request, pizza_id):
    try:
        name = Sicilian_Pizza.objects.get(pk=pizza_id)
        request.session['click_id'] = name.id
        request.session['name'] = "Sicilian Pizza"
        request.session['type'] = name.name
        request.session['topp_num'] = name.topp_num
    except Regular_Pizza.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No pizza"})

    context = {
        "r_pizza": Regular_Pizza.objects.all(),
        "s_pizza": Sicilian_Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Subs_Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_Platter.objects.all(),
        "click": name,
        "food": 'pizza',
        "pizza": 'sicilian',
        "hide": True,
        "topp_num": name.topp_num
    }

    return render(request, "orders/menu.html", context)


@login_required
def subs(request, sub_id):
    try:
        name = Sub.objects.get(pk=sub_id)
        request.session['click_id'] = name.id
        request.session['name'] = "Sub"
        request.session['type'] = name.name
        request.session['one_size'] = name.one_size
    except Sub.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No subs"})

    context = {
        "r_pizza": Regular_Pizza.objects.all(),
        "s_pizza": Sicilian_Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Subs_Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_Platter.objects.all(),
        "click": name,
        "food": 'subs',
        "hide": True,
        "s_toppings": name.toppings.all,
        "one_size": name.one_size
    }
    
    return render(request, "orders/menu.html", context)


@login_required
def pasta(request, pasta_id):
    try:
        name = Pasta.objects.get(pk=pasta_id)
        request.session['click_id'] = name.id
        request.session['name'] = "Pasta"
        request.session['type'] = name.name
    except Pasta.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No pasta"})

    context = {
        "r_pizza": Regular_Pizza.objects.all(),
        "s_pizza": Sicilian_Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Subs_Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_Platter.objects.all(),
        "click": name,
        "food": 'pasta',
        "hide": True,
        "select": 0
    }
    return render(request, "orders/menu.html", context)

@login_required
def salad(request, salad_id):
    try:
        name = Salad.objects.get(pk=salad_id)
        request.session['click_id'] = name.id
        request.session['name'] = "Salad"
        request.session['type'] = name.name
    except Salad.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No salad"})

    context = {
        "r_pizza": Regular_Pizza.objects.all(),
        "s_pizza": Sicilian_Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Subs_Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_Platter.objects.all(),
        "click": name,
        "food": 'salad',
        "hide": True,
        "select": 0
    }
    return render(request, "orders/menu.html", context)

@login_required
def platters(request, platter_id):
    try:
        name = Dinner_Platter.objects.get(pk=platter_id)
        request.session['click_id'] = name.id
        request.session['name'] = "Dinner Platter"
        request.session['type'] = name.name
    except Dinner_Platter.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No dinner platter"})

    context = {
        "r_pizza": Regular_Pizza.objects.all(),
        "s_pizza": Sicilian_Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Subs_Extra.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_Platter.objects.all(),
        "click": name,
        "food": 'platter',
        "hide": True,
        "select": 0
    }
    return render(request, "orders/menu.html", context)

@login_required
def delete(request, item_id):
    try:
        get_item = Cart.objects.get(pk=item_id)
        get_item.delete()
        
    except Cart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "Error"})

    get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
    
    if not get_obj:
        total = 0.0  
    else:
        total = Cart.objects.all().filter(buyer_name=request.user.username).aggregate(Sum('price'))
        total = round(total['price__sum'], 2)

    context = {
        "obj": get_obj,
        "total": total
    }

    return render(request, "orders/cart.html", context) 

@login_required
def order(request):
    get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
    if not get_obj:
        context = {
            "total": 0.0,
            "message": "You must have at least one item in your cart!"
        }
        return render(request, "orders/cart.html", context)
        
    total = Cart.objects.all().filter(buyer_name=request.user.username).aggregate(Sum('price'))    

    if total['price__sum'] is None:
        total = 0.0
    else:
        total = round(total['price__sum'], 2)

    context = {
        "message": "Order sent!"
    }

    time = datetime.datetime.now()

    for item in get_obj:
        all_orders = All_Order(buyer_name=request.user.username, name=item.name, type_p=item.type_p, size=item.size, toppings=item.toppings, price=item.price, total = total, time=time)
        all_orders.save()

    try:
        get_obj = Cart.objects.all().filter(buyer_name=request.user.username)
        get_obj.delete()
        
    except Cart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "Error"})

    return render(request, "orders/cart.html", context) 


@login_required
def status(request, item_id):
    try:
        get_item = All_Order.objects.get(pk=item_id)
        get_item.status = "Completed"
        get_item.save()
        
    except All_Order.DoesNotExist:
        return render(request, "orders/error.html", {"message": "Error"})

    return redirect(reverse(orders)) 
