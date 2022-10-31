import datetime
import time
import requests

from typing import Optional
import threading

import concurrent.futures


class Count:

    def __init__(self, function):
        self.function = function
        self.urls = get_api_urls()
        self.counters = {}
        self._lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        with self._lock:
            for url in self.urls:
                if self.counters.get(url, None):
                    if self.counters[url]['qty'] <= 29:
                        print(
                            f'Функция {self.function.__name__} вызвала api {self.counters[url]}  {self.counters[url]["qty"]} раз')
                        self.counters[url]['qty'] = self.counters[url]['qty'] + 1
                        return self.function(args[0], url)
                    else:
                        s = datetime.datetime.now() - self.counters[url]['time']
                        if s.seconds >= 60:
                            d = {'time': datetime.datetime.now(), 'qty': 1}
                            print(
                                f'Функция {self.function.__name__} вызвала api {self.counters[url]}  {self.counters[url]["qty"]} раз')
                            self.counters[url] = d
                            return self.function(args[0], url)
                        else:
                            continue
                else:

                    d = {'time': datetime.datetime.now(), 'qty': 1}
                    self.counters[url] = d
                    print(
                        f'Функция {self.function.__name__} вызвала api {self.counters[url]}  {self.counters[url]["qty"]} раз')
                    time.sleep(0.1)
                    return self.function(args[0], url)
            for url in get_api_urls():
                s = datetime.datetime.now() - self.counters[url]['time']
                if s.seconds >= 60:
                    return self.function(args[0], url)
                else:
                    s = datetime.datetime.now() - self.counters[get_api_urls()[0]]['time']
                    print(f'Результат по url - {url} для поста {args[0]}  будет через {60 - s.seconds} секунд')
                    # print(self.counters)
            time.sleep(1)
        self.__call__(args[0], kwargs)


def get_api_urls():
    api_urls = ['https://jsonplaceholder.typicode.com', 'http://188.127.251.4:8240']
    return api_urls


@Count
def get_post_info(post_id: int, url: Optional[str] = None) -> str:
    """
        функция для получения запрошенных данных
    """
    url = f'{url}/posts/{post_id}'
    r = requests.get(url)
    print(url, post_id, r.headers)
    return r.text


if __name__ == '__main__':
    # with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    #   executor.map(get_post_info, range(100))

    for i in range(90):
        t = threading.Thread(target=get_post_info, args=(i,))
        d = threading.Thread(target=get_post_info, args=(i,))
        t.start(), d.start()
