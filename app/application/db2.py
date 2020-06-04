import sqlalchemy as db
from sqlalchemy import Column, String, Integer, Numeric, Table, DateTime, ARRAY, ForeignKey, create_engine, LargeBinary, Enum, Text
from sqlalchemy.orm import sessionmaker, relationship, column_property
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import enum
from flask import Flask
import time

engine = db.create_engine('mysql+mysqldb://root@server/fs2?charset=utf8mb4', echo=False, encoding="utf8", pool_size=1000, max_overflow=0, pool_pre_ping=True)

Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False)

# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-object

class Recipe(Base):
    __tablename__ = "recipe"
    recipe_id = Column('recipe_id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', Text)
    instructions = Column('instructions', Text)
    url = Column('url', Text)
    img = Column('img', LargeBinary(length=(2**32)-1))
    imgURL = Column('imgURL', Text)
    ingredient = relationship("RecIngred", back_populates="recipe")

class RecIngred(Base):

    __tablename__ = 'recingred'
    ingredient_amount = Column('ingredient_amount', Text)
    ingredient_amount_mu = Column('ingredient_amount_mu', Text)    # measurement unit

    recipe = relationship("Recipe", back_populates="ingredient")
    ingredient = relationship("Ingredient", back_populates="recipe")

    recipe_id = Column(Integer, ForeignKey('recipe.recipe_id'), primary_key=True)
    ingredient_name = Column(String(200), ForeignKey('ingredient.name'), primary_key=True)


class Ingredient(Base):
    __tablename__ = "ingredient"
    name = Column('name', String(200), primary_key=True)
    recipe = relationship("RecIngred", back_populates="ingredient")
    trunks = relationship("IngredTrunk", back_populates="ingredient")

class IngredTrunk(Base):
    __tablename__ = 'ingredtrunk'
    ingredient_name = Column(String(200), ForeignKey('ingredient.name'), primary_key=True)
    trunk_name = Column(String(50), ForeignKey('trunk.name'), primary_key=True)

    ingredient = relationship("Ingredient", back_populates="trunks")
    trunk = relationship("Trunk", back_populates="ingredients")

class Trunk(Base):
    __tablename__ = "trunk"
    name = Column('name', String(50), primary_key=True)
    ingredients = relationship("IngredTrunk", back_populates="trunk")


def initDB(counter=0):
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)
        counter += 1
        if counter < 13:
            time.sleep(5)
            initDB(counter)

initDB()