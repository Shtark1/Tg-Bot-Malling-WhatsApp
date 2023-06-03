import openpyxl
import os
import base64
import re
import logging

from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.utils import StatesAdmin, StatesMalling
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.cfg import TOKEN, ADMIN_ID
from dop_functional.SearchGroup import all_name_groups, malling_users, check_number, get_excel, malling_users_excel

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


# ===================================================
# =============== СТАНДАРТНЫЕ КОМАНДЫ ===============
# ===================================================
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    # print(StatesAdmin.all()[8])
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


# ===================================================
# ================= РАССЫЛКА ПО ГРУППАМ ================
# ===================================================
@dp.message_handler(lambda message: message.text.lower() == 'рассылка по группам')
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        state = dp.current_state(user=message.from_user.id)

        text = "Список всех групп:\n➖➖➖➖➖➖➖"
        all_groups = all_name_groups()
        for idx, group in enumerate(all_groups[0]):
            text += f"\n{idx+1}. {group}"
        await message.answer(text, reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await message.answer(MESSAGES["id_group"])
        await state.update_data(all_groups=all_groups)
        await state.set_state(StatesAdmin.all()[1])


# ================= ВЫБОР ТИПА РАССЫЛКИ ================
@dp.message_handler(state=StatesAdmin.STATES_1)
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        try:
            users_group = await state.get_data()
            users_group = users_group["all_groups"][1][int(message.text) - 1]

            await state.update_data(id_group=f"{message.text}")
            await message.answer(MESSAGES["view_malling"], reply_markup=BUTTON_TYPES["BTN_VIEW_MALLING"])
            await state.set_state(StatesAdmin.all()[2])

        except:
            await message.answer(MESSAGES["not_number_group"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[1])
    else:
        await message.answer(MESSAGES["not_number_group"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


# ================= ЗАПРОС ТЕКСТА ДЛЯ РАССЫЛКИ ================
@dp.message_handler(state=StatesAdmin.STATES_2)
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    elif message.text.lower() == "текст" or message.text.lower() == "текст + картинка":
        await message.answer(MESSAGES['text_malling'])

        if message.text.lower() == "текст":
            await state.set_state(StatesAdmin.all()[3])

        elif message.text.lower() == "текст + картинка":
            await state.set_state(StatesAdmin.all()[4])

    else:
        await message.answer(MESSAGES["not_view_malling"], reply_markup=BUTTON_TYPES["BTN_VIEW_MALLING"])
        await state.set_state(StatesAdmin.all()[2])


# ================= ЗАПРОС ФОТО ДЛЯ РАССЫЛКИ ================
@dp.message_handler(state=StatesAdmin.STATES_4)
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    else:
        await state.update_data(text_malling=f"{message.text}")
        await message.answer(MESSAGES['photo_malling'])
        await state.set_state(StatesAdmin.all()[3])


# ================= ЗАПРОС ДАТЫ И ВРЕМЕНИ ДЛЯ РАССЫЛКИ ================
@dp.message_handler(content_types=["photo"], state=StatesAdmin.STATES_3)
@dp.message_handler(state=StatesAdmin.STATES_3)
async def id_admin(message: Message, state: FSMContext):
    try:
        await message.photo[-1].download(destination_file=f'{message.message_id}.jpg')

        with open(f"{message.message_id}.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        await state.update_data(photo=f"{encoded_string}")

        os.remove(f"{message.message_id}.jpg")

        await message.answer(MESSAGES['malling_time'], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[5])
    except:
        if message.text.lower() == "отмена":
            await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()
        else:
            try:
                all_data = await state.get_data()
                text_malling = all_data["text_malling"]

                await message.answer(MESSAGES["not_photo_malling"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
                await state.set_state(StatesAdmin.all()[3])
            except:
                await state.update_data(text_malling=f"{message.text}")
                await message.answer(MESSAGES['malling_time'], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
                await state.set_state(StatesAdmin.all()[5])


# ================= ЗАПИСЬ ДАТЫ И ВРЕМЕНИ ================
@dp.message_handler(state=StatesAdmin.STATES_5)
async def id_admin(message: Message, state: FSMContext):
    match = re.match(r'\d{2}\.\d{2}\.\d{4} \d{2}\.\d{2}', message.text)

    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    elif message.text == "0" or match is not None:
        if message.text == "0":
            await message.answer(MESSAGES["malling_start"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        else:
            await message.answer(f"Рассылка заплонирована на {message.text}", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.update_data(time_malling=f"{message.text}")

        all_data = await state.get_data()
        text_malling = all_data["text_malling"]
        date_malling = message.text

        users_group = all_data["all_groups"][1][int(all_data["id_group"]) - 1]
        try:
            photo_malling = all_data["photo"]
            await state.finish()
            await malling_users(photo_malling, date_malling, text_malling, users_group)
        except Exception as ex:
            print(ex)
            await state.finish()
            await malling_users(False, date_malling, text_malling, users_group)

    elif match is None:
        await message.answer("Неверный формат")
        await message.answer(MESSAGES["malling_time"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[5])


# ===================================================
# ================= ПРОВЕРКА НОМЕРА =================
# ===================================================
@dp.message_handler(lambda message: message.text.lower() == 'проверить номер')
async def add_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES["check_number"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[6])


@dp.message_handler(state=StatesAdmin.STATES_6)
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif re.match(r'^7\d{10}$', message.text):
        what_num = str(check_number(message.text))
        if what_num == "False":
            await message.reply(f"❎ {what_num.upper( )} ❎", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        else:
            await message.reply(f"✅ {what_num.upper()} ✅", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.finish()
    else:
        await message.answer(MESSAGES["not_number"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[6])


# =============================================================
# ================= СКИНУТЬ СПИСОК ВСЕХ ЧАТОВ =================
# =============================================================
@dp.message_handler(lambda message: message.text.lower() == 'список чатов')
async def add_admin(message: Message):
    try:
        if message.from_user.id in ADMIN_ID:
            await get_excel(message, bot)

            with open(f'{message.message_id}.xlsx', 'rb') as file:
                await bot.send_document(chat_id=message.chat.id, document=file, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

            os.remove(f"{message.message_id}.xlsx")

    except:
        await message.answer(MESSAGES["error_excel"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


# =======================================================
# ================= РАССЫЛКА ПО НОМЕРАМ =================
# =======================================================
@dp.message_handler(lambda message: message.text.lower() == 'рассылка по номерам')
async def add_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES["malling_excel"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesMalling.all()[0])


# ================= ЗАПРОС ТЕКСТА =================
@dp.message_handler(state=StatesMalling.STATE_0, content_types=["document", "text"])
async def id_admin(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "отмена":
            await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()
        else:
            await message.answer(MESSAGES["not_malling_excel"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesMalling.all()[0])
    except:
        try:
            file_obj = await bot.get_file(message.document.file_id)
            file_path = file_obj.file_path

            await bot.download_file(file_path, f'{message.message_id}.xlsx')
            workbook = openpyxl.load_workbook(f'{message.message_id}.xlsx')
            sheet = workbook.active
            column_a = []
            for row in sheet.iter_rows(values_only=True):
                column_a.append(row[0])
            await state.update_data(all_number=column_a)

            os.remove(f'{message.message_id}.xlsx')
            await message.answer(MESSAGES["excel_file"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesMalling.all()[1])

        except Exception as ex:
            print(ex)
            await message.answer(MESSAGES["not_malling_excel"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesMalling.all()[0])


# ================= ЗАПРОС ФОТО =================
@dp.message_handler(state=StatesMalling.STATE_1)
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await state.update_data(text_malling=f"{message.text}")
        await message.answer(MESSAGES["excel_malling_photo"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesMalling.all()[2])


# ================= ЗАПРОС ФОТО =================
@dp.message_handler(state=StatesMalling.STATE_2,content_types=["photo", "text"])
async def id_admin(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "отмена":
            await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()
        else:
            await state.update_data(text_malling=f"{message.text}")
            await message.answer(MESSAGES["malling_time"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesMalling.all()[3])
    except:
        await message.photo[-1].download(destination_file=f'{message.message_id}.jpg')

        with open(f"{message.message_id}.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        await state.update_data(photo=f"{encoded_string}")
        os.remove(f"{message.message_id}.jpg")

        await message.answer(MESSAGES["malling_time"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesMalling.all()[3])


# ================= ЗАПИСЬ ДАТЫ И ВРЕМЕНИ ================
@dp.message_handler(state=StatesMalling.STATE_3)
async def id_admin(message: Message, state: FSMContext):
    match = re.match(r'\d{2}\.\d{2}\.\d{4} \d{2}\.\d{2}', message.text)

    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    elif message.text == "0" or match is not None:
        if message.text == "0":
            await message.answer(MESSAGES["malling_start"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        else:
            await message.answer(f"Рассылка заплонирована на {message.text}", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.update_data(time_malling=f"{message.text}")
        all_data = await state.get_data()
        date_malling = all_data["time_malling"]
        text_malling = all_data["text_malling"]
        users_group = all_data["all_number"]
        try:
            photo_malling = all_data["photo"]
            await state.finish()
            await malling_users_excel(photo_malling, date_malling, text_malling, users_group)
        except Exception as ex:
            print(ex)
            await state.finish()
            await malling_users_excel(False, date_malling, text_malling, users_group)

    elif match is None:
        await message.answer("Неверный формат")
        await message.answer(MESSAGES["malling_time"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[5])



# ===================================================
# ================= ДОБАВИТЬ АДМИНА =================
# ===================================================
@dp.message_handler(lambda message: message.text.lower() == 'добавить админа')
async def add_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[0])


# =============== ВВОД ID АДМИНА ===============
@dp.message_handler(state=StatesAdmin.STATES_0)
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        ADMIN_ID.append(new_users_id)
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[0])


# ===================================================
# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
# ===================================================
@dp.message_handler()
async def not_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES['not_command'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def start():
    executor.start_polling(dp, on_shutdown=shutdown)
