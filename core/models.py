from django.db import models
import uuid

# Create your models here.

class User(models.Model):
    class UserRoles(models.TextChoices):
        SUPERUSER = "SUPERUSER", "Superuser"
        ADMIN = "ADMIN", "Admin"
        ORGANIZER = "ORGANIZER", "Organizer"
        USER = "USER", "User"
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
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
    type = models.CharField(max_length=255)
    price = models.IntegerField()
    quota = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relation
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    
class TicketItem(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        RESERVED = "RESERVED", "Reserved"
        SOLD = "SOLD", "Sold"
        CANCELLED = "CANCELLED", "Cancelled"
        USED = "USED", "Used"
        
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    serial_number = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    
    # Relations
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticket_items")
    
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name="ticket_item", )

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    amount = models.IntegerField()
    method = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relations
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name="payment", null=True, blank=True)