import steam_auth
import json


def main():
    user_data = None
    while True:
        print('Введите комманду:', end= ' ')
        command = input().lower()

        if command == 'enter_userdata':
            print('Введите имя пользователя:', end=' ')
            login = input()
            print('Введите пароль:', end=' ')
            password = input()
            try:
                user_data = steam_auth.SteamData(login, password)
            except Exception as e:
                print(e)
                continue
            login, password = '', ''
            print('Если хотите сохранить данные в файл введите команду save:', end=' ')
            if input().lower() == 'save':
                try:
                    with open('auth_data.json', 'w') as file:
                        data = {"username": user_data.login, "password": user_data.password}
                        json.dump(data, file,indent=4)
                        del data
                    del user_data
                except Exception as e:
                    print(e)

        elif command == 'clear_userdata':
            try:
                with open('auth_data.json', 'w') as file:
                    json.dump({}, file)
            except Exception as e:
                print(e)

        elif command == 'auth_steam':
            try:
                with open('auth_data.json', 'r') as file:
                    data = json.load(file)
                    if data == {}:
                        if user_data == None:
                            print('Введите имя пользователя:', end= ' ')
                            login = input()
                            print('Введите пароль:', end=' ')
                            password = input()
                            user_data = steam_auth.SteamData(login, password)
                    else:
                        user_data = steam_auth.SteamData(data['username'], data['password'])

                    print('Введите код Steam Guard:', end=' ')
                    user_data.guard = input()

                    client = steam_auth.SteamClient(user_data.login, user_data.password, user_data.guard)
                    client.steam_auth()
            except Exception as e:
                print(e)

        elif command == 'exit':
            print('Программа закрыта')
            return 0

        elif command == 'help':
            print('Список доступных комманд:'
                  '\nenter_userdata  -  ввести/сохранить данные (имя пользователя и пароль) аккаунта в файл;'
                  '\nclear_userdata  -  удалить данные аккаунта из файла'
                  '\nauth_steam  -  авторизоваться в стиме (сохранение данных в файл необязательно);'
                  '\nexit  -  закрыть программу')
        else:
            print('Неверная команда (help  -  для доступа к списку комманд)')

if __name__ == '__main__':
    main()