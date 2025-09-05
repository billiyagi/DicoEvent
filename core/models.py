from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import uuid

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email=email)
        user = self.model(username, email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(Group, related_name="user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="user_set", blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self) -> str:
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() if self.first_name and self.last_name else self.username

class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    quota = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relation
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    
    def __str__(self) -> str:
        return self.title
    
class Registration(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    # Relation
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations")
    
class Ticket(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    price = models.IntegerField()
    quota = models.IntegerField()
    sales_start = models.DateTimeField()
    sales_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relation
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")


class Payment(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    payment_method = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    amount_paid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relations
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name="payment", null=True, blank=True)