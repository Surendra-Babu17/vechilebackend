from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password

# Custom User Manager
class UserRegManager(BaseUserManager):
    def create_user(self, email, userName, password=None):
        if not email:
            raise ValueError("Email required")
        user = self.model(email=self.normalize_email(email), userName=userName)
        user.set_password(password)  # hash password
        user.save()
        return user

    def create_superuser(self, email, userName, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, userName, password, **extra_fields)


# Custom User Model
class userReg(AbstractBaseUser):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    userPhone = models.CharField(max_length=10, unique=True)
    userLocation = models.CharField(max_length=100, default="yourcity")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserRegManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userName']

    def __str__(self):
        return self.email


# Optional Client Model
class clientReg(models.Model):
    clientName = models.CharField(max_length=100, null=False)
    clientEmail = models.EmailField(unique=True)
    clientPhone = models.CharField(max_length=10)
    clientLocation = models.CharField(max_length=50, default="yourcity")
    clientPhoto = models.CharField(max_length=500)
    clientPassword = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clientPassword = make_password(self.clientPassword)
        super().save(*args, **kwargs)

    def check_client_password(self, raw_password):
        return check_password(raw_password, self.clientPassword)
