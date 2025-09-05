from django.urls import path
from . import views

urlpatterns = [
    # Events
    path('events/', views.EventView.as_view(), name='events-list'),
    path('events/<uuid:id>/', views.EventDetailView.as_view(), name='events-detail'),
    
    # Registrations
    path('registrations/', views.RegistrationView.as_view()),
    path('registrations/<uuid:id>/', views.RegistrationDetailView.as_view()),
    
    # Tickets
    path('tickets/', views.TicketView.as_view()),
    path('tickets/<uuid:id>/', views.TicketDetailView.as_view()),

    # Payments
    path('payments/', views.PaymentView.as_view()),
    path('payments/<uuid:id>/', views.PaymentDetailView.as_view()),
    
    # Register
    path('register/', views.RegisterView.as_view()),
    
    # Group
    path('groups/', views.GroupListCreateView.as_view(), name='group-list'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),
    path('assign-roles/', views.AssignRoleView.as_view(), name='assign-roles'),
    
    path('users/',views.UserView.as_view(), name='user-list'),
    path('users/<uuid:id>/',views.UserDetailView.as_view(), name='user-list')
]
