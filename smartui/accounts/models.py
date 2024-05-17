from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from smartui.utils.base_class import BaseModel
import uuid


def user_images_upload_location(instance, filename: str) -> str:
    """Get Location for user profile photo upload."""
    return f"accounts/images/{filename}"
 

class CustomUser(AbstractUser, BaseModel ):
    """
    Custom user model extending Django's AbstractUser and BaseModel. 
    Adds additional fields like email, image, address, date of birth, gender, bio, role, 
    phone number, and custom password validation to better suit application-specific requirements.

    Fields:
    - first_name: Stores the user's first name, non-nullable.
    - email: Unique email address for user authentication, non-nullable.
    - image: Optional image field, storing location of user's uploaded image.
    - address: Optional extended address of the user.
    - date_of_birth: Stores user's date of birth; nullable.
    - gender: User's gender, defaults to 'other' if not specified.
    - bio: Optional biographical information about the user.
    - role: Specifies the role of the user within the application, non-nullable.
    - phone_number: Unique phone number for contact, non-nullable.
    - password: User password with specific validation criteria.

    This model is designed to cater to a wide range of user attributes required by the application,
    extending the default capabilities provided by Django's built-in user model.
    """


    first_name = models.CharField(
        _("first name"), max_length=150, blank=False, null=False
    )
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    image = models.ImageField(upload_to=user_images_upload_location, blank=True)
    address = models.CharField(_("address"), max_length=500, blank=True)
    date_of_birth = models.DateTimeField(blank=False, null=True)
    gender = models.CharField(max_length=10, default="other")
    bio = models.CharField(max_length=500, blank=True, null=True)
    role = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    password = models.CharField(
        _("password"), max_length=128, validators=[validate_password]
    )
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if len(self.password) < 8:
            raise ValidationError(
                {"password": _("Password must be at least 8 characters long.")}
            )

        super().save(*args, **kwargs)


class OTP(models.Model):
    otp = models.CharField(max_length=10, blank=False, null=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
