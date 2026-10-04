import imaplib, email
from email.header import decode_header

IMAP4_SERVER = "pi-server.home"
PORT = 143
PORT_SSL = 3990
USER_NAME = "dex"
PASS = 'secret'

def read_eamil_with_imap():
    mailbox = imaplib.IMAP4(IMAP4_SERVER, PORT)
    mailbox.login(USER_NAME, PASS)
    print("Zalogowano pomyślnie!\n")
    mailbox.select("inbox")
    result, data = mailbox.search(None, "ALL")
    print(f"{result} {data}")
    # print(mailbox)
    mailbox.logout()


def read_real_eamil_imap():

    # 1. Konfiguracja konta
    IMAP_SERVER = "pi-server.home"  # np. imap.wp.pl, imap.gmail.com
    PORT = 3142
    EMAIL = "student"
    PASSWORD = "haslo123"

    try:
        # 2. Łączenie z serwerem i logowanie (zawsze używamy SSL!)
        print("Łączenie z serwerem...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, PORT)
        mail.login(EMAIL, PASSWORD)
        print("Zalogowano pomyślnie!\n")

        # 3. Wybór folderu (domyślnie 'INBOX' to skrzynka odbiorcza)
        mail.select("INBOX")

        # 4. Szukanie wiadomości (ALL = wszystkie, UNSEEN = tylko nieprzeczytane)
        status, messages = mail.search(None, "ALL")

        # Wynik to bajty z numerami ID, np. b'1 2 3 4', musimy to rozbić
        mail_ids = messages[0].split()

        if mail_ids:
            # Pobieramy ID ostatniej (najnowszej) wiadomości
            latest_email_id = mail_ids[-1]

            # 5. Pobieranie pełnej treści wiadomości (RFC822)
            status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

            # msg_data to lista, z której wyciągamy krotkę z danymi
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parsowanie surowych bajtów do obiektu wiadomości
                    msg = email.message_from_bytes(response_part[1])

                    # Odkodowanie tematu (maile często mają zakodowane znaki specjalne)
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    # Odkodowanie nadawcy
                    from_ = msg.get("From")

                    print("--- NAJNOWSZA WIADOMOŚĆ ---")
                    print(f"Od: {from_}")
                    print(f"Temat: {subject}")
                    print("Treść:")

                    # 6. Odczytywanie treści (maile mogą być 'multipart', np. tekst + HTML + załączniki)
                    if msg.is_multipart():
                        for part in msg.walk():
                            # Szukamy tylko zwykłego tekstu
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode()
                                print(body)
                                break  # Wypisujemy tylko pierwszą część tekstową
                    else:
                        # Wiadomość nie jest multipart (tylko jeden typ treści)
                        body = msg.get_payload(decode=True).decode()
                        print(body)

        else:
            print("Brak wiadomości w skrzynce.")

        # 7. Zamykanie połączenia
        mail.close()
        mail.logout()

    except imaplib.IMAP4.error as e:
        print(f"Błąd logowania lub IMAP: {e}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    read_eamil_with_imap()