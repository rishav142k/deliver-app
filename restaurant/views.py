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
        #Step2 : Get orders placed this month. Also Check for shipped orders

        orders = OrderModel.objects.filter(created_on__year = today.year, 
        created_on__month = today.month)
        unshipped_orders = []
        monthDict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 
            7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        #Step3 : Calculate revenue and pass it to template
        total_revenue = 0
        total_paid_orders = 0
        for order in orders :
            if order.is_paid :  
                total_revenue += order.price
                total_paid_orders += 1
            if not order.is_shipped :  
                unshipped_orders.append(order)
        
        context = {
            'orders' : orders,
            'revenue' : total_revenue,
            'total_orders' : len(orders),
            'total_paid_orders' : total_paid_orders,
            'month' : monthDict[today.month],
            'year' : today.year,
        }
        return render(request, "restaurant/dashboard.html", context)

class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self): 
        return self.request.user.groups.filter(name = "Staff").exists()

    def get(self, request, pk, *args, **kwargs) : 
        order = OrderModel.objects.get(pk = pk)
        context = {
            'order': order,
        }
        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk = pk)
        order.is_shipped = True
        order.save()

        context = {
            'order' : order,
        }
        return render(request, 'restaurant/order-details.html', context)


