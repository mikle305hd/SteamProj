from datetime import datetime
import requests


class SteamData:
    def __init__(self, login, password):
        if (type(login) and type(password) == str):
            self.__login == login
            self.__password == password
            self.__guard = ''
        else:
            raise Exception('Не валидные данные для входа в аккаунт')

    @property
    def guard(self):
        return self.__guard

    @guard.setter
    def guard(self, guard):
        if (type(guard) == str) and (len(list(guard)) == 5):
            self.__guard = guard
        else:
            raise Exception('Не валидный код 2FA')

    @property
    def login(self):
        return self.__login

    @property
    def password(self):
        return self.__password

class SteamAuth:
    def __init__(self, login, password, steam_guard):
        if ((type(login) == str and type(password) == str and type(steam_guard) == str) and len(str(steam_guard)) == 5):
            self.__login = login
            self.__password = password
            self.__guard = str(steam_guard).upper()
        else:
            raise Exception("Не валидные данные для входа в аккаунт")

    def __get_timestamp(self):
        return int(datetime.now().timestamp() * 1000)

    def do(self):
        self.__url = 'https://steamcommunity.com/'
        headers = {

        }
        with requests.session() as session:
            url = self.__url + 'login/getrsakey/'
            data = f'donotcache={self.__get_timestamp()}&username={self.__login}'
            response = session.post(url, data, headers=headers)
            print(response.status_code)
            print(response)