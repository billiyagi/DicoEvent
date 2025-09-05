from django.shortcuts import render
from .models import User, Event, Registration, Ticket, Payment
from .serializers import UserSerializer, EventSerializer, RegistrationSerializer, TicketSerializer, PaymentSerializer, UserRegisterSerializer, GroupSerializer, AssignRoleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsSuperUser, IsUser, IsAdminOrSuperUser
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404



# Create your views here.

class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "POST" or self.request.method == "GET":
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]
    
    def get(self, request):
        users = User.objects.all().order_by('created_at')[:10]
        serializer = UserSerializer(users, many=True)
        return Response({
                'users': serializer.data
            })
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "PUT" or self.request.method == "GET" or self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]
    
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]
    
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
    
class EventDetailView(APIView):
    
    def get_object(self, id):
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404
    
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsUser()]
        return [IsAuthenticated(), IsAdminOrSuperUser()]
    
    def get(self, request, id):
        event = self.get_object(id=id)
        serializer = EventSerializer(event)
        return Response({
                    'event': serializer.data
                })
        
    def put(self, request, id):
        event = self.get_object(id=id)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        event = self.get_object(id=id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RegistrationView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]
    
    def get(self, request):
        registrations = Registration.objects.all().order_by('created_at')[:10]
        serializer = RegistrationSerializer(registrations, many=True)
        return Response({
                'registrations': serializer.data
            })
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsUser()]
        return [IsAuthenticated(), IsAdminOrSuperUser()]
    
    def get_object(self, id):
        try:
            return Registration.objects.get(id=id)
        except Registration.DoesNotExist:
            raise Http404
    
    def get(self, request, id):
        registration = self.get_object(id=id)
        serializer = RegistrationSerializer(registration, data=request.data)
        
        if serializer.is_valid():
            return Response({
                    'registration': serializer.data
                })
        
    def put(self, request, id):
        registration = self.get_object(id=id)
        serializer = RegistrationSerializer(registration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        event = self.get_object(id=id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TicketView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsUser()]
        return [IsAuthenticated(), IsAdminOrSuperUser()]
    
    def get(self, request):
        tickets = Ticket.objects.all().order_by('created_at')[:10]
        serializer = TicketSerializer(tickets, many=True)
        return Response({
                'tickets': serializer.data
            })
    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsUser()]
        return [IsAuthenticated(), IsAdminOrSuperUser()]
    
    def get_object(self, id):
        try:
            return Ticket.objects.get(id=id)
        except Ticket.DoesNotExist:
            raise Http404
    
    def get(self, request, id):
        tickets = self.get_object(id=id)
        serializer = TicketSerializer(tickets, data=request.data)
        
        if serializer.is_valid():
            return Response({
                    'tickets': serializer.data
                })
        
    def put(self, request, id):
        tickets = self.get_object(id=id)
        serializer = TicketSerializer(tickets, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        tickets = self.get_object(id=id)
        tickets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Payment
class PaymentView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsUser()]
        return [IsAuthenticated(), IsAdminOrSuperUser()]
    
    def get(self, request):
        payments = Payment.objects.all().order_by('created_at')[:10]
        serializer = PaymentSerializer(payments, many=True)
        return Response({'payments': serializer.data})

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(status='PENDING')  # Payment dibuat PENDING

            # Ambil registrasi terkait
            registration = payment.registration

            # Ambil tiket yang terkait dengan event registrasi (misal 1 tiket per event)
            ticket = Ticket.objects.filter(event=registration.user.events.first()).first()
            if not ticket:
                return Response({"error": "No ticket available for this event"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "payment": serializer.data,
                "ticket_item": ticket_item_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsUser()]
        return [IsAuthenticated(), IsAdminOrSuperUser()]
    
    def get_object(self, id):
        try:
            return Payment.objects.get(id=id)
        except Payment.DoesNotExist:
            raise Http404

    def get(self, request, id):
        payment = self.get_object(id=id)
        serializer = PaymentSerializer(payment)
        return Response({'payment': serializer.data})

    def put(self, request, id):
        payment = self.get_object(id)
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Cek jika status diupdate menjadi CONFIRMED
            if serializer.validated_data.get('status') == "CONFIRMED":
                registration = payment.registration
                if registration and hasattr(registration, "ticket_item"):
                    ticket_item = registration.ticket_item
                    ticket_item.status = "SOLD"
                    ticket_item.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        payment = self.get_object(id=id)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        return [IsAuthenticated(), IsSuperUser()]
    
    def get(self, request):
        groups = Group.objects.all().order_by('name')[:10]
        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response({'groups': serializer.data})
 
    def post(self, request):
        serializer = GroupSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        return [IsAuthenticated(), IsSuperUser()]
    
    def get_object(self, pk):
        try:
            group = Group.objects.get(pk=pk)
            self.check_object_permissions(self.request, group)
            return group
        except Group.DoesNotExist:
            raise Http404
 
    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data)
 
    def put(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class AssignRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        return [IsAuthenticated(), IsSuperUser()]
    
    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])
        group = get_object_or_404(Group, pk=serializer.validated_data['group_id'])
 
        user.groups.add(group)
        return Response(status=status.HTTP_201_CREATED)
