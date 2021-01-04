from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name = "index"),
    path('about/', views.About.as_view(), name='about'),
    path('order/', views.Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>/', views.OrderConfirmation.as_view(),
        name='order-confirmation'),
    path('order-complete/', views.Order_complete.as_view(), name = "order-complete"),
    path('menu/', views.Menu.as_view(), name = "menu"),
    path('menu/search/', views.MenuSearch.as_view, name = "menu-search")
]