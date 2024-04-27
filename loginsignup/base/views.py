from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm
import logging
from django.shortcuts import redirect, get_object_or_404
from base.models import Medicines,ProductItems,ReviewForm,MyOrders,CustomUser,Ayurveda,BlogPost,Video
from django.http import HttpResponse
from django.urls import reverse
import uuid


logger = logging.getLogger(__name__)

def product(request):
  all_products = ProductItems.objects.all() 
  sort_by = request.GET.get('sort_by')
  if sort_by == 'name':
        all_products = all_products.order_by('prod_name')
  elif sort_by == 'price':
        all_products = all_products.order_by('prod_price')


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
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name':
        mymed = mymed.order_by('medicine_name')
    elif sort_by == 'price':
        mymed = mymed.order_by('medicine_price')
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
            return redirect('base:product_detail', product_id=product_id)
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
    myayur=Ayurveda.objects.all()
    context={"mymed":mymed,"myprod":myprod,"myayur":myayur}
    return render(request, "home.html",context)


def myorders(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to place the Order....")
        return redirect("base:login")
    
    mymed = Medicines.objects.all()
    myprod = ProductItems.objects.all()
    myayur = Ayurveda.objects.all()
    
    # Fetching the data from MyOrders table based on email id
    current_user = request.user.username
    items = MyOrders.objects.filter(email=current_user)
    
    context = {"myprod": myprod, "mymed": mymed, "myayur": myayur, "items": items}
    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        item = request.POST.get("items")
        quan = request.POST.get("quantity")
        address = request.POST.get("address")
        phone = request.POST.get("num")
        
        # Retrieving the price based on the selected item
        price = None
        
        for med in mymed:
            if item == med.medicine_name:
                price = med.medicine_price
                break
        
        if not price:
            for prod in myprod:
                if item == prod.prod_name:
                    price = prod.prod_price
                    break
        
        if not price:
            for ayur in myayur:
                if item == ayur.ayur_name:
                    price = ayur.ayur_price
                    break
        
        if price:
            newPrice = int(price) * int(quan)
            myquery = MyOrders(name=name, email=email, items=item, address=address, quantity=quan, price=newPrice, phone_num=phone)
            myquery.save()
            messages.info(request, f"Order is successful")
        else:
            messages.error(request, "Item not found")
    
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
        allPostsAyurveda = Ayurveda.objects.filter(med_name__icontains=query)
        allItems = allPostsMedicines.union(allPostsProducts, allPostsAyurveda)
        return render(request, "search.html", {"Med": allPostsMedicines, "Prod": allPostsProducts, "Ayur": allPostsAyurveda, "allItems": allItems, "query": query})
    else:
        # Handle case where 'getdata' key is not found
        # For example, redirect to a page with an error message
        return HttpResponse("No search query provided")
    
def ayurveda(request):
    myayur=Ayurveda.objects.all()
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name':
        myayur = myayur.order_by('med_name')
    elif sort_by == 'price':
        myayur = myayur.order_by('med_price')
    context={"myayur":myayur}
    # print(context)
    return render(request,"ayurveda.html",context)

def blog_category_view(request):
    # Get all blog posts
    all_posts = BlogPost.objects.all()

    # Organize posts by category
    categorized_posts = {}
    for category, _ in BlogPost.CATEGORY_CHOICES:
        categorized_posts[category] = all_posts.filter(category=category)

    context = {
        'categorized_posts': categorized_posts
    }

    return render(request, 'blog.html', context)

def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def medicine_detail(request, product_id):
    try:
        medicine = Medicines.objects.get(pk=product_id)
        print(product_id)
    except Medicines.DoesNotExist:
        return render(request, 'error.html', context={'message': 'medicine not found'})  # Handle missing product gracefully

    reviews = medicine.reviews.all()  # Get all reviews for this product

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Don't save yet
            review.user = request.user  # Assign current user
            review.medicines = medicine  # Assign current product
            review.save()

            messages.success(request, 'Your review has been submitted successfully!') 
            return redirect('base:medicine_detail', product_id=product.id)
    else:
        form = ReviewForm()

    context = {
        'medicine': medicine,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'medicine_detail.html', context)
    
def ayurveda_detail(request, product_id):
    try:
        ayurveda = Ayurveda.objects.get(pk=product_id)
        print(product_id)
    except Medicines.DoesNotExist:
        return render(request, 'error.html', context={'message': 'medicine not found'})  # Handle missing product gracefully

    reviews = ayurveda.reviews.all()  # Get all reviews for this product

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Don't save yet
            review.user = request.user  # Assign current user
            review.ayurveda = ayurveda  # Assign current product
            review.save()

            messages.success(request, 'Your review has been submitted successfully!') 
            return redirect('base:ayurveda_detail', product_id=product.id)
    else:
        form = ReviewForm()

    context = {
        'ayurveda': ayurveda,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'ayurveda_detail.html', context)
    