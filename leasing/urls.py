from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.redirect_to_login, name='redirect_to_login'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('contract/add/', views.edit_contract, name='add_contract'),
    path('contract/<int:pk>/edit/', views.edit_contract, name='edit_contract'),
    path('contract/list/', views.list_contract, name='list_contract'),
    path('contract/<int:pk>/', views.view_contract, name='view_contract'),
    path('contract/<int:pk>/payments/', views.view_payments, name='view_payments'),

    path('payment/requested/', views.request_paid_list, name='request_paid_list'),
    path('payment/<int:pk>/request/', views.request_payment, name='request_payment'),
    path('payment/<int:pk>/<str:action>/', views.toggle_payment, name='toggle_payment_status'),

    path('warranty/list/', views.list_warranty, name='list_warranty'),
    path('warranty/add/', views.edit_warranty, name='add_warranty'),
    path('warranty/<int:pk>/edit/', views.edit_warranty, name='edit_warranty'),
    path('warranty/<int:pk>/', views.view_warranty, name='view_warranty'),
]
