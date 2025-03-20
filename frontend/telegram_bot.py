import json

import dotenv
import asyncio
import os
from pathlib import Path
import requests
from random import randint
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

from backend.user_data_service import get_data, save_data
from backend.models import ResultMeas
from backend.audio_service import trans_audio

project_path = Path.cwd().parent
data_path = project_path / "data"
data_path.mkdir(exist_ok=True)
users_path = project_path / "data" / "users.json"

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

rand_sp_word = ["Рыба раду радует, рыба радостна всегда.",
    "Рома ростом рос, да не дорос.",
    "Рано роза распустилась, рано роза отцвела.",
    "Рубят ровно, рубят рьяно, рубят рощу у реки.",
    "Рой воробьёв растревожил рябчика.",
    "Расскажи про рака, про ракову жену.",
    "Рамка рвётся, рот раскрылся, рычит рассерженный ротвейлер.",
    "Река разлилась, разом рощу разделила.",
    "Робкий ровный ряд ребят ритмично речку роет.",
    "Рано утром радуга разлилась разноцветьем.",
    "Рекруты ругали ростовщика за разбитый рубль.",
    "Рябина рыжая роняет россыпью рябые листья.",
    "Ручеёк радужно разрезал ров у рощицы.",
    "Рак рычит, рот разинул, рыбу рвёт на ровные куски.",
    "Роща рассыпала рябину россыпью рыжей.",
    "Рваный рюкзак растерял разные редкие вещи.",
    "Ромашковый рой резво рыскает рядом.",
    "Река рычит, рябь разносит ровными кругами.",
    "Рыбак рыбачил, рыбу резал, ровно разделил куски.",
    "Рыжий рысак резво рванул рысью.",
    "Ремень рвётся, рюкзак рвёт рубаху.",
    "Рёв раскатистый раздался рядом с рощей.",
    "Рябина рдеет, роса рассветная расплескалась.",
    "Рыбак рюмку роняет – ртуть разливается.",
    "Ржавый робот ритмично раскручивает ротор.",
    "Рой рябчиков резво ринулся в рощу.",
    "Разноцветные розы распустились в росе.",
    "Родник разлился, ромашки раскинулись рядом.",
    "Рак расправил рыжие рога, развернулся и рванул.",
    "Резко ринулся ретивый рысак, роняя рыжую гриву."


]
@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer(
        text="<b>Привет!</b> 👋\nОтправь голосовое сообщение или файл формата .mp3 для распознавания дефектов речи!\nНапиши /profile чтобы узнать время и результат последней проверки!\nНапиши /task чтобы я дал тебе скороговорку",
        parse_mode=ParseMode.HTML
    )


@dp.message(Command("profile"))
async def profile_message(message: types.Message):
    user_id = str(message.from_user.id)

    result = get_data(users_path, user_id)
    if result:
        result_meas = ResultMeas(
            data_last_meas=result.data_last_meas,
            res_last_meas=result.res_last_meas
        )

        message_res = f"<b>Дата последней проверки:</b> {result_meas.data_last_meas.strftime('%Y-%m-%d %H:%M')}\n<b>Обнаружена ли картавость:</b> {'да' if result_meas.res_last_meas else 'нет'}"
    else:
        message_res = "Вы еще не проверяли есть ли у вас картавость"

    await message.answer(
        text=message_res,
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("task"))
async def task_message(message: types.Message):
    await message.answer(
        text=f"Повтори-ка:\n{rand_sp_word[randint(0, 29)]}",
        parse_mode=ParseMode.HTML
    )


@dp.message(lambda message: message.audio or message.voice)
async def audio(message: types.Message):
    user_id = str(message.from_user.id)
    file_id = message.audio.file_id if message.audio else message.voice.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = data_path / f"audio_{user_id}.mp3"

    await bot.download_file(file_path, destination=destination)

    data_last_meas = datetime.now()
    translated_audio, sr = trans_audio(destination)

    data = json.dumps({
        "y": translated_audio,
        "sr": sr
    })

    response = requests.post(url=f"http://127.0.0.1:8000/libr_audio/", data=data)

    if response.status_code == 200:
        res_last_meas = response.json()["burr"]
        result_meas = ResultMeas(data_last_meas=data_last_meas, res_last_meas=res_last_meas)

        if res_last_meas:
            message_res = "<b>У вас обнаружена картавость</b>❌"
        else:
            message_res = "<b>У вас не обнаружено картавости</b>✅"

        save_data(users_path, user_id, result_meas)
    else:
        message_res = "<b>Неудачное подключение к модели</b>❌"

    await message.reply(
        text=message_res,
        parse_mode=ParseMode.HTML
    )

    if destination.exists():
        destination.unlink()


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
