from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Restaurant, Item
from .forms import *
import jsonpickle

# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name="main/home.html",
                  context={"restaurants":Restaurant.objects.all(),
                           "items": Item.objects.all()})

def nutrition(request, restaurant_slug="", drinks="", calories = 0):
    request = request
    template_name = "main/nutrition.html"
    if restaurant_slug != "":
        if drinks == "no-drinks":
            context={"restaurants": Restaurant.objects.filter(slug=restaurant_slug).order_by("name"),
                     "items": Item.objects.filter(restaurant__slug=restaurant_slug).exclude(calories__lt=calories).exclude(type_of_item="drink").order_by("name"),
                     "drinks":False}
        else:
            context={"restaurants": Restaurant.objects.filter(slug=restaurant_slug).order_by("name"),
                     "items": Item.objects.filter(restaurant__slug=restaurant_slug).exclude(calories__lt=calories).order_by("name"),
                     "drinks":True}
    else:
        if drinks == "no-drinks":
            context={"restaurants": Restaurant.objects.all().order_by("name"),
                     "items": Item.objects.all().exclude(calories__lt=calories).exclude(type_of_item="drink").order_by("name"),
                     "drinks":False}
        else:
            context={"restaurants": Restaurant.objects.all().order_by("name"),
                     "items": Item.objects.all().exclude(calories__lt=calories).order_by("name"),
                     "drinks":True}

    return render(request=request, template_name=template_name, context=context)

def is_valid_queryparam(param):
    return param!= '' and param is not None

def calculator(request, restaurant_slug=""):
    items = Item.objects.all().order_by("name")
    restaurants = Restaurant.objects.all().order_by("name")
    template_name = "main/calculator.html"

    #Search Requests
    searched_items = []
    for i in range(1,21):
        searched_items.append(request.GET.get(f'itemName{i}'))

    searched_items_quantity = []
    for i in range(1,21):
        searched_items_quantity.append(request.GET.get(f'itemQuantity{i}'))

    output = calculator_order(searched_items, searched_items_quantity, len(searched_items))

    chosen_restaurant = "All"
    if restaurant_slug != "":
        items = Item.objects.filter(restaurant__slug=restaurant_slug)
        chosen_restaurant = Restaurant.objects.filter(slug=restaurant_slug)[0]
    item_list = []
    for item in items:
        item_list.append(item.name)
    options = []
    for i in range(1,21):
        options.append(i)
    context={"restaurants": restaurants,
             "items": items,
             "chosen_restaurant": chosen_restaurant,
             "item_list": item_list,
             "options": options,
             "output": output}
    return render(request, template_name, context)

def calculator_order(searched_items, searched_items_quantity, length):
    order = []
    valid_counter = 1
    for i in range(length):
        if is_valid_queryparam(searched_items[i]):
            if len((Item.objects.filter(name__iexact=searched_items[i]))) > 0:
                order.append(f"<b>{valid_counter}</b>. {Item.objects.filter(name__iexact=searched_items[i])[0]} ({searched_items_quantity[i]})")
                valid_counter+=1

    return order

def methodology(request):
    return render(request = request,
                  template_name="main/methodology.html",
                  context={"restaurants":Restaurant.objects.all(),
                           "items": Item.objects.all()})

def contact(request):
    return render(request = request,
                  template_name="main/contact.html",
                  context={"restaurants":Restaurant.objects.all(),
                           "items": Item.objects.all()})

#"items": Item.objects.all( ).exclude(calories__lte=500).order_by('protein')
