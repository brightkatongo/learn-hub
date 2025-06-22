from django.urls import path
from . import views

app_name = 'mobile_payments'

urlpatterns = [
    # Provider endpoints
    path('providers/', views.MobileMoneyProviderListView.as_view(), name='provider-list'),
    
    # Transaction endpoints
    path('transactions/', views.MobileMoneyTransactionListView.as_view(), name='transaction-list'),
    path('transactions/<str:reference_code>/', views.MobileMoneyTransactionDetailView.as_view(), name='transaction-detail'),
    
    # Payment flow endpoints
    path('initiate/', views.initiate_payment, name='initiate-payment'),
    path('status/<str:reference_code>/', views.payment_status, name='payment-status'),
    path('cancel/<str:reference_code>/', views.cancel_payment, name='cancel-payment'),
    path('instructions/<str:reference_code>/', views.payment_instructions, name='payment-instructions'),
    
    # Utility endpoints
    path('validate-phone/', views.validate_phone_number, name='validate-phone'),
    path('webhook/sms/', views.sms_webhook, name='sms-webhook'),
]
