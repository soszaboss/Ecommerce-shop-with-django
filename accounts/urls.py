from django.urls import path

from .forms import PasswordReset, PasswordResetConfirm
from .views import Login, Logout, RegisterView, activate_account
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
urlpatterns = [
    path("login/", Login.as_view(), name='login'),
    path("register/", RegisterView.as_view(), name='register'),
    path("logout/", Logout.as_view(), name='logout'),
    path("activate/<uidb64>/<token>/", activate_account, name='activate'),
    path('password-reset/', PasswordResetView.as_view(template_name='authentification/password_reset.html', form_class=PasswordReset), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='authentification/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='authentification/password_reset_confirm.html', form_class=PasswordResetConfirm), name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='authentification/password_reset_complete.html'),
         name='password_reset_complete'),

]

