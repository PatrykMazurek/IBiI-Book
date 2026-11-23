import imaplib, requests, json
from email.message import EmailMessage
from email.utils import format_datetime
from datetime import datetime, timedelta, timezone

from MZI_Book.Code.temp import response

# --- KONFIGURACJA GREENMAIL ---
IMAP_HOST = "pi-server.local"
IMAP_PORT = 3143          # Domyślny port IMAP w GreenMail (standalone/Docker)
USER_EMAIL = "test"
USER_PASS = "test"

# Katalogi do utworzenia (bez polskich znaków, żeby uniknąć problemów z kodowaniem UTF-7 w IMAP)
FOLDERS = ["INBOX", "Praca", "Faktury", "Prywatne", "Spam", "PustyKatalog"]

# Baza wiadomości: (katalog, nadawca, tytuł, treść, ile_dni_temu)
EMAILS = [
    # --- INBOX (35 wiadomości -> test paginacji 20 + 15) ---
    ("INBOX", "szef@firma.pl", "Pilne: Spotkanie zarządu jutro", "Proszę o przygotowanie slajdów.", 0),
    ("INBOX", "jan.kowalski@example.com", "Hej, kawa w piątek?", "Dawno się nie widzieliśmy, daj znać.", 1),
    ("INBOX", "ksiegowosc@firma.pl", "Faktura nr 101/2026 do akceptacji", "W załączeniu szczegóły rozliczenia.", 2),
    ("INBOX", "newsletter@sklep.pl", "Promocja -50% tylko dzisiaj!", "Sprawdź naszą nową ofertę.", 3),
    ("INBOX", "hr@firma.pl", "Wniosek urlopowy zaakceptowany", "Miłego wypoczynku!", 4),
    ("INBOX", "szef@firma.pl", "Raport kwartalny - uwagi", "Dorzuć jeszcze wykres sprzedaży.", 5),
    ("INBOX", "alert@bank.pl", "Potwierdzenie przelewu", "Przelew został zrealizowany poprawnie.", 6),
    ("INBOX", "jan.kowalski@example.com", "Re: Spotkanie projektowe", "Pasuje mi wtorek o 10:00.", 7),
    ("INBOX", "devops@firma.pl", "Pilne: Przerwa techniczna serwera", "Dziś w nocy o 2:00 restartujemy bazę.", 8),
    ("INBOX", "newsletter@sklep.pl", "Nowa kolekcja jesień/zima", "Zobacz nowości w sklepie.", 9),
    ("INBOX", "szef@firma.pl", "Spotkanie 1-on-1", "Porozmawiamy o celach na kolejny kwartał.", 10),
    ("INBOX", "anna.nowak@firma.pl", "Raport z testów aplikacji", "Wszystkie testy przeszły na zielono.", 11),
    ("INBOX", "ksiegowosc@firma.pl", "Przypomnienie: Faktura za internet", "Termin płatności mija za 3 dni.", 12),
    ("INBOX", "hr@firma.pl", "Szkolenie BHP - przypomnienie", "Pamiętaj o wypełnieniu testu online.", 13),
    ("INBOX", "jan.kowalski@example.com", "Zdjęcia z wyjazdu", "Wrzucam link do galerii.", 14),
    ("INBOX", "szef@firma.pl", "Raport tygodniowy - granica 15 dni", "Wiadomość dokładnie sprzed 15 dni.", 15),
    ("INBOX", "szef@firma.pl", "Stary raport - 16 dni temu", "Ta wiadomość powinna odpaść przy filtrze <= 15 dni.", 16),
    ("INBOX", "newsletter@sklep.pl", "Promocja na elektronikę", "Rabaty do 30%.", 17),
    ("INBOX", "alert@bank.pl", "Wyciąg miesięczny", "Twój wyciąg jest gotowy do pobrania.", 18),
    ("INBOX", "anna.nowak@firma.pl", "Spotkanie zespołu frontend", "Omawiamy nową architekturę.", 19),
    ("INBOX", "devops@firma.pl", "Aktualizacja certyfikatów SSL", "Certyfikaty zostały odnowione.", 20),
    ("INBOX", "ksiegowosc@firma.pl", "Faktura korygująca nr 12/2026", "Proszę o weryfikację kwoty.", 22),
    ("INBOX", "jan.kowalski@example.com", "Pilne: pożyczysz ładowarkę?", "Zostawiłem swoją w biurze.", 24),
    ("INBOX", "hr@firma.pl", "Nowe benefity pracownicze", "Od przyszłego miesiąca nowe karty sportowe.", 25),
    ("INBOX", "szef@firma.pl", "Podsumowanie miesiąca", "Dobra robota zespołu!", 27),
    ("INBOX", "newsletter@sklep.pl", "Ostatnie godziny promocji", "Nie przegap okazji.", 29),
    ("INBOX", "anna.nowak@firma.pl", "Code review - prośba", "Zerkniesz na mój Pull Request?", 31),
    ("INBOX", "alert@bank.pl", "Zmiana regulaminu konta", "Wchodzi w życie od kolejnego miesiąca.", 33),
    ("INBOX", "devops@firma.pl", "Raport zużycia zasobów", "CPU w normie, dysk w 70% pełny.", 35),
    ("INBOX", "jan.kowalski@example.com", "Plan na weekend", "Jedziemy w góry?", 38),
    ("INBOX", "ksiegowosc@firma.pl", "Faktura za telefon służbowy", "Rozliczenie za poprzedni okres.", 40),
    ("INBOX", "szef@firma.pl", "Spotkanie integracyjne", "Głosujemy nad terminem wyjścia.", 42),
    ("INBOX", "newsletter@sklep.pl", "Kod rabatowy dla stałych klientów", "Użyj kodu VIP20.", 45),
    ("INBOX", "hr@firma.pl", "Ankieta satysfakcji", "Wypełnienie zajmie 5 minut.", 50),
    ("INBOX", "anna.nowak@firma.pl", "Pilne: Błąd na produkcji", "Już naprawione, fałszywy alarm.", 55),

    # --- Praca (8 wiadomości) ---
    ("Praca", "szef@firma.pl", "Plan sprintu #14", "Zadania są już na Jirze.", 1),
    ("Praca", "anna.nowak@firma.pl", "Dokumentacja API", "Zaktualizowałam endpointy w Swaggerze.", 4),
    ("Praca", "devops@firma.pl", "Dostęp do środowiska staging", "Klucze SSH zostały dodane.", 9),
    ("Praca", "szef@firma.pl", "Pilne: Demo dla klienta", "Zaczynamy o 14:00 na Teamsach.", 14),
    ("Praca", "anna.nowak@firma.pl", "Spotkanie retrospektywne", "Wpiszcie swoje punkty przed spotkaniem.", 18),
    ("Praca", "devops@firma.pl", "Raport z backupów", "Wszystkie kopie zapasowe poprawne.", 23),
    ("Praca", "hr@firma.pl", "Ocena roczna - terminy", "Wybierz slot w kalendarzu.", 30),
    ("Praca", "szef@firma.pl", "Nowy projekt - kickoff", "Szczegóły w załączniku.", 40),

    # --- Faktury (6 wiadomości) ---
    ("Faktury", "ksiegowosc@firma.pl", "Faktura VAT 01/11/2026", "Kwota: 1230 PLN.", 2),
    ("Faktury", "faktury@dostawca.pl", "Faktura za hosting", "Opłacono automatycznie kartą.", 6),
    ("Faktury", "ksiegowosc@firma.pl", "Faktura VAT 15/10/2026", "Kwota: 850 PLN.", 15),
    ("Faktury", "faktury@dostawca.pl", "Faktura za domenę", "Przedłużenie na kolejny rok.", 21),
    ("Faktury", "ksiegowosc@firma.pl", "Faktura za sprzęt biurowy", "Monitor 27 cali.", 35),
    ("Faktury", "faktury@dostawca.pl", "Faktura zaliczkowa", "Rozliczenie końcowe w przyszłym miesiącu.", 60),

    # --- Prywatne (4 wiadomości) ---
    ("Prywatne", "mama@dom.pl", "Obiad w niedzielę", "Będzie rosół i schabowy, wpadaj!", 1),
    ("Prywatne", "jan.kowalski@example.com", "Bilety na koncert", "Kupiłem dla nas dwa miejsca.", 10),
    ("Prywatne", "mama@dom.pl", "Przepis na sernik", "Wysyłam tak jak prosiłeś.", 19),
    ("Prywatne", "jan.kowalski@example.com", "Stare zdjęcia ze studiów", "Znalazłem na starym dysku.", 44),

    # --- Spam (5 wiadomości) ---
    ("Spam", "promo@superokazje.pl", "Wygrałeś nowy telefon!", "Kliknij tutaj, aby odebrać nagrodę.", 0),
    ("Spam", "newsletter@sklep.pl", "MEGA Promocja Black Week", "Wszystko za pół ceny!", 5),
    ("Spam", "ksiaze@nigeria.example", "Pilne: Spadek 10 milionów dolarów", "Potrzebuję tylko numeru Twojej karty.", 12),
    ("Spam", "promo@superokazje.pl", "Kredyt 0% bez BIK", "Sprawdź naszą ofertę już dziś.", 20),
    ("Spam", "newsletter@sklep.pl", "Ostatnia szansa na rabat", "Koszyk na Ciebie czeka.", 32),
]

def add_email_to_user(user, password):
    print(f"Łączenie z GreenMail ({IMAP_HOST}:{IMAP_PORT})...")
    imap = imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
    imap.login(user, password)

    for folder in FOLDERS:
        if folder != "INBOX":
            imap.create(folder)  # Jeśli już istnieje, serwer zwróci NO i nic się nie stanie

    for folder, sender, subject, body, days_ago in EMAILS:
        add_email(imap, folder, sender, subject, body, days_ago)

    imap.logout()
    print(f"Gotowe! Wgrano {len(EMAILS)} wiadomości do {len(FOLDERS)} katalogów.")

def create_account():

    url = "http://pi-server.local:8080/api/user"

    email = f"{USER_EMAIL}@ps-uken.pl"

    new_user = { "email": email, "login": USER_EMAIL, "password": USER_PASS }

    response = requests.post(url, json=new_user )
    if response.status_code == 200:
        print(f"Dodano nowego użytkownika {email}")
        print("uzupełnienie skrzynki wiadomościami")
        add_email_to_user(USER_EMAIL, USER_PASS)
    else:
        print(f"Błąd {response.status_code}: {response.text}")


def add_email(imap, folder, sender, subject, body, days_ago):
    dt = datetime.now(timezone.utc) - timedelta(days=days_ago)

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = USER_EMAIL
    msg["Subject"] = subject
    msg["Date"] = format_datetime(dt)
    msg.set_content(body)

    internal_date = imaplib.Time2Internaldate(dt.timestamp())
    status, resp = imap.append(folder, None, internal_date, msg.as_bytes())
    if status != "OK":
        print(f"Błąd przy dodawaniu do {folder}: {resp}")


def main():
    create_account()

if __name__ == "__main__":
    main()