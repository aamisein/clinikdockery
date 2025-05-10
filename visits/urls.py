from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    path('', views.VisitCreateView.as_view(), name='home'),
    path('success/', views.VisitSuccessView.as_view(), name='success'),
    path('visit-list/', views.VisitListView.as_view(), name='visit_list'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('visit/<int:pk>/edit/', views.VisitUpdateView.as_view(), name='visit_update'),
    path('visit/<int:pk>/delete/', views.VisitDeleteView.as_view(), name='visit_delete'),
    path('calculate-factorial/', views.calculate_factorial_view, name='calculate_factorial'),
]