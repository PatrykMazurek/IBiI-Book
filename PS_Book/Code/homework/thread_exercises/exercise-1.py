import threading, time, os, sys

def scan_folder():
    print("stan przed rozpoczęciem pracy")
    base_scan = os.listdir(os.path.join("folder"))
    print(base_scan)
    print(len(base_scan))
    for i in range(20):
        time.sleep(3)
        print("skanowanie")
        new_csan = os.listdir(os.path.join("folder"))
        # wersja protsza różnica elemntów
        print(f"różnica w elementach {len(new_csan) - len(base_scan)}")
        # wersja pośrednia jakie elementy zostały zmodyfikowane

        # wersja zaawansowana sprawdzenie modyfikacji pliku po jego rozmiarze i dacie modyfikacji
        
        base_scan = new_csan

def main():
    th = threading.Thread(target=scan_folder, name="scan_thread")



if __name__=="__main__":
    print("rozpoczęcie pracy programu")
    main()