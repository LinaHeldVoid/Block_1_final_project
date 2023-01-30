from heapq import nlargest
import requests
import json
import os
import project
import configparser

from pprint import pprint
from progress.bar import IncrementalBar
import requests, json, os

class VK:

    def __init__(self, version='5.131'):
        config = configparser.ConfigParser()
        config.read("TOKENS_DANGER.ini")
        self.token = config['VK']['access_token']
        self.id = config['VK']['user_id']
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.data_point = self.id.isdigit()

    def users_info(self):                                                             # получение информации о пользователе
        if self.data_point == 0:
            url = 'https://api.vk.com/method/users.get'                                 # с помощью screen_name
            params = {'user_ids': self.id}
            response = requests.get(url, params={**self.params, **params})
            id_data = json.loads(response.text)
            pprint(id_data)
            self.id = id_data['response'][0]['id']
        else:
            url = 'https://api.vk.com/method/users.get'                                 # с помощью id
            params = {'user_ids': self.id}
            response = requests.get(url, params={**self.params, **params})
        for_print = f'{json.loads(response.text)}'
        pprint(for_print)
        return response

    def get_photos_data(self, owner_id, token, version='5.131', offset=0):          # получение информации о фото из ВК
        pprint(self.users_info())
        self.id = owner_id
        self.token = token
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'access_token': self.token,
                  'rev': 0,
                  'extended': 1,
                  'v': self.version,
                  'photo_sizes': 1,
                  'offset': offset
                  }
        response = requests.get(url, params=params)
        return json.loads(response.text)

    def load_ya_disk(self):
        data = self.get_photos_data(self.id, self.token)
        count_foto = data['response']['count']
        i = 0
        photos = []
        while i < count_foto:                                             # сортировка всех фото по максимальной высоте
            height_list = []
            for pics in data['response']['items'][i]['sizes']:
                height_list.append(pics['height'])
            max_height = max(height_list)
            photos.append(max_height)
            i += 1
        photos.sort(reverse=1)                                                # n самых больших фото по высоте
        photo_amount = project.photo_amount
        photos_for_load = nlargest(photo_amount, photos)
        print(photos_for_load)
        load_pics = []

        fin_file = {}
        k = 0
        while k < count_foto:                            # создаём словарь с информацией о выбранных фото
            for pics in data['response']['items'][k]['sizes']:
                if pics['height'] in photos_for_load:
                    load_pics.append(pics)
            k += 1

        j = 0
        while j < count_foto:                 # удаляем из словаря лишнюю информацию, добавляем данные о лайках
            for pics in data['response']['items'][j]['sizes']:
                if pics in load_pics:
                    likes = data['response']['items'][j]['likes']['count']
                    fin_file[likes] = pics
            j += 1

        file_list = []                                                      # подготовка структуры для записи в файл
        file_dict = {}
        for likes in fin_file.keys():
            file_dict['file_name'] = f'{likes}.txt'
            pic_height = fin_file[likes]['height']
            pic_width = fin_file[likes]['width']
            pic_size = f'{pic_height}' + 'x' + f'{pic_width}'
            file_dict['size'] = f'{pic_size}'
            file_list.append(file_dict)
        return fin_file

    def write_file(self):                                                      # запись в файл
        path = os.getcwd()
        path_to_file = os.path.join(path, 'for_upload.txt')
        dictionary = self.load_ya_disk()
        with open(path_to_file, 'w') as file:
            file.write('В данном файле записано количество лайков, размер и ссылка на скачивание'
                       ' в наилучшем качестве для каждой фотографии.' + '\n' + '\n' + '\n')
            for lines in dictionary.items():
                file.write('Лайков: ' + f'{lines[0]}' + '\n')
                height = lines[1]['height']
                width = lines[1]['width']
                size = f'{height}' + 'x' + f'{width}'
                file.write('Размер фото: ' + size + '\n')
                url = lines[1]['url']
                file.write('Ссылка для загрузки: ' + f'{url}')
                file.write('\n' + '\n')
        response = 'Запись в файл произведена успешно'
        return response
