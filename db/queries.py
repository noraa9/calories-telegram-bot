from lesson2.db.connect import products_collection
from rapidfuzz import fuzz

def find_products(query):
    all_products = list(products_collection.find())
    scored = []

    for product in all_products:
        score = fuzz.partial_ratio(query.lower(), product['title'].lower())
        if score > 70:  # фильтр по порогу
            scored.append((score, product))

    scored.sort(reverse=True, key=lambda x: x[0])  # сортируем от лучших
    return [p[1] for p in scored]
