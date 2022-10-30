import datetime
import time

import requests


def get_api_urls():
    api_urls = ['https://jsonplaceholder.typicode.com', 'http://188.127.251.4:8240']
    return api_urls


def count(func):
    """
    Декоратор - счётчик возможности использовать апи
    """

    counters = {}
    urls = get_api_urls()

    def wrapper(*args, **kwargs):
        for url in urls:
            if counters.get(url, None):
                if counters[url]['qty'] <= 29:
                    print(f'Функция {func.__name__} вызвала api {counters[url]}  {counters[url]["qty"]} раз')
                    counters[url]['qty'] = counters[url]['qty'] + 1
                    return func(args[0], url)
                else:
                    s = datetime.datetime.now() - counters[url]['time']
                    if s.seconds >= 60:
                        d = {'time': datetime.datetime.now(), 'qty': 1}
                        counters[url] = d
                        return func(args[0], url)
                    else:
                        continue
            else:
                d = {'time': datetime.datetime.now(), 'qty': 1}
                counters[url] = d
                print(f'Функция {func.__name__} вызвала api {counters[url]}  {counters[url]["qty"]} раз')
                return func(args[0], url)
        time.sleep(10)
        print('Таймаут для возможности вызвать юрлы без блокировки')
        print(counters)
        wrapper(args, kwargs)

    return wrapper


@count
def get_post_info(post_id: int, url: str) -> str:
    """
        функция для получения запрошенных данных
    """
    url = f'{url}/posts/{post_id}'
    r = requests.get(url)
    print(r.status_code)
    return r.text


if __name__ == '__main__':
    for i in range(10000):
        get_post_info(20)
