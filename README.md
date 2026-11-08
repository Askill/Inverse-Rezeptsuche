# Inverse-Rezeptsuche (Inverse Recipe Search)

Find recipes you can cook from the ingredients you already have.

Built on a dataset of 10,000 recipes scraped from Chefkoch.de. Ingredient queries return results in under half a second (measured on the deployed build).

**Stack:** Python, Flask, FlaskRESTful, SQLAlchemy, PostgreSQL, pandas, natural-language processing.

The recipe database itself is not distributed, for copyright reasons. The DB model can be viewed in db2.py.

## Deutsch

Eine Webapp zum Finden von Rezepten, die mit vorhandenen Zutaten zubereitet werden können. Basierend auf einer Datenbasis von 10k Rezepten von Chefkoch.de werden Rezepte in <0.5s returned. Die Datenbank wird aus urheberrechtlichen Gründen nicht bereitgestellt, das DB Modell kann aber in db2.py eingesehen werden.
