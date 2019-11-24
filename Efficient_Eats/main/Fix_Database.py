from .models import Item, Restaurant
import sqlite3
from django.template.defaultfilters import slugify
import os

def open_database_connection(database_name):
    conn = sqlite3.connect(database_name)
    return conn


def open_database_cursor(conn):
    c = conn.cursor()
    return c

database_name = "db.sqlite3"
conn = open_database_connection(database_name)
c = open_database_cursor(conn)

dirpath = os.getcwd()+'/main'


def populate_database(filename):
    with open(os.path.join(dirpath, f"{filename}"), 'r+') as f:
        line = f.readline()
        while line:
            if "@" in line and "^":
                splitline = line.split("^")
                name = splitline[0].strip("@").strip()
                slug = slugify(name)
                description = splitline[1].strip()
                logo = os.path.join(dirpath+f"\static\main\media\Logos\{slug}.png")
                r = Restaurant(name=name,
                            slug=slug,
                            description=description,
                            logo = logo)
                r.save()
                getMenuItems(r)
                print(r.name)
                print(r.slug)
                print(r.description)
                print(r.logo)
                print("%"*50)
            line = f.readline()

def getMenuItems(restaurant):
    menu = itemQuerySet(restaurant, "main_item")
    for item in menu:
        i = Item(name=item[1],
                 type_of_item=item[2],
                 calories=item[3],
                 total_fat=item[4],
                 sat_fat=item[5],
                 trans_fat=item[6],
                 cholesterol=item[7],
                 sodium=item[8],
                 carbs=item[9],
                 fiber=item[10],
                 sugar=item[11],
                 protein=item[12],
                 floz=item[13],
                 slug=slugify(item[1]),
                 restaurant=restaurant)
        i.save()
        print(f"Name: {i.name}")
        print(f"Slug: {i.slug}")
        print(f"Restaurant: {i.restaurant}")
        print(f"Type Of Item: {i.type_of_item}")
        print(f"Calories: {i.calories}")
        print(f"Protein: {i.protein}")
        print(f"Carbs: {i.carbs}")
        print(f"Total Fat: {i.total_fat}")
        print(f"Saturated Fat: {i.sat_fat}")
        print(f"Trans Fat: {i.trans_fat}")
        print(f"Cholesterol: {i.cholesterol}")
        print(f"Sodium: {i.sodium}")
        print(f"Sugar: {i.sugar}")
        print(f"Fiber: {i.fiber}")
        print(f"Fl Oz: {i.floz}")
        print('-' * 50)

def itemQuerySet(restaurant, table_name, c=c):
    c.execute(f'SELECT * FROM {table_name} WHERE restaurant =:restaurant', {'restaurant': restaurant.name})
    return c.fetchall()

def update_attribute(table_name, name, restaurant_id, attribute_type, attribute_value, conn=conn, c=c):
    with conn:
        c.execute(f'''UPDATE {table_name} SET {attribute_type} = :attribute
                    WHERE name = :name AND restaurant_id = :restaurant_id''',
                  {'name': name,
                   'restaurant_id': restaurant_id,
                   'attribute': attribute_value})

drink_args = [#"Tea",
              # "Coffee",
              # "Coke",
              # "Pepsi",
              # "Juice",
               "Lemonade"]

def fix_drinks(table_name, c=c, arguments=drink_args):
    lst = []
    for arg in arguments:
        c.execute(f'SELECT * FROM {table_name} WHERE name LIKE "%{arg}%"')
        lst.extend(c.fetchall())
    print(lst)
    for item in lst:
        print(item)
        update_attribute(table_name, item[1], item[15], "type_of_item", "drink")
        print("Attribute updated")

    print("DONE")

def fix_meals(table_name, c=c, arguments=["Steak", "Cake", "Roll", "Pizza", "Burrito", "Cheesesteak"]):
    lst = []
    for arg in arguments:
        c.execute(f'SELECT * FROM {table_name} WHERE name LIKE "%{arg}%"')
        lst.extend(c.fetchall())
    print(lst)
    for item in lst:
        print(item)
        update_attribute(table_name, item[1], item[15], "type_of_item", "meal")
        print("Attribute updated")

    print("DONE")