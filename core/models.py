from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    first_name = models.CharField(max_length=255, blank=True, default="", null=False)
    last_name = models.CharField(max_length=255, blank=True, default="", null=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() if self.first_name or self.last_name else self.username

class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True, blank=True)
    quota = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relation
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    
    def __str__(self) -> str:
        return self.name

class Ticket(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
    price = models.IntegerField()
    quota = models.IntegerField()
    sales_start = models.DateTimeField()
    sales_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relation
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")

class Registration(models.Model):
        
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relation
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations")
    
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name="registration", null=True, blank=True)


class Payment(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    payment_method = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    amount_paid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relations
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name="payment", null=True, blank=True)