from heapq import nlargest
from pprint import pprint
from progress.bar import IncrementalBar
import requests
import json
import os
import time
from heapq import nlargest
import project
import configparser
from VK_module import VK
from Ya_Disk_module import Yandex_disk

# __________________________________________________________________________________________________________________
TOKEN = "___________________________________________"                            # данные для Яндекс Диска
upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
folder_url = "https://cloud-api.yandex.net/v1/disk/resources"


access_token = '___________________________________________'                     # данные для ВК
user_id = '_________'
#_____________________________________________________________________________________________________________________

# тело программы
vk = VK(access_token, user_id)                                                # получение информации о пользователе
pprint(vk.users_info())

#

# def get_user_id():
#     url = 'https://api.vk.com/method/users.get'
#     token_vk = get_token()
#     params = {'access_token': token_vk, 'user_ids': screen_name}
#     response = requests.get(url, params={**self.params, **params})
#     return response.json()
# _____________________________________________________________________________________________
pprint(vk.load_ya_disk())                                                    # получение данных о фотографиях, сортировка
data = vk.load_ya_disk()
print('\n')

print(vk.write_file())                                                      # запись информации в файл

# интерфейс
greeting = 'Привет! Эта программа умеет переносить фотографии из профиля ВК на Яндекс Диск. Приступим:)'
print(greeting)
time.sleep(1)


while True:
    answer = input('Ты знаешь свой ВК id? (он выглядит как набор цифр) ')
    answer = answer.lower()
    if answer == 'да':
        config = configparser.ConfigParser()
        config.read("tokens.ini")
        user_id = config['VK']['user_id']
        screen_name = 0
        break
    elif answer == 'нет':
        text = 'Ничего страшного! Тогда введи свой screen_name'
        print(text)
        screen_name = input('screen_name: ')
        break
    else:
        text = 'Твой ответ не распознан программой( Попробуй ещё раз (ответ принимается в формате "Да/Нет"'
        print(text)

photo_amount = int(input('Теперь скажи, сколько фото ты хочешь загрузить со страницы (напиши число)? '))

#тело программы                                               # получение информации о пользователе
vk = VK()
result = vk.users_info()
pprint(result)
#
#
pprint(vk.load_ya_disk())                                                 # получение данных о фотографиях, сортировка
data = vk.load_ya_disk()
print('\n')
#
print(vk.write_file())                                                      # запись информации в файл
#
ya = Yandex_disk(data)                                                       # загрузка на Яндекс Диск
print(ya.upload_url_to_disk(data))
