def format_product(product):
    return (
        f"📌 {product['title']}\n"
        f"🔥 Калории: {product['calories']}\n"
        f"💪 Белки: {product['proteins']}\n"
        f"🧈 Жиры: {product['fats']}\n"
        f"🍞 Углеводы: {product['carbohydrates']}"
    )
