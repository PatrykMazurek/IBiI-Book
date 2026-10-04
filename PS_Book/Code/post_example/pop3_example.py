import poplib
from email import parser

POP3_SERVER = "imap.pi-server.home"
PORT = 3110
PORT_SSL = 3990
USER_NAME = "tester"
PASS = 'pass123'

def read_mail_with_pop3():
    mailbox = poplib.POP3_SSL(POP3_SERVER, PORT_SSL)
    mailbox.user(USER_NAME)
    mailbox.pass_(PASS)
    count, size = mailbox.stat()
    print(f"{count} messages, {size} bytes")

    mailbox.quit()

def read_real_mail_with_pop3():
    try:
        # 2. Łączenie z serwerem przez SSL
        server = poplib.POP3_SSL(POP3_SERVER, PORT)
        server.user(USER_NAME)
        server.pass_(PASS)

        # 3. Pobieranie statystyk skrzynki
        # server.stat() zwraca krotkę: (ilość wiadomości, całkowity rozmiar w bajtach)
        num_messages = len(server.list()[1])
        print(f"Masz {num_messages} wiadomości na serwerze.")

        if num_messages > 0:
            # 4. Pobranie najnowszej wiadomości
            # (POP3 indeksuje wiadomości od 1, więc num_messages to ostatni mail)
            response, lines, octets = server.retr(num_messages)

            # 'lines' to lista linii wiadomości w postaci bajtów. Trzeba to złączyć i odkodować.
            msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')

            # 5. Parsowanie wiadomości na bardziej czytelny obiekt
            msg = parser.Parser().parsestr(msg_content)

            print("\n--- Najnowsza wiadomość ---")
            print(f"Temat: {msg.get('Subject', 'Brak tematu')}")
            print(f"Od: {msg.get('From', 'Nieznany nadawca')}")

        # Zakończenie sesji
        server.quit()

    except Exception as e:
        print(f"Wystąpił błąd podczas odbierania: {e}")

if __name__ == "__main__":
    read_mail_with_pop3()