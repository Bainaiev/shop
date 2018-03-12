from . import forms
from . import models

from shop.paginator import MyPaginator
from shop.tokens import account_activation_token

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

DEFAULT_SEX = 'All Categories'
sex_values = [DEFAULT_SEX, 'Man', 'Woman']

def user_preference(request, category=None):
    # define search
    search = request.GET.get('products')

    # define sex products!
    sex = request.GET.get('sex')
    if not sex or sex not in sex_values:
        sex = request.session.get('sex', DEFAULT_SEX)
    if sex !=  DEFAULT_SEX and search:
        product_list = models.Product.objects.filter(sex__exact=sex.lower()).filter(title__icontains=search)
    elif sex !=  DEFAULT_SEX:
        product_list = models.Product.objects.filter(sex__exact=sex.lower())
    elif sex == DEFAULT_SEX and search:
        product_list = models.Product.objects.filter(title__icontains=search)    
    else:
        product_list = models.Product.objects.all()
    request.session['sex'] = sex 

    if category:
        product_list = product_list.filter(category__exact=category)

    paginator = MyPaginator(product_list, 12)

    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
        numbers = paginator.my_range(int(page))
    except PageNotAnInteger:
        products = paginator.page(1)
        numbers = paginator.my_range(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        numbers = paginator.my_range(paginator.num_pages)

    return {'numbers': numbers, 'sex': sex, 'products': products}    

  

def home(request):
    d = user_preference(request)
  
    return render(request, 'shop/home.html',
     {
     'nav': 'home',
     'url': '/shop/home',
     'products': d['products'],
     'numbers': d['numbers'],
     'sex': d['sex'],
     }
     )

def clothing(request):
    d = user_preference(request, 'clothing')
    return render(request, 'shop/home.html',
     {
     'nav' : 'clothing',
     'url': '/shop/clothing',
     'products' : d['products'],
     'numbers' : d['numbers'],
     'sex': d['sex'],

     }
     )

def shoes(request):
    d = user_preference(request, 'shoes')
    return render(request, 'shop/home.html',
     {
     'nav' : 'shoes',
     'url': '/shop/shoes',
     'products' : d['products'],
     'numbers' : d['numbers'],
     'sex': d['sex'],

     }
     ) 

def electronics(request):
    d = user_preference(request, 'electronics')
    return render(request, 'shop/home.html',
     {
     'nav' : 'electronics',
     'url': '/shop/electronics',
     'products' : d['products'],
     'numbers' : d['numbers'],
     'sex': d['sex'],

     }
     )  

def perfumes(request):
    d = user_preference(request, 'perfumes')
    return render(request, 'shop/home.html',
     {
     'nav' : 'perfumes',
     'url': '/shop/perfumes',
     'products' : d['products'],
     'numbers' : d['numbers'],
     'sex': d['sex'],

     }
     )

def about(request):
    return render(request, 'shop/about.html', {'nav' : 'about'})       

def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/shop/home')
    else:
        form = forms.ContactForm()                
    return render(request, 'shop/contact.html', {'nav' : 'contact', 'form': form})

def item(request, id):
    obj = models.Product.objects.get(pk=id)
    return render(request, 'shop/item.html', {'item': obj})

def add_checkout(request, id):
    obj = models.Product.objects.get(pk=id)
    return render(request, 'shop/basket.html', {'item': obj})
   

def nav(request):
    return render(request, 'shop/nav.html', {'nav':'home'})

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Memostra Shop Account'
            message = render_to_string('shop/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
            user.email_user(subject, message)
            return redirect('/shop/account_activation_sent')
    else:
        form = forms.UserCreationForm()
    return render(request, 'shop/registration/signup.html', {'form': form})
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/shop/home')
    else:
        return render(request, 'shop/registration/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'shop/registration/account_activation_sent.html')                                    

@login_required
def profile(request):
    u = request.user
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance = u)
        if form.is_valid():
            form.save()
            return redirect('/shop/about/')
    else:
        form = forms.ProfileForm(instance = u)
    return render(request, 'shop/registration/profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('/shop/profile/')
        else: 
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'shop/registration/change_password.html', {'form': form})                                      





