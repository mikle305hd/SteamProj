import requests


class Currency:
    def get_currency(self):
        with requests.session() as session:
            response = session.get('https://www.finanz.ru/valyuty/v-realnom-vremeni-rub')
        text = response.text
        print("URI:", response.url)
        print("\nСтатус и сообщение:", response.status_code, response.reason)
        print("\nЗаголовки:")
        for key in sorted(response.headers):
            print("  - {}: {}".format(key, response.headers[key]))
        print("\nКодировка:", response.encoding)
        text = text[text.find('<table class="quote_list">') + 26:]
        text = text[:text.find('</table>')]
        quote_list = text.split('</tr>')
        del text
        new_list = []
        for block in quote_list:
            if 'USD/RUB' in block or 'CNY/RUB' in block:
                new_list.append(block.replace('\t', '').replace('<tr>', ''))
                if len(new_list) == 2:
                    del quote_list
                    break

        for block in new_list:
            if 'USD/RUB' in block:
                pass