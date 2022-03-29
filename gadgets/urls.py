from django.urls import path
from . import views

app_name = 'gadgets'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('separate/new', views.CreateView.as_view(), name='new'),
    path('separate/purchase', views.CreatePurchaseView.as_view(), name='new_purchase'),
    path('separate/gift', views.CreateGiftView.as_view(), name='new_gift'),
]
