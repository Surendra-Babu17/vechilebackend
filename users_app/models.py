from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password   # <- ADDED

# ---------- Custom User Manager ----------
class UserRegManager(BaseUserManager):
    def create_user(self, email, userName, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        user = self.model(email=email, userName=userName, **extra_fields)
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
        return self.create_user(email, userName, password, **extra_fields)


# ---------- Custom User Model ----------
class userReg(AbstractBaseUser, PermissionsMixin):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
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
    clientPhone = models.CharField(max_length=10, null=True, blank=True)
    clientLocation = models.CharField(max_length=50, default="yourcity")
    clientPhoto = models.CharField(max_length=500, null=True, blank=True)  # made optional
    clientPassword = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hash password only on create or when raw password looks unhashed
        if not self.pk:
            # if clientPassword already hashed, make_password will still return a hashed string,
            # but we want to avoid double-hashing — a safe simple approach is:
            if self.clientPassword and not self.clientPassword.startswith('pbkdf2_'):
                self.clientPassword = make_password(self.clientPassword)
        super().save(*args, **kwargs)

    def check_client_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.clientPassword)

    def __str__(self):
        return self.clientEmail
