from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот по калорийности продуктов. Введите название продукта.")

def register_handlers(dp):
    dp.include_router(router)