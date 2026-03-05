from django.shortcuts import get_object_or_404, render ,redirect
from django.http import HttpResponse, JsonResponse
from .models import * 
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Seller
from django.core.files.storage import default_storage
from django.shortcuts import render
from .models import Register
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from django.shortcuts import render, redirect
from .models import Register
from django.shortcuts import render
from .models import Order
from django.shortcuts import render, redirect
from .models import Order
from django.shortcuts import render, redirect
from .models import Order, Notification
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Furniture, Category, Seller
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import (
    Furniture, RentalFurniture, Register, Order, Notification
)
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect
from .models import Register
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
import os
# Create your views here.
import re
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Seller, Renter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Register, Renter, Seller
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Register, Renter, Seller
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Register, Renter, Seller
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Register, Renter, Seller
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Register, Renter, Seller, Admin


#Index view
def index(request):
    return render(request,'index.html')
# ================= USER REGISTER =================
def registration(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_picture = request.FILES.get("profile_picture")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("registration")

        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("registration")

        Register.objects.create(
            name=name,
            email=email,
            number=number,
            address=address,
            password=make_password(password),
            profile_picture=profile_picture
        )

        messages.success(request, "User Registered Successfully")
        return redirect("login")

    return render(request, "registration.html")


# ================= RENTER REGISTER =================
def renter(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        rental_business_name = request.POST.get("rental_business_name")
        rental_address = request.POST.get("rental_address")
        gst_number = request.POST.get("gst_number", "").upper().strip()
        license_number = request.POST.get("license_number", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_picture = request.FILES.get("profile_picture")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("renter")

        if Renter.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("renter")

        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'
        license_pattern = r'^[A-Za-z0-9]{6,20}$'

        if not gst_number and not license_number:
            messages.error(request, "Provide either GST Number OR License Number")
            return redirect("renter")

        if gst_number and not re.match(gst_pattern, gst_number):
            messages.error(request, "Invalid GST Number format")
            return redirect("renter")

        if license_number and not re.match(license_pattern, license_number):
            messages.error(request, "Invalid License Number format")
            return redirect("renter")

        Renter.objects.create(
            name=name,
            email=email,
            number=number,
            rental_business_name=rental_business_name,
            rental_address=rental_address,
            gst_number=gst_number if gst_number else None,
            license_number=license_number if license_number else None,
            password=make_password(password),
            profile_picture=profile_picture
        )

        messages.success(request, "Renter Registered. Wait for admin approval.")
        return redirect("login")

    return render(request, "renter.html")

# ================= SELLER REGISTER =================
def seller(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        shop_name = request.POST.get("shop_name")
        shop_address = request.POST.get("shop_address")
        gst_number = request.POST.get("gst_number", "").upper().strip()
        license_number = request.POST.get("license_number", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_picture = request.FILES.get("profile_picture")

        # Password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("seller")

        # Email check
        if Seller.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("seller")

        # GST & License validation
        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'
        license_pattern = r'^[A-Za-z0-9]{6,20}$'

        if not gst_number and not license_number:
            messages.error(request, "Provide either GST Number OR License Number")
            return redirect("seller")

        if gst_number and not re.match(gst_pattern, gst_number):
            messages.error(request, "Invalid GST Number format")
            return redirect("seller")

        if license_number and not re.match(license_pattern, license_number):
            messages.error(request, "Invalid License Number format")
            return redirect("seller")

        Seller.objects.create(
            name=name,
            email=email,
            number=number,
            shop_name=shop_name,
            shop_address=shop_address,
            gst_number=gst_number if gst_number else None,
            license_number=license_number if license_number else None,
            password=make_password(password),
            profile_picture=profile_picture
        )

        messages.success(request, "Seller Registered. Wait for admin approval.")
        return redirect("login")

    return render(request, "seller.html")

# ================= COMMON LOGIN =================
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # ===== Check Admin =====
        admin = Admin.objects.filter(email=email, password=password).first()
        if admin:
            request.session["admin_id"] = admin.id
            request.session["role"] = "admin"
            return redirect("admin_index")

        # ===== Check User =====
        user = Register.objects.filter(email=email).first()
        if user:
            if user.status == "blocked":
                messages.error(request, "Your account is blocked by admin.")
                return redirect('login')

            # ✅ Corrected this line
            if check_password(password, user.password) and user.status == "active":
                request.session["user_id"] = user.id
                request.session["role"] = "user"
                return redirect("user_index")

        # ===== Check Renter =====
        renter = Renter.objects.filter(email=email).first()
        if renter and check_password(password, renter.password):
            if renter.is_approved:
                request.session["renter_id"] = renter.id
                request.session["role"] = "renter"
                return redirect("renter_index")
            else:
                messages.error(request, "Renter not approved yet")
                return redirect("login")

        # ===== Check Seller =====
        seller = Seller.objects.filter(email=email).first()
        if seller and check_password(password, seller.password):
            if seller.is_approved:
                request.session["seller_id"] = seller.id
                request.session["role"] = "seller"
                return redirect("seller_index")
            else:
                messages.error(request, "Seller not approved yet")
                return redirect("login")

        messages.error(request, "Invalid Email or Password")
        return redirect("login")

    return render(request, "login.html")
###admin###




#admin index
def admin_index(request):
    return render(request,"admin/admin_index.html")


# admin view users

def view_users(request):
    users = Register.objects.all()
    return render(request, 'admin/view_users.html', {'users': users})



def block_user(request):
    user_id = request.GET.get('id')
    user = get_object_or_404(Register, id=user_id)
    user.status = "blocked"
    user.save()
    return redirect('view_users')


def unblock_user(request):
    user_id = request.GET.get('id')
    user = get_object_or_404(Register, id=user_id)
    user.status = "active"
    user.save()
    return redirect('view_users')


def delete_user(request):
    user_id = request.GET.get('id')
    user = get_object_or_404(Register, id=user_id)
    user.delete()
    return redirect('view_users')



# Manage Renter and Seller
def manage_renter(request):
    # Get the users with pending, approved, and rejected statuses
    pending_renters = Renter.objects.filter(
        Q(is_approved=False) & Q(status='pending')
    )
    approved_renters = Renter.objects.filter(status='approved')
    rejected_renters = Renter.objects.filter(status='rejected')

    return render(request, 'admin/manage_renter.html', {
        'pending_renters': pending_renters,
        'approved_renters': approved_renters,
        'rejected_renters': rejected_renters
    })

def approve_renter(request):
    renter_id=request.GET.get("id")
    renter = Renter.objects.get(id=renter_id)
    renter.is_approved = True  # Mark user as approved
    renter.status='approved'
    renter.save()
    messages.success(request, f'Renter {renter.name} has been approved.')
    return redirect('manage_renter')

def reject_renter(request):
    renter_id = request.GET.get("id")
    renter = Renter.objects.get(id=renter_id)
    renter.is_approved = False 
    renter.status="rejected"
    renter.save()  # Reject by deleting user (or handle as you see fit)
    messages.error(request, f'Renter {renter.name} has been rejected.')
    return redirect('manage_renter')
    
def manage_seller(request):
    # Get the users with pending, approved, and rejected statuses
    pending_sellers = Seller.objects.filter(
        Q(is_approved=False) & Q(status='pending')
    )
    approved_sellers = Seller.objects.filter(status='approved')
    rejected_sellers = Seller.objects.filter(status='rejected')

    return render(request, 'admin/manage_seller.html', {
        'pending_sellers': pending_sellers,
        'approved_sellers': approved_sellers,
        'rejected_sellers': rejected_sellers
    })

def approve_seller(request):
    seller_id=request.GET.get("id")
    seller = Seller.objects.get(id=seller_id)
    seller.is_approved = True  # Mark user as approved
    seller.status='approved'
    seller.save()
    messages.success(request, f'Seller {seller.name} has been approved.')
    return redirect('manage_seller')

def reject_seller(request):
    seller_id = request.GET.get("id")
    seller = Seller.objects.get(id=seller_id)
    seller.is_approved = False 
    seller.status="rejected"
    seller.save()  # Reject by deleting user (or handle as you see fit)
    messages.error(request, f'Seller {seller.name} has been rejected.')
    return redirect('manage_seller')






# View all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, "admin/category_list.html", {"categories": categories})

# Add category
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
        return redirect("category_list")
    return render(request, "admin/add_category.html")

# Edit category
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            category.name = name
            category.save()
            return redirect("category_list")
    return render(request, "admin/edit_category.html", {"category": category})

# Delete category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect("category_list")



################### User ##############

#user index


def user_index(request):
    user_id = request.session.get("user_id")   # get logged-in user id
    user = Register.objects.filter(id=user_id).first()

    if not user:
        return redirect("index")  # redirect to login if not logged in

    return render(request, 'user/user_index.html', {"user": user})





def profile_settings(request):
    user_id = request.session.get("user_id")
    user = Register.objects.filter(id=user_id).first()

    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    return render(request, 'user/view_user_profile.html', {'user': user})

def profile_edit(request):
    user_id = request.session.get("user_id")
    user = Register.objects.filter(id=user_id).first()

    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    if request.method == 'POST':
        # Update basic details
        user.name = request.POST.get('name', user.name)
        user.number = request.POST.get('number', user.number)
        user.address = request.POST.get('address', user.address)

        # Update password if provided
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password:
            if password == confirm_password:
                user.password = make_password(password)  # ✅ Hash the password
            else:
                messages.error(request, "Passwords do not match!")
                return redirect('profile_edit')

        # Update profile picture if uploaded
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            if user.profile_picture and default_storage.exists(user.profile_picture.path):
                default_storage.delete(user.profile_picture.path)
            user.profile_picture = profile_picture

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile_settings')

    return render(request, 'user/profile_edit.html', {'user': user})




# ---------- Helper ----------
def get_logged_in_user(request):
    """Fetch user from session safely"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return Register.objects.filter(id=user_id).first()


# ---------- Product Detail Views ----------
def product_detail(request, product_id):
    product = get_object_or_404(Furniture, id=product_id)
    user = get_logged_in_user(request)
    return render(request, 'user/view_details.html', {
        'product': product,
        'user': user
    })


def product_details(request, id):
    product = get_object_or_404(RentalFurniture, id=id)
    user = get_logged_in_user(request)
    return render(request, 'user/rview_details.html', {
        'product': product,
        'user': user
    })


# ---------- Product Listing Views ----------
def view_furniture(request):
    products = Furniture.objects.all()
    user = get_logged_in_user(request)
    return render(request, 'user/furniture.html', {
        'products': products,
        'user': user
    })


def rental_products(request):
    rent_products = RentalFurniture.objects.all()
    user = get_logged_in_user(request)
    return render(request, 'user/rent_furniture.html', {
        'rent_products': rent_products,
        'user': user
    })


# ---------- Buying / Orders ----------
def buy_now(request, product_type, product_id):
    user = get_logged_in_user(request)
    if not user:
        messages.error(request, "You must be logged in to proceed.")
        return redirect('login')

    # Identify product type
    if product_type == 'furniture':
        product = get_object_or_404(Furniture, id=product_id)
    elif product_type == 'rental':
        product = get_object_or_404(RentalFurniture, id=product_id)
    else:
        messages.error(request, "Invalid product type.")
        return redirect('user_index')

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            buyer_name = request.POST.get('buyer_name')
            phone_number = request.POST.get('phone_number')
            delivery_location = request.POST.get('delivery_location')

            total_price = product.price * quantity

            order = Order(
                user=user,
                furniture_product=product if product_type == 'furniture' else None,
                rental_product=product if product_type == 'rental' else None,
                buyer_name=buyer_name,
                phone_number=phone_number,
                delivery_location=delivery_location,
                quantity=quantity,
                total_price=total_price,
                status='Pending'
            )
            order.full_clean()
            order.save()
            return redirect('order_confirmation', order_id=order.id)
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'user/buy.html', {
        'product': product,
        'user': user
    })


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = get_logged_in_user(request)

    product = order.furniture_product or order.rental_product
    product_name = getattr(product, 'product_name', None) or getattr(product, 'name', '')

    return render(request, 'user/confirmation.html', {
        'order': order,
        'product': product,
        'product_name': product_name,
        'user': user
    })


# ---------- Bookings ----------
def my_bookings(request):
    user = get_logged_in_user(request)
    if not user:
        return redirect("login")

    seller_bookings = Order.objects.filter(user_id=user.id, furniture_product__isnull=False)
    renter_bookings = Order.objects.filter(user_id=user.id, rental_product__isnull=False)

    return render(request, 'user/my_bookings.html', {
        'seller_bookings': seller_bookings,
        'renter_bookings': renter_bookings,
        'user': user
    })


# ---------- Notifications ----------
def user_notifications_view(request):
    user = get_logged_in_user(request)
    if not user:
        return redirect("login")

    notifications = Notification.objects.filter(user_id=user.id).order_by('-created_at')
    return render(request, 'user/notifications.html', {
        'notifications': notifications,
        'user': user
    })



############### Seller ###############

# seller index #
def seller_index(request):
    return render(request,"seller/seller_index.html")




def add_furniture(request):
    seller_id = request.session.get("seller_id")
    seller = get_object_or_404(Seller, id=seller_id)
    categories = Category.objects.all()  # ✅ Fetch all categories

    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        category_id = request.POST.get("category")   # will be id now
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        description = request.POST.get("description")
        image = request.FILES.get("product_image")

        if all([product_name, category_id, price, quantity, description, image]):
            try:
                category = get_object_or_404(Category, id=category_id)
                product = Furniture.objects.create(
                    seller=seller,
                    product_name=product_name,
                    category=category,
                    price=price,
                    quantity=quantity,
                    description=description,
                    image=image,
                    product_type="sale"  # or "rent" if needed
                )
                messages.success(request, "Added Successfully!")
                return redirect("manage_products")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Please fill in all fields and upload an image.")

    return render(request, "seller/add_furniture.html", {"categories": categories})


def manage_products(request):
    seller_id = request.session.get("seller_id")
    products = Furniture.objects.filter(seller_id=seller_id)
    return render(request, 'seller/manage_products.html', {'products': products})


def delete_furniture(request, product_id):
    product = get_object_or_404(Furniture, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('manage_products')


def edit_products(request, product_id):
    product = get_object_or_404(Furniture, id=product_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id)
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.description = request.POST.get('description')

        image = request.FILES.get('image')
        if image:
            product.image = image

        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('manage_products')

    return render(request, 'seller/edit_products.html', {'product': product, 'categories': categories})


def seller_profile(request):
    seller_id = request.session.get("seller_id")
    seller = get_object_or_404(Seller, id=seller_id)

    return render(request, "seller/seller_profile.html", {"seller": seller})

def seller_edit(request):
    seller_id = request.session.get("seller_id")
    seller = get_object_or_404(Seller, id=seller_id)

    if request.method == "POST":

        seller.name = request.POST.get("name")
        seller.number = request.POST.get("number")
        seller.shop_name = request.POST.get("shop_name")
        seller.shop_address = request.POST.get("shop_address")
        seller.gst_number = request.POST.get("gst_number")
        seller.license_number = request.POST.get("license_number")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password:
            if password == confirm_password:
                seller.password = make_password(password)
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "Passwords do not match!")
                return redirect("seller_edit")

        seller.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("seller_profile")

    return render(request, "seller/seller_edit.html", {"seller": seller})

  
def seller_bookings_view(request):
    user_id = request.session.get('seller_id')  # Adjust as needed

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        try:
            booking = Order.objects.get(id=booking_id, user_id=user_id, furniture_product__isnull=False)
            if action == 'approve':
                booking.status = 'Approved'
            elif action == 'reject':
                booking.status = 'Rejected'
            booking.save()

            # Create notification
            Notification.objects.create(
                user=booking.user,
                title=f"Booking {booking.status}",
                message=f"Your booking for {booking.furniture_product} has been {booking.status.lower()}.",
                status=booking.status,
            )
        except Order.DoesNotExist:
            pass
        return redirect('seller_bookings')

    bookings = Order.objects.filter(user_id=user_id, furniture_product__isnull=False).order_by('-id')
    return render(request, 'seller/view_seller_bookings.html', {'bookings': bookings})


















# Renter #####

# renter index #
def renter_index(request):
    return render(request,'renter/renter_index.html')


def add_renter_furniture(request):
    renter_id = request.session.get("renter_id")
    renter = Renter.objects.filter(id=renter_id).first()
    categories = Category.objects.all()  # ✅ fetch categories

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')  # will be ID
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id)  # ✅ fetch Category object

        RentalFurniture.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            image=image,
            owner=renter,
            availability=True
        )

        return redirect('add_renter_furniture')

    return render(request, 'renter/add_renter_furniture.html', {'categories': categories})








def manage_products_renter(request):
    renter_id = request.session.get("renter_id")
    products = RentalFurniture.objects.filter(owner_id=renter_id)  # Correct field name
    return render(request, 'renter/renter_view_products.html', {'products': products})


def delete_furniture_renter(request):
    product_id = request.GET.get("id")
    if product_id:
        product = RentalFurniture.objects.filter(id=product_id).first()
        product.delete()
    return redirect('manage_products_renter')
def edit_products_renter(request):
    product_id = request.GET.get("id")
    product = get_object_or_404(RentalFurniture, id=product_id)
    categories = Category.objects.all()  # ✅ fetch categories

    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        category_id = request.POST.get('category', product.category.id)
        product.category = Category.objects.get(id=category_id)  # ✅ update category
        product.price = request.POST.get('price', product.price)
        product.quantity = request.POST.get('quantity', product.quantity)
        product.description = request.POST.get('description', product.description)

        image = request.FILES.get('image')
        if image:
            product.image = image

        product.save()
        return redirect('manage_products_renter')

    return render(request, 'renter/edit_product_renter.html', {
        'product': product,
        'categories': categories
    })


def renter_profile(request):
    # Retrieve the seller's ID from the session
    renter_id = request.session.get("renter_id")
    renter = Renter.objects.filter(id=renter_id).first()

    if not renter:
        messages.error(request, "renter not found.")
        return redirect('login')  # Redirect to login if seller is not found

    if request.method == 'POST':
        # Handle username update
        name = request.POST.get('name')
        if name and name != renter.name:
            renter.name = name

        # Handle password update
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password:
            if password == confirm_password:
                renter.password = make_password(password)  # Hash the new password
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "Passwords do not match.")
                return redirect('renter_profile')

        # Handle profile picture upload
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            # Delete the old profile picture if it exists
            if renter.profile_picture and default_storage.exists(renter.profile_picture.path):
                default_storage.delete(renter.profile_picture.path)
            renter.profile_picture = profile_picture

        # Save the seller object after all updates
        renter.save()
        messages.success(request, "Profile updated successfully!")

    return render(request, 'renter/renter_profile.html', {'renter': renter})

def renter_edit(request):
    renter_id = request.session.get("renter_id")
    renter = Renter.objects.filter(id=renter_id).first()

    if not renter:
        return redirect("login")

    if request.method == "POST":

        renter.name = request.POST.get("name")
        renter.number = request.POST.get("number")
        renter.rental_business_name = request.POST.get("rental_business_name")
        renter.rental_address = request.POST.get("rental_address")

        gst_number = request.POST.get("gst_number")
        license_number = request.POST.get("license_number")

        # GST OR License validation
        if not gst_number and not license_number:
            messages.error(request, "Provide either GST Number or License Number.")
            return redirect("renter_edit")

        renter.gst_number = gst_number
        renter.license_number = license_number

        # Password update
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password:
            if password == confirm_password:
                renter.password = make_password(password)
                messages.success(request, "Password updated successfully.")
            else:
                messages.error(request, "Passwords do not match.")
                return redirect("renter_edit")

        # Profile picture update
        profile_picture = request.FILES.get("profile_picture")
        if profile_picture:
            if renter.profile_picture and default_storage.exists(renter.profile_picture.path):
                default_storage.delete(renter.profile_picture.path)
            renter.profile_picture = profile_picture

        renter.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("renter_profile")

    return render(request, "renter/renter_edit.html", {"renter": renter})
    
def renter_bookings_view(request):
    user_id = request.session.get('renter_id')  # Adjust if needed

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        try:
            booking = Order.objects.get(id=booking_id, user_id=user_id, rental_product__isnull=False)
            if action == 'approve':
                booking.status = 'Approved'
            elif action == 'reject':
                booking.status = 'Rejected'
            booking.save()

            # Create notification
            Notification.objects.create(
                user=booking.user,
                title=f"Booking {booking.status}",
                message=f"Your booking for {booking.rental_product} has been {booking.status.lower()}.",
                status=booking.status,
            )
        except Order.DoesNotExist:
            pass
        return redirect('renter_bookings_view')

    bookings = Order.objects.filter(user_id=user_id, rental_product__isnull=False).order_by('-id')
    return render(request, 'renter/view_bookings.html', {'bookings': bookings})






















# def manage_shops(request):
#     shops = Shop.objects.all()
#     return render(request, 'admin/manage_shops.html', {'shops': shops})

# def add_shop(request):
#     shop= shop.objects.all()
#     if request.method == 'POST':
#         form = ShopForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_shops')
#     else:
#         form = ShopForm()
#     return render(request, 'add_shop.html', {'form': form})

# def edit_shop(request, shop_id):
#     shop = get_object_or_404(Shop, id=shop_id)
#     if request.method == 'POST':
#         form = ShopForm(request.POST, instance=shop)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_shops')
#     else:
#         form = ShopForm(instance=shop)
#     return render(request, 'edit_shop.html', {'form': form, 'shop': shop})

# def delete_shop(request, shop_id):
#     shop = get_object_or_404(Shop, id=shop_id)
#     if request.method == 'POST':
#         shop.delete()
#         return redirect('manage_shops')
#     return render(request, 'delete_shop.html', {'shop': shop})

