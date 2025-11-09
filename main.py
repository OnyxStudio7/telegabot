import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import FastAPI
import uvicorn
from bot.api import app as api_app
from bot.config import BOT_TOKEN, WEB_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Играть", web_app=WebAppInfo(url=WEB_URL))]
    ])
    await message.answer("Добро пожаловать в Premium Slot! 🎰", reply_markup=keyboard)

async def run_bot():
    await dp.start_polling(bot)

# объединяем бота и API в одном процессе
fastapi_app = FastAPI()
fastapi_app.mount("/", api_app)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
