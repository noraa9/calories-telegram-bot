# from aiogram import Router, types
# from aiogram.filters import CommandStart
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from lesson2.db.queries import find_products
# from lesson2.utils.formatters import format_product
# from rapidfuzz import fuzz
#
# router = Router()
# user_states = {}
#
# main_menu = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="🔍 Поиск продукта")],
#     [KeyboardButton(text="📋 Список категорий")]
# ], resize_keyboard=True)
#
# @router.message(CommandStart())
# async def start_handler(message: types.Message):
#     await message.answer(
#         "Привет! Я бот по калорийности продуктов. Введите название продукта.",
#         reply_markup=main_menu
#     )
#
#
# @router.message(lambda msg: msg.text == "🔍 Поиск продукта")
# async def ask_product_name(message: types.Message):
#     await message.answer("Введите название продукта, который вас интересует.")
#
#
# @router.message(lambda msg: msg.text == "📋 Список категорий")
# async def categories_handler(message: types.Message):
#     await message.answer("🔧 Функция списка категорий в разработке...")
#
#
# @router.callback_query(lambda call: call.data == "more")
# async def show_more(call: types.CallbackQuery):
#     state = user_states.get(call.from_user.id)
#
#     if not state:
#         await call.message.answer("❌ Ничего не найдено.")
#         return
#
#     offset = state["offset"]
#     results = state["results"]
#
#     next_batch = results[offset:offset + 5]
#     if not next_batch:
#         await call.message.answer("⚠️ Больше ничего нет.")
#         return
#
#     for prod in next_batch:
#         await call.message.answer(format_product(prod))
#
#     state["offset"] += 5
#
#     if state["offset"] < len(results):
# #         Еще остались результаты, посмотреть еще
#         keyboard = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="Показать ещё", callback_data="more")]
#         ])
#         await call.message.answer("Продолжим?", reply_markup=keyboard)
#     else:
#         await call.message.answer("✅ Это всё, что нашлось.")
#
#
# @router.message()
# async def search_handler(message: types.Message):
#     query = message.text
#     results = find_products(query)
#
#     if results:
#         best_match = results[0]
#
#         if fuzz.partial_ratio(query.lower(), best_match['title'].lower()) < 90:
#             keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                 [InlineKeyboardButton(text="Да", callback_data="confirm_match")],
#                 [InlineKeyboardButton(text="Нет", callback_data="calcel_match")]
#             ])
#             user_states[message.from_user.id] = {
#                 "query": query,
#                 "offset": 0,
#                 "results": results,
#                 "suggeted": best_match
#             }
#             await message.answer(
#                 f"Вы имели в виду: {best_match['title']}?"
#             )
#             return
#
#         user_states[message.from_user.id] = {
#             "query": query,
#             "offset": 5,
#             "results": results
#         }
#
#         for prod in results[:5]:
#             await message.answer(format_product(prod))
#
#         user_states[message.from_user.id]["offset"] += 5
#         print(results)
#         if len(results) > 5:
#             keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                 [InlineKeyboardButton(text="Показать ещё", callback_data="more")]
#             ])
#             await message.answer("Найдено больше результатов:", reply_markup=keyboard)
#     else:
#         await message.answer("❌ Ничего не найдено. Попробуйте другое название.")
#
# def register_handlers(dp):
#     dp.include_router(router)

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from lesson2.db.queries import find_products
from lesson2.utils.formatters import format_product
from rapidfuzz import fuzz

router = Router()
user_states = {}
# Тут будут хранятся названия продуктов которые он имел в виду
user_confirmed_matches = {}

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🔍 Поиск продукта")],
    [KeyboardButton(text="📋 Список категорий")]
], resize_keyboard=True)


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот по калорийности продуктов. Введите название продукта.",
        reply_markup=main_menu
    )


@router.message(lambda msg: msg.text == "🔍 Поиск продукта")
async def ask_product_name(message: types.Message):
    await message.answer("Введите название продукта, который вас интересует.")


@router.message(lambda msg: msg.text == "📋 Список категорий")
async def categories_handler(message: types.Message):
    await message.answer("🔧 Функция списка категорий в разработке...")


@router.callback_query(lambda call: call.data == "more")
async def show_more(call: types.CallbackQuery):
    state = user_states.get(call.from_user.id)

    if not state:
        await call.message.answer("❌ Ничего не найдено.")
        return

    offset = state["offset"]
    results = state["results"]

    next_batch = results[offset:offset + 5]
    if not next_batch:
        await call.message.answer("⚠️ Больше ничего нет.")
        return

    for prod in next_batch:
        await call.message.answer(format_product(prod))

    state["offset"] += 5

    if state["offset"] < len(results):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Показать ещё", callback_data="more")]
        ])
        await call.message.answer("Показать ещё?", reply_markup=keyboard)
    else:
        await call.message.answer("✅ Это всё, что нашлось.")


@router.callback_query(lambda call: call.data == "confirm_match")
async def confirm_match(call: types.CallbackQuery):
    user_id = call.from_user.id
    state = user_states.get(user_id)
    if not state:
        await call.message.answer("❌ Что-то пошло не так.")
        return

    suggested = state["suggested"]
    original_query = state["query"]

    # 📌 Сохраняем подтверждённое соответствие
    user_confirmed_matches.setdefault(user_id, {})[original_query.lower()] = suggested

    results = state["results"]
    await call.message.answer(f"🔢 Найдено {len(results)} подходящих товаров:")
    for prod in results[:5]:
        await call.message.answer(format_product(prod))

    state["offset"] = 5

    if len(results) > 5:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Показать ещё", callback_data="more")]
        ])
        await call.message.answer("Найдено больше результатов:", reply_markup=keyboard)


@router.callback_query(lambda call: call.data == "cancel_match")
async def cancel_match(call: types.CallbackQuery):
    await call.message.answer("Попробуйте ввести название продукта иначе.")


@router.message()
async def search_handler(message: types.Message):
    query = message.text
    user_id = message.from_user.id
    lower_query = query.lower()

    results = find_products(query)

    if not results:
        await message.answer("❌ Ничего не найдено. Попробуйте другое название.")
        return

    # ✅ Если пользователь уже подтверждал это слово раньше — не спрашиваем
    if user_id in user_confirmed_matches and lower_query in user_confirmed_matches[user_id]:
        confirmed_title = user_confirmed_matches[user_id][lower_query]
        # ставим подтверждённый товар в начало
        results = [r for r in results if r["title"] == confirmed_title] + [r for r in results if r["title"] != confirmed_title]

    else:
        # 💬 Проверяем, стоит ли уточнить
        best_match = results[0]
        similarity = fuzz.partial_ratio(query.lower(), best_match["title"].lower())
        if similarity < 90:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Да", callback_data="confirm_match")],
                [InlineKeyboardButton(text="Нет", callback_data="cancel_match")]
            ])
            user_states[user_id] = {
                "query": query,
                "offset": 0,
                "results": results,
                "suggested": best_match["title"]
            }
            await message.answer(
                f"🔎 Вы имели в виду: *{best_match['title']}*?",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            return

    # 🟩 Если всё ок — показываем
    user_states[user_id] = {
        "query": query,
        "offset": 5,
        "results": results
    }

    await message.answer(f"🔢 Найдено {len(results)} подходящих товаров:")

    for prod in results[:5]:
        await message.answer(format_product(prod))

    if len(results) > 5:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Показать ещё", callback_data="more")]
        ])
        await message.answer("Найдено больше результатов:", reply_markup=keyboard)



def register_handlers(dp):
    dp.include_router(router)
