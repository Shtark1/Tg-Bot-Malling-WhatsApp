import datetime
import asyncio
import requests
import openpyxl


def all_name_groups():
    url = "https://wappi.pro/api/sync/chats/get?profile_id=63ef4aa6-5fa6&limit=200&show_all=true&offset=0"

    headers = {
      'Authorization': ''
    }

    response = requests.request("GET", url, headers=headers).json()["dialogs"]
    name_groups = []
    users_group = []
    for all_users in response:
        try:
            name_groups = name_groups + [all_users["group"]["Name"]]
            users_group = users_group + [all_users["group"]["Participants"]]
        except:
            pass

    return [name_groups, users_group]


async def malling_users(photo_malling, date_malling, text_malling, users_group):
    if date_malling == "0":
        pass
    else:
        current_time = datetime.datetime.now()
        target_time = datetime.datetime.strptime(date_malling, "%d.%m.%Y %H.%M")

        time_difference = target_time - current_time

        seconds = time_difference.total_seconds()
        await asyncio.sleep(seconds)

    for user in users_group:
        user_id = user["JID"]
        if not user["IsAdmin"]:
            if photo_malling:
                url = "https://wappi.pro/api/async/message/img/send?profile_id=63ef4aa6-5fa6"
                payload = f"{{\r\n    \"recipient\" : \"{user_id.split('@')[0]}\",\r\n    \"caption\": \"{text_malling}\",\r\n    \"b64_file\" : \"{photo_malling}\"\r\n}}".encode("utf-8")
                headers = {
                    'Authorization': ''
                }
                requests.request("POST", url, headers=headers, data=payload)

            else:
                url = "https://wappi.pro/api/async/message/send?profile_id=63ef4aa6-5fa6"
                payload = f"{{\r\n    \"body\":\"{text_malling}\",\r\n    \"recipient\":\"{user_id.split('@')[0]}\"\r\n}}".encode("utf-8")

                headers = {
                    'Authorization': ''
                }
                requests.request("POST", url, headers=headers, data=payload)


def check_number(phone):
    url = f"https://wappi.pro/api/sync/contact/check?profile_id=63ef4aa6-5fa6&phone={phone}"
    headers = {'Authorization': ''}

    response = requests.request("GET", url, headers=headers).json()["on_whatsapp"]

    return response


async def get_excel(message, bot):
    i = 0
    all_info = []

    while True:
        url = f"https://wappi.pro/api/sync/chats/get?profile_id=63ef4aa6-5fa6&limit=200&&offset={i}"

        headers = {
            'Authorization': ''
        }
        try:
            response = requests.request("GET", url, headers=headers).json()["dialogs"]
            for user in response:
                try:
                    user_id = user["id"].split('@')[0]
                    name = user["contact"]["FullName"]
                    push_name = user["contact"]["PushName"]

                    all_info = all_info + [[user_id, name, push_name]]
                except:
                    pass

        except:
            break
        i += 200

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for row_data in all_info:
        sheet.append(row_data)

    workbook.save(f"{message.message_id}.xlsx")


async def malling_users_excel(photo_malling, date_malling, text_malling, users_group):
    if date_malling == "0":
        pass
    else:
        current_time = datetime.datetime.now()
        target_time = datetime.datetime.strptime(date_malling, "%d.%m.%Y %H.%M")

        time_difference = target_time - current_time

        seconds = time_difference.total_seconds()
        await asyncio.sleep(seconds)

    for user in users_group:
        if photo_malling:
            url = "https://wappi.pro/api/async/message/img/send?profile_id=63ef4aa6-5fa6"
            payload = f"{{\r\n    \"recipient\" : \"{user}\",\r\n    \"caption\": \"{text_malling}\",\r\n    \"b64_file\" : \"{photo_malling}\"\r\n}}".encode("utf-8")
            headers = {
                'Authorization': ''
            }
            requests.request("POST", url, headers=headers, data=payload)

        else:
            url = "https://wappi.pro/api/async/message/send?profile_id=63ef4aa6-5fa6"
            payload = f"{{\r\n    \"body\":\"{text_malling}\",\r\n    \"recipient\":\"{user}\"\r\n}}".encode("utf-8")

            headers = {
                'Authorization': ''
            }
            requests.request("POST", url, headers=headers, data=payload)