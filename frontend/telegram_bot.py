import dotenv
import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

project_path = Path.cwd().parent
data_path = project_path / "data"
data_path.mkdir(exist_ok=True)

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer(
        text="Привет! 👋\nОтправь голосовое сообщение или файл формата .mp3 для распознавания дефектов речи!",
        parse_mode=ParseMode.HTML
    )


@dp.message(lambda message: message.audio or message.voice)
async def audio(message: types.Message):
    file_id = message.audio.file_id if message.audio else message.voice.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = data_path / "audio.mp3"

    await bot.download_file(file_path, destination=destination)

    # Обращение к API

    if destination.exists():
        destination.unlink()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
