from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, AddressForm
from django.utils import timezone
from django.utils.timezone import timedelta
from django.core.mail import send_mail
from .models import CustomUser, Address, Cart, Product
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, F
import json


def signup_view(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Generate a magic link (you may need to implement this function)
            magic_link = generate_magic_link(user)
            send_mail(
                'Link for verification to register on our website CoreCrust.in',
                f'Click here to verify your account: {magic_link}',
                'noreply@example.com',
                [user.username],
                fail_silently=False,
            )
            return redirect('login')  # Redirect to login after sending the magic link
        else:
            messages.error(request,"Invalid form submission")
            return redirect('signup')
    else:
        form = SignupForm()
        return render(request, 'account.html', {'form':form,'action':'signup'})

def generate_magic_link(user): 
    token = uuid.uuid4()  # Generate a unique token
    user.magic_link_token = token
    user.magic_link_expiration = timezone.now() + timedelta(hours=1)  # Set expiration time (1 hour)
    user.save()
    return f"http://localhost:8000/verify/{token}/"

def verify_magic_link(request, token):
    try:
        user = CustomUser.objects.get(magic_link_token=token)
        if user.magic_link_expiration > timezone.now():
            user.is_active = True  # Activate the user
            user.magic_link_token = None  # Clear the token after use
            user.magic_link_expiration = None  # Clear the expiration
            user.save()
            messages.success(request, "Your account has been activated. You can now log in.")
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, "This magic link has expired.")
            return redirect('login')
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid magic link.")
        return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/account')
    if request.method == "POST":
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None: # Check if the user is active
                login(request, user)
                return redirect('account')
            else:
                messages.error(request, "Your account is not active. Please verify your email.")
                return redirect('login')
        else:
            return render(request, 'account.html', {'form': form, 'action': 'login'})
    else:
        form = LoginForm()
        return render(request, 'account.html', {'form': form, 'action': 'login'})
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = request.GET.get('next', '/account/')  # Respect `next` if present
            return redirect(next_url)
        return super().dispatch(request, *args, **kwargs)

def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        # print(cart_items)
    else:
        session_id = request.session.session_key or request.session.create()
        cart_items = Cart.objects.filter(session_id=session_id)
        # print(cart_items)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id)
            
            if request.user.is_authenticated:
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
            else:
                session_id = request.session.session_key or request.session.create()
                cart_item, created = Cart.objects.get_or_create(
                    session_id=session_id,
                    product=product,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()

            cart_count = Cart.objects.filter(
                user=request.user if request.user.is_authenticated else None,
                session_id=None if request.user.is_authenticated else session_id
            ).aggregate(total_items=Sum('quantity'))['total_items'] or 0

            return JsonResponse({
                'success': True,
                'cart_count': cart_count
            })
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        
        try:
            if request.user.is_authenticated:
                cart_item = Cart.objects.get(id=item_id, user=request.user)
            else:
                session_id = request.session.session_key
                cart_item = Cart.objects.get(id=item_id, session_id=session_id)
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
                
            return JsonResponse({'success': True})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user=request.user
    return render(request,'account.html',{'user':user})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)  # Ensure user owns the address
    
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('account')  # Redirect back to account page after saving
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'edit_address.html', {
        'form': form,
        'title' : 'Edit the Address',
        'submit_text': 'Edit Address'
        })

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('account')  # or wherever you want to redirect after success
    else:
        form = AddressForm()
    
    return render(request, 'accounts/address_form.html', {
        'form': form,
        'title': 'Add New Address',
        'submit_text': 'Add Address'
    })

def password_reset_view(request):
    return render(request,'password_reset_form.html')

# def password_reset_done_view(request):
#     return render(request,'password_reset_done.html')

# def password_reset_confirm_view(request,uidb64,token):
#     return render(request,'password_reset_confirm.html',{'uidb64':uidb64,'token':token})

# def password_reset_complete_view(request):
#     return render(request,'password_reset_complete.html')

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).aggregate(
            total_items=Sum('quantity'))['total_items'] or 0
    else:
        session_id = request.session.session_key or request.session.create()
        cart_count = Cart.objects.filter(session_id=session_id).aggregate(
            total_items=Sum('quantity'))['total_items'] or 0
    
    return JsonResponse({'cart_count': cart_count})
