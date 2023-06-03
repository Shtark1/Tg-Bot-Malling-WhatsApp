from telegram_bot.utils import StatesAdmin

# СООБЩЕНИЯ ОТ БОТА
start_admin_message = "Приветствую админ 👋"
not_command_message = "Такой команды нет"
add_admin_message = """ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
not_admin_id_message = """Это не число, ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
id_group_message = 'Введи номер группы по которой сделать рассылку\nили\nжми "Отмена"'
not_number_group_message = "Такого номера группы нет!\nПопробуй ввести снова:"
view_malling_message = "Выбери тип рассылки:"
not_view_malling_message = 'Такого типа рассылки нет!\n➖➖➖➖➖➖➖➖➖\nВыбери тип рассылки\nили\nжми "Отмена"'
text_malling_message = "Введи текст для рассылки:"
photo_malling_message = "Скинь фото для рассылки:"
not_photo_malling_message = 'Это не фото!\n➖➖➖➖➖➖➖➖➖\nСкинь фото для рассылки\nили\nжми "Отмена"'
malling_time_message = """Укажи дату когда сделать рассылку в таком формате 
"26.02.2023 15.00"
➖➖➖➖➖➖➖➖➖
Если рассылку надо сделать сейчас то пиши 0"""
malling_start_message = "Рассылка началась!"
check_number_message = "Введи номер телефона с 7\nПример: 79217788731"
not_number_message = "Вы ввели не в том формате\nПример: 79217788731"
error_excel_message = "Упс...\nПроизошла ошибка, попробуй снова!"
malling_excel_message = "Отправь Excel файл с номерами для которых сделать рассылку"
not_malling_excel_message = "Это не excel файл\nОтправь Excel файл с номерами для которых сделать рассылку"
excel_file_message = "✅ Номера добавлены для рассылки ✅\n➖➖➖➖➖➖➖➖➖➖➖➖\nВведи текст рассылки:"
excel_malling_photo_message = 'Отправь фото если оно нужно в рассылке\n➖➖➖➖➖➖➖➖➖➖➖➖\nИли жми "Пропустить"'

MESSAGES = {
    "start_admin": start_admin_message,
    "not_command": not_command_message,
    "add_admin": add_admin_message,
    "not_admin_id": not_admin_id_message,
    "id_group": id_group_message,
    "not_number_group": not_number_group_message,
    "view_malling": view_malling_message,
    "not_view_malling": not_view_malling_message,
    "text_malling": text_malling_message,
    "photo_malling": photo_malling_message,
    "not_photo_malling": not_photo_malling_message,
    "malling_time": malling_time_message,
    "malling_start": malling_start_message,
    "check_number": check_number_message,
    "not_number": not_number_message,
    "error_excel": error_excel_message,
    "malling_excel": malling_excel_message,
    "not_malling_excel": not_malling_excel_message,
    "excel_file": excel_file_message,
    "excel_malling_photo": excel_malling_photo_message,
}
