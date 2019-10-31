"""Efficient_Eater URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "main"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('nutrition/', include([
        path('all/', include([
            path('', views.nutrition, name="nutrition_all"),
            path('<slug:drinks>/', views.nutrition, name="nutrition_all_drinks")])),
        path('<slug:restaurant_slug>/', include([
            path('', views.nutrition, name="nutrition_all"),
            path('<slug:drinks>/',views.nutrition, name="nutrition_all_drinks")]))
        ])),
    path('calculator/', include([
        path('', include([
            path('', views.calculator, name="calculator"),
            path('all/', views.calculator, name="calculator_all"),
            path('<slug:restaurant_slug>/', views.calculator, name="calculator_restaurant")]))
    ])),
    path('lookup/', include([
        path('<slug:restaurant_slug>/', include([
            path('', views.lookup, name="lookup_restaurant"),
            path('<slug:item_slug>/', views.lookup, name="lookup_restaurant_item")])),
        path('', views.lookup, name="lookup")
    ])),
    path('methodology/', views.methodology, name="methodology"),
    path('contact/', views.contact, name="contact"),
]
urlpatterns += staticfiles_urlpatterns()