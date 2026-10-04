import pathlib
import threading, time, os, sys

from networkx.classes import number_of_nodes


def scan_folder():
    print("stan przed rozpoczęciem pracy")
    base_scan = os.listdir(os.path.join("folder"))
    dict_scan = dict()
    for file in base_scan:
        print(file)
        # dict_scan[file] =
    print(base_scan)
    print(len(base_scan))
    for i in range(20):
        time.sleep(5)
        print("skanowanie")
        new_csan = os.listdir(os.path.join("folder"))
        # wersja protsza różnica elemntów
        number_file = len(new_csan) - len(base_scan)
        if number_file > 0:
            print(f"dodano nowe pliki {number_file}")
        elif number_file == 0:
            print("liczba plików bez zmian")
        else:
            print(f"usunięto pliki {abs(number_file)}")
        # wersja pośrednia jakie elementy zostały zmodyfikowane
        set_base = set(base_scan)
        set_new = set(new_csan)
        # elementy, któe są w base_scan
        roznice_a = set(set_base - set_new)
        print(f"elementy, które zostały usunięte {roznice_a}")
        roznice_b = set(set_new - set_base)
        print(f"pliki, które zostały dodane {roznice_b}")
        # wersja zaawansowana sprawdzenie modyfikacji pliku po jego rozmiarze i dacie modyfikacji
        # sprawdzenie czy są te same pliki
        roznice_c = list(base_scan & new_csan)
        for f in roznice_c:
            # porównaj wielkość plików i datę modyfikacji ze słownika i aktualnego skanu
            continue
        base_scan = new_csan

def main():
    # th = threading.Thread(target=scan_folder, name="scan_thread")
    print("stan przed rozpoczęciem pracy")
    base_scan = os.listdir(os.path.join("folder"))
    dict_scan = dict()
    for file in base_scan:
        print(file)
        dict_scan[file] = [os.path.getsize(os.path.join("folder", file)), os.path.getctime(os.path.join("folder", file))]

    print(dict_scan)


if __name__=="__main__":
    print("rozpoczęcie pracy programu")
    main()