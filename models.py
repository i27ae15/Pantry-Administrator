from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.expression import delete, null
from data_base import Base
from flask_login import UserMixin

class _User(UserMixin, Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    level = Column(Integer)
    


class _People(Base):
    __tablename__ = 'People'
    date = Column(Date,  primary_key=True)
    total = Column(Integer, default=0)


# ---------------------------------------------------------------------------------------------
# Classes for food in stock -------------------------------------------------------------------


class _FoodsInStock(Base):
    __tablename__ = 'FoodsInStock'

    date = Column(Date,  primary_key=True)

    breakfasts = relationship('_BreakfastsInStock')
    lunch = relationship('_LunchInStock')
    snacks = relationship('_SnacksInStock')
    cereals = relationship('_CerealsInStock')
    fruits = relationship('_FruitsInStock')
    cookies = relationship('_CookiesInStock')
    chocolates = relationship('_ChocolatesInStock')
    others = relationship('_OtherFoodsInStock')

    total_breakfasts = Column(Integer, default=0)
    total_lunch = Column(Integer, default=0)
    total_snacks = Column(Integer, default=0)
    total_cereals = Column(Integer, default=0)
    total_fruits = Column(Integer, default=0)
    total_cookies = Column(Integer, default=0)
    total_chocolates = Column(Integer, default=0)
    total_others = Column(Integer, default=0)

    total = Column(Integer, default=0)
    initial_stock = Column(Integer, default=0)

    #items_id
    current_breakfast_id = Column(Integer, default=0)
    current_lunch_id = Column(Integer, default=0)
    current_snack_id = Column(Integer, default=0)
    current_cereal_id = Column(Integer, default=0)
    current_fruit_id = Column(Integer, default=0)
    current_cookie_id = Column(Integer, default=0)
    current_chocolate_id = Column(Integer, default=0)
    current_other_id = Column(Integer, default=0)

    # added food
    total_breakfasts_added = Column(Integer, default=0)
    total_lunch_added = Column(Integer, default=0)
    total_snacks_added = Column(Integer, default=0)
    total_cereals_added = Column(Integer, default=0)
    total_fruits_added = Column(Integer, default=0)
    total_cookies_added = Column(Integer, default=0)
    total_chocolates_added = Column(Integer, default=0)
    total_others_added = Column(Integer, default=0)

    total_food_added = Column(Integer, default=0)


class _FoodItemsInfo(Base):
    __tablename__ = 'FoodItemsInfo'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    name = Column(String, nullable=False)
    added_date = Column(String, nullable=False)
    type = Column(String, nullable=False)
    deleted_date = Column(String)

    def __str__(self):
        return (f'name: {self.name}, type:{self.type}')


class _BreakfastsInStock(Base):
    __tablename__ = 'BreakfastsInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)


class _LunchInStock(Base):
    __tablename__ = 'LunchInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)


class _SnacksInStock(Base):
    __tablename__ = 'SnacksInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)


class _CerealsInStock(Base):
    __tablename__ = 'CerealsInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)


class _FruitsInStock(Base):
    __tablename__ = 'FruitsInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)


class _CookiesInStock(Base):
    __tablename__ = 'CookiesInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)


class _ChocolatesInStock(Base):
    __tablename__ = 'ChocolatesInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)


class _OtherFoodsInStock(Base):
    __tablename__ = 'OtherFoodsInStock'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('FoodsInStock.date'), nullable=False)

# --------------------------------------------------------------------------------------------------------
# Classes for Beverages in sock --------------------------------------------------------------------------

class _BeveragesInStock(Base):
    __tablename__ = 'BeveragesInStock'

    date = Column(Date,  primary_key=True)

    sodas = relationship('_SodasInStock')
    juices = relationship('_JuicesInStock')
    water = relationship('_WatersInStock')
    others = relationship('_OtherBeveragesInStock')
    
    total_waters = Column(Integer, default=0)
    total_juices = Column(Integer, default=0)
    total_sodas = Column(Integer, default=0)
    total_others = Column(Integer, default=0)

    total = Column(Integer, default=0)
    initial_stock = Column(Integer, default=0)

    # items id
    current_water_id = Column(Integer, default=0)
    current_juice_id = Column(Integer, default=0)
    current_soda_id = Column(Integer, default=0)
    current_other_id = Column(Integer, default=0)
    
    # added beverages
    total_waters_added = Column(Integer, default=0)
    total_juices_added = Column(Integer, default=0)
    total_sodas_added = Column(Integer, default=0)
    total_others_added = Column(Integer, default=0)

    total_beverages_added = Column(Integer, default=0)


class _BeverageItemsInfo(Base):
    __tablename__ = 'BeverageItemsInfo'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    name = Column(String, nullable=False)
    added_date = Column(String, nullable=False)
    type = Column(String, nullable=False)
    deleted_date = Column(String)

    def __str__(self):
        return (f'name: {self.name}, type:{self.type}')


class _SodasInStock(Base):
    __tablename__ = 'SodasInStock'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('BeveragesInStock.date'), nullable=False)


class _JuicesInStock(Base):
    __tablename__ = 'JuicesInStock'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('BeveragesInStock.date'), nullable=False)


class _WatersInStock(Base):
    __tablename__ = 'WatersInStock'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('BeveragesInStock.date'), nullable=False)


class _OtherBeveragesInStock(Base):
    __tablename__ = 'OtherBeveragesInStock'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)

    name = Column(String)

    initial_stock = Column(Integer)
    added = Column(Integer)
    stock = Column(Integer)

    date = Column(Date, ForeignKey('BeveragesInStock.date'), nullable=False)


# -----------------------------------------------------------------------------------------------------------
# data bases for consumtions of the items ------------------------------------------------------------------
# Food expenses

class _FoodExpenses(Base):
    __tablename__ = 'FoodExpenses'

    date = Column(Date,  primary_key=True)

    breakfasts = relationship('_BreakfastExpenses')
    lunch = relationship('_LunchExpenses')
    snacks = relationship('_SnackExpenses')
    cereals = relationship('_CerealExpenses')
    fruits = relationship('_FruitExpenses')
    cookies = relationship('_CookiesExpenses')
    chocolates = relationship('_ChocolatesExpenses')
    others = relationship('_OtherFoodsExpenses')

    total_breakfasts = Column(Integer, default=0)
    total_lunch = Column(Integer, default=0)
    total_snacks = Column(Integer, default=0)
    total_cereals = Column(Integer, default=0)
    total_fruits = Column(Integer, default=0)
    total_cookies = Column(Integer, default=0)
    total_chocolates = Column(Integer, default=0)
    total_others = Column(Integer, default=0)

    total = Column(Integer, default=0)


class _BreakfastExpenses(Base):
    __tablename__ = 'BreakfastExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _LunchExpenses(Base):
    __tablename__ = 'LunchExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _SnackExpenses(Base):
    __tablename__ = 'SnackExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _CerealExpenses(Base):
    __tablename__ = 'CerealExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _FruitExpenses(Base):
    __tablename__ = 'FruitExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _CookiesExpenses(Base):
    __tablename__ = 'CookiesExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _ChocolatesExpenses(Base):
    __tablename__ = 'ChocolatesExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _OtherFoodsExpenses(Base):
    __tablename__ = 'OtherFoodsExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('FoodExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


# Beverage expenses ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------


class _BeverageExpenses(Base):
    __tablename__ = 'BeverageExpenses'

    date = Column(Date,  primary_key=True)

    waters = relationship('_WaterExpenses')
    juices = relationship('_JuiceExpenses')
    sodas = relationship('_SodaExpenses')
    others = relationship('_OtherBeveragesExpenses')

    total_sodas = Column(Integer, default=0)
    total_waters = Column(Integer, default=0)
    total_juices = Column(Integer, default=0)
    total_others = Column(Integer, default=0)

    total = Column(Integer, default=0)


class _WaterExpenses(Base):
    __tablename__ = 'WaterExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('BeverageExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _JuiceExpenses(Base):
    __tablename__ = 'JuiceExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('BeverageExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _SodaExpenses(Base):
    __tablename__ = 'SodaExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('BeverageExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)


class _OtherBeveragesExpenses(Base):
    __tablename__ = 'OtherBeveragesExpenses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    consumption = Column(Integer)
    date = Column(Date, ForeignKey('BeverageExpenses.date'), nullable=False)
    item_id = Column(Integer, nullable=False)

