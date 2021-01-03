import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel
from django.http import JsonResponse


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        starters = MenuItem.objects.filter(category__name__contains='Starter')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        main_courses = MenuItem.objects.filter(category__name__contains='Main Course')
        entres = MenuItem.objects.filter(category__name__contains='Entre')



        # pass into context
        context = {
            'starters' : starters,
            'entres': entres,
            'desserts': desserts,
            'main_courses' : main_courses,

        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)


        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # context = {
        #     'items': order_items['items'],
        #     'price': price
        # }

        return redirect('order-confirmation', pk=order.pk)
    

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        # print(request.body)
        data = json.loads(request.body)

        if data['isPaid'] :
            order = OrderModel.objects.get(pk = pk)
            order.is_paid = True
            order.save()
        return redirect('order-complete')

class Order_complete(View):
    def get(self, request,*args, **kwargs):
        return render(request, 'customer/order_confirmed.html')