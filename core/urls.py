from django.urls import path, re_path
from . import views

urlpatterns = [
    # Events
    path('events/', views.EventView.as_view(), name='events-list'),
    re_path(r'^events/(?P<id>[0-9a-f-]+)/?$', views.EventDetailView.as_view(), name='events-detail'),
    
    # Registrations
    path('registrations/', views.RegistrationView.as_view()),
    re_path(r'^registrations/(?P<id>[0-9a-f-]+)/?$', views.RegistrationDetailView.as_view()),
    
    # Tickets
    path('tickets/', views.TicketView.as_view()),
    re_path(r'^tickets/(?P<id>[0-9a-f-]+)/?$', views.TicketDetailView.as_view()),

    # Payments
    path('payments/', views.PaymentView.as_view()),
    re_path(r'^payments/(?P<id>[0-9a-f-]+)/?$', views.PaymentDetailView.as_view()),
    
    # Register
    path('register/', views.RegisterView.as_view()),
    
    # Group
    path('groups/', views.GroupListCreateView.as_view(), name='group-list'),
    re_path(r'^groups/(?P<pk>\d+)/?$', views.GroupDetailView.as_view(), name='group-detail'),
    path('assign-roles/', views.AssignRoleView.as_view(), name='assign-roles'),
    
    path('users/',views.UserView.as_view(), name='user-list'),
    re_path(r'^users/(?P<id>[0-9a-f-]+)/?$',views.UserDetailView.as_view(), name='user-list')
]
