from bs4 import BeautifulSoup as bs
from .models import Item, Restaurant
import sqlite3
from django.template.defaultfilters import slugify
import requests
from decimal import *
import platform
import os

completed_list=["Subway",
                "McDonald's",
                "Starbucks",
                "Dunkin' Donuts",
                "Pizza Hut",
                "Burger King",
                "Taco Bell",
                "Wendy's",
                "Domino's",
                "Dairy Queen",
                "KFC",
                "Sonic",
                "Arby's",
                "Papa John's Pizza",
                "Jimmy John's",
                "Jack in the Box",
                "Popeyes",
                "Chick-fil-A",
                "Culver's",
                "Hardee's",
                "Five Guys",
                "Tim Hortons",
                "Little Caesars Pizza",
                "Panera Bread",
                "In-N-Out Burger",
                "Zaxby's",
                "White Castle",
                "Panda Express",
                "Applebees",
                "Carl's Jr."
]

foods = ["Steak",
         "Cake",
         "Roll",
         "Pizza",
         "Burrito",
         "Cheesesteak"]

drinks = ["Tea",
           "Coffee",
           "Coke",
           "Pepsi",
           "Juice",
           "Lemonade"]

dirpath = os.getcwd()+'/main'
current_dir = os.path.dirname(os.path.realpath(__file__))
if platform.system().lower() == 'windows' or platform.system().lower() == 'win32':
    OS = 'Windows'
elif platform.system().lower() == 'darwin':
    OS = 'Mac'

def open_database_connection(database_name):
    conn = sqlite3.connect(database_name)
    return conn


def open_database_cursor(conn):
    c = conn.cursor()
    return c

database_name = "db.sqlite3"
conn = open_database_connection(database_name)
c = open_database_cursor(conn)

MENU_SITE_URL = "https://www.menuwithprice.com/nutrition/"

def getMenuItemsFromRestaurant(restaurant):
    page_index = 1
    page_exists = True
    menu = []
    while page_exists:
            url = f'{MENU_SITE_URL}{restaurant.slug}/p/{page_index}'
            print(url)
            page_source_menu = requests.get(url).content
            soup = bs(page_source_menu, "html.parser")
            if len(soup.find_all('tr')) > 0:
                for item in soup.find_all('tr'):
                    if len(item.find_all('th')) == 0:
                        page_source_item = requests.get(item.find('a')['href']).content
                        item_soup = bs(page_source_item, "html.parser")
                        item_object = createItemFromData(item_soup, restaurant)
                        print("Creating item")
                        menu.append(item_object)
            else:
                print(f"Finished compiling Full Menu for {restaurant}")
                page_exists = False
            page_index += 1

    return menu

def populate_database(filename):
    with open(os.path.join(dirpath, f"{filename}"), 'r+') as f:
        line = f.readline()
        while line:
            if "@" in line and "^":
                splitline = line.split("^")
                name = splitline[0].strip("@").strip()
                if name not in completed_list:
                    slug = slugify(name)
                    description = splitline[1].strip()
                    logo = f"\static\main\media\Logos\{slug}.png"
                    r = Restaurant(name=name,
                                   slug=slug,
                                   description=description,
                                   logo = logo)
                    r.save()
                    getMenuItemsFromRestaurant(r)
                    print(r.name)
                    print(r.slug)
                    print(r.description)
                    print(r.logo)
                    print("%"*50)
            line = f.readline()


def createItemFromData(soup, restaurant):

    name = soup.find('dd').text
    name = name.replace('®','')
    name = name.replace('©','')
    type_of_item = 'meal'
    floz = 0
    for dd in soup.find_all('dd'):
        if 'fl oz' in dd.text:
            floz = Decimal(dd.text.split(' ')[-3])
            type_of_item = 'drink'
        for item in drinks:
            if item in name:
                type_of_item = 'drink'
        for item in foods:
            if item in name:
                type_of_item = 'meal'
        for metric in dd.find_all('li'):
            if "Calories " in metric.text:
                calories = int(metric.text.split(' ')[-1])
            elif "Total Fat" in metric.text:
                total_fat = Decimal(metric.text.split(' ')[-1].strip('g'))
            elif "Saturated Fat" in metric.text:
                sat_fat = Decimal(metric.text.split(' ')[-1].strip('g'))
            elif "Trans Fat" in metric.text:
                trans_fat = Decimal(metric.text.split(' ')[-1].strip('g'))
            elif "Cholesterol" in metric.text:
                cholesterol = Decimal(metric.text.split(' ')[-1].strip('mg'))
            elif "Sodium" in metric.text:
                sodium = Decimal(metric.text.split(' ')[-1].strip('mg'))
            elif "Carbohydrates" in metric.text:
                carbs = Decimal(metric.text.split(' ')[-1].strip('g'))
            elif "Fiber" in metric.text:
                fiber = Decimal(metric.text.split(' ')[-1].strip('g'))
            elif "Sugar" in metric.text:
                sugar = Decimal(metric.text.split(' ')[-1].strip('g'))
            elif "Protein" in metric.text:
                protein = Decimal(metric.text.split(' ')[-1].strip('g'))
    item = Item(name=name,
                type_of_item=type_of_item,
                calories=calories,
                total_fat=total_fat,
                sat_fat=sat_fat,
                trans_fat=trans_fat,
                cholesterol=cholesterol,
                sodium=sodium,
                carbs=carbs,
                fiber=fiber,
                sugar=sugar,
                protein=protein,
                floz=floz,
                slug=slugify(name),
                restaurant=restaurant)
    item.save()
    print(f"Name: {item.name}")
    print(f"Slug: {item.slug}")
    print(f"Restaurant: {item.restaurant}")
    print(f"Type Of Item: {item.type_of_item}")
    print(f"Calories: {item.calories}")
    print(f"Protein: {item.protein}")
    print(f"Carbs: {item.carbs}")
    print(f"Total Fat: {item.total_fat}")
    print(f"Saturated Fat: {item.sat_fat}")
    print(f"Trans Fat: {item.trans_fat}")
    print(f"Cholesterol: {item.cholesterol}")
    print(f"Sodium: {item.sodium}")
    print(f"Sugar: {item.sugar}")
    print(f"Fiber: {item.fiber}")
    print(f"Fl Oz: {item.floz}")
    print("O"*50)
    print("Saved Item to Database")
    print("O"*50)
    return item

def main():
    menu=[]
    with open(os.path.join(current_dir, 'Restaurants'), 'r') as file:
        line = file.readline()
        while line:
            restaurant = line.strip()
            print(f"Gathering items from {restaurant}")
            menu.extend(getMenuItemsFromRestaurant(restaurant))
            line = file.readline()
    print(len(menu))
    '''
    menu.extend(getMenuItemsFromRestaurant("McDonald's"))
    new_menu= (sortByMetric(menu, metric='calories', descending=True))
    for item in new_menu:
        print(item)
        print(item.calories)
    print('-'*50)
    new_menu = (sortByMetric(menu, metric='protein_efficiency', descending=True))
    for item in new_menu:
        print(item)
        print(item.protein_efficiency)
    print('-'*50)
    new_menu = (sortByMetric(menu, metric='sugar_per_floz', descending=True))
    for item in new_menu:
        print(item)
        print(item.sugar_per_floz)
    '''

if __name__ == "__main__":
    main()