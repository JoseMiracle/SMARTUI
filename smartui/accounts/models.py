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
 image = models.ImageField(upload_to=user_images_upload_location, blank=True)


class CustomUser(AbstractUser, BaseModel ):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
