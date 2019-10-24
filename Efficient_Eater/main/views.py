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

def nutrition(request, restaurant_slug="", drinks=""):
    request = request
    template_name = "main/nutrition.html"
    chosen_restaurant = "All"
    if restaurant_slug != "":
        if drinks == "no-drinks":
            context={"restaurants": Restaurant.objects.all().order_by("name"),
                     "items": Item.objects.filter(restaurant__slug=restaurant_slug).exclude(type_of_item="drink").order_by("name"),
                     "drinks":False,
                     "chosen_restaurant": Restaurant.objects.filter(slug=restaurant_slug).order_by("name")[0]}
        else:
            context={"restaurants": Restaurant.objects.all().order_by("name"),
                     "items": Item.objects.filter(restaurant__slug=restaurant_slug).order_by("name"),
                     "drinks":True,
                     "chosen_restaurant": Restaurant.objects.filter(slug=restaurant_slug).order_by("name")[0]}
    else:
        if drinks == "no-drinks":
            context={"restaurants": Restaurant.objects.all().order_by("name"),
                     "items": Item.objects.all().exclude(type_of_item="drink").order_by("name"),
                     "drinks":False,
                     "chosen_restaurant":chosen_restaurant}
        else:
            context={"restaurants": Restaurant.objects.all().order_by("name"),
                     "items": Item.objects.all().order_by("name"),
                     "drinks":True,
                     "chosen_restaurant":chosen_restaurant}

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
    print(f"\n\n\n {searched_items} \n\n\n")
    searched_items_quantity = []
    for i in range(1,21):
        searched_items_quantity.append(request.GET.get(f'itemQuantity{i}'))

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
    order = calculator_order(searched_items, searched_items_quantity, len(searched_items))
    output = calculate_nutrition(order)
    context={"restaurants": restaurants,
             "items": items,
             "chosen_restaurant": chosen_restaurant,
             "item_list": item_list,
             "options": options,
             "order": order,
             "output": output}
    return render(request, template_name, context)

def calculator_order(searched_items, searched_items_quantity, length):
    order = []
    valid_counter = 1
    for i in range(length):
        if is_valid_queryparam(searched_items[i]):
            if len((Item.objects.filter(id=searched_items[i]))) == 1:
                order.append([valid_counter,f"{Item.objects.filter(id=searched_items[i])[0]}",searched_items_quantity[i]])
                valid_counter+=1
    return order

def calculate_nutrition(order):
    calories = 0
    total_fat = 0
    sat_fat = 0
    trans_fat = 0
    cholesterol = 0
    sodium = 0
    carbs = 0
    fiber = 0
    sugar = 0
    protein = 0
    floz = 0
    #for itemList in order:
        #print(Item.objects.filter(id=itemList[1])[0].calories)
        #calories += (itemList[2] * Item.objects.filter(name=itemList[1])[0].calories)

    print(f"\n {calories} \n")

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
