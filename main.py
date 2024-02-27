
import re
from urllib.request import urlopen
class PhoneFinder:
    def __init__(self, list_urls):
        self.list_urls = list_urls
    
    def find_phone_numbers(self) -> list[str]:
        """
        Получает из инициализации класса список URL-адресов
        Возвращает список телефонов найденных в HTML-страницах этих сайтов
        """
        # Регулярное выражение
        pattern = r'^(\+\s?7|8)\s?\(?\d{3}\)?\s?\d{3}\s?(?:-)?\s?\d{2}\s?(?:-)?\s?\d{2}$'
        res = set()
        num = 0
        for url in self.list_urls:
            # Скачиваем веб-страницу
            num += 1
            try:
                with urlopen(url) as webpage:
                    content = webpage.read()
                with open(f'{num}.html', 'wb') as f:
                    f.write(content)
            except Exception as e:
                print(f'Error url \"{url}\" -> {e}')
                continue
            
            decoded_content = content.decode('utf-8')
            decoded_content = decoded_content.replace('&nbsp;', '') # пробелы
            # Окном проходим по тексту страницы
            for i in range(len(decoded_content) - 21):
                r = 11
                if decoded_content[i] not in '+8':
                    continue
                while r <= 21:
                    tmp = decoded_content[i:r + i]
                    left = decoded_content[i - 1]
                    right = decoded_content[r + i + 1]
                    if re.match(pattern, tmp) and not (left.isdigit() or right.isdigit()):
                        tmp = tmp.replace('(', "")
                        tmp = tmp.replace(')', "")
                        tmp = tmp.replace('-', "")
                        tmp = tmp.replace(' ', "")
                        tmp = tmp.replace('+7', "8")
                        res.add(tmp)
                    r += 1

        return list(res)

# Example
if __name__ == "__main__":
    urls = ['https://hands.ru/company/about', 'https://repetitors.info']
    finder = PhoneFinder(urls)
    print(finder.find_phone_numbers())

