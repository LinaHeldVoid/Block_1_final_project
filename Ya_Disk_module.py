from progress.bar import IncrementalBar
import requests
import configparser

############################################################################################

upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
folder_url = "https://cloud-api.yandex.net/v1/disk/resources"

###############################################################################################


class Yandex_disk:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("TOKENS_DANGER.ini")
        self.token = config['YANDEX']['ya_token']

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def new_folder(self):                                                              # создание новой папки на Диске
        url = folder_url
        headers = self.get_headers()
        response = requests.put(f'{url}?path=Фото', headers=headers)
        print(response)
        return 'Папка для фотографий создана!'

    def upload_url_to_disk(self, data):                                                # загрузка на Диск
        bar = IncrementalBar('Загрузка фотографий на диск', max=100)
        headers = self.get_headers()
        folder = self.new_folder()
        print(folder)
        for photos in data.items():
            print('\n')
            name = f'{photos[0]}.jpg'
            upload_link = f'{upload_url}?path=Фото/{name}'
            url = photos[1]['url']
            params_upload = {'path': name, 'url': url}
            response = requests.post(url=upload_link, params=params_upload, headers=headers)
            print(response)
            bar.next()
        bar.finish()
        text = 'Загрузка на Диск успешно завершена!'
        return text
