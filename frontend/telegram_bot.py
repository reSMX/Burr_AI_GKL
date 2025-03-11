import dotenv
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer(
        text="Привет! 👋\n Отправь голосовое сообщение или файл формата .mp3 для распознавания дефектов речи!",
        parse_mode=ParseMode.HTML
    )


@dp.message(lambda message: message.audio or message.voice)
async def audio(message: types.Message):
    if message.audio:
        # Отправлен файл .mp3
        ...
    elif message.voice:
        # Отправлено голосовое сообщение
        ...


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
