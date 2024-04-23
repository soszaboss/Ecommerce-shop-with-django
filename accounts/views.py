from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from .forms import LoginForm, RegistrationForm
from .models import Account
from faker import Faker
import random


def generate_username():
    fake = Faker()
    username = f"{fake.word().capitalize()}_{fake.word().capitalize()}_{random.randint(100, 999)}"
    return username


class Login(LoginView):
    form_class = LoginForm
    template_name = 'authentification/signin.html'
    # success_url = reverse_lazy('home')
    next_page = reverse_lazy('home')


class Logout(LogoutView):
    next_page = reverse_lazy('login')


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'authentification/register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password1')
            user = Account(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                           password=password, username=generate_username())
            user.save()
            messages.success(request, 'Account was successfully registered.')
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
