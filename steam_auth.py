from datetime import datetime
import requests

requests.

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

    def __get_timestamp_now(self):
        return int(datetime.now().timestamp() * 1000)

    def do(self):
        self.__url = 'https://steamcommunity.com/'
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Host": "steamcommunity.com",
            "Accept-Language": "ru-Ru,ru;q=0.9",
            "sec-ch-ua":
                "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \"; Not A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://steamcommunity.com"
            }
        with requests.session() as session:
            response = session.
            data = f'donotcache={self.__get_timestamp_now()}&username={self.__login}'
            response = session.post(url=self.__url, data=data, headers=headers)
            print(response.status_code)
            print(response)




            data = f"donotcache={self.__get_timestamp_now()}'&password=rsa"