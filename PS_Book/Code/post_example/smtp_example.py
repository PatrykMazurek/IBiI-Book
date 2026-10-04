import smtplib
from email.message import EmailMessage

SMTP_SERVER = "pi-server.home"
PORT = 3025
SSL_PORT = 3990
USER_NAME = "tester"
PASS = 'pass123'

def send_mail_with_smtp(msg:str, address_to:str):
    # 1. Przygotowanie treści i metadanych wiadomości
    msg = EmailMessage()
    msg["Subject"] = "Raport wdrożeniowy – Sierpień 2026"
    msg["From"] = "system@lab.pl"
    msg["To"] = "dev@lab.pl"
    msg.set_content(
        """Cześć,
        Wdrożenie nowej wersji przebiegło pomyślnie.
        Wszystkie usługi działają poprawnie.

        Pozdrawiamy,
        Zespół IT
        """
    )

    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.ehlo()
        # Opcjonalnie: negocjacja szyfrowania, jeśli serwer je wspiera
        # server.starttls()
        # server.ehlo()

        server.login(USER_NAME, PASS)
        server.send_message(msg)
        print("wiadomosć wysłana")
        server.close()
    except smtplib.SMTPException as e:
        print(f"Błąd podczas komunikacji SMTP: {e}")

if __name__ == "__main__":
    send_mail_with_smtp("test mail", "student@example.com")