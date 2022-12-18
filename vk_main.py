from my_config import user_token, comm_token, offset, line
import vk_api
import requests
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_base import *


class VKBot:
    def __init__(self):
                
        self.vk = vk_api.VkApi(token=comm_token)  
        self.longpoll = VkLongPoll(self.vk)
        print('Activate bot')  
    
    def write_msg(self, user_id, message): # sending message
            self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def name(self, user_id): #getting unit name
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token, 'user_ids': user_id, 'v': '5.131'}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            unit_information = response['response']
            for i in unit_information:
                for key, value in i.items():
                    name = i.get('first_name')
                    return name
        except KeyError:
            self.write_msg(user_id, 'Ошибка токена')

    def sex(self, user_id): #getting unit sex
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            unit_information = response['response']
            for i in unit_information:
                if i.get('sex') == 2:
                    find_sex = 1
                    return find_sex
                elif i.get('sex') == 1:
                    find_sex = 2
                    return find_sex
        except KeyError:
            self.write_msg(user_id, 'Ошибка токена')

    def age(self, user_id): #getting unit age
        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            unit_information = response['response']
            for i in unit_information:
                date = i.get('bdate')
            date_decomp = date.split('.')
            age = int(datetime.date.today().year) - int(date_decomp[2])
            
            self.write_msg(user_id, 'Введите допустимый разброс возраста (годы): ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    tolerance = int(event.text)
                    age_from = age - tolerance
                    age_to = age + tolerance
                    return age_from, age_to
        except KeyError:
            self.write_msg(user_id, 'Ошибка токена')

    def city(self, user_id): #getting city
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            unit_information = response['response']
            for i in unit_information:
                city = i.get('city')
                id = str(city.get('id'))
                return id
        except KeyError:
            self.write_msg(user_id, 'Ошибка токена')
    
    def find_user(self, user_id): #serching units
        age_from, age_to = self.age(user_id)
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.sex(user_id),
                  'age_from': age_from,
                  'age_to': age_to,
                  'city': self.city(user_id),
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': 500}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            resp_1 = response ['response']
            resp_2 = resp_1 ['items']
            for persone in resp_2:
                if persone.get('is_closed') == False:
                    name = persone.get('first_name')
                    surname = persone.get('last_name')
                    vk_id = str(persone.get('id'))
                    vk_link = 'vk.com/id' + str(persone.get('id'))
                    insert_data_units_serch(name, surname, vk_id, vk_link)
                else:
                    continue
            return f'Поиск завершён'
        except KeyError:
            self.write_msg(user_id, 'Ошибка токена')

    def photo_id(self, user_id): # get all photo id
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        req = requests.get(url, params=params)
        photos = dict()
        response = req.json()
        try:
            resp_1 = response['response']
            resp_2 = resp_1['items']
            for i in resp_2:
                photo_id = str(i.get('id'))
                likes = i.get('likes')
                if likes.get('count'):
                    like = likes.get('count')
                    photos[like] = photo_id
            ids = sorted(photos.items(), reverse=True)
            return ids
        except KeyError:
            self.write_msg(user_id, 'Ошибка токена')

    def photo_1(self, user_id):
        list = self.photo_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 1:
                return i[1]

    def photo_2(self, user_id):
        list = self.photo_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 2:
                return i[1]

    def photo_3(self, user_id):
        list = self.photo_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 3:
                return i[1]

    def send_1(self, user_id, message, offset):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.photo_1(self.person_id(offset))}',
                                         'random_id': 0})

    def send_2(self, user_id, message, offset):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.photo_2(self.person_id(offset))}',
                                         'random_id': 0})

    def send_3(self, user_id, message, offset):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.photo_3(self.person_id(offset))}',
                                         'random_id': 0})

    def find_persons(self, user_id, offset):
        self.write_msg(user_id, self.found_person_info(offset))
        self.person_id(offset)
        # insert_data_units_seen(self.person_id(offset)) # offset has been delited as nonfunctional parameter
        self.photo_id(self.person_id(offset))
        self.send_1(user_id, 'Лучшее фото', offset)
        if self.photo_2(self.person_id(offset)) != None:
            self.send_2(user_id, 'Вторая фотка', offset)
            self.send_3(user_id, 'Третья фотка', offset)
        else:
            self.write_msg(user_id, f'Больше фотографий нет')
        insert_data_units_seen(self.person_id(offset)) # offset has been delited as nonfunctional parameter

    def found_person_info(self, offset):
        person_info = select(offset)
        list_person = []
        for i in person_info:
            list_person.append(i)
        return f'{list_person[0]} {list_person[1]}, ссылка - {list_person[3]}'

    def person_id(self, offset):
        person_info = select(offset)
        list_person = []
        for i in person_info:
            list_person.append(i)
        return str(list_person[2])

bot = VKBot()

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = str(event.user_id)
        request = event.text.lower()
        print(request)
        print(offset)
        if request == "начать поиск":
            name = bot.name(user_id)
            bot.write_msg(user_id, f"Привет, {name}")
            creating_database()
            bot.find_user(user_id)
            bot.write_msg(event.user_id, f'Нашёл для тебя пару, введи слово "ага"')
            bot.find_persons(user_id, offset)

        elif request == 'ага':
            
            offset += 1
            bot.find_persons(user_id, offset)
                    
        elif request == "пока":
            bot.write_msg(user_id, f"Пока, {name}")
            break
        
        else:
            bot.write_msg(user_id, "Не понял вашего ответа...")
