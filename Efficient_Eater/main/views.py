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
    #print(f"\n\n\n {searched_items} \n\n\n")
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
    order = calculator_order(searched_items, searched_items_quantity, len(searched_items), chosen_restaurant)
    output = calculate_nutrition(order)
    context={"restaurants": restaurants,
             "items": items,
             "chosen_restaurant": chosen_restaurant,
             "item_list": item_list,
             "options": options,
             "order": order,
             "output": output}
    return render(request, template_name, context)

def calculator_order(searched_items, searched_items_quantity, length, chosen_restaurant):
    order = []
    valid_counter = 1
    for i in range(length):
        if is_valid_queryparam(searched_items[i]):
            if chosen_restaurant != "All":
                item_name = searched_items[i]
                item_restaurant=chosen_restaurant
            else:
                itemNameComponents = searched_items[i].split(' | ')
                item_name = searched_items[i].split(' | ')[0]
                item_restaurant = "Invalid Restaurant"
                if len(itemNameComponents) > 1:
                    item_restaurant = searched_items[i].split(' | ')[1]

            itemQuery = Item.objects.filter(name__iexact=item_name).filter(restaurant__name__iexact=item_restaurant)
            if len(itemQuery) == 1:
                item = itemQuery[0]
                itemQuantity = int(searched_items_quantity[i])
                restaurant = Restaurant.objects.filter(name__iexact=item_restaurant)[0]
                attribute_inputName="inputName"+str(valid_counter)
                attribute_itemName="itemName"+str(valid_counter)
                attribute_itemQuantity="itemQuantity"+str(valid_counter)
                order.append([valid_counter, #Number of valid item in order #0
                              f"{item}", #Name of item #1
                              int(itemQuantity), #Quantity of item #2
                              item.id, #ID of item #3
                              item.calories*itemQuantity, #Calories of item in the quantity ordered #4
                              item.carbs*itemQuantity, #Carbs of item in the quantity ordered #5
                              item.total_fat*itemQuantity, #Fats of item in the quantity ordered #6
                              item.protein*itemQuantity, #Protein of item in the quantity ordered #7
                              restaurant.logo, #Logo of restaurant of the food item #8
                              attribute_inputName, #attribute id of item #9
                              attribute_itemName, #attribute name of item #10
                              attribute_itemQuantity, #attribute name for select of item #11
                              restaurant.name, #name of restaurant of item #12
                              ])
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
    for itemList in order:
        item = Item.objects.filter(id=itemList[3])[0]
        itemQuantity = int(itemList[2])
        #Calculate all nutritional information
        calories+=(itemList[4])
        total_fat+=(itemList[6])
        sat_fat+=(itemQuantity*item.sat_fat)
        trans_fat+=(itemQuantity*item.cholesterol)
        cholesterol+=(itemQuantity*item.cholesterol)
        sodium+=(itemQuantity*item.sodium)
        carbs+=(itemList[5])
        fiber+=(itemQuantity*item.fiber)
        sugar+=(itemQuantity*item.sugar)
        protein+=(itemList[7])
        if item.type_of_item == "drink":
            floz = (itemQuantity*item.floz)
        else:
            floz = None

    results = {
        "calories": calories,
        "total_fat": total_fat,
        "sat_fat": sat_fat,
        "trans_fat": trans_fat,
        "cholesterol": cholesterol,
        "sodium": sodium,
        "carbs": carbs,
        "fiber": fiber,
        "sugar": sugar,
        "protein": protein,
        "floz": floz
    }
    return results

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

