from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payment-list'),
    path('<uuid:id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('create-intent/', views.create_payment_intent, name='create-payment-intent'),
    path('confirm/', views.confirm_payment, name='confirm-payment'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('validate-coupon/', views.validate_coupon, name='validate-coupon'),
    path('instructor/payouts/', views.InstructorPayoutListView.as_view(), name='instructor-payouts'),
    path('instructor/earnings/', views.instructor_earnings, name='instructor-earnings'),
]
