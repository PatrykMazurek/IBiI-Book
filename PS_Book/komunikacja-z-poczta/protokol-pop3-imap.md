# Protokół POP3/IMAP

W tej części laboratorium przedstawione i omówione zostaną protokoły IMAP i POP3 w wersji bez szyfrowania i z szyfrowaniem połączenia.

#### POP3

Protokół POP3 (Post Office Protocol version 3) zgodnie z dokumentacją RFC 1939 pozwala na nawiązanie połączenia z serwerem, uwierzytelnieni się za pomocą loginu i hasła oraz pobranie lub usunięcie wiadomości z serwera pocztowego.

Przykład skryptu w języku Python

```python
import poplib

POP3_SERVER = "pi-server.home"
PORT = 3110
USER_NAME = "student"
PASS = 'haslo123'

def read_mail_with_pop3():
    mailbox = poplib.POP3(POP3_SERVER, PORT)
    mailbox.user(USER_NAME)
    mailbox.pass_(PASS)
    count, size = mailbox.stat()
    print(f"{count} messages, {size} bytes")

    mailbox.quit()

if __name__ == "__main__":
    read_mail_with_pop3()
```

Powyższy fragment kodu przedstawia prosty sposób na połączenie się z serwerem pocztowym i sprawdzenie łączną liczbę maili oraz ich wielkość. Dodatkowe treści opisujące działanie pozostałych metod dostępnych w bibliotece `poplib`.

Przedstawiony fragment kodu wykonuje połączenie nieszyfrowane, jeżeli serwer obsługuje szyfrowanie wystarczy zastosować następującą metodę aby aby uzyskac szfrowane połączenie.

```python
mailbox = poplib.POP3_SSL(POP3_SERVER, SSL_PORT)
```

#### IMAP

Protokół IMAP (Internet Message Access Protocol) -  powala na zarządzanie wiadomościami, które znajdują się na serwerze pocztowym, zgodnie z początkowymi założeniami wiadomości pozostają na serwerze.

```python
import imaplib

IMAP4_SERVER = "pi-server.home"
PORT = 3143
USER_NAME = "student"
PASS = 'haslo123'

def read_eamil_with_imap():
    mailbox = imaplib.IMAP4(IMAP4_SERVER, PORT)
    mailbox.login(USER_NAME, PASS)
    print("Zalogowano pomyślnie!\n")
    mailbox.select("inbox")
    result, data = mailbox.search(None, "ALL")
    print(f"{result} {data}")
    mailbox.logout()
    
if __name__ == "__main__":
    read_eamil_with_imap()
```

Powyższy fragment kodu przedstawia prosty sposób na połączenie z serwerem pocztowym i wyszukanie maili z głównego folderu oraz zwrócenie ich w postaci listy tytułów.

Powyższy fragment przedstawiał połączenie przez protokół IMAP bez szyfrowania. Jeżeli serwer obsługuje szyfrowanie, wystarczy zastosować poniższą metodę aby wykonać połączenie szyfrowane.

```python
mailbox = imaplib.IMAP4_SSL(IMAP4_SERVER, SSL_PORT)
```

#### Realne rozwiązania

W przypadku realnych rozwiązań wykorzystanie samych protokołów POP3 czy IMAP nie wystarczą do pracy z wiadomościami email. W środowisku Python udostępniono bibliotekę `email`, która pomaga w prasowaniu różnych wiadomości, które mogą zawierać tabele, kod HTML czy załączniki.

Poniżej przedstawiony jest fragment kodu, który odczytuje najnowszą wiadomości z serwera pocztowego i wyświetla informacje o temacie i nadawcę wiadomości.

```python
import poplib
from email import parser

POP3_SERVER = "pop3.twoja-poczta.pl"
POP3_PORT = 995 # Standardowy port dla POP3 z SSL
EMAIL = "twoj_email@domena.pl"
PASSWORD = "twoje_super_tajne_haslo"

try:
    server = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
    server.user(EMAIL)
    server.pass_(PASSWORD)

    num_messages = len(server.list()[1])
    print(f"Masz {num_messages} wiadomości na serwerze.")

    if num_messages > 0:
        response, lines, octets = server.retr(num_messages)
        msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
        msg = parser.Parser().parsestr(msg_content)
        
        print("\n--- Najnowsza wiadomość ---")
        print(f"Temat: {msg.get('Subject', 'Brak tematu')}")
        print(f"Od: {msg.get('From', 'Nieznany nadawca')}")
        
    server.quit()

except Exception as e:
    print(f"Wystąpił błąd podczas odbierania: {e}")
```

#### Zadania

1.

#### Literatura

{% embed url="https://docs.python.org/3/library/poplib.html" %}

{% embed url="https://www.w3schools.com/python/ref_module_poplib.asp" %}

{% embed url="https://realpython.com/ref/stdlib/poplib/" %}

{% embed url="https://www.tutorialspoint.com/python_network_programming/python_pop3.htm" %}

{% embed url="https://docs.python.org/3/library/imaplib.html" %}

{% embed url="https://realpython.com/ref/stdlib/imaplib/" %}

{% embed url="https://medium.com/my-activity-diaries/mail-app-1x02-using-python-and-imap-to-fetch-only-the-time-slots-i-care-about-57fee05e052a" %}

{% embed url="https://docs.python.org/3/library/email.examples.html" %}
