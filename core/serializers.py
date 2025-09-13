from rest_framework import serializers
from .models import User, Event, Registration, Ticket, Payment
from datetime import date, datetime
from rest_framework.reverse import reverse
from django.contrib.auth.models import Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 🔑 hash password
        user.is_active = True
        user.save()
        if groups is not None:
            user.groups.set(groups)
        if user_permissions is not None:
            user.user_permissions.set(user_permissions)
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.is_active = True
        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        if user_permissions is not None:
            instance.user_permissions.set(user_permissions)
        return instance

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 🔑 hash password
        user.save()
        if groups is not None:
            user.groups.set(groups)
        if user_permissions is not None:
            user.user_permissions.set(user_permissions)
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        if user_permissions is not None:
            instance.user_permissions.set(user_permissions)
        return instance

class EventSerializer(serializers.ModelSerializer):
    organizer_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Event
        exclude = ['organizer']
    

    def create(self, validated_data):
        organizer_id = validated_data.pop('organizer_id')
        organizer = User.objects.get(pk=organizer_id)
        validated_data['organizer'] = organizer
        return super().create(validated_data)

    def update(self, instance, validated_data):
        organizer_id = validated_data.pop('organizer_id', None)
        if organizer_id:
            organizer = User.objects.get(pk=organizer_id)
            validated_data['organizer'] = organizer
        return super().update(instance, validated_data)
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # 1. Pastikan end_date setelah start_date
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError(
                {"end_date": "The finish date must be after the start date."}
            )

        return data
    
class RegistrationSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='user',
        queryset=User.objects.all()
    )
    ticket_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='ticket',
        queryset=Ticket.objects.all()
    )

    class Meta:
        model = Registration
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'ticket': {'required': False}
        }

    def create(self, validated_data):
        # Setelah menggunakan PrimaryKeyRelatedField, DRF sudah mengubah UUID menjadi instance
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class TicketSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(write_only=True)
    event = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = '__all__'
    
    def create(self, validated_data):
        event_id = validated_data.pop('event_id')
        event = Event.objects.get(pk=event_id)
        validated_data['event'] = event
        return super().create(validated_data)

    def update(self, instance, validated_data):
        event_id = validated_data.pop('event_id', None)
        if event_id:
            event = Event.objects.get(pk=event_id)
            validated_data['event'] = event
        return super().update(instance, validated_data)
    def get_event(self, obj):
        return str(obj.event.id)

    
class PaymentSerializer(serializers.ModelSerializer):
    registration_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='registration',  # ini akan mengisi field registration
        queryset=Registration.objects.all()
    )
    
    class Meta:
        model = Payment
        fields = ['id', 'registration', 'registration_id', 'payment_method', 'payment_status', 'amount_paid', 'created_at', 'updated_at']
        read_only_fields = ['id', 'registration', 'created_at', 'updated_at']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    group_id = serializers.IntegerField()