import sqlalchemy as db
from sqlalchemy import Column, String, Integer, Numeric, Table, DateTime, ARRAY, ForeignKey, create_engine, LargeBinary, Enum, Text
from sqlalchemy.orm import sessionmaker, relationship, column_property
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import enum
from flask import Flask
import time

engine = db.create_engine('mysql+mysqldb://root@server/fs?charset=utf8mb4', echo=False, encoding="utf8", pool_size=1000, max_overflow=0)

Base = declarative_base()
Session = sessionmaker(bind=engine)

# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-object


class Recipe(Base):
    __tablename__ = "recipe"
    recipe_id = Column('recipe_id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', Text)
    instructions = Column('instructions', Text)
    url = Column('url', Text)
    img = Column('img', LargeBinary(length=(2**32)-1))
    ingredient = relationship("Ingredient", backref="recipe")
    trunk = relationship("Trunk", backref="recipe")

    def ingredients(self):
        l = []
        for i in self.ingredient:
            l.append(i.ingredients())
        return l

    def ingredientDict(self):
        l = {}
        for i in self.ingredient:
            l[i.ingredients()] = [i.ingredient_amount, i.ingredient_amount_mu]
        return l

    def serialize(self):
        ingredients = []

        if self.img is not None:
            img = self.img.decode('utf-8')
        else:
            img = None

        data = {
            "recipe_id": self.recipe_id,
            "name":self.name,
            "instructions":self.instructions,
            "url": self.url,
            "img": img,
            "ingredients": self.ingredients()  
        }
        return data

class Ingredient(Base):
    __tablename__ = "ingredient"
    ingredient_id = Column('ingredient_id', Integer,  primary_key=True, autoincrement=True)
    name = Column('name', Text)
    ingredient_amount = Column('ingredient_amount', Text)
    ingredient_amount_mu = Column('ingredient_amount_mu', Text)    # measurement unit

    recipe_id = Column(Integer, ForeignKey('recipe.recipe_id'))
    

class Trunk(Base):
    __tablename__ = "trunk"
    trunk_id = Column('trunk_id', Integer,  primary_key=True, autoincrement=True)
    name = Column('name', Text)

    recipe_id = Column(Integer, ForeignKey('recipe.recipe_id'))

def initDB(counter):
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)
        counter += 1
        if counter < 13:
            time.sleep(5)
            initDB(counter)

initDB(0)