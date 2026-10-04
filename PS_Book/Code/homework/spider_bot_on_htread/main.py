import threading
from time import sleep
from datetime import datetime, timedelta
import numpy as np
from Code.homework.spider_bot_on_htread.spider_bot import SpiderBot

def main():
    # tworzę trzy wątki, które będą przeszukiwać strony w poszukiwaniu linków.
    print("podaj strony od, których ma się zacząć poszukiwanie linków")
    print("jeżeli podajeś więcej stron odziel przecinkiem ','" )
    # start_urls = input()
    list_spider_obj = []
    list_spider_thred = []
    list_web_to_start = ["https://agh.edu.pl", "https://www.lemonde.fr/", "https://interia.pl",
                         "https://www.lemode.net/en/", "https://www.alltrails.com/", "https://dziennikzachodni.pl/"]

    raport_time = datetime.today() + timedelta(minutes=20)

    for i, u in enumerate(list_web_to_start):
        list_spider_obj.append(SpiderBot(u, f"res_th_{i}.txt", 6))

    for obj in list_spider_obj:
        t = threading.Thread(target=obj.start_bot)
        list_spider_thred.append(t)
        t.start()

    while True:
        sleep(120)
        temp_list_size = []
        if raport_time < datetime.today():
            raport_time = datetime.today() + timedelta(minutes=20)
            print(f"raport z {datetime.today()}")
            for i, obj in enumerate(list_spider_obj):
                print(f"obiekt {i} wielkość listy {len(obj.list_of_urls_to_visit)}")
                temp_list_size.append(len(obj.list_of_urls_to_visit))

        if np.all( np.array(temp_list_size) == 0):
            print("wszystkie wątki opróżniły listę do odwiedzenia")
            break

    for t in list_spider_thred:
        t.join()

    print("--- wszystkie strony zostały przeszukane ---")

if __name__ == "__main__":
    print("rozpoczynam prace wątka demona")
    main()