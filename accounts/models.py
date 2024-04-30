from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,username, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            password=password,
            #date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,username, phone_number, password=None):#date_of_birth):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            password=password,
            #date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)

    #required
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    #Returns True if the user has the specified permission, where perm is in the format "<app label>.<permission codename>". If obj is provided, the permission will be checked against that specific object.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    #Returns True if the user has any permissions in the given app label.
    def has_module_perms(self, app_label):
        return True


# class Acoounts_Activation(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def time_expired(self):
#         setted_expired_time = self.date + timedelta(hours=24)
#         return timezone.now() > setted_expired_time
