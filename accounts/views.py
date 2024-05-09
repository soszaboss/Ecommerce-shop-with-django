from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView

from carts.models import Cart, CartItem
from carts.views import _card_id
from .forms import LoginForm, RegistrationForm
from .models import Account
from faker import Faker
import random
from django.conf import settings

def generate_username():
    fake = Faker()
    username = f"{fake.word().capitalize()}_{fake.word().capitalize()}_{random.randint(100, 999)}"
    return username


class Login(LoginView):
    form_class = LoginForm
    template_name = 'authentification/signin.html'
    # success_url = reverse_lazy('home')
    next_page = reverse_lazy('home')
    redirect_authenticated_user = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(cart_id=_card_id(request))
            if cart:
                cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    for item in CartItem.objects.filter(cart=cart):
                        email = request.POST.get('username')
                        user = Account.objects.get(email=email)
                        if item.user is None:
                            if item.product.allow_variants:
                                try:
                                    variant = CartItem.objects.get(variant_key=item.variant_key, user=user)
                                    variant.quantity += item.quantity
                                    variant.save()
                                except CartItem.DoesNotExist:
                                    pass
                            else:
                                try:
                                    product = item.product
                                    new_item = CartItem.objects.get(user=user, product=product)
                                    if  new_item:
                                        new_item.quantity += item.quantity
                                        new_item.save()
                                except CartItem.DoesNotExist:
                                    item.user = user
                                    item.save()
        except Cart.DoesNotExist:
            pass
        return super().post(request, *args, **kwargs)



class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'authentification/register.html'
    # success_url = f'accounts/login/?command=verification&email={email}'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password1')
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                           password=password, username=generate_username())
            # user.save()
            self.success_url = reverse_lazy('login') + f'?command=verification&email={email}'
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            message = render_to_string('authentification/account_verification_email.html', context)
            to_email = email
            print(settings.EMAIL_HOST_USER)
            print(settings.EMAIL_HOST_PASSWORD)
            send_email = EmailMessage(
                                    subject=mail_subject,
                                    from_email=settings.EMAIL_HOST_USER,
                                    body=message,
                                    to=[to_email]
                                      )
            send_email.send()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class Logout(LogoutView):
    next_page = reverse_lazy('login')

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        messages.error(request, 'Account does not exist.')
    else:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account was successfully activated.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid token.')
            return redirect('register')