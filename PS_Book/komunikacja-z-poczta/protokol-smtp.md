# Protokół SMTP

W tej części laboratorium omówione i przedstawione zostaną przykłady dotyczące wysyłania wiadomości email z wykorzystaniem protokołu SMTP.

#### SMTP

W sytuacja kiedy projekt poza pobraniem wiadomości z serwera musi też wysłać wiadomość, przychodzi nam z pomocą protokół SMTP (Simple Mail Transfer Protocol), protokół ma za zadanie odpowiednio dostosować wiadomość i przekazać ją do serwera pocztowego i przesłać do odpowiedniego serwera pocztowego. Poniższy fragment kodu przedstawia przygotowanie i przekazanie wiadomości do serwera pocztowego.

```python
import smtplib
from email.message import EmailMessage

# 1. Konfiguracja konta i serwera (zmień na swoje dane)
SMTP_SERVER = "smtp.twoja-poczta.pl"
SMTP_PORT = 465 # Standardowy port dla SMTP z SSL
EMAIL = "twoj_email@domena.pl"
PASSWORD = "twoje_super_tajne_haslo"

def write_mail_with_smtp():

# 2. Tworzenie wiadomości
msg = EmailMessage()
msg.set_content("Siemano, to jest testowa wiadomość wysłana z Pythona!")
msg['Subject'] = "Wiadomość testowa - Python SMTP"
msg['From'] = EMAIL
msg['To'] = "odbiorca@domena.pl"

# 3. Wysyłanie
try:
    # Używamy SMTP_SSL dla bezpieczeństwa
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
    print("Poszło! Wiadomość wysłana pomyślnie.")
except Exception as e:
    print(f"Wystąpił błąd podczas wysyłania: {e}")
```

Powyższy kod, przedstawia wykonanie połączenia z serwerem pocztowym i wysłanie zadania,

#### Autoryzacja OAuth2

#### Zadania

1. Stwórz aplikację, która wyśle maila do wybranego odbiorcy z:
   1. treścią formatowaną w HTML-u
   2. dowolnym plikiem jako załącznik np. txt, png, jpg., pdf
   3. wyślij wiadomość z osadzonym plikiem graficznym w wiadomości
   4. uwzględnieniem odbiorców jako "Do wiadomości (DW)" i "Ukryty do wiadomości (UDW)"
2. Stwórz rozwiązanie, które pozwoli wysłać maila do wielu osób, bazując na jednym szablonie wiadomości

#### Literatura

{% embed url="https://docs.python.org/3/library/smtplib.html" %}

{% embed url="https://www.w3schools.com/python/ref_module_smtplib.asp" %}

{% embed url="https://realpython.com/python-send-email/" %}

{% embed url="https://medium.com/jungletronics/python-send-email-using-smtp-6ecf0b1dd608" %}
