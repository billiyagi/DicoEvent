from rest_framework import serializers
from .models import User, Event, Registration, Ticket, TicketItem, Payment
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role','created_at', 'updated_at']
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'start_date', 'end_date', 'created_at', 'updated_at', 'organizer']
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # 1. Pastikan end_date setelah start_date
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError(
                {"end_date": "The finish date must be after the start date."}
            )
        # 2. Pastikan start_date tidak di masa lalu
        if start_date and start_date <= date.today():
            raise serializers.ValidationError(
                {"start_date": "The start date cannot be in the past."}
            )

        return data
    
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'status', 'created_at', 'updated_at', 'user']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'type', 'price', 'quota', 'created_at', 'updated_at', 'event']
    
    # Todo nanti harus bisa validasi data ticket item nya apakah melebihi quota?

class TicketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketItem
        fields = ['id', 'serial_number', 'status', 'created_at', 'updated_at', 'registration', 'ticket']
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'method', 'status', 'created_at', 'updated_at', 'registration']