import os
import pandas as pd
from pymongo import MongoClient

# Подключение к лок бд
client = MongoClient("mongodb://localhost:27017")
db = client["nutrition_db"]
collection = db["products"]

# Очистим коллекцию
collection.delete_many({})

# Проход по всем csv файлам
for filename in os.listdir("data"):
    if filename.endswith(".csv"):
        df = pd.read_csv(os.path.join("data", filename))

        # Пропускаем, если не найден нужный столбец
        if "Продукт" not in df.columns:
            continue

        # Переименование колонок (Mongo не любит кириллицу в ключах)
        df = df.rename(columns={
            "Продукт": "title",
            "Калорийность": "calories",
            "Белки": "proteins",
            "Жиры": "fats",
            "Углеводы": "carbohydrates"
        })

        collection.insert_many(df.to_dict("records"))

print("✅ Данные загружены в MongoDB!")


