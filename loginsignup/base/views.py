from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm
import logging
from django.shortcuts import redirect, get_object_or_404
from base.models import Medicines,ProductItems,ReviewForm,MyOrders,CustomUser,Ayurveda,BlogPost,Video,Prescription,Skincare
from django.http import HttpResponse
import re
from PIL import Image
import pytesseract



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

def skincare(request):
    skinc=Skincare.objects.all()
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name':
        skinc = skinc.order_by('skinc_name')
    elif sort_by == 'price':
        skinc = skinc.order_by('skinc_price')
    context={"skinc":skinc}
    # print(context)
    return render(request,"skincare.html",context)

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
    
def prescription_scan(request):
    if request.method == 'POST':
        print("POST request received.")
        prescription_image = request.FILES['prescription_image']
        # Check if the form contains a file input named 'prescription_image'
        if prescription_image:
            # File is being uploaded, so proceed with processing
            print("Prescription image received.")
            
            prescription = Prescription.objects.create(image=prescription_image)
            extracted_text = prescription.process_image()
            print("Prescription image processed.")
            # Extract medicine names from the extracted text
            medicine_names = extract_medicine_names(extracted_text)
            processed_text = extracted_text

            print("Medicine names extracted:", medicine_names)
            # Pass the extracted medicine names to the template
            return render(request, 'confirm_medicines.html', {'medicine_names': medicine_names, 'processed_text': processed_text})

    # If the request method is not POST or if no file is uploaded,
    # render the prescription upload form
    print("Rendering presc_upload.html...")
    return render(request, 'presc_upload.html')

def process_prescription(request):
  if request.method == 'POST':
    print("POST request received.")

    confirmed_medicines = request.POST.getlist('confirmed_medicines')
    print("Confirmed medicines:", confirmed_medicines)

    matching_products = filter_medicines(confirmed_medicines)  # Use filter_medicines function
    print("Matching products:", matching_products)

    return render(request, 'matching_products.html', {'matching_products': matching_products})
  return redirect('prescription_scan')

def process_image(image_path):
  # Configure Tesseract path (if not in system PATH)
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path
  
  # Read image and perform OCR
  img = Image.open(image_path)
  text = pytesseract.image_to_string(img)
  return text.strip()  # Remove leading/trailing whitespaces

def extract_medicine_names(text):
  # Improved regular expression pattern (adjust as needed)
  medicine_pattern = r'\b(?:[A-Z][a-z]+\s?(?:(?:[A-Z][a-z]+)|(?:[0-9]+(?:\.[0-9]+)?(?:mg|ml|g|u)?))?|\([^)]+\))\b'
  
  medicine_matches = re.findall(medicine_pattern, text, flags=re.IGNORECASE)
  unique_medicine_names = list(set(medicine_matches))
  return unique_medicine_names

def confirm_medicines(request):
    if request.method == 'GET':
        medicine_names = request.GET.getlist('medicine_names', [])
        processed_text = request.GET.get('processed_text', '')
        return render(request, 'confirm_medicines.html', {'medicine_names': medicine_names, 'processed_text': processed_text})
    
def filter_medicines(confirmed_medicines):
  # Fuzzy matching using fuzzywuzzy (install it: pip install fuzzywuzzy)
  from fuzzywuzzy import fuzz  # Import for fuzzy matching
  
  medicine_objects = Medicines.objects.all()
  matching_products = []
  
  for confirmed_med in confirmed_medicines:
    for medicine in medicine_objects:
      # Consider both exact and fuzzy matches with a minimum score (adjust threshold)
      if confirmed_med.lower() == medicine.medicine_name.lower() or fuzz.ratio(confirmed_med.lower(), medicine.medicine_name.lower()) >= 80:
        matching_products.append(medicine)
        break  # Avoid duplicates for the same confirmed medicine
  
  return matching_products