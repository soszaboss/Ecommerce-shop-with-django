from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Account


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code="inactive",
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control mb-3", "required": True, "placeholder": "Email Adress"})

        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "required": True, "placeholder": "Password"})


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "required": True, "placeholder": "First Name"})
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "required": True, "placeholder": "Last Name"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "required": True, "placeholder": "Example@email.com"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "required": True, "placeholder": "Phone Number"})
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "required": True, "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "required": True, "placeholder": "Confirm Password"})
        # self.fields["username"].label = "Username"
        # self.fields["email"].label = "Email address"
        # self.fields["email"].label = "Phone Number"
        # self.fields["password1"].label = "Password"
        # self.fields["password2"].label = "Confirm Password"

class PasswordReset(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Example@email.com"}
        )

class PasswordResetConfirm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "New Password"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Confirm Your New Password"}
        )
