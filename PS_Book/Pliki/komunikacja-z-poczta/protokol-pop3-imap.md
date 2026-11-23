# Protokół POP3/IMAP

W tej części laboratorium przedstawione i omówione zostaną protokoły IMAP i POP3 w wersji bez szyfrowania i z szyfrowaniem połączenia.

### POP3

Protokół POP3 (Post Office Protocol version 3) zgodnie z dokumentacją RFC 1939 pozwala na nawiązanie połączenia z serwerem, uwierzytelnieni się za pomocą loginu i hasła oraz pobranie lub usunięcie wiadomości z serwera pocztowego.

Przykład skryptu w języku Python

```python
import poplib
from email import parser

POP3_SERVER = "localhost" # dwolny inny adres serwera pocztowego
PORT = 3110     # port do komunikacji z serwerem, zależny od dostawcy
USER_NAME = "student"
PASS = 'haslo123'

def read_mail_with_pop3():
    try:
        server = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
        server.user(USER_NAME)
        server.pass_(PASS)

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

if __name__ == "__main__":
    read_mail_with_pop3()
```

Powyższy przykład przedstawia jak można odczytać liczbę wiadomości w głównym katalogu i pobrać z niego wiadomości. W powyższym przykładzie wykorzystane zostały biblioteki `poplib` oraz `email` i metodę `parser`, któy pomaga przy odpowiedniej konwersji maila, które mogą zawierać tabele, kod HTML czy załączniki.

Przykład korzysta z połączenia w wersji nie szyfrowanej, jeżeli, jeżeli serwer obsługuje szyfrowanie wystarczy zastosować następującą metodę aby aby uzyskac szfrowane połączenie.

```python
mailbox = poplib.POP3_SSL(POP3_SERVER, SSL_PORT)
```

### IMAP

Protokół IMAP (Internet Message Access Protocol) -  pozwala na zarządzanie wiadomościami, które znajdują się na serwerze pocztowym, zgodnie z początkowymi założeniami wiadomości pozostają na serwerze.

```python
import imaplib, email
from email.header import decode_header

IMAP4_SERVER = "pi-server.home"
PORT = 3143
USER_NAME = "student"
PASS = 'haslo123'

def get_body(msg):
    """Wyciąga czystą treść tekstową z wiadomości."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace")
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace")
    return ""

def read_email_with_imap():
    with imaplib.IMAP4(IMAP4_SERVER, PORT) as mailbox:
        mailbox.login(USER_NAME, PASS)
        print("Zalogowano pomyślnie!\n")
        mailbox.select("inbox", readonly=True)
        status, message = mailbox.search(None, "ALL")

        for num in message[0].split():
            status, msg_data = mailbox.fetch(num,"(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            part, encoding = decode_header(msg['Subject'])[0]
            print(part.decode(encoding or "utf-8", errors="replace"))
            print(msg['From'])
            print(get_body(msg))
    
if __name__ == "__main__":
    read_email_with_imap()
```

Powyższy fragment kodu przedstawia sposób synchronizacji wiadomości z serwerem pocztowym. W przykłądzie skorzystano z bibliotek `imaplib` oraz `email` i skorzystano z metody `decode_header`. W przykładzie zdefinoiowano metodę `get_body()` zadaniem, której jest dekodowanie wiadomości z wersji binarnej do stringa z wykorzystaniem znaków UNICODE. Konwersja wiadomości pobranych z serwera do obiektu `email` pomaga przy odczytaniu nagłówków wiadomości oraz ewentualnemu dekodowaniu do odpowiednich znaków. 

Powyższy fragment przedstawiał połączenie przez protokół IMAP bez szyfrowania. Jeżeli serwer obsługuje szyfrowanie, wystarczy zastosować poniższą metodę aby wykonać połączenie szyfrowane.

```python
mailbox = imaplib.IMAP4_SSL(IMAP4_SERVER, SSL_PORT)
```

### Zadania

1. Stwórz aplikację, która odczyta listę katalogów i zwróci liczbę wiadomości w danym katalogu
2. Stwórz aplikację, która pozwoli użytkownikowi wybrać odpowiedni katalog i wyświetli po 20 wiadomości w postaci nadawca i tytuł. Zastosuje odpowiedni protokół, który pozostawi wiadomości na serwerze pocztowym.
3. Stwórz aplikację, która będzie filtrować wiadomości:
   1. wyświetli wiadomości nie starsze niż 15 dni
   2. pozwoli wyszukać wiadomości, które zawierają wybraną frazę w tytule
   3. pozwoli wyszukać wisomości od konkretnego madawcy

### Literatura

{% embed url="https://docs.python.org/3/library/poplib.html" %}

{% embed url="https://www.w3schools.com/python/ref_module_poplib.asp" %}

{% embed url="https://realpython.com/ref/stdlib/poplib/" %}

{% embed url="https://www.tutorialspoint.com/python_network_programming/python_pop3.htm" %}

{% embed url="https://docs.python.org/3/library/imaplib.html" %}

{% embed url="https://realpython.com/ref/stdlib/imaplib/" %}

{% embed url="https://medium.com/my-activity-diaries/mail-app-1x02-using-python-and-imap-to-fetch-only-the-time-slots-i-care-about-57fee05e052a" %}

{% embed url="https://docs.python.org/3/library/email.examples.html" %}
