from datetime import datetime
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode


class SteamData:
    def __init__(self, login: str, password: str):
        if type(login) == str and type(password) == str:
            self.__login = login
            self.__password = password
            self.__guard = ''
        else:
            raise Exception('Не валидные данные для входа в аккаунт')

    @property
    def guard(self) -> str:
        return self.__guard

    @guard.setter
    def guard(self, guard: str):
        if (type(guard) == str) and (len(guard) == 5):
            self.__guard = guard
        else:
            raise Exception('Не валидный код 2FA')

    @property
    def login(self) -> str:
        return self.__login

    @property
    def password(self) -> str:
        return self.__password


class Helpers:
    @staticmethod
    def get_timestamp_now() -> int:
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def rsa_encrypt(message: str, publickey_mod: int, publickey_exp: int) -> bytes:
        """
        RSA encrypt message with public key
        :param message: шифруемое сообщение
        :param publickey_mod: modulus открытого ключа
        :param publickey_exp: exponent открытого ключа
        :return: зашифрованное сообщение base64
        """
        if type(message) != str:
            raise Exception('RSA: Шифруемое сообщение должно являться строкой')
        public_key = RSA.construct((publickey_mod, publickey_exp))
        if not public_key.can_encrypt():
            raise Exception('RSA: Неверный publickey для шифрования')
        return b64encode(PKCS1_v1_5.new(public_key).encrypt(message.encode('ascii')))


class SteamClient:
    def __init__(self, login: str, password: str, steam_guard: str):
        if len(str(steam_guard)) == 5:
            self.__login = login
            self.__password = password
            self.__guard = steam_guard.upper()
            self.__steam_url = 'https://steamcommunity.com/'
        else:
            raise Exception('Не валидные данные для входа в аккаунт')

    def steam_auth(self):
        """

        :return:
        """

        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/89.0.4389.90 Safari/537.36",
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
            data = {
                "donotcache": Helpers.get_timestamp_now(),
                "username": self.__login
            }
            # 1-ый запрос
            try:
                response = session.post(url=self.__steam_url + 'login/getrsakey', data=data, headers=headers)
                response_dict = response.json()
            except Exception as ex:
                raise Exception(f'Ошибка соединения: {ex}')
            if not response_dict['success']:
                raise Exception('Ошибка при авторизации в steam')
            data = {
                'username': self.__login,
                'password': Helpers.rsa_encrypt(self.__password, int(response_dict['publickey_mod'], 16),
                                                int(response_dict['publickey_exp'], 16)),
                'emailauth': '',
                'emailsteamid': '',
                'twofactorcode': self.__guard,
                'captchagid': -1,
                'captcha_text': '',
                'loginfriendlyname': '',
                'rsatimestamp': response_dict['timestamp'],
                'remember_login': 'true',
                'donotcache': Helpers.get_timestamp_now(),
                'tokentype': -1
            }
            # 2-ой запрос
            try:
                response = session.post(url=self.__steam_url + 'login/dologin', data=data, headers=headers)
                response_dict = response.json()
            except Exception as ex:
                raise Exception(f'Ошибка соединения: {ex}')
            if not response_dict['success']:
                raise Exception('Ошибка при авторизации в steam')

            return session.cookies

    def csm_auth(self, cookies):
        return cookies
