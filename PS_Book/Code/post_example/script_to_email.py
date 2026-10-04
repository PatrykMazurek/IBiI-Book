import smtplib
from email.headerregistry import Address
from email.message import EmailMessage

SMTP_HOST = "pi-server.home"
SMTP_PORT = 3025  # Standardowy port SMTP w GreenMail
RECIPIENT = "student@example.com"


def send_mail(msg: EmailMessage):
    """Wysyła wiadomość do serwera SMTP."""
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)
        print(f"[✓] Wysłano: {msg['Subject']}")


def create_base_message(subject: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Address("Wykładowca", "wykladowca", "uczelnia.pl")
    msg["To"] = (Address("Student", "student", "example.com"),)
    return msg


# --- 1. Mail z polskimi znakami diakrytycznymi (Zadanie 1 i 3) ---
def send_polish_chars_email():
    msg = create_base_message(
        "Zażółć gęślą jaźń — ważne ogłoszenie o zaliczeniu!"
    )
    msg.set_content(
        "Dzień dobry,\n\n"
        "Przypominam o terminie nadsyłania sprawozdań z laboratoriów sieciowych.\n"
        "Proszę zadbać o poprawność kodowania znaków (UTF-8 / ISO-8859-2).\n\n"
        "Z poważaniem,\n"
        "Prowadzący zajęcia"
    )
    send_mail(msg)


# --- 2. Mail wieloczęściowy: Plain Text + HTML (Zadanie 3) ---
def send_multipart_html_email():
    msg = create_base_message("Materiały dydaktyczne do Laboratorium nr 3")
    msg.set_content(
        "Wersja tekstowa: Proszę pobrać materiały ze strony kursu."
    )

    # Dodanie alternatywnej wersji HTML
    msg.add_alternative(
        """\
    <!DOCTYPE html>
    <html>
      <body>
        <h2 style="color: #2e6c80;">Materiały do Laboratorium</h2>
        <p>Oto lista wymaganych zagadnień:</p>
        <ul>
          <li>Protokół <b>POP3</b> (RFC 1939)</li>
          <li>Protokół <b>IMAP4rev1</b> (RFC 3501)</li>
          <li>Format wiadomości internetowych (RFC 5322 / MIME)</li>
        </ul>
      </body>
    </html>
    """,
        subtype="html",
    )
    send_mail(msg)


# --- 3. Mail z załącznikiem binarnym (Zadanie 4) ---
def send_attachment_email():
    msg = create_base_message("Raport pomiarowy i wykres wydajności [ZAŁĄCZNIK]")
    msg.set_content(
        "W załączeniu przesyłam wygenerowany plik z danymi pomiarowymi."
    )

    # Przykładowy 1x1 przezroczysty piksel PNG w bajtach
    fake_png_data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05"
        b"\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )

    msg.add_attachment(
        fake_png_data,
        maintype="image",
        subtype="png",
        filename="wykres_wydajnosci.png",
    )

    # Dodatkowy plik tekstowy/CSV jako załącznik
    csv_data = "id;protokol;port\n1;POP3;110\n2;IMAP;143\n3;SMTP;25\n"
    msg.add_attachment(
        csv_data.encode("utf-8"),
        maintype="text",
        subtype="csv",
        filename="konfiguracja_portow.csv",
    )

    send_mail(msg)


# --- 4. Mail oznaczony jako SPAM (Zadanie 2) ---
def send_spam_email():
    msg = create_base_message("[SPAM] Wygrałeś nowego laptopa! Odbierz nagrodę")
    msg.set_content(
        "Gratulacje! Zostałeś wybrany do odbioru nagrody. Kliknij tutaj natychmiast."
    )
    send_mail(msg)


if __name__ == "__main__":
    print("Inicjalizacja wysyłki wiadomości do GreenMail...")
    send_polish_chars_email()
    send_multipart_html_email()
    send_attachment_email()
    send_spam_email()
    print("\nSkrzynka testowa została pomyślnie zasiana!")