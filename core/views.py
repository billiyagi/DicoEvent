from django.shortcuts import render
from .models import User, Event, Registration, Ticket, TicketItem, Payment
from .serializers import UserSerializer, EventSerializer, RegistrationSerializer, TicketSerializer, TicketItemSerializer, PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404



# Create your views here.
class EventView(APIView):
    def get(self, request):
        events = Event.objects.all().order_by('created_at')[:10]
        serializer = EventSerializer(events, many=True)
        return Response({
                'events': serializer.data
            })
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
