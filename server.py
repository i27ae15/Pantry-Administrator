# Flask imports
from flask.helpers import flash
from flask_bootstrap import Bootstrap
from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.sql.expression import false
from werkzeug.security import generate_password_hash, check_password_hash

# Sqlalchemy
from sqlalchemy.sql.sqltypes import Integer, String
from sqlite3 import Connection as SQLite3connection
from sqlalchemy import event
from sqlalchemy.engine import Engine
from data_base import engine

# DataBase imports 
from data_base import db
from create_new_entries import _create_new_entries
from models import _FoodsInStock, _FoodExpenses, _BeveragesInStock, _BeverageExpenses, _BeverageItemsInfo, _FoodItemsInfo, _BreakfastsInStock, _BreakfastExpenses, _LunchExpenses, _LunchInStock, _SnackExpenses, _SnacksInStock, _CerealExpenses, _CerealsInStock, _FruitExpenses, _FruitsInStock, _People, _WaterExpenses, _WatersInStock, _SodaExpenses, _SodasInStock, _JuiceExpenses, _OtherFoodsExpenses, _OtherFoodsInStock, _CookiesInStock,  _ChocolatesInStock,  _CookiesExpenses, _ChocolatesExpenses, _OtherBeveragesExpenses, _OtherBeveragesInStock, _JuicesInStock, _User 

# other imports
# remeber to change the ofline stuff to online 
from datetime import date, datetime, timedelta
import os

NOW = datetime.now()
TODAY = NOW.date()

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['SECRET_KEY'] = "(*&a90a8r)(fa89k" # os.environ.get('SECRET_KEY', 'hsd@fweks@$^fiwskq')
app.config['WTF_CSRF_ENABLED'] = True
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

# Constants
# App configuration --------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///DataBase.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

@event.listens_for(Engine, 'connect')
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foregin_keys=ON')
        cursor.close()
    

@app.template_filter()
def jinja_get_weekday(date):
    # date = get_date_from_string(date)
    return day_to_weekday_name(date.isoweekday())


@app.template_filter()
def jinja_translate_item_type(element_type:String):
    element_type = element_type.upper()

    if element_type == 'SNACK' or element_type == 'CEREAL' or element_type == 'CHOCOLATE':
        return element_type.capitalize()

    if element_type == 'BREAKFAST':
        return 'Desayuno'
    elif element_type == 'LUNCH':
        return 'Almuerzo'
    elif element_type == 'FRUIT':
        return 'Fruta'
    elif element_type == 'COOKIE':
        return 'Galleta'

    elif element_type == 'WATER':
        return 'Agua'
    elif element_type == 'JUICE':
        return 'Jugo'
    elif element_type == 'SODA':
        return 'Refresco'

    
    elif element_type == 'OTHER':
        return 'Otro'
    
    raise ValueError(f'the element_type provided is not a valid type in the data base: {element_type}')


@login_manager.user_loader
def load_user(user_id):
    return _User.query.get(int(user_id))
  

#-----------------------------------------------------------------------------------------------------------
# classes 
class ItemsInStockInformation:
    """
        A class to store the amount of differents properties that the different types of food can have.
    """
    def __init__(self, main_type, itemType, items_expenses=[], items_in_stock=[], initial_average_stock=[],         final_average_stock=[], daily_average_consumption=[], total_consumed=[]):
        self.main_type = main_type 
        self.itemType = itemType
        
        self.items_expenses = items_expenses
        self.items_in_stock = items_in_stock
        
        self.initial_average_stock = initial_average_stock
        self.final_average_stock = final_average_stock
        
        self.daily_average_consumption = daily_average_consumption
        self.total_consumed = total_consumed


class ItemInformation:
    """
    
    This class is for storing the information related to the objects that were deleted but are needed to be shown in
    the between dates report
    
    """
    def __init__(self, dates:list, main_type:String, sub_type:String, _id:int, name:String, initial_stock=0, final_stock=0, total_consumed=0, deleted_date=None, added_date=None):
        self._id = _id
        self.name = name
        
        self.dates = dates
        self.deleted_date = deleted_date
        self.added_date = added_date

        self.main_type = main_type
        self.sub_type = sub_type

        self.initial_stock = initial_stock
        self.initial_stock_avg = 0

        self.final_stock = final_stock
        self.final_stock_avg = 0

        self.total_consumed = total_consumed
        self.daily_consumed = 0

# functions-----------------------------------------------------

def get_date_next_previous(date, previous_day=False):

    date_time_obj = get_date_from_string(date)
    
    if previous_day:
        date = (date_time_obj - timedelta(1)).date()
    else:
        date = (date_time_obj + timedelta(1)).date()

    return date


def get_date_from_string(date:String, format='%Y-%m-%d'):
    return datetime.strptime(date, format)


def day_to_weekday_name(day:Integer, english=True):
    
    if english:
        if day == 1:
            return 'Monday'
        if day == 2:
            return 'Tuesday'
        if day == 3:
            return 'Wednesday'
        if day == 4:
            return 'Thursday'
        if day == 5:
            return 'Friday'
        if day == 6:
            return 'Saturday'
        if day == 7:
            return 'Sunday'
    else:
        if day == 1:
            return 'Lunes'
        if day == 2:
            return 'Martes'
        if day == 3:
            return 'Miercoles'
        if day == 4:
            return 'Jueves'
        if day == 5:
            return 'Viernes'
        if day == 6:
            return 'Sabado'
        if day == 7:
            return 'Domingo'


def get_dates_between(start_date, end_date):

    """
    
    Return => list of datetime.date objects 
    
    """

    # start_date = get_date_from_string(start_date, format='%d-%m-%Y').date()
    end_date = get_date_from_string(end_date, format='%d-%m-%Y').date()

    list_of_dates = [get_date_from_string(start_date, format='%d-%m-%Y').date()]
    n = 1

    while True:

        date_time_obj = get_date_from_string(start_date, format='%d-%m-%Y')
        current_date = (date_time_obj + timedelta(n)).date()
        list_of_dates.append(current_date)
        n += 1

        if current_date == end_date:
            return list_of_dates


def get_averages_from_table(table, dates):
    total = 0
    for date in dates:
        total += table.query.get(date).total

    if total == 0 or len(dates) == 0:
        return 0
    else:
        return round(total / len(dates))
        
    
def get_boolean(variable):
    if str(variable).upper() == 'TRUE' or str(variable) == '1':
        return True
    return False

       
def translate_item_type(element_type:String, from_espanish_to_english=False, from_english_to_spanish=False):
    element_type = element_type.upper()

    if element_type == 'SNACK' or element_type == 'CEREAL' or element_type == 'CHOCOLATE':
        return element_type

    if from_espanish_to_english:
        if element_type == 'DESAYUNO':
            return 'BREAKFAST'
        elif element_type == 'ALMUERZO':
            return 'LUNCH'
        elif element_type == 'FRUTA':
            return 'FRUIT'
        elif element_type == 'GALLETA':
            return 'COOKIE'

        elif element_type == 'AGUA':
            return 'WATER'
        elif element_type == 'JUGO':
            return 'JUICE'
        elif element_type == 'REFRESCO':
            return 'SODA'

        elif 'OTRO' in element_type:
            return 'OTHER'

    elif from_english_to_spanish:
        if element_type == 'BREAKFAST':
            return 'DESAYUNO'
        elif element_type == 'LUNCH':
            return 'ALMUERZO'
        elif element_type == 'FRUIT':
            return 'FRUTA'
        elif element_type == 'COOKIE':
            return 'GALLETA'

        elif element_type == 'WATER':
            return 'AGUA'
        elif element_type == 'JUICE':
            return 'JUGO'
        elif element_type == 'SODA':
            return 'REFRESCO'

        
        elif element_type == 'OTHER':
            return 'OTRO'
    
    raise ValueError(f'the element_type provided is not a valid type in the data base: {element_type}')


def create_main_tables(date, last_food_table, last_beverage_table):
    new_food = _FoodsInStock(
            date = date, 
            total_breakfasts = last_food_table.total_breakfasts,
            total_lunch = last_food_table.total_lunch,
            total_cereals = last_food_table.total_cereals,
            total_snacks = last_food_table.total_snacks,
            total_fruits = last_food_table.total_fruits,
            total_chocolates = last_food_table.total_chocolates,
            total_cookies = last_food_table.total_cookies,
            total_others = last_food_table.total_others,
            total = last_food_table.total,
            initial_stock = last_food_table.initial_stock,

            current_breakfast_id = last_food_table.current_breakfast_id,
            current_lunch_id = last_food_table.current_lunch_id,
            current_snack_id = last_food_table.current_snack_id,
            current_cereal_id = last_food_table.current_cereal_id,
            current_fruit_id = last_food_table.current_fruit_id,
            current_chocolate_id = last_food_table.current_chocolate_id,
            current_cookie_id = last_food_table.current_cookie_id,
            current_other_id = last_food_table.current_other_id,

            total_breakfasts_added = 0,
            total_lunch_added = 0,
            total_snacks_added = 0,
            total_cereals_added = 0,
            total_fruits_added = 0,
            total_chocolates_added = 0,
            total_cookies_added = 0,
            total_others_added = 0,

            total_food_added = 0
        )
    db.add(new_food)
    
    new_beverage = _BeveragesInStock(
        date = date, 
        total_sodas = last_beverage_table.total_sodas,
        total_juices = last_beverage_table.total_juices,
        total_waters = last_beverage_table.total_waters,
        total_others = last_beverage_table.total_others,
        total = last_beverage_table.total,
        initial_stock = last_beverage_table.initial_stock,

        current_water_id = last_beverage_table.current_water_id,
        current_juice_id = last_beverage_table.current_juice_id,
        current_soda_id = last_beverage_table.current_soda_id,
        current_other_id = last_beverage_table.current_other_id,

        total_waters_added = 0,
        total_juices_added = 0,
        total_sodas_added = 0,
        total_others_added = 0,

        total_beverages_added = 0
    )
    db.add(new_beverage)

    new_food_expenses = _FoodExpenses(
        date = date,
        total_breakfasts = 0,
        total_lunch = 0,
        total_snacks = 0,
        total_cereals = 0,
        total_fruits = 0,
        total_chocolates = 0,
        total_cookies = 0,
        total_others = 0,
        total = 0
    )
    db.add(new_food_expenses)

    new_beverages_expenses = _BeverageExpenses(
        date = date,
        total_sodas = 0,
        total_waters = 0,
        total_juices = 0,
        total_others = 0,
        total = 0
    )
    db.add(new_beverages_expenses)
    
    db.commit()


def create_tables(date, last_food_table, last_beverage_table):

    tables_in_last_food_stock = [last_food_table.breakfasts, last_food_table.lunch, last_food_table.cereals, last_food_table.snacks, last_food_table.fruits, last_food_table.chocolates, last_food_table.cookies, last_food_table.others]

    tables_in_last_beverage_stock = [last_beverage_table.sodas, last_beverage_table.juices, last_beverage_table.water, last_beverage_table.others]

    # we need to copy each table of the last date so we start with the tables with a reationship to the food data base

    list_of_food_tables = [_BreakfastsInStock, _LunchInStock, _CerealsInStock, _SnacksInStock, _FruitsInStock, _ChocolatesInStock, _CookiesInStock, _OtherFoodsInStock]
    for index, tables in enumerate(tables_in_last_food_stock):           
        for table in tables:              
            new_item = list_of_food_tables[index](
                name = table.name,
                item_id = table.item_id,
                initial_stock = table.stock, 
                added = 0,
                stock = table.stock, 
                date = date 
            )
            db.add(new_item)

    list_of_food_expenses_tables = [_BreakfastExpenses, _LunchExpenses, _CerealExpenses, _SnackExpenses, _FruitExpenses, _ChocolatesExpenses, _CookiesExpenses, _OtherFoodsExpenses]
    for index, tables in enumerate(tables_in_last_food_stock):           
        for table in tables:              
            new_item = list_of_food_expenses_tables[index](
                name = table.name,
                consumption = 0,
                date = date,
                item_id = table.item_id
            )
            db.add(new_item)

    # and then the tables that contains the data from beverages

    list_of_beverages_tables = [_SodasInStock, _JuicesInStock, _WatersInStock, _OtherBeveragesInStock]
    for index, tables in enumerate(tables_in_last_beverage_stock):
        for table in tables:
            new_item = list_of_beverages_tables[index](
                name = table.name,
                item_id = table.item_id,
                initial_stock = table.stock, 
                added = 0,
                stock = table.stock, 
                date = date 
            )
            db.add(new_item)

    list_of_beverages_expenses_tables = [_SodaExpenses, _JuiceExpenses, _WaterExpenses, _OtherBeveragesExpenses]
    for index, tables in enumerate(tables_in_last_beverage_stock):           
        for table in tables:              
            new_item = list_of_beverages_expenses_tables[index](
                name = table.name,
                consumption = 0,
                date = date,
                item_id = table.id
            )
            db.add(new_item)


def create_new_date_in_db(today=TODAY):
    # we create the new date in the data base
    food = _FoodsInStock.query.get(today)

    if food is not None:
         return f'The table with date: {today} has already been created'

    # create the new date in the data base
    # last_food_table = db.query(_FoodsInStock).order_by(_FoodsInStock.id.desc()).first()
    try:
        last_food_table = db.query(_FoodsInStock).order_by(_FoodsInStock.date)[-1]
        last_beverage_table = db.query(_BeveragesInStock).order_by(_BeveragesInStock.date)[-1]
    except IndexError:
        # if we run this and there is an index error it will mean that there is no data base created yet so we have to create it 
        _create_new_entries()
        return 'New entries created'

    date_to_evaluate = (last_food_table.date + timedelta(1))

    while date_to_evaluate != today:
        create_main_tables(date_to_evaluate, last_food_table, last_beverage_table)
        create_tables(date_to_evaluate, last_food_table, last_beverage_table)
        date_to_evaluate = (date_to_evaluate + timedelta(1))

    create_main_tables(date_to_evaluate, last_food_table, last_beverage_table)
    create_tables(date_to_evaluate, last_food_table, last_beverage_table)

    db.commit()
    return f'The table with date: {today} was successfully created'


def get_averages_for_each_item(list_of_related_tables, worked_days, consumption=False):
    
    if consumption:
        list_of_total = [] 
        list_of_averages = []
        # the list of total is going to be used to store the total consumption of each item, so that we can take the average at the end
        for index, tables in enumerate(list_of_related_tables):
            for n in range(len(tables)):
                # comparing the n to be able to know if we finish counting the tables to evaluate 
                # if n if bigger than then len of list_of_total that will mean that we haven't count all the 
                # items, but if the len of list_of_total is bigger will mean that we counted all the items to evaluate so that we can start to add the current values to them in the list
                if n >= len(list_of_total):
                    list_of_total.append(tables[n].consumption)
                else:
                    list_of_total[n] += tables[n].consumption
                    if index + 1 == len(list_of_related_tables):
                        list_of_averages.append(round(list_of_total[n] / len(worked_days)))

        if len(worked_days) == 1 and len(list_of_total) > 0:      
            for n in range(len(list_of_total)):
                list_of_averages.append(round(list_of_total[n] / 1))
                
        if len(list_of_total) < 0:
            list_of_total = None
        
        if len(list_of_averages) < 0:
            list_of_averages = None

        return list_of_total, list_of_averages

    else:
        initial_stock = [] 
        final_stock = [] 
        initial_stock_averages = []
        final_stock_averages = []

        for index, related_tables in enumerate(list_of_related_tables):
            # getting the n index in the main tables
            # if the n index is bigger or equal to the len of the initital_stock, it will mean that 
            # no data has been introduced in the list, so we append the curren valute to the different lists
            for n in range(len(related_tables)):
                if n >= len(initial_stock):
                    initial_stock.append(related_tables[n].initial_stock)
                    final_stock.append(related_tables[n].stock)
                # others wise, it means that we have already gone through the entire table and we are here again to
                # add more date to the lists so we sum the new date in the n position 
                else:
                    initial_stock[n] += related_tables[n].initial_stock
                    final_stock[n] += related_tables[n].stock

                    if index + 1 == len(list_of_related_tables):

                        initial_stock_averages.append(round(initial_stock[n] / len(worked_days)))
                        final_stock_averages.append(round(final_stock[n] / len(worked_days)))

        if len(worked_days) == 1 and len(initial_stock) > 0:
            
            for n in range(len(initial_stock)):

                initial_stock_averages.append(round(initial_stock[n] / 1))
                final_stock_averages.append(round(final_stock[n] / 1))

        return initial_stock_averages, final_stock_averages


def get_averages(food_classes, beverages_classes, worked_dates, food_names, beverages_names):
    
    for name in food_names:
        
        food_classes[name].total_consumed, food_classes[name].daily_average_consumption = get_averages_for_each_item(food_classes[name].items_expenses, worked_dates, True)

        food_classes[name].initial_average_stock, food_classes[name].final_average_stock = get_averages_for_each_item(food_classes[name].items_in_stock, worked_dates)

    
    for name in beverages_names:

        beverages_classes[name].total_consumed, beverages_classes[name].daily_average_consumption = get_averages_for_each_item(beverages_classes[name].items_expenses, worked_dates, True)

        beverages_classes[name].initial_average_stock, beverages_classes[name].final_average_stock = get_averages_for_each_item(beverages_classes[name].items_in_stock, worked_dates)


def parse_items_dictionary(items_dictionary):
    if not bool(items_dictionary):
        return None

    
    objects = {
        'BREAKFAST':[],
        'LUNCH':[],
        'SNACK':[],
        'CEREAL':[],
        'FRUIT':[],

        'WATER':[],
        'JUICE':[],
        'SODA':[],
        'OTHER':[]
    }

    for item in items_dictionary:
        current_item = items_dictionary[item]

        objects[current_item.sub_type].append(current_item)
    
    del items_dictionary

    return objects


def get_deleted_items_averages(items, start_date, dates, food=True):
    items_dict = {}

    tables = {
        'food':{
            'BREAKFAST': [_BreakfastsInStock, _BreakfastExpenses],
            'LUNCH': [_LunchInStock, _LunchExpenses],
            'SNACK': [_SnacksInStock, _SnackExpenses],
            'CEREAL': [_CerealsInStock, _CerealExpenses],
            'FRUIT': [_FruitsInStock, _FruitExpenses],
            'COOKIES': [_CookiesInStock, _CookiesExpenses],
            'CHOCOLATE': [_ChocolatesInStock, _ChocolatesExpenses],
            'OTHER': [_OtherFoodsInStock, _OtherFoodsExpenses]
        },
        'beverages':{
            'WATER': [_WatersInStock, _WaterExpenses],
            'SODA': [_SodasInStock, _SodaExpenses],
            'JUICE': [_JuicesInStock, _JuiceExpenses],
            'OTHER': [_OtherBeveragesInStock, _OtherBeveragesExpenses]
        } 
    }

    if food:
        main_type = 'food'
    else:
        main_type = 'beverages'

    for item in items:
        # we are going to create a new object that will store the values of the items 
        day_before_delated = (get_date_from_string(item.deleted_date) - timedelta(1)).date() 
        between_dates = get_dates_between(start_date, day_before_delated)
        # we must to clean the dates comparing them with the given in the arguments since they the between_dates
        # variable can contain dates that are no-working days, so take care of them in the following for loop
        worked_dates = []
        for date in between_dates:
            if date in dates:
                worked_dates.append(date)
        
        # initilazing the object and storing it in the dictionary of objects 
        items_dict[item.name] = ItemInformation(worked_dates, main_type, item.type, int(item.item_id), item.name, deleted_date=item.deleted_date)
    
        # once we have created the object we need to get the averages that we need
        # with a query in the items that are in the data base we are going to be able to get that information 

        # we select the node from the dict of items
        current_node = items_dict[item.name]
        for date in current_node.dates:
            # we select the current item from the corresponding table (stock table)
            try:
                current_in_stock_item = tables[current_node.main_type][current_node.sub_type][0].query.filter_by(item_id=current_node._id, date=date).one()
            except:
                continue

            current_node.initial_stock += current_in_stock_item.initial_stock
            current_node.final_stock += current_in_stock_item.stock
            
            # now we need the expenses data from the other tables
            current_expenses_item = tables[current_node.main_type][current_node.sub_type][1].query.filter_by(item_id=current_node._id, date=date).one()

            current_node.total_consumed += current_expenses_item.consumption
    
        # once done that we are good to calucate the average within the gived dates

        current_node.initial_stock_avg = round(current_node.initial_stock / len(current_node.dates))
        current_node.final_stock_avg = round(current_node.final_stock / len(current_node.dates))
        current_node.daily_consumed = round(current_node.total_consumed / len(current_node.dates))

    # we need to parse this ditcionary since the items on it are desorganazied

    return parse_items_dictionary(items_dict) 


def get_items_added_between_dates_averages(items):
    if not bool(items):
        return None

    objects = {
        'BREAKFAST':[],
        'LUNCH':[],
        'SNACK':[],
        'CEREAL':[],
        'FRUIT':[],
        'COOKIE':[],
        'CHOCOLATE':[],
        'OTHERF':[],

        'WATER':[],
        'JUICE':[],
        'SODA':[],
        'OTHERB':[]
    }

    for item in items:
        current_node = items[item]

        current_node.initial_stock_avg = round(current_node.initial_stock / len(current_node.dates))
        current_node.final_stock_avg = round(current_node.final_stock / len(current_node.dates))
        current_node.daily_consumed = round(current_node.total_consumed / len(current_node.dates))

        if current_node.main_type == 'food' and current_node.sub_type == 'other':
            key = 'OTHERF'
        elif current_node.main_type == 'beverage' and current_node.sub_type == 'other':
            key = 'OTHERB'
        else:
            key = current_node.sub_type.upper()

        objects[key].append(current_node)
        
    del items
    return objects
        

def update_items_in_stock(items, classes):
    food_classes = [_BreakfastsInStock, _LunchInStock, _SnacksInStock, _CerealsInStock, _FruitsInStock, _CookiesInStock, _ChocolatesInStock, _OtherFoodsInStock]   
    beverages_classes = [_WatersInStock, _JuicesInStock, _SodasInStock, _OtherBeveragesInStock]
    date = TODAY

    for item_index, item in enumerate(items):
        # 0, water_info
        for table_index, id in enumerate(item['id']):
            #0, 1
            item_to_evaluate = item['value'][table_index].strip()
            
            if item_to_evaluate == '' or item_to_evaluate == '-':
                continue
            
            if int(item_to_evaluate) != 0:
                db.query(classes[item_index]).filter(classes[item_index].id == int(id)).update({'added':classes[item_index].added + item['value'][table_index]})

                db.query(classes[item_index]).filter(classes[item_index].id == int(id)).update({'stock':classes[item_index].stock + item['value'][table_index]})
            
            if classes[item_index] in food_classes:
                table_to_increase = _FoodsInStock
                total_added_to_increase = 'total_food_added'

                if classes[item_index] == food_classes[0]:
                    field_to_increase_added = 'total_breakfasts_added'
                    field_to_increase_stock = 'total_breakfasts'

                    field_in_table_added = _FoodsInStock.total_breakfasts_added
                    field_in_table_stock = _FoodsInStock.total_breakfasts

                elif classes[item_index] == food_classes[1]:
                    field_to_increase_added = 'total_lunch_added'
                    field_to_increase_stock = 'total_lunch'

                    field_in_table_added = _FoodsInStock.total_lunch_added
                    field_in_table_stock = _FoodsInStock.total_lunch
                
                elif classes[item_index] == food_classes[2]:
                    field_to_increase_added = 'total_snacks_added'
                    field_to_increase_stock = 'total_snacks'

                    field_in_table_added = _FoodsInStock.total_snacks_added
                    field_in_table_stock = _FoodsInStock.total_snacks
            
                elif classes[item_index] == food_classes[3]:
                    field_to_increase_added = 'total_cereals_added'
                    field_to_increase_stock = 'total_cereals'

                    field_in_table_added = _FoodsInStock.total_cereals_added
                    field_in_table_stock = _FoodsInStock.total_cereals

                elif classes[item_index] == food_classes[4]:
                    field_to_increase_added = 'total_fruits_added'
                    field_to_increase_stock = 'total_fruits'

                    field_in_table_added = _FoodsInStock.total_fruits_added
                    field_in_table_stock = _FoodsInStock.total_fruits
                
                elif classes[item_index] == food_classes[5]:
                    field_to_increase_added = 'total_cookies_added'
                    field_to_increase_stock = 'total_cookies'

                    field_in_table_added = _FoodsInStock.total_cookies_added
                    field_in_table_stock = _FoodsInStock.total_cookies

                elif classes[item_index] == food_classes[6]:
                    field_to_increase_added = 'total_chocolates_added'
                    field_to_increase_stock = 'total_chocolates'

                    field_in_table_added = _FoodsInStock.total_chocolates_added
                    field_in_table_stock = _FoodsInStock.total_chocolates

                elif classes[item_index] == food_classes[7]:
                    field_to_increase_added = 'total_others_added'
                    field_to_increase_stock = 'total_others'

                    field_in_table_added = _FoodsInStock.total_others_added
                    field_in_table_stock = _FoodsInStock.total_others

                db.query(table_to_increase).filter(table_to_increase.date == date).update({total_added_to_increase:table_to_increase.total_food_added + item['value'][table_index]})

                db.query(table_to_increase).filter(table_to_increase.date == date).update({'total':table_to_increase.total + item['value'][table_index]})

            else:
                table_to_increase = _BeveragesInStock
                total_added_to_increase = 'total_beverages_added'

                if classes[item_index] == beverages_classes[0]:
                    field_to_increase_added = 'total_waters_added'
                    field_to_increase_stock = 'total_waters'

                    field_in_table_added = _BeveragesInStock.total_waters_added
                    field_in_table_stock = _BeveragesInStock.total_waters

                elif classes[item_index] == beverages_classes[1]:
                    field_to_increase_added = 'total_juices_added'
                    field_to_increase_stock = 'total_juices'

                    field_in_table_added = _BeveragesInStock.total_juices_added
                    field_in_table_stock = _BeveragesInStock.total_juices
                
                elif classes[item_index] == beverages_classes[2]:
                    field_to_increase_added = 'total_sodas_added'
                    field_to_increase_stock = 'total_sodas'

                    field_in_table_added = _BeveragesInStock.total_sodas_added
                    field_in_table_stock = _BeveragesInStock.total_sodas
            
                elif classes[item_index] == beverages_classes[3]:
                    field_to_increase_added = 'total_others_added'
                    field_to_increase_stock = 'total_others'

                    field_in_table_added = _BeveragesInStock.total_others_added
                    field_in_table_stock = _BeveragesInStock.total_others
                
                db.query(table_to_increase).filter(table_to_increase.date == date).update({total_added_to_increase:table_to_increase.total_beverages_added + item['value'][table_index]})

                db.query(table_to_increase).filter(table_to_increase.date == date).update({'total':table_to_increase.total + item['value'][table_index]})
            
            db.query(table_to_increase).filter(table_to_increase.date == date).update({field_to_increase_added:field_in_table_added + item['value'][table_index]})

            db.query(table_to_increase).filter(table_to_increase.date == date).update({field_to_increase_stock:field_in_table_stock + item['value'][table_index]})
  
    db.commit()


def add_items_to_data_base(date, item_type, stock, item_name, number_of_rows, food, multiple_days=False, item_added=True):
    last_food_table = _FoodsInStock.query.get(TODAY)
    last_beverage_table = _BeveragesInStock.query.get(TODAY)

    # we need to check if the day is in the dateBase is None, if it is not, then we create a new entry in the database
    if _FoodsInStock.query.get(date) is None:
        _create_new_entries(date)

    total_food_added = 0
    total_beverages_added = 0
    
    tables = {
        'Breakfast': [_BreakfastsInStock, _BreakfastExpenses],
        'Lunch': [_LunchInStock, _LunchExpenses],
        'Snack': [_SnacksInStock, _SnackExpenses],
        'Cereal': [_CerealsInStock, _CerealExpenses],
        'Fruit': [_FruitsInStock, _FruitExpenses],
        'Cookie': [_CookiesInStock, _CookiesExpenses],
        'Chocolate': [_ChocolatesInStock, _ChocolatesExpenses],
        'OtherC': [_OtherFoodsInStock, _OtherFoodsExpenses],

        'Water': [_WatersInStock, _WaterExpenses],
        'Soda': [_SodasInStock, _SodaExpenses],
        'Juice': [_JuicesInStock, _JuiceExpenses],
        'OtherB': [_OtherBeveragesInStock, _OtherBeveragesExpenses],
    }
    # the index == 1 in the dicticonary key is used the store the total amount of that item added to the data base in this date 
    table_fields = {
        'Breakfast': [last_food_table.current_breakfast_id, 0, 'current_breakfast_id'],
        'Lunch': [last_food_table.current_lunch_id, 0, 'current_lunch_id'],
        'Snack': [last_food_table.current_snack_id, 0, 'current_snack_id'],
        'Cereal': [last_food_table.current_cereal_id, 0, 'current_cereal_id'],
        'Fruit': [last_food_table.current_fruit_id, 0, 'current_fruit_id'],
        'Chocolate': [last_food_table.current_cookie_id, 0, 'current_cookie_id'],
        'Cookie': [last_food_table.current_chocolate_id, 0, 'current_chocolate_id'],
        'OtherC': [last_food_table.current_other_id, 0, 'current_other_id'],

        'Water': [last_beverage_table.current_water_id, 0, 'current_water_id'],
        'Juice': [last_beverage_table.current_juice_id, 0, 'current_juice_id'],
        'Soda': [last_beverage_table.current_soda_id, 0, 'current_soda_id'],
        'OtherB': [last_beverage_table.current_other_id, 0, 'current_other_id'],
    }     

    food_items = ['Breakfast', 'Lunch', 'Snack', 'Cereal', 'Fruit', 'Cookie', 'Chocolate', 'Other']
    beverages_items = ['Water','Juice', 'Soda', 'Other']

    items_already_in_db = []
    
    for n in range(number_of_rows):
            current_item_type = item_type[n]

            # making a query to know if the item is already in the database
            for item in tables:
                current_item_name = item_name[n].strip().upper()

                if tables[item][0].query.filter_by(name=current_item_name).first() is not None:                    
                    
                    if not multiple_days:
                        db.query(tables[item][0]).filter(tables[item][0].name == current_item_name).update({
                            'stock': tables[item][0].stock + stock[n], 'added':tables[item][0].added + stock[n]
                        })                  
                        items_already_in_db.append(current_item_name)

                    # adding the data in the main Food table
                    if current_item_type in food_items and food:
    
                        db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                            'total': _FoodsInStock.total + int(stock[n])
                        })
                        if current_item_type == food_items[0]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_breakfasts': _FoodsInStock.total_breakfasts + int(stock[n])
                            })
                            # the bu was in the line 568
                        elif current_item_type == food_items[1]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_lunch': _FoodsInStock.total_lunch + int(stock[n])
                            })
                        elif current_item_type == food_items[2]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_snacks': _FoodsInStock.total_snacks + int(stock[n])
                            })
                        elif current_item_type == food_items[3]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_cereals': _FoodsInStock.total_cereals + int(stock[n])
                            })
                        elif current_item_type == food_items[4]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_fruits': _FoodsInStock.total_fruits + int(stock[n])
                            })
                        elif current_item_type == food_items[5]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_cookies': _FoodsInStock.total_cookies + int(stock[n])
                            })
                        elif current_item_type == food_items[6]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_chocolates': _FoodsInStock.total_chocolates + int(stock[n])
                            })
                        elif current_item_type == food_items[7]:
                            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update({
                                'total_others': _FoodsInStock.total_others + int(stock[n])
                            })
                        
                    # adding the main beverages table
                    if current_item_type in beverages_items and not food:
                    
                        db.query(_BeveragesInStock).filter(_BeveragesInStock.date == date).update({
                            'total': _BeveragesInStock.total + int(stock[n])
                        })

                        if current_item_type == beverages_items[0]:
                            db.query(_BeveragesInStock).filter(_BeveragesInStock.date == date).update({
                                'total_waters': _BeveragesInStock.total_waters + int(stock[n])
                            })

                        elif current_item_type == beverages_items[1]:
                            db.query(_BeveragesInStock).filter(_BeveragesInStock.date == date).update({
                                'total_juices': _BeveragesInStock.total_juices + int(stock[n])
                            })

                        elif current_item_type == beverages_items[2]:
                            db.query(_BeveragesInStock).filter(_BeveragesInStock.date == date).update({
                                'total_sodas': _BeveragesInStock.total_sodas + int(stock[n])
                            })

                        elif current_item_type == beverages_items[3]:
                            db.query(_BeveragesInStock).filter(_BeveragesInStock.date == date).update({
                                'total_others': _BeveragesInStock.total_others + int(stock[n])
                            })

                    # there is neccesary to put update the data in the FoodStock and in the BeveragesStock
                    break
            
            if current_item_name in items_already_in_db:
                break
            else:

                if item_added:
                    added = stock[n]
                else:
                    added = 0
     
                # we select the two tables associated with the current item
                # [TableInStock, TableExpenses]
                if current_item_type == 'Other':
                    if food:
                        current_item_type += 'C'
                    else:
                        current_item_type += 'B'

                current_tables = tables[current_item_type]

                # we increment the total_added of the current item
                table_fields[current_item_type][1] += int(stock[n])

                # current_item
                current_item = current_tables[0].query.filter_by(name=current_item_name).first()

                in_stock_table = current_tables[0]
                expenses_table = current_tables[1]
                
                # we need to check if the item is None to be able to give it an id 
                if current_item is not None:
                    current_item_id = current_item.item_id
                else:
                    
                    # increasing the current item in the data base
                    if food:
                        db.query(_FoodsInStock).filter_by(date=TODAY).update({table_fields[current_item_type][2]: table_fields[current_item_type][0] + 1})
                    else:
                        db.query(_BeveragesInStock).filter_by(date=TODAY).update({table_fields[current_item_type][2]: table_fields[current_item_type][0] + 1})

                    current_item_id = table_fields[current_item_type][0] + 1                  
                    table_fields[current_item_type][0] += 1

                # we create our new item entry

                new_item = in_stock_table(
                    name = current_item_name,
                    stock = stock[n],
                    initial_stock = stock[n],
                    added = added,
                    date = date,
                    item_id = current_item_id
                )
                db.add(new_item)
                # the new item_expense entry
                new_item_expenses = expenses_table(
                    name = current_item_name,
                    consumption = 0,
                    date = date,
                    item_id = current_item_id
                )
                db.add(new_item_expenses)

                if food:

                    total_food_added += int(stock[n])
                    if item_added:
                        new_food_info = _FoodItemsInfo(
                            item_id = current_item_id,
                            name = current_item_name,
                            added_date = date,
                            type = current_item_type.upper()
                        )
                        db.add(new_food_info)

                else:

                    total_beverages_added += int(stock[n])
                    if item_added:
                        new_beverage_info = _BeverageItemsInfo(
                            item_id = current_item_id,
                            name = current_item_name,
                            added_date = date,
                            type = current_item_type.upper()
                        )
                        db.add(new_beverage_info)            

    # adding the total amounts to the db
    other_c = 'OtherC'
    other_b = 'OtherB'
    for key in table_fields:

        if food:
            if key in food_items or key == other_c:
                table_to_query = _FoodsInStock
            else:
                continue
        else:
            if key in beverages_items or key == other_b:
                table_to_query = _BeveragesInStock
            else:
                continue

        table_to_query.query.get(date).initial_stock += table_fields[key][1]

    if added:
        if food:
            db.query(_FoodsInStock).filter(_FoodsInStock.date == date).update(
                {'total_breakfasts': _FoodsInStock.total_breakfasts + table_fields['Breakfast'][1],
                'total_breakfasts_added': _FoodsInStock.total_breakfasts_added + table_fields['Breakfast'][1],

                'total_lunch_added': _FoodsInStock.total_lunch_added + table_fields['Lunch'][1],
                'total_lunch': _FoodsInStock.total_lunch + table_fields['Lunch'][1],

                'total_snacks_added': _FoodsInStock.total_snacks_added + table_fields['Snack'][1],
                'total_snacks': _FoodsInStock.total_snacks + table_fields['Snack'][1],

                'total_cereals_added': _FoodsInStock.total_cereals_added + table_fields['Cereal'][1],
                'total_cereals': _FoodsInStock.total_cereals + table_fields['Cereal'][1],

                'total_fruits_added': _FoodsInStock.total_fruits_added + table_fields['Fruit'][1],
                'total_fruits': _FoodsInStock.total_fruits + table_fields['Fruit'][1],

                'total_cookies_added': _FoodsInStock.total_cookies_added + table_fields['Cookie'][1],
                'total_cookies': _FoodsInStock.total_cookies + table_fields['Cookie'][1],

                'total_chocolates_added': _FoodsInStock.total_chocolates_added + table_fields['Chocolate'][1],
                'total_chocolates': _FoodsInStock.total_chocolates + table_fields['Chocolate'][1],

                'total_others_added': _FoodsInStock.total_others_added + table_fields['OtherC'][1],
                'total_others': _FoodsInStock.total_others + table_fields['OtherC'][1],

                'total_food_added': _FoodsInStock.total_food_added + total_food_added,
                'total': _FoodsInStock.total + total_food_added,
                })
        else:
            db.query(_BeveragesInStock).filter(_BeveragesInStock.date == date).update(
                {'total_waters_added': _BeveragesInStock.total_waters_added + table_fields['Water'][1],
                'total_waters': _BeveragesInStock.total_waters + table_fields['Water'][1],

                'total_juices_added': _BeveragesInStock.total_juices_added + table_fields['Juice'][1],
                'total_juices': _BeveragesInStock.total_juices + table_fields['Juice'][1],

                'total_sodas_added': _BeveragesInStock.total_sodas_added + table_fields['Soda'][1],
                'total_sodas': _BeveragesInStock.total_sodas + table_fields['Soda'][1],
                
                'total_others_added': _BeveragesInStock.total_others_added + table_fields['OtherB'][1],
                'total_others': _BeveragesInStock.total_others + table_fields['OtherB'][1],

                'total_beverages_added': _BeveragesInStock.total_beverages_added + total_beverages_added,
                'total': _BeveragesInStock.total + total_beverages_added,
                })

    db.commit()


def decrease_items(date, total_elements, new_stock, old_stock, item_type, item_id, food, decrease, multiple_days, decrease_item_initial_stock):
    
    tables = {
        'breakfast': [_BreakfastsInStock, _BreakfastExpenses],
        'lunch': [_LunchInStock, _LunchExpenses],
        'snack': [_SnacksInStock, _SnackExpenses],
        'cereal': [_CerealsInStock, _CerealExpenses],
        'fruit': [_FruitsInStock, _FruitExpenses],
        'cookie': [_CookiesInStock, _CookiesExpenses],
        'chocolate': [_ChocolatesInStock, _ChocolatesExpenses],
        'otherc': [_OtherFoodsInStock, _OtherFoodsExpenses],

        'water': [_WatersInStock, _WaterExpenses],
        'soda': [_SodasInStock, _SodaExpenses],
        'juice': [_JuicesInStock, _JuiceExpenses],
        'otherb': [_OtherBeveragesInStock, _OtherBeveragesExpenses],
    }

    for n in range(total_elements):
        new_stock_integer = int(new_stock[n])
        old_stock_integer = int(old_stock[n])
        
        decrease_amount = old_stock_integer - new_stock_integer

        if decrease_amount == 0:
            continue

        current_item_type = item_type[n]

        if current_item_type != 'lunch':
            _field = f'total_{current_item_type}s'
        else:
            _field = f'total_{current_item_type}'

        if food:
            main_stock_table, main_expenses_table = _FoodsInStock, _FoodExpenses
            if current_item_type == 'other':
                current_item_type += 'c'
        else:
            main_stock_table, main_expenses_table = _BeveragesInStock, _BeverageExpenses
            if current_item_type == 'other':
                current_item_type += 'b'


        db.query(main_stock_table).filter(main_stock_table.date == date).update({'total':main_stock_table.total - decrease_amount })

        db.query(main_stock_table).filter_by(date = date).update({_field: getattr(main_stock_table, _field) - decrease_amount})

        db.query(tables[current_item_type][0]).filter_by(date = date, item_id=item_id[n]).update({tables[current_item_type][0].stock: tables[current_item_type][0].stock - decrease_amount})

        if decrease_item_initial_stock:
            db.query(tables[current_item_type][0]).filter_by(date = date, item_id=item_id[n]).update({tables[current_item_type][0].initial_stock: tables[current_item_type][0].initial_stock - decrease_amount })

        # decrease is entered once to not duplicate the values
        if decrease:
            db.query(tables[current_item_type][1]).filter_by(date = date, item_id=item_id[n]).update({tables[current_item_type][1].consumption: tables[current_item_type][1].consumption + decrease_amount})

            db.query(main_expenses_table).filter(main_expenses_table.date == date).update({'total':main_expenses_table.total + decrease_amount})

            db.query(main_expenses_table).filter_by(date = date).update({_field: getattr(main_expenses_table, _field) + decrease_amount})


        if multiple_days:
            db.query(main_stock_table).filter(main_stock_table.date == date).update({'initial_stock':main_stock_table.initial_stock - decrease_amount })


def get_items_between_dates(list_items, item_type, start_date, date, items_introduced_between_dates, items_between_dates_dict, deleted_items, food=True, in_stock=True):
    
    """
    Getting the elemens that were introduced during the two dates and store them in the items_introduced_between_dates dictionary
    return: the items that were in the db before the start_date => list of tables objects
    
    """

    start_date = get_date_from_string(start_date, format='%d-%m-%Y').date()
    table_inf = _FoodItemsInfo
    main_type = 'food'

    if not food:
        table_inf = _BeverageItemsInfo
        main_type = 'beverage'

    items_between_dates_list = []
    
    for item in list_items:
        try:   
            other_type = False
            if item_type == 'other':
                other_type = True
                if food:
                    item_type += 'c'
                else:
                    item_type += 'b'

            current_item_inf = table_inf.query.filter_by(item_id=item.item_id, type=item_type.upper()).one()

            if other_type:
                item_type = item_type[:-1]

        except:
            return []

        # if the element was introduced before the start date and it is not in the deleted items dictionary we 
        # are good to add it to the items_between_dates_dict  

        if get_date_from_string(current_item_inf.added_date).date() < start_date:         

            if deleted_items is not None:       
                for node in deleted_items[item_type.upper()]:           
                    if node._id == current_item_inf.item_id:               
                        break

            items_between_dates_list.append(item)
            # this is used for the dictionary object
            current_type = item_type.upper()
            if current_type == 'OTHER':
                if food:
                    current_type += '_FOOD'
                else:
                    current_type += '_BEVERAGES'


            if item.name not in items_between_dates_dict[current_type]:
                items_between_dates_dict[current_type].append(item.name)
            continue
        
        # otherwise it is neccessary to get its information to be able to calculate the averages 
        # since it was introduced between the dates that are being evaluated

        
        if item.name in items_introduced_between_dates:

            # if the tables is the stock one it means that we have not finished it getting the dates where 
            # we can find the item so we append the current date in the object
            if in_stock:
                current_item_in_dict = items_introduced_between_dates[item.name]
                
                # and increase other values
                current_item_in_dict.dates.append(date)

                current_item_in_dict.initial_stock += item.initial_stock
                current_item_in_dict.final_stock += item.stock

            else:
            # otherwise it will mean that we are now with the tables in the expenses part so now we have to start 
            # increasing the total_consumed variable in the object
                items_introduced_between_dates[item.name].total_consumed += item.consumption
    
        # if the item does not exist in the class we create a new object and we store it in the class
        else:
            object_inf = ItemInformation([date], main_type, item_type, item.item_id, item.name, initial_stock=item.initial_stock, final_stock=item.stock, added_date=current_item_inf.added_date)

            items_introduced_between_dates[item.name] = object_inf

    return items_between_dates_list
    
# --------------------------------------------------------------
# Routes -------------------------------------------------------
# public routes ------------------------------------------------
@app.route('/')
def home():
    return render_template('pantry/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form.get('email')
        user = _User.query.filter_by(email=email).first()
        if user is not None:
            password = request.form.get('password')
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('pantry'))
            else:
                error = 'Mail or password are incorrect'
        else:
            error = 'Mail or password are incorrect'

    return render_template('pantry/login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if _User.query.filter_by(email=email).first():
            flash('There is already an account with that email')
            return redirect(url_for('login'))
       
        else:

            hashed_password = generate_password_hash(request.form.get('password'))
            
            new_user = _User(
                name=request.form.get('name'),
                email=email,
                password=hashed_password,
                level=3
            )

            db.add(new_user)
            db.commit()
            
            login_user(new_user)

            return redirect(url_for('pantry'))

    return render_template('pantry/register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/documentation')
def documentation():
    return render_template('pantry/documentation.html')


# autorization is needed to access to these routes
@app.route('/Pantry')
@login_required
def pantry():
    # the new dates in the data base must be created since the last date in the record to the present day, and them
    # the attendance will decleare whcih days  have to be included in the reports 
    print(create_new_date_in_db())

    food = _FoodsInStock.query.get(TODAY)
    beverages = _BeveragesInStock.query.get(TODAY)
    people_in_last_five_days = db.query(_People).order_by(_People.date.desc()).limit(5)

    last_five_days = []

    total_people_in_last_five_days = 0

    # getting the last five days converted to string
    for person in people_in_last_five_days:
        total_people_in_last_five_days += person.total
        last_five_days.append(day_to_weekday_name(person.date.isoweekday()))
    
    average_people_in_last_five_days = round(total_people_in_last_five_days / 5)

    return render_template('pantry/dashboard.html', 
    food=food, 
    beverages=beverages, 
    average_people_in_last_five_days=average_people_in_last_five_days,
    people_in_last_five_days=people_in_last_five_days,
    last_five_days=last_five_days)


# routes for food ----------------------------------------------
# look for defaultloads
@app.route('/comida?<edit_item>&<day>&<month>&<year>&<searcher>', defaults={'edit_item':False, 'day':None, 'month':None, 'year':None, 'searcher':True}, methods=['GET', 'POST'])
@app.route('/Comida?<edit_item>&<day>&<month>&<year>&<searcher>', methods=['GET', 'POST'])
@login_required
def food_details(edit_item, day, month, year, searcher):
    searcher = get_boolean(searcher)
    if request.method == 'POST' and searcher:
        day = request.form['daySelect0']
        month = request.form['monthSelect0']
        year = request.form['yearSelect0']
    elif day is None:
        day = NOW.strftime('%d')
        month = NOW.strftime('%m')
        year = NOW.strftime('%Y')

    date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
    food = _FoodsInStock.query.get(date)

    if food is None:
        return 'There is no data for the selected date'
    
    # the default organization in the food details table is for type of food
    breakfasts = food.breakfasts
    lunch = food.lunch
    snacks = food.snacks
    cereals = food.cereals
    fruits = food.fruits
    cookies = food.cookies
    chocolates = food.chocolates
    others = food.others 

    total_items = len(breakfasts) + len(lunch) + len(snacks) + len(cereals) + len(fruits) + len(cookies) + len(chocolates) + len(others)

    return render_template('pantry/food_details.html', food=food, breakfasts=breakfasts, lunch=lunch, snacks=snacks, cereals=cereals, fruits=fruits, cookies=cookies, chocolates=chocolates, others=others, edit_item=True, total_items=total_items, day=day, month=month, year=year)


# routes for beverages
@app.route('/bebidas?<edit_item>&<day>&<month>&<year>&<searcher>', defaults={'edit_item':False, 'day':None, 'month':None, 'year':None, 'searcher':True}, methods=['GET', 'POST'])
@app.route('/Bebidas?<edit_item>&<day>&<month>&<year>&<searcher>', methods=['GET', 'POST'])
@login_required
def beverage_details(edit_item, day, month, year, searcher):
    searcher = get_boolean(searcher)
    if request.method == 'POST' and searcher:
        day = request.form['daySelect0']
        month = request.form['monthSelect0']
        year = request.form['yearSelect0']
    elif day is None:
        day = NOW.strftime('%d')
        month = NOW.strftime('%m')
        year = NOW.strftime('%Y')

    date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
    beverages = _BeveragesInStock.query.get(date)

    if beverages is None:
        return 'There is no data for the selected date'

    waters = beverages.water
    juices = beverages.juices
    sodas = beverages.sodas
    others = beverages.others

    total_items = len(waters) + len(juices) + len(sodas) + len(others)

    return render_template('pantry/beverage_details.html', edit_item=True, total_items=total_items, beverage=beverages, waters=waters, juices=juices, sodas=sodas, others=others, day=day, month=month, year=year)


@app.route('/Personas', methods=['GET', 'POST'])
@login_required
def people():
    if request.method == 'POST':
        day = request.form['daySelect0']
        month = request.form['monthSelect0']
        year = request.form['yearSelect0']

        date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
        total_people = request.form['totalPeople']

        people = _People.query.get(date)

        if people is None:
            new_people = _People(
                date = date,
                total = total_people
            )
            db.add(new_people)
        else:
            db.query(_People).filter(_People.date == date).update({'total': total_people})
        
        db.commit()

    day = NOW.strftime('%d')
    month = NOW.strftime('%m')
    year = NOW.strftime('%Y')

    people_data = db.query(_People).order_by(_People.date.desc()).all()
    return render_template('pantry/people.html', people_data=people_data, day=day, month=month, year=year)


@app.route('/AumentarStockDeBebidas?<increase_food>', defaults={'increase_food':True})
@app.route('/AumentarStockDeComida?<increase_food>')
@login_required
def get_increase_stock(increase_food):
    increase_food = get_boolean(increase_food)
    # we have to take the name of the food and the beverages in the data base so we can show them in the UI
    items_info = {}
    item_one_info = {}
    item_two_info = {}
    item_three_info = {}
    item_four_info = {}
    item_five_info = {}
    item_six_info = {}
    item_seven_info = {}
    item_eight_info = {}
    
    if increase_food:
        # getting the elements in the last table so we can show them in the UI
        last_food_table = db.query(_FoodsInStock).order_by(_FoodsInStock.date)[-1]
        # 
        for table in last_food_table.breakfasts:
            item_one_info[table.name] = table.id
            item_one_info['to_show'] = 'Breakfast'
        items_info['breakfast'] = item_one_info
        
        for table in last_food_table.lunch:
            item_two_info[table.name] = table.id
            item_two_info['to_show'] = 'Lunch'
        items_info['lunch'] = item_two_info

        for table in last_food_table.snacks:
            item_three_info[table.name] = table.id
            item_three_info['to_show'] = 'Snack'
        items_info['snack'] = item_three_info

        for table in last_food_table.cereals:
            item_four_info[table.name] = table.id
            item_four_info['to_show'] = 'Cereal'
        items_info['cereal'] = item_four_info

        for table in last_food_table.fruits:
            item_five_info[table.name] = table.id
            item_five_info['to_show'] = 'Fruit'
        items_info['fruit'] = item_five_info

        for table in last_food_table.cookies:
            item_six_info[table.name] = table.id
            item_six_info['to_show'] = 'Cookie'
        items_info['cookie'] = item_six_info

        for table in last_food_table.chocolates:
            item_seven_info[table.name] = table.id
            item_seven_info['to_show'] = 'Chocolate'
        items_info['chocolate'] = item_seven_info

        for table in last_food_table.others:
            item_eight_info[table.name] = table.id
            item_eight_info['to_show'] = 'Other'
        items_info['other'] = item_eight_info
               
    else:
        last_beverage_table = db.query(_BeveragesInStock).order_by(_BeveragesInStock.date)[-1]

        for table in last_beverage_table.water:
            item_one_info[table.name] = table.id
            item_one_info['to_show'] = 'Water'
        items_info['water'] = item_one_info
        
        for table in last_beverage_table.juices:
            item_two_info[table.name] = table.id
            item_two_info['to_show'] = 'Juice'
        items_info['juice'] = item_two_info

        for table in last_beverage_table.sodas:
            item_three_info[table.name] = table.id
            item_three_info['to_show'] = 'Soda'
        items_info['soda'] = item_three_info

        for table in last_beverage_table.others:
            item_four_info[table.name] = table.id
            item_four_info['to_show'] = 'Other'
        items_info['other'] = item_four_info
      
    return render_template('pantry/increase_stock.html', increase_food=increase_food, items_info=items_info)


@app.route('/increase_stock?<increase_food>', methods=['POST'])
@login_required
def post_increase_stock(increase_food):
    increase_food = get_boolean(increase_food)

    if increase_food:
        breakfasts_info = {
            'id': request.form.getlist('breakfastID'),
            'value': request.form.getlist('breakfastValue'),
        }
        lunch_info = {
            'id': request.form.getlist('lunchID'),
            'value': request.form.getlist('lunchValue'),
        }
        snacks_info = {
            'id': request.form.getlist('snackID'),
            'value': request.form.getlist('snackValue'),
        }
        cereals_info = {
            'id': request.form.getlist('cerealID'),
            'value': request.form.getlist('cerealValue'),
        }
        fruits_info = {
            'id': request.form.getlist('fruitID'),
            'value': request.form.getlist('fruitValue'),
        }
        cookies_info = {
            'id': request.form.getlist('cookieID'),
            'value': request.form.getlist('cookieValue'),
        }
        chocolates_info = {
            'id': request.form.getlist('chocolateID'),
            'value': request.form.getlist('chocolateValue'),
        }
        others_info = {
            'id': request.form.getlist('otherID'),
            'value': request.form.getlist('otherValue'),
        }

        items = [breakfasts_info, lunch_info, snacks_info, cereals_info, fruits_info, cookies_info, chocolates_info, others_info]
        classes = [_BreakfastsInStock, _LunchInStock, _SnacksInStock, _CerealsInStock, _FruitsInStock, _CookiesInStock, _ChocolatesInStock, _OtherFoodsInStock]

        update_items_in_stock(items, classes)

        return redirect(url_for('food_details'))

    else:
        waters_info = {
            'id': request.form.getlist('waterID'),
            'value': request.form.getlist('waterValue'),
        }
        juices_info = {
            'id': request.form.getlist('juiceID'),
            'value': request.form.getlist('juiceValue'),
        }
        sodas_info = {
            'id': request.form.getlist('sodaID'),
            'value': request.form.getlist('sodaValue'),
        }
        others_info = {
            'id': request.form.getlist('otherID'),
            'value': request.form.getlist('otherValue'),
        }

        items = [waters_info, juices_info, sodas_info, others_info]
        classes = [_WatersInStock, _JuicesInStock, _SodasInStock, _OtherBeveragesInStock]

        update_items_in_stock(items, classes)
        
        return redirect(url_for('beverage_details'))
        

# ------------------------------------------------------------------------------
@app.route('/decrease_beverages_in_data_base?<int:total_elements>&<food>', methods=['POST'], defaults={'food':False})
@app.route('/decrease_food_in_data_base?<int:total_elements>&<food>', methods=['POST'])
@login_required
def decrease_items_in_data_base(total_elements, food):
    NEW_STOCK = request.form.getlist('newStock')
    OLD_STOCK = request.form.getlist('oldStock')
    ITEM_TYPE = request.form.getlist('itemType')
    ITEM_ID = request.form.getlist('itemId')

    day = request.form['day']
    month = request.form['month']
    year = request.form['year']

    current_day = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')

    decrease = True
    multiple_days = False
    decrease_item_initial_stock = False

    while current_day.date() != TODAY:
        multiple_days = True
        decrease_items(current_day.date(), total_elements, NEW_STOCK, OLD_STOCK, ITEM_TYPE, ITEM_ID, food, decrease, multiple_days=multiple_days, decrease_item_initial_stock=decrease_item_initial_stock)
        current_day = (current_day + timedelta(1))
        decrease = False
        decrease_item_initial_stock = True


    decrease_items(current_day.date(), total_elements, NEW_STOCK, OLD_STOCK, ITEM_TYPE, ITEM_ID, food, decrease, multiple_days=multiple_days, decrease_item_initial_stock=True)

    db.commit()

    if food:
        return redirect(url_for('food_details', edit_item=False))
    else:
        return redirect(url_for('beverage_details', edit_item=False))


@app.route('/agregarNuevasBebidas?<food>', methods=['GET', 'POST'], defaults={'food':False})
@app.route('/agregarNuevasComidas?<food>', methods=['GET', 'POST'])
@login_required
def add_new_items(food): 
    if request.method == 'POST':
        
        ITEM_TYPE = request.form.getlist('inputType')
        STOCK = request.form.getlist('stockInput')
        ITEM_NAME = request.form.getlist('nameInput')

        day = request.form['daySelect0']
        month = request.form['monthSelect0']
        year = request.form['yearSelect0']

        DATE = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
        current_day = DATE
        
        NUMBER_OF_ROWS = len(STOCK)

        if _FoodsInStock.query.get(DATE) is None:
            _create_new_entries(DATE, False)

        multiple_days = False
        if current_day != TODAY:
            multiple_days = True

        added = True

        while current_day.date() != TODAY:
            add_items_to_data_base(current_day.date(), ITEM_TYPE, STOCK, ITEM_NAME, NUMBER_OF_ROWS, food, multiple_days, added)
            current_day = (current_day + timedelta(1))
            added = False

        add_items_to_data_base(current_day.date(), ITEM_TYPE, STOCK, ITEM_NAME, NUMBER_OF_ROWS, food, multiple_days, item_added=added)
   
        if food:
            return redirect(url_for('food_details'))
        else:
            return redirect(url_for('beverage_details'))

    day = NOW.strftime('%d')
    month = NOW.strftime('%m')
    year = NOW.strftime('%Y')
    return render_template('pantry/add_new_item.html', food=food, day=day, month=month, year=year)


@app.route('/deleteFoodItems?<food>', defaults = {'food': True})
@app.route('/deleteBeverageItems?<food>')
def delete_items(food):
    
    food = get_boolean(food)

    food_table = None
    beverage_table = None

    if food:
        food_table = _FoodsInStock.query.get(TODAY)
    else:
        beverage_table = _BeveragesInStock.query.get(TODAY)

    return render_template('pantry/deleteItems.html', food=food_table, beverages=beverage_table)


@app.route('/deleteItem', methods=['DELETE'])
def delete_items_api():

    data = request.json

    food = data['food']
    item_type = int(data['item_type'])
    _id = int(data['id'])

    food_stock_tables = [_BreakfastsInStock, _LunchInStock, _SnacksInStock, _CerealsInStock, _FruitsInStock, _CookiesInStock, _ChocolatesInStock, _OtherFoodsInStock]

    food_expenses_tables = [_BreakfastExpenses, _LunchExpenses, _SnackExpenses, _CerealExpenses, _FruitExpenses, _CookiesExpenses, _ChocolatesExpenses, _OtherFoodsExpenses]

    beverages_stock_tables = [_WatersInStock, _JuicesInStock, _SodasInStock, _OtherBeveragesInStock]
    beverages_expenses_tables = [_WaterExpenses, _JuiceExpenses, _SodaExpenses, _OtherBeveragesExpenses]

    # we need also to delete the possible stock that affect the current stock in the data base
    if food:
        current_table = food_stock_tables[item_type]

        item = current_table.query.filter_by(item_id=_id, date=TODAY).one()
        current_table.query.filter_by(item_id=_id, date=TODAY).delete()

        initial_stock = item.initial_stock
        stock = item.stock
        added = item.added

        # for expenses deleting

        current_table = food_expenses_tables[item_type]
        item = current_table.query.filter_by(item_id=_id, date=TODAY).one()
        current_table.query.filter_by(item_id=_id, date=TODAY).delete()

        consumption = item.consumption

        # we update the new values to in the data base
        food_in_stock = _FoodsInStock.query.get(TODAY)
        food_in_stock.total -= stock
        food_in_stock.initial_stock -= initial_stock
        food_in_stock.total_food_added -= added 

        food_expenses = _FoodExpenses.query.get(TODAY)
        food_expenses.total += consumption

        # then we need to what is the table we deleted since we have to decrease the amount
        # of items that were in that table

        # breakfast type
        if item_type == 0:
            food_in_stock.total_breakfasts -= stock
            food_in_stock.total_breakfasts_added -= added
            food_expenses.total_breakfasts += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='BREAKFAST').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='BREAKFAST').delete()

        
        # lunch type 
        elif item_type == 1:
            food_in_stock.total_lunch -= stock
            food_in_stock.total_lunch_added -= added
            food_expenses.total_lunch += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='LUNCH').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='LUNCH').delete()

        # snack type 
        elif item_type == 2:
            food_in_stock.total_snacks -= stock
            food_in_stock.total_snacks_added -= added
            food_expenses.total_snacks += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='SNACK').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='SNACK').delete()
        
        # cereal type 
        elif item_type == 3:
            food_in_stock.total_cereals -= stock
            food_in_stock.total_cereals_added -= added
            food_expenses.total_cereals += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='CEREAL').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='CEREAL').delete()

        # fruit type 
        elif item_type == 4:
            food_in_stock.total_fruits -= stock
            food_in_stock.total_fruits_added -= added
            food_expenses.total_fruits += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='FRUIT').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='FRUIT').delete()
        
        # cookie type
        elif item_type == 5:
            food_in_stock.total_cookies -= stock
            food_in_stock.total_cookies_added -= added
            food_expenses.total_cookies += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='COOKIE').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='COOKIE').delete()

        # Chocolate type
        elif item_type == 6:
            food_in_stock.total_chocolates -= stock
            food_in_stock.total_chocolates_added -= added
            food_expenses.total_chocolates += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='CHOCOLATE').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='CHOCOLATE').delete()
                
        # others type
        elif item_type == 7:
            food_in_stock.total_others -= stock
            food_in_stock.total_others_added -= added
            food_expenses.total_others += consumption
            current_item = _FoodItemsInfo.query.filter_by(item_id = _id, type='OTHERC').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _FoodItemsInfo.query.filter_by(item_id = _id, type='OTHERC').delete()

        

    else:
        current_table = beverages_stock_tables[item_type]

        item = current_table.query.filter_by(item_id=_id, date=TODAY).one()
        current_table.query.filter_by(item_id=_id, date=TODAY).delete()

        initial_stock = item.initial_stock
        stock = item.stock
        added = item.added

        # for beverages expenses

        current_table = beverages_expenses_tables[item_type]
        
        item = current_table.query.filter_by(item_id=_id, date=TODAY).one()
        current_table.query.filter_by(item_id=_id, date=TODAY).delete()

        consumption = item.consumption

        # update the values in the beverages main tables

        beverages_in_stock = _BeveragesInStock.query.get(TODAY)
        beverages_in_stock.total -= stock
        beverages_in_stock.initial_stock -= initial_stock
        beverages_in_stock.total_beverages_added -= added 

        beverages_expenses = _BeverageExpenses.query.get(TODAY)
        beverages_expenses.total += consumption

        # then we need to what is the table we deleted since we have to decrease the amount
        # of items that were in that table

        # water type
        if item_type == 0:
            beverages_in_stock.total_waters -= stock
            beverages_in_stock.total_waters_added -= added
            beverages_expenses.total_waters += consumption
            current_item = _BeverageItemsInfo.query.filter_by(item_id = _id, type='WATER').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _BeverageItemsInfo.query.filter_by(item_id = _id, type='WATER').delete()
        
        # juice type 
        elif item_type == 1:
            beverages_in_stock.total_juices -= stock
            beverages_in_stock.total_juices_added -= added
            beverages_expenses.total_juices += consumption
            current_item = _BeverageItemsInfo.query.filter_by(item_id = _id, type='JUICE').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _BeverageItemsInfo.query.filter_by(item_id = _id, type='JUICE').delete()
        
        # soda type 
        elif item_type == 2:
            beverages_in_stock.total_sodas -= stock
            beverages_in_stock.total_sodas_added -= added
            beverages_expenses.total_sodas += consumption
            current_item = _BeverageItemsInfo.query.filter_by(item_id = _id, type='SODA').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _BeverageItemsInfo.query.filter_by(item_id = _id, type='SODA').delete()
        
        # other type 
        elif item_type == 3:
            beverages_in_stock.total_others -= stock
            beverages_in_stock.total_others_added -= added
            beverages_expenses.total_others += consumption
            current_item = _BeverageItemsInfo.query.filter_by(item_id = _id, type='OTHERB').one()
            current_item.deleted_date = TODAY

            if current_item.deleted_date == current_item.added_date:
                _BeverageItemsInfo.query.filter_by(item_id = _id, type='OTHERB').delete()

        # fruit type 

    db.commit()

    return '200'


@app.route('/Reportes?<between_dates>&<date>', defaults={'between_dates': False, 'date': TODAY}, methods=['POST', 'GET'])
@app.route('/reportes?<between_dates>&<date>', methods=['POST', 'GET'])
def reports(between_dates, date):

    if request.method == 'POST':

        if between_dates:           
            day_start = request.form['daySelect1']
            month_start = request.form['monthSelect1']
            year_start = request.form['yearSelect1']
            start_date = f'{day_start}-{month_start}-{year_start}'

            day_end = request.form['daySelect2']
            month_end = request.form['monthSelect2']
            year_end = request.form['yearSelect2']
            end_date = f'{day_end}-{month_end}-{year_end}'
         
            return redirect(url_for('report_between_dates', 
            # dates
            start_date=start_date, 
            end_date=end_date, 
            day=day_start, 
            month=month_start, 
            year=year_start,
            # for share or not  
            report_for_share=False, 
            show_link=True,
        ))
        
        else:
            day = request.form['daySelect0']
            month = request.form['monthSelect0']
            year = request.form['yearSelect0']

            date = f'{year}-{month}-{day}'

    if request.method == 'GET':
        # date_time_obj = get_date_from_string(date).date()
        day = TODAY.strftime('%d')
        month = TODAY.strftime('%m')
        year = TODAY.strftime('%Y')
    
    return redirect(url_for('report_for_specific_date', 
    # dates
    date=date, 
    day=day, 
    month=month,
    year=year,
    # for share or not 
    report_for_share=False, 
    show_link=True,
    ))


@app.route('/ConsultarUnaFecha?<report_for_share>&<show_link>&<date>&<day>&<month>&<year>&<get_previous_date>&<get_next_date>', defaults={'get_previous_date': False, 'get_next_date': False})
@app.route('/consultarUnaFecha?<report_for_share>&<show_link>&<date>&<day>&<month>&<year>&<get_previous_date>&<get_next_date>')
def report_for_specific_date(date, day, month, year, report_for_share, show_link, get_previous_date, get_next_date):
    get_previous_date = get_boolean(get_previous_date)
    get_next_date = get_boolean(get_next_date)
    report_for_share = get_boolean(report_for_share)
    show_link = get_boolean(show_link)

    if get_next_date:
        date = get_date_next_previous(date)
    elif get_previous_date:
        date = get_date_next_previous(date, previous_day=True)
    else:
        date = datetime.strptime(date, '%Y-%m-%d').date()

    if get_next_date or get_previous_date:
        day = datetime.strftime(date, '%d')
        month = datetime.strftime(date, '%m')
        year = datetime.strftime(date, '%Y')

    food = _FoodsInStock.query.get(date)
    beverages = _BeveragesInStock.query.get(date)
    food_expenses = _FoodExpenses.query.get(date)
    beverage_expenses = _BeverageExpenses.query.get(date)

    if food is None:
        return f'There is no data for the selected date: {date}'

    if _People.query.get(date) is None or _People.query.get(date).total == 0:
        flash('The selected day has not been added yet (click to add)', category='info')
        people_asisted = 'N/A'
    else:
        people_asisted = _People.query.get(date).total

    breakfasts = len(food.breakfasts)
    lunch = len(food.lunch)
    snacks = len(food.snacks)
    cereals = len(food.cereals)
    fruits = len(food.fruits)
    cookies = len(food.cookies)
    chocolates = len(food.chocolates)
    other_foods = len(food.others)

    waters = len(beverages.water)
    juices = len(beverages.juices)
    sodas = len(beverages.sodas)
    other_beverages = len(beverages.others)

    
    if food is None or beverages is None:
        return render_template('pantry/report_for_specific_date.html', data=False)

    # we return the data with of the current date
    return render_template('pantry/report_for_specific_date.html', 
    food=food, 
    beverages=beverages, 
    data=True, 
    food_expenses=food_expenses, 
    beverage_expenses=beverage_expenses, 
    between_dates=False, 
    date=date, 
    # food items 
    breakfasts=breakfasts, 
    lunch=lunch, 
    snacks=snacks, 
    cereals=cereals, 
    fruits=fruits, 
    cookies=cookies,
    chocolates=chocolates,
    other_foods=other_foods,
    # beverages items 
    waters=waters, 
    juices=juices, 
    sodas=sodas, 
    other_beverages=other_beverages, 

    # people
    people_asisted=people_asisted, 

    # others  things 
    day=day, 
    month=month, 
    year=year, 
    report_for_share=report_for_share, 
    show_link=show_link)


@app.route('/ConsultaEntreFechas?<report_for_share>&<show_link>&<start_date>&<end_date>&<day>&<month>&<year>')
def report_between_dates(start_date, end_date, day, month, year, report_for_share, show_link):
    
    report_for_share = get_boolean(report_for_share)
    show_link = get_boolean(show_link)
    
    dates = get_dates_between(start_date, end_date)

    # as we did with the deleted items we have to do the same thing with the items that were introduced during 
    # the two dates, always that the start_date > introduced date
    list_of_people = []

    worked_days = 0
    no_worked_days = 0

    weekdays = []
    worked_dates = []
    no_worked_dates = []

    # parsing the dates to weekdays 

    for date in dates:
        weekdays.append(day_to_weekday_name(date.isoweekday()))
    
    food_classes = {}
    beverages_classes = {}
    items_introduced_between_dates = {}

    items_between_dates = {
        'info': False,

        'BREAKFAST':[],
        'LUNCH':[],
        'SNACK':[],
        'CEREAL':[],
        'FRUIT':[],
        'COOKIE':[],
        'CHOCOLATE':[],
        'OTHER_FOOD':[],

        'WATER':[],
        'JUICE':[],
        'SODA':[],
        'OTHER_BEVERAGES':[]
    }

    food_tables_names = ['breakfasts', 'lunch', 'snacks', 'cereals', 'fruits', 'cookies', 'chocolates', 'others']
    beverages_tables_names = ['waters', 'juices', 'sodas', 'others']

    main_food_tables = [_FoodsInStock, _FoodExpenses]
    main_beverages_tables = [_BeveragesInStock, _BeverageExpenses]
    
    for name in food_tables_names:
        new_data = ItemsInStockInformation('food', name, [], [], [], [], [], [])
        food_classes[name] = new_data

    for name in beverages_tables_names:
        new_data = ItemsInStockInformation('beverages', name, [], [], [], [], [], [])
        beverages_classes[name] = new_data

    for date in dates:
        people = _People.query.get(date)
        if people is not None and people.total != 0:
            worked_days += 1
            worked_dates.append(date)

            items_between_dates['info'] = True

            list_of_people.append(_People.query.get(date))
        else:
            no_worked_days += 1
            no_worked_dates.append(date)

    if not items_between_dates['info']:
        return 'There is no data between the two selected dates or no attendance has been added between these two dates. Try other dates or check attendance for those dates'
    # we first add the deleted items and the added items, so that we avoid showing double items

    f_d = _FoodItemsInfo.query.all()
    b_d = _BeverageItemsInfo.query.all()

    deleted_food = []
    deleted_beverages = []

    for item in f_d:
        if item.deleted_date in dates:
            deleted_food.append(item)

    for item in b_d:
        if item.deleted_date in dates:
            deleted_beverages.append(item)

    # we need to return a dictionary with the following data: initial_stock_avg, final_stock_avg, daily_consumption, total_consumed
    # we get from this fucntion a dictionary contaning a object: ItemInformation

    deleted_food_object = get_deleted_items_averages(deleted_food, start_date, worked_dates)
    deleted_beverages_object = get_deleted_items_averages(deleted_beverages, start_date, worked_dates, food=False)

    # getting the averages of the items that were added before the start_date
    # getting the items between the dates

    for date in worked_dates:
        # getting the data from the selected days, due to the fact that there can be 
        # None types since there are days in which people do not go to work we need to care about that 
        # there are two 'others' since we have to evaluate tha others from the food and beverage tables
        tables = ['breakfasts', 'lunch', 'snacks', 'cereals', 'fruits', 'cookies', 'chocolates', 'others', 'water', 'juices', 'sodas', 'others']

        others_food = True

        # first getting the tables in stock 
        for table in tables:

            # we have two make this twice since it is necessary to get InStock and Expenses
            for n in range(2):
                # getting the table realt
                try:
                    list_of_items = getattr(main_food_tables[n].query.get(date), table)
                    
                    if not others_food and table == 'others':
                        raise(AttributeError)

                except AttributeError:
                    list_of_items = getattr(main_beverages_tables[n].query.get(date), table)

                if table in food_tables_names and others_food:
                    current_object = food_classes
                    food = True
                    deleted_items = deleted_food_object
                else:
                    current_object = beverages_classes
                    food = False
                    deleted_items = deleted_beverages_object
                
                if table == 'water':
                    table = 'waters'

                if table == 'lunch':
                    item_type = table
                else:
                    item_type = table[:-1]
           
                if n == 0:
                    current_object[table].items_in_stock.append(get_items_between_dates(list_of_items, item_type, start_date, date, items_introduced_between_dates, items_between_dates, deleted_items=deleted_items, food=food, in_stock=True))
                elif n == 1:
                    current_object[table].items_expenses.append(get_items_between_dates(list_of_items, item_type, start_date, date, items_introduced_between_dates, items_between_dates, deleted_items=deleted_items, food=food, in_stock=False))

            if others_food and table == 'others':
                others_food = False
                

    # getting the main averages
    average_foods_in_stock = get_averages_from_table(_FoodsInStock, worked_dates)
    average_beverages_in_stock = get_averages_from_table(_BeveragesInStock, worked_dates)

    average_food_expenses = get_averages_from_table(_FoodExpenses, worked_dates)

    average_beverages_expenses = get_averages_from_table(_BeverageExpenses, worked_dates)
    average_people = get_averages_from_table(_People, worked_dates)

    get_averages(food_classes, beverages_classes, worked_dates, food_tables_names, beverages_tables_names)
    # once done this we will convert the objects in list that we can send to the fronted

    items_added_between_dates = get_items_added_between_dates_averages(items_introduced_between_dates)


    return render_template('pantry/report_between_dates.html',
    # list of elements
    items_between_dates=items_between_dates,
    # food
    items_added_between_dates=items_added_between_dates,
    #
    deleted_food_object = deleted_food_object,
    #food_in_db=food_in_db,
    # beverages
    deleted_beverages_object=deleted_beverages_object,
    #beverages_in_db=beverages_in_db,
    # dates
    start_date=start_date, 
    end_date=end_date, 
    dates=dates, 
    weekdays=weekdays,
    total_days=len(dates),
    worked_days=worked_days,
    no_worked_days=no_worked_days,
    # expenses 
    # averages for tables
    # in stock
    average_foods_in_stock=average_foods_in_stock,
    average_beverages_in_stock=average_beverages_in_stock,
    # Poeple
    average_people=average_people,
    # expenses
    average_food_expenses=average_food_expenses,
    average_beverages_expenses=average_beverages_expenses,
    # averages and total consumed for items 
    total_item_breakfast_consumed=food_classes['breakfasts'].total_consumed,
    item_breakfast_average_consumed=food_classes['breakfasts'].daily_average_consumption,
    initial_average_breakfast_stock=food_classes['breakfasts'].initial_average_stock,
    final_average_breakfast_stock=food_classes['breakfasts'].final_average_stock,
    # - 
    total_item_lunch_consumed=food_classes['lunch'].total_consumed,
    item_lunch_average_consumed=food_classes['lunch'].daily_average_consumption,
    initial_average_lunch_stock=food_classes['lunch'].initial_average_stock,
    final_average_lunch_stock=food_classes['lunch'].final_average_stock,
    #-
    total_item_snack_consumed=food_classes['snacks'].total_consumed,
    item_snack_average_consumed=food_classes['snacks'].daily_average_consumption,
    initial_average_snacks_stock=food_classes['snacks'].initial_average_stock,
    final_average_snacks_stock=food_classes['snacks'].final_average_stock,
    #-
    total_item_cereal_consumed=food_classes['cereals'].total_consumed,
    item_cereal_average_consumed=food_classes['cereals'].daily_average_consumption,
    initial_average_cereals_stock=food_classes['cereals'].initial_average_stock,
    final_average_cereals_stock=food_classes['cereals'].final_average_stock,
    #-
    total_item_fruit_consumed=food_classes['fruits'].total_consumed,
    item_fruit_average_consumed=food_classes['fruits'].daily_average_consumption,
    initial_average_fruits_stock=food_classes['fruits'].initial_average_stock,
    final_average_fruits_stock=food_classes['fruits'].final_average_stock,
    #-
    total_item_cookie_consumed=food_classes['cookies'].total_consumed,
    item_cookie_average_consumed=food_classes['cookies'].daily_average_consumption,
    initial_average_cookies_stock=food_classes['cookies'].initial_average_stock,
    final_average_cookies_stock=food_classes['cookies'].final_average_stock,
    #-
    total_item_chocolate_consumed=food_classes['chocolates'].total_consumed,
    item_chocolate_average_consumed=food_classes['chocolates'].daily_average_consumption,
    initial_average_chocolates_stock=food_classes['chocolates'].initial_average_stock,
    final_average_chocolates_stock=food_classes['chocolates'].final_average_stock,
    #-
    total_item_other_foods_consumed=food_classes['others'].total_consumed,
    item_other_foods_average_consumed=food_classes['others'].daily_average_consumption,
    initial_average_other_foods_stock=food_classes['others'].initial_average_stock,
    final_average_other_foods_stock=food_classes['others'].final_average_stock,

    # Beverages 
    total_item_water_consumed=beverages_classes['waters'].total_consumed,
    item_water_average_consumed=beverages_classes['waters'].daily_average_consumption,
    initial_average_waters_stock=beverages_classes['waters'].initial_average_stock,
    final_average_waters_stock=beverages_classes['waters'].final_average_stock,
    # -
    total_item_juice_consumed=beverages_classes['juices'].total_consumed,
    item_juice_average_consumed=beverages_classes['juices'].daily_average_consumption,
    initial_average_juices_stock=beverages_classes['juices'].initial_average_stock,
    final_average_juices_stock=beverages_classes['juices'].final_average_stock,  
    # -
    total_item_soda_consumed=beverages_classes['sodas'].total_consumed,
    item_soda_average_consumed=beverages_classes['sodas'].daily_average_consumption,
    initial_average_sodas_stock=beverages_classes['sodas'].initial_average_stock,
    final_average_sodas_stock=beverages_classes['sodas'].final_average_stock,
    # -
    total_item_other_beverages_consumed=beverages_classes['others'].total_consumed,
    item_other_beverages_average_consumed=beverages_classes['others'].daily_average_consumption,
    initial_average_other_beverages_stock=beverages_classes['others'].initial_average_stock,
    final_average_other_beverages_stock=beverages_classes['others'].final_average_stock,
    # bloomber_view
    report_for_share=report_for_share,
    # for js
    day=day,
    month=month,
    year=year,
    show_link=show_link
    )


if __name__ == '__main__':
    app.run(debug=False)

    
