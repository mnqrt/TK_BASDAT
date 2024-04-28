from django.urls import path
from subscription.views import *

app_name = 'subscription'
urlpatterns = [
    path('', show_offers, name='show_offers'),
    path('payment/<str:jenis>/', payment_page, name='payment_page'),  

]