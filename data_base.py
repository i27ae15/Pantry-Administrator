from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///DataBase.db')
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db.query_property()

def init_db():
    from models import _FoodsInStock, _FoodExpenses, _BeveragesInStock, _BeverageExpenses, _BeverageItemsInfo, _FoodItemsInfo, _BreakfastsInStock, _BreakfastExpenses, _LunchExpenses, _LunchInStock, _SnackExpenses, _SnacksInStock, _CerealExpenses, _CerealsInStock, _FruitExpenses, _FruitsInStock, _CookiesInStock, _CookiesExpenses, _ChocolatesInStock, _ChocolatesExpenses, _OtherFoodsInStock, _OtherFoodsExpenses, _People, _WaterExpenses, _WatersInStock, _SodaExpenses, _SodasInStock, _JuiceExpenses, _OtherBeveragesExpenses, _OtherBeveragesInStock, _JuicesInStock, _User
    Base.metadata.create_all(bind=engine) 

init_db()