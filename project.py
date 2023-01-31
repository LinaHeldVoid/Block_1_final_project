from pprint import pprint
import time
from VK_module import VK
from Ya_Disk_module import Yandex_disk


def main():
    greeting = 'Привет! Эта программа умеет переносить фотографии из профиля ВК на Яндекс Диск. Приступим:)'
    print(greeting)
    time.sleep(1)

    photo_amount = int(input('Cколько фото ты хочешь загрузить со страницы (напиши число)? '))
    vk = VK()
    result = vk.users_info()
    pprint(result)

    data = vk.load_ya_disk(photo_amount)                # получение данных о фотографиях, сортировка
    pprint(data)
    print('\n')

    vk.write_file(photo_amount)                                        # запись информации в файл

    ya = Yandex_disk()                                               # загрузка на Яндекс Диск
    print(ya.upload_url_to_disk(data))


if __name__ == "__main__":
    main()
