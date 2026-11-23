# Protokuł SMTP

W tej części laboratorium przedstawione zostaną przykłady wysyłania wiadomości e-mail z wykorzystaniem protokołu SMTP.

#### SMTP

W sytuacji, gdy projekt – poza pobraniem wiadomości z serwera – musi również ją wysłać, z pomocą przychodzi protokół SMTP (Simple Mail Transfer Protocol). Jego zadaniem jest odpowiednie przygotowanie wiadomości, przekazanie jej do serwera pocztowego, a następnie przesłanie dalej – do serwera odbiorcy. Poniższy fragment kodu przedstawia przygotowanie i przekazanie wiadomości do serwera pocztowego.

```python
import smtplib
from email.message import EmailMessage

# 1. Konfiguracja konta i serwera (zmień na swoje dane)
SMTP_SERVER = "localhost" # inny dowolny adres serwera pocztowego
SMTP_PORT = 3025  # Przykładowy port serwera testowego (standardowe porty SMTP to 25, 465 lub 587)
EMAIL = "s<indeks>"
PASSWORD = "h<indeks>"

def write_mail_with_smtp():
    # 2. Tworzenie wiadomości
    msg = EmailMessage()
    msg.set_content("Cześć, to jest testowa wiadomość wysłana z Pythona!")
    msg['Subject'] = "Wiadomość testowa - Python SMTP"
    msg['From'] = EMAIL
    msg['To'] = "odbiorca@domena.pl"

    # 3. Wysyłanie
    try:
        # Nawiązujemy nieszyfrowane połączenie z serwerem SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print("Wiadomość została wysłana pomyślnie.")
    except Exception as e:
        print(f"Wystąpił błąd podczas wysyłania: {e}")
```

Powyższy kod przedstawia zastosowanie bibliotek `smtplib` oraz `email` do przygotowania wiadomości, przekazania jej na serwer pocztowy, a następnie wysłania do zewnętrznego serwera lub innego użytkownika w ramach tej samej usługi pocztowej.

W przedstawionym przykładzie użyto połączenia nieszyfrowanego. Jeśli serwer obsługuje szyfrowanie, wystarczy wykorzystać poniższą klasę, aby nawiązać bezpieczne połączenie:

```python
mailbox = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
```

#### Zadania

1. Stwórz aplikację, która wyśle wiadomość e-mail do wybranego odbiorcy z:
   1. treścią formatowaną w HTML-u;
   2. dowolnym plikiem jako załącznikiem, np. txt, png, jpg, pdf;
   3. osadzonym w treści plikiem graficznym;
   4. uwzględnieniem pól „Do wiadomości” (DW) oraz „Ukryty do wiadomości” (UDW).
2. Stwórz rozwiązanie, które pozwoli wysłać wiadomość e-mail do wielu osób, bazując na jednym szablonie wiadomości.

#### Literatura

{% embed url="https://docs.python.org/3/library/smtplib.html" %}

{% embed url="https://www.w3schools.com/python/ref_module_smtplib.asp" %}

{% embed url="https://realpython.com/python-send-email/" %}

{% embed url="https://medium.com/jungletronics/python-send-email-using-smtp-6ecf0b1dd608" %}
