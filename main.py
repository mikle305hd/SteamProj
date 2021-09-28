import json
import os
import pickle
import steam_auth


def main():
    user_data = None
    cookies = None
    while True:
        print('Введите комманду:', end=' ')
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
                        json.dump(data, file, indent=4)
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
                        if user_data is None:
                            print('Введите имя пользователя:', end=' ')
                            login = input()
                            print('Введите пароль:', end=' ')
                            password = input()
                            user_data = steam_auth.SteamData(login, password)
                    else:
                        user_data = steam_auth.SteamData(data['username'], data['password'])

                    print('Введите код Steam Guard:', end=' ')
                    user_data.guard = input()

                    print('Авторизация. Подождите...')
                    client = steam_auth.SteamClient(user_data.login, user_data.password, user_data.guard)
                    cookies = client.steam_auth()
                    print('Авторизация в steam прошла успешно.')
                    print('Если хотите сохранить сессию в файл введите команду save:', end=' ')
                    if input().lower() == 'save':
                        try:
                            with open('cookies.dat', 'wb') as pickle_file:
                                pickle.dump(cookies, pickle_file)
                        except Exception as e:
                            print('Ошибка при сохранении сессии в файл', e)
                            continue
            except Exception as e:
                print('Ошибка при авторизации в steam.\n', e)
                continue

        elif command == 'auth_csm':
            print('Если хотите загрузить сессию из файла введите команду load:', end=' ')
            if input().lower() == 'load':
                if os.stat('cookies.dat') == 0:
                    print('Ошибка - файл сессии пустой')
                try:
                    with open('cookies.dat', 'rb') as file:
                        cookies = pickle.load(file)
                except Exception as e:
                    print('Ошибка при чтении файла сессии.', e)
                    continue

            if cookies is None:
                print('Ошибка - авторизация steam не выполнена. Для дальнейших действий требуется auth_steam.')
                continue
            try:
                print('Авторизация. Подождите...')
                cookies = client.csm_auth(cookies)
                print('Авторизация на old.cs.money прошла успешно.')
                print('Если хотите сохранить сессию в файл введите команду save:', end=' ')
                if input().lower() == 'save':
                    try:
                        with open('cookies.dat', 'wb') as file:
                            pickle.dump(cookies, file)
                    except Exception as e:
                        print('Ошибка при сохранении сессии.', e)
                        continue
            except Exception as e:
                print('Ошибка при авторизации на old.cs.money.\n', e)
                continue

        elif command == 'exit':
            print('Программа закрыта.')
            return 0

        elif command == 'help':
            print('Список доступных комманд:'
                  '\nenter_userdata  -  ввести/сохранить данные (имя пользователя и пароль) steam аккаунта в файл;'
                  '\nclear_userdata  -  удалить данные steam аккаунта из файла'
                  '\nauth_steam  -  авторизоваться в steam (сохранение данных в файл необязательно);'
                  '\nauth_csm  -  авторизоваться на old.cs.money;'
                  '\nexit  -  закрыть программу'
                  )
        else:
            print('Неверная команда (help  -  для доступа к списку комманд)')


if __name__ == '__main__':
    main()
