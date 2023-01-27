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


#_____________________________________________________________________________________________________________________

# # тело программы
# vk = VK(access_token, user_id)                                                # получение информации о пользователе
# pprint(vk.users_info())

#

# def get_user_id():
#     url = 'https://api.vk.com/method/users.get'
#     token_vk = get_token()
#     params = {'access_token': token_vk, 'user_ids': screen_name}
#     response = requests.get(url, params={**self.params, **params})
#     return response.json()
# _____________________________________________________________________________________________
# pprint(vk.load_ya_disk())                                                    # получение данных о фотографиях, сортировка
# data = vk.load_ya_disk()
# print('\n')
#
# print(vk.write_file())                                                      # запись информации в файл

# интерфейс
greeting = 'Привет! Эта программа умеет переносить фотографии из профиля ВК на Яндекс Диск. Приступим:)'
print(greeting)
time.sleep(1)

photo_amount = int(input('Cколько фото ты хочешь загрузить со страницы (напиши число)? '))

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
