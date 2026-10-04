import os, requests, datetime
import random
import threading
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class SpiderBot:

    def __init__(self, start_url : str, dest_file : str, time: int):
        self.url = start_url
        self.file = dest_file
        self.finish_time = datetime.datetime.today() + datetime.timedelta(hours=time)
        self.list_of_urls_to_visit = []
        self.list_of_urls_to_visit.append(start_url)
        self.list_of_urls_visited = []
        self.headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    )
                }

    def start_bot(self):
        thread_name = threading.current_thread().name
        # time_to_log = datetime.datetime.today() + datetime.timedelta(minutes=2)
        print(f" rozpoczęcie racy przez wątek {thread_name}")
        while len(self.list_of_urls_to_visit) > 0:
            url = self.list_of_urls_to_visit.pop(0)
            res = self.__get_site_content(url)
            if res is not None:
                lang, desc = self.__get_description_and_links(res.text)
                # if time_to_log < datetime.datetime.today():
                #     print(f"[ {thread_name} ]wilkość listy do odwiedzenia: {len(self.list_of_urls_to_visit)}" )
                #     time_to_log = datetime.datetime.today() + datetime.timedelta(minutes=2)
                self.__save_to_file(url, lang, desc)
            self.list_of_urls_visited.append(url)
        print(f"zakończenie pracy przez wątke {thread_name} w poszukiwaniu linków")

    def __get_site_content(self, url:str):
        # pobieranie treści strony
        response = None
        time.sleep(random.random())
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Błąd podczas pobierania strony: {e}")
        return response

    def __get_description_and_links(self, content:str):
        soup = BeautifulSoup(content, "html.parser")
        # poszukiawnie języka strony
        html_tag = soup.find("html")
        language = None

        if html_tag and html_tag.get("lang"):
            language = html_tag["lang"].strip()

        if not language:
            meta_locale = (
                    soup.find("meta", attrs={"property": "og:locale"})
                    or soup.find("meta", attrs={"name": "og:locale"})
                    or soup.find("meta", attrs={"http-equiv": "content-language"})
            )
            if meta_locale and meta_locale.get("content"):
                language = meta_locale["content"].strip()

        if not language:
            language = "-"
        # poszukiwanie opisu strony
        description = "-"
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
            )
        if meta_desc and meta_desc.get("content"):
            description = meta_desc["content"].strip()

        if self.finish_time > datetime.datetime.today():
            # poszukiwanie linków na stronie tylko bezwzględne
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"].strip()
                if href.startswith("http") or href.startswith("https"):
                    if href not in self.list_of_urls_to_visit:
                        self.list_of_urls_to_visit.append(href)
        return language, description

    def __save_to_file(self, url, lang, desc):
        try:
            with open(self.file, "a+", encoding="utf-8") as f:
                f.write(f"{url};{lang};{datetime.datetime.today()};{desc}\n")
        except FileExistsError as fee:
            print(fee.errno)



