# Inverse-Rezeptsuche (Inverse Recipe Search)

Find recipes you can cook from the ingredients you already have.

Built on a dataset of 10,000 recipes scraped from Chefkoch.de. Ingredient queries return results in under half a second (measured on the deployed build).

**Stack:** Python, Flask, FlaskRESTful, SQLAlchemy, PostgreSQL, pandas, natural-language processing.

The data pipeline lives in this repo: `app/background/mine.py` scrapes the recipes from Chefkoch.de, and `app/background/migrate.py` cleans, stems, and loads them into PostgreSQL. The scraped database itself is not distributed, for copyright reasons; the DB model can be viewed in `app/application/db2.py`.

## Deutsch

Eine Webapp zum Finden von Rezepten, die mit vorhandenen Zutaten zubereitet werden können. Basierend auf einer Datenbasis von 10k Rezepten von Chefkoch.de werden Rezepte in <0.5s returned. Die Datenbank wird aus urheberrechtlichen Gründen nicht bereitgestellt; die Scraping-Pipeline liegt in `app/background/mine.py` und `app/background/migrate.py`, das DB Modell in `app/application/db2.py`.
