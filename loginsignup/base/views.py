from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm
import logging
from django.shortcuts import redirect, get_object_or_404
from base.models import Medicines,ProductItems,ReviewForm,MyOrders,CustomUser,Ayurveda
from django.http import HttpResponse
from django.urls import reverse


logger = logging.getLogger(__name__)

def product(request):
  all_products = ProductItems.objects.all()  
#   print(products)# Fetch all products from the database
  context = {'products': all_products}
  return render(request, 'product.html', context)

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                logger.info("User %s logged in successfully", email)
                return redirect('base:home')
            else:
                logger.error("Login failed")
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('fname')  # Update to 'fname'
        last_name = request.POST.get('lname')   # Update to 'lname'
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        birth_date = request.POST.get('dob')    # Update to 'dob'
        gender = request.POST.get('gender')
        password = request.POST.get('password1')  # Update to 'password1'
        confirm_password = request.POST.get('password2')  # Update to 'password2'

        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Email:", email)
        print("Phone Number:", phone_number)
        print("Birth Date:", birth_date)
        print("Gender:", gender)
        print("Password:", password)
        print("Confirm Password:", confirm_password)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('base:register')
        
        form = CreateUserForm(request.POST)
        print("C")
        if form.is_valid():
            user = form.save()
            print("D")
            try:
                messages.success(request, 'Account created successfully. Please log in.')
            except Exception as e:
                messages.error(request, "An error occurred during registration.")
            return redirect('base:custom_login')
            
        else:
            print(form.errors)
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('base:custom_login')  # Redirect to login page
    else:
        form = CreateUserForm()


    context = {'form': form}
    return render(request, 'signup.html', context=context)

# @login_required
def index(request):
    return render(request, "index.html",{})

def HandleLogout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('base:custom_login')  # Redirect to your login page URL pattern
    return redirect('admin:index')

def about(request):
    return render(request, "about.html")

def medicines(request):
    mymed=Medicines.objects.all()
    context={"mymed":mymed}
    # print(context)
    return render(request,"medicines.html",context)

def product_detail(request, product_id):
    try:
        product = ProductItems.objects.get(pk=product_id)
        print(product)
    except ProductItems.DoesNotExist:
        return render(request, 'error.html', context={'message': 'Product not found'})  # Handle missing product gracefully

    reviews = product.reviews.all()  # Get all reviews for this product

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Don't save yet
            review.user = request.user  # Assign current user
            review.product = product  # Assign current product
            review.save()

            messages.success(request, 'Your review has been submitted successfully!') 
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'product_detail.html', context)


def home(request):
    mymed=Medicines.objects.all()
    myprod=ProductItems.objects.all()
    context={"mymed":mymed,"myprod":myprod}
    return render(request, "home.html",context)


def myorders(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login to place the Order....")
        return redirect("base:login")
    mymed=Medicines.objects.all()
    myprod=ProductItems.objects.all()

    # i am writing a logic to get the user details orders
    current_user=request.user.username
    # print(current_user)
    # i am fetching the data from table MyOrders based on emailid
    items=MyOrders.objects.filter(email=current_user)
    print(items)
    context={"myprod":myprod,"mymed":mymed,"items":items}
    if request.method =="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        item=request.POST.get("items")
        quan=request.POST.get("quantity")
        address=request.POST.get("address")
        phone=request.POST.get("num")
        print(name,email,item,quan,address,phone)
        
        price=""
        for i in mymed:
            if item==i.medicine_name:
                price=i.medicine_price

            pass
        for i in myprod:
            if item==i.prod_name:
                price=i.prod_price

            pass

        newPrice=int(price)*int(quan)
        myquery=MyOrders(name=name,email=email,items=item,address=address,quantity=quan,price=newPrice,phone_num=phone)
        myquery.save()
        messages.info(request,f"Order is Successfull")
        

    
    context = {"myprod": myprod, "mymed": mymed, "items": items}
    return render(request, "orders.html", context)

@login_required
def user_details(request):
    user = request.user
    custom_user = CustomUser.objects.get(pk=user.pk)
    context = {'custom_user': custom_user}
    return render(request, 'user_details.html', context)

def search(request):
    if 'getdata' in request.GET:
        query = request.GET.get("getdata")
        print(query)
        allPostsMedicines = Medicines.objects.filter(medicine_name__icontains=query)
        allPostsProducts = ProductItems.objects.filter(prod_name__icontains=query)
        allPosts = allPostsMedicines.union(allPostsProducts)
        return render(request, "search.html", {"Med": allPostsMedicines, "Prod": allPostsProducts, "allItems": allPosts})
    else:
        # Handle case where 'getdata' key is not found
        # For example, redirect to a page with an error message
        return HttpResponse("No search query provided")

def ayurveda(request):
    myayur=Ayurveda.objects.all()
    context={"myayur":myayur}
    # print(context)
    return render(request,"ayurveda.html",context)