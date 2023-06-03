from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# КНОПКИ МЕНЮ
btn_malling = KeyboardButton("Рассылка по группам")
btn_malling_excel = KeyboardButton("Рассылка по номерам")
btn_all_chat = KeyboardButton("Список чатов")
btn_check = KeyboardButton("Проверить номер")
btn_add_admin = KeyboardButton("Добавить админа")

btn_malling_text = KeyboardButton("Текст")
btn_malling_photo = KeyboardButton("Текст + картинка")

btn_cancel = KeyboardButton("Отмена")


BUTTON_TYPES = {
    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_malling, btn_malling_excel).add(btn_all_chat, btn_check).add(btn_add_admin),
    "BTN_VIEW_MALLING": ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_malling_text, btn_malling_photo).add(btn_cancel),
    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),

}
