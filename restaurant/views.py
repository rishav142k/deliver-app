from django.shortcuts import render, redirect
from django.views import View

class AlreadyLoggedIn(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'restaurant/already-logged-in.html')

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        return render(request, "restaurant/dashboard.html")
