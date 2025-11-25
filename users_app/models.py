from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password

# ---------- Custom User Manager ----------
class UserRegManager(BaseUserManager):
    def create_user(self, email, userName, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        # Ensure phone is stored as None (not empty string) when not provided
        phone = extra_fields.pop('userPhone', None) or None

        # Create user instance with phone explicitly set
        user = self.model(email=email, userName=userName, userPhone=phone, **extra_fields)

        # Set password or make unusable password if none provided
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, userName, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, userName, password, **extra_fields)


# ---------- Custom User Model ----------
class userReg(AbstractBaseUser, PermissionsMixin):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # allow NULL/blank and keep uniqueness for non-null values
    userPhone = models.CharField(max_length=10, unique=True, null=True, blank=True)
    userLocation = models.CharField(max_length=100, default="yourcity")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserRegManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userName']

    def __str__(self):
        return self.email


# ---------- Optional Client Model ----------
class clientReg(models.Model):
    clientName = models.CharField(max_length=100)
    clientEmail = models.EmailField(unique=True)
    # allow NULL/blank for client phone as well
    clientPhone = models.CharField(max_length=10, null=True, blank=True)
    clientLocation = models.CharField(max_length=50, default="yourcity")
    clientPhoto = models.CharField(max_length=500)
    clientPassword = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hash password only on create (when pk not present)
        if not self.pk:
            self.clientPassword = make_password(self.clientPassword)
        super().save(*args, **kwargs)

    def check_client_password(self, raw_password):
        return check_password(raw_password, self.clientPassword)

    def __str__(self):
        return self.clientEmail
