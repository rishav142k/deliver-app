from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel

class AlreadyLoggedIn(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'restaurant/already-logged-in.html')

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View): 

    def test_func(self): 
        return self.request.user.groups.filter(name = "Staff").exists()
    
    def get(self, request, *args, **kwargs):
        #Step1: Get the current date.
        today = datetime.today()
        #Step2 : Get orders placed today.

        orders = OrderModel.objects.filter(created_on__year = today.year, 
        created_on__month = today.month, 
        created_on__day = today.day)

        #Step3 : Calculate revenue and pass it to template
        total_revenue = 0
        for order in orders : 
            total_revenue == order.price
        
        context = {
            'orders' : orders,
            'revenue' : total_revenue,
            'total_orders' : len(orders),
        }
        return render(request, "restaurant/dashboard.html", context)

