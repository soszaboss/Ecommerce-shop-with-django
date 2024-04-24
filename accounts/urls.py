from django.urls import path
from .views import Login, Logout, RegisterView

urlpatterns = [
    path("accounts/login/", Login.as_view(), name='login'),
    path("accounts/register/", RegisterView.as_view(), name='register'),
    path("logout/", Logout.as_view(), name='logout')

]
