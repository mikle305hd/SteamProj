import steam_auth
import requests


def main():
    try:
        auth = steam_auth.SteamAuth('mikle305hd', '213', '12345')
    except Exception as e:
        print(e)

    auth.do()

    while True:
        print('Введите комманду: ')
        command = input().lower()

        if command == 'enter_userdata':
            print('Введите имя пользователя')
            login = input()
            print('Введите пароль')
            password = input()
            try:
                my_auth_data = steam_auth.SteamData(login, password)
            except Exception as e:
                print(e)
                continue
            login, password = '', ''
            print('Если хотите сохранить данные в файл введите команду save')
            if input().lower() == 'save':
                try:
                    with open('settings.txt', 'w') as file:
                        file.write('username:' + my_auth_data.login + '\npassword:' + my_auth_data.password)
                    del my_auth_data
                except Exception as e:
                    print(e)

        elif command == 'auth':
            try:
                with open('settings.txt', 'r', encoding='utf8') as file:
                    file_strings = file.readlines()
            except Exception as e:
                print(e)
            for string in file_strings:
                if string.find('username'):
                    login = string.replace('login:', '')
                if string.find('password'):
                    password = string.replace('password', '')

        elif command == 'exit':
            return 0

        elif command == 'help':
            print('Список доступных комманд:'
                  '\nenter_userdata  -  ввести/сохранить данные (имя пользователя и пароль) от аккаунта в файл;'
                  '\nclear_userdata  -  удалить данные аккаунта из файла'
                  '\nauth  -  авторизоваться в стиме (сохранение данных в файл необязательно);'
                  '\nexit  -  закрыть программу')

        else:
            print('Неверная команда (help  -  для доступа к списку комманд)')

if __name__ == '__main__':
    main()