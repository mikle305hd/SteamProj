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