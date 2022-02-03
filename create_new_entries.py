from data_base import db
from datetime import datetime

from models import _FoodsInStock, _FoodExpenses, _BeveragesInStock, _BeverageExpenses, _BeverageItemsInfo, _FoodItemsInfo, _BreakfastsInStock, _BreakfastExpenses, _LunchExpenses, _LunchInStock, _SnackExpenses, _SnacksInStock, _CerealExpenses, _CerealsInStock, _FruitExpenses, _FruitsInStock, _CookiesInStock, _CookiesExpenses, _ChocolatesInStock, _ChocolatesExpenses, _OtherFoodsInStock, _OtherFoodsExpenses, _People, _WaterExpenses, _WatersInStock, _SodaExpenses, _SodasInStock, _JuiceExpenses, _OtherBeveragesExpenses, _OtherBeveragesInStock, _JuicesInStock, _User

def _create_new_entries(date=None, people=True):

    now = datetime.now()

    if date is None:
        date = now.date()

    if people:
        new_people = _People(
            date=date,
        )

        db.add(new_people)


    new_food = _FoodsInStock(
        date=date,
    )

    new_beverages = _BeveragesInStock(
        date=date,
    )

    new_food_expenses = _FoodExpenses(
        date=date,
    )

    new_expenses_beverages = _BeverageExpenses(
        date=date,
    )


    db.add(new_food)
    db.add(new_beverages)
    db.add(new_food_expenses)
    db.add(new_expenses_beverages)
    db.commit()