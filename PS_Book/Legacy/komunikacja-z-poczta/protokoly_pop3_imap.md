# Protokoły POP3/IMAP

W tej części laboratorium przedstawione i omówione zostaną protokoły POP3 i IMAP w wersji nieszyfrowanej oraz z szyfrowaniem połączenia.

## POP3

Protokół POP3 (Post Office Protocol version 3), zgodnie z dokumentacją RFC 1939, pozwala na nawiązanie połączenia z serwerem, uwierzytelnienie się za pomocą loginu i hasła oraz pobranie lub usunięcie wiadomości z serwera pocztowego.

Przykład skryptu w języku Python:

```python
import poplib
from email import parser

POP3_SERVER = "localhost" # dowolny inny adres serwera pocztowego
PORT = 3110     # port do komunikacji z serwerem, zależny od dostawcy
USER_NAME = "s<indeks>"
PASS = 'h<indeks>'

def read_mail_with_pop3():
    try:
        server = poplib.POP3(POP3_SERVER, PORT)
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

Powyższy przykład przedstawia, jak można odczytać liczbę wiadomości w głównym katalogu i pobrać z niego wiadomości. W kodzie wykorzystano biblioteki `poplib` i `email` oraz moduł `parser`, który pomaga przy odpowiedniej konwersji wiadomości e-mail, które mogą zawierać tabele, kod HTML czy załączniki.

Przykład korzysta z połączenia w wersji nieszyfrowanej. Jeżeli serwer obsługuje szyfrowanie, wystarczy zastosować następującą metodę, aby uzyskać szyfrowane połączenie:

```python
mailbox = poplib.POP3_SSL(POP3_SERVER, SSL_PORT)
```

## IMAP

Protokół IMAP (Internet Message Access Protocol) pozwala na zarządzanie wiadomościami, które znajdują się na serwerze pocztowym. Zgodnie z początkowymi założeniami wiadomości pozostają na serwerze.

```python
import imaplib, email
from email.header import decode_header

IMAP4_SERVER = "localhost" # dowolny inny adres serwera pocztowego
PORT = 3143
USER_NAME = "s<indeks>"
PASS = 'h<indeks>'

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

Powyższy fragment kodu przedstawia sposób synchronizacji wiadomości z serwerem pocztowym. W przykładzie skorzystano z bibliotek `imaplib` i `email` oraz funkcji `decode_header`. Zdefiniowano w nim również funkcję `get_body()`, której zadaniem jest dekodowanie wiadomości z wersji binarnej do ciągu znaków (typu `str`) z wykorzystaniem znaków Unicode. Konwersja wiadomości pobranych z serwera do obiektu `email` pomaga przy odczytaniu nagłówków wiadomości oraz ewentualnym dekodowaniu do odpowiednich znaków.

Powyższy fragment przedstawia połączenie przez protokół IMAP bez szyfrowania. Jeżeli serwer obsługuje szyfrowanie, wystarczy zastosować poniższą metodę, aby wykonać połączenie szyfrowane:

```python
mailbox = imaplib.IMAP4_SSL(IMAP4_SERVER, SSL_PORT)
```

## Zadania

1. Stwórz aplikację, która odczyta listę katalogów i zwróci liczbę wiadomości w danym katalogu.
2. Stwórz aplikację, która pozwoli użytkownikowi wybrać odpowiedni katalog i wyświetli po 20 wiadomości w formacie: nadawca i tytuł. Zastosuj odpowiedni protokół, który pozostawi wiadomości na serwerze pocztowym.
3. Stwórz aplikację, która będzie filtrować wiadomości:
   1. wyświetli wiadomości nie starsze niż 15 dni,
   2. pozwoli wyszukać wiadomości, które zawierają wybraną frazę w tytule,
   3. pozwoli wyszukać wiadomości od konkretnego nadawcy.

## Literatura

{% embed url="https://docs.python.org/3/library/poplib.html" %}

{% embed url="https://www.w3schools.com/python/ref_module_poplib.asp" %}

{% embed url="https://realpython.com/ref/stdlib/poplib/" %}

{% embed url="https://www.tutorialspoint.com/python_network_programming/python_pop3.htm" %}

{% embed url="https://docs.python.org/3/library/imaplib.html" %}

{% embed url="https://realpython.com/ref/stdlib/imaplib/" %}

{% embed url="https://medium.com/my-activity-diaries/mail-app-1x02-using-python-and-imap-to-fetch-only-the-time-slots-i-care-about-57fee05e052a" %}

{% embed url="https://docs.python.org/3/library/email.examples.html" %}
