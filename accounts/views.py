from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, LoginForm
from django.utils import timezone
from django.utils.timezone import timedelta
from django.core.mail import send_mail
from .models import CustomUser
import uuid
from django.contrib import messages
# from django.contrib.auth.backends import ModelBackend

# Create your views here.

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
    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request,data=request.POST)
        # print(request.POST.get("password"))
        print(form.is_valid())
        # user=form.get_user()
        # print(form)
        # print(form.errors.as_json())
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            # user = form.get_user()           
            # print(form.error.as_json())
            # if user.is_active(): 
            if user is not None: # Check if the user is active
                login(request, user)
                return redirect('shop:home')
            else:
                messages.error(request, "Your account is not active. Please verify your email.")

                return redirect('login')
        else:
            return render(request, 'account.html', {'form': form, 'action': 'login'})
    else:
        form = LoginForm()
        return render(request, 'account.html', {'form': form, 'action': 'login'})

def logout_view(request):
    logout(request)
    return redirect('index')

# def profile_view(request):
#     if request.method == "POST":
#         user_form = UserUpdateForm(request.POST,instance=request.user)
#         profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('profile')
#         else:
#             messages.error(request,"Invalid form submission")
#             return redirect('profile')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.profile)
#         return render(request,'profile.html',{'user_form':user_form,'profile_form':profile_form})

def password_reset_view(request):
    return render(request,'password_reset_form.html')

# def password_reset_done_view(request):
#     return render(request,'password_reset_done.html')

# def password_reset_confirm_view(request,uidb64,token):
#     return render(request,'password_reset_confirm.html',{'uidb64':uidb64,'token':token})

# def password_reset_complete_view(request):
#     return render(request,'password_reset_complete.html')
