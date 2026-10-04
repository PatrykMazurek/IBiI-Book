# Wstęp do protokołów IMAP, POP3, SMTP

W przypadku projektów, które wykorzystują komunikację z pocztą elektroniczną, programiści mają do dyspozycji protokoły pozwalające na pełne zarządzanie taką komunikacją. W tym celu można wykorzystać takie protokoły jak: IMAP/POP3 do pobierania i zarządzania wiadomościami w skrzynce pocztowej oraz SMTP do wysyłania wiadomości. Większość serwerów pocztowych do bezpiecznej komunikacji wykorzystuje szyfrowania oraz protokoły OAuth aby bezpiecznie potwierdzić tożsamość użytkownika.&#x20;

#### Historia

Protokół POP -&#x20;

Protokół IMAP -&#x20;

Protokół SMTP -&#x20;

#### Środowisko pracy

W ramach zajęć skorzystamy z narzędzia **GreenMail Standalone** do łatwiejszego i bezpieczniejszego zarządzania pocztą. Dostęp do aplikacji można uzyskać na dwa sposoby:

1. **Pliki źródłowe** - pobierając z oficjalnego repozytorium [GitHub](https://github.com/greenmail-mail-test/greenmail) i budując cały projekt w środowisku JAVA.
2. **Docker Image** - przygotowany został obraz Dockera, który można pobrać i uruchomić. Poniższe polecenie pobierze i uruchmi pusty serwer pocztowy. '

```bash
docker run -d --name greenmail \
  -p 3025:3025 -p 3110:3110 -p 3143:3143 -p 8080:8080 \
  -e GREENMAIL_OPTS='-Dgreenmail.setup.test.all -Dgreenmail.hostname=0.0.0.0 -Dgreenmail.users=student:haslo123@example.com' \
  greenmail/standalone:latest
```

Niezależnie od wybranej wersji polecam zapoznać się z oficjalną stroną projektu w celu uzyskania szczegółów dotyczących projektu. [Oficjalna Strona GreenMail](https://greenmail-mail-test.github.io/greenmail/)

Każde z rozwiązań dostarcza pusty serwer pocztowy, na potrzeby zajęć i przewidzianych zadań można zastosować poniższy skrypt (język Python), który uzupełnia pocztę wiadomościami.

**miejsce na skrypt**

#### **Uwaga**

Praca na własnej skrzynce pocztowej jest **nie zalecana i wykonywane jest tylko i wyłącznie na własną odpowiedzialność.**&#x20;

Dla bezpiecznego przeprowadzenia zajęć wykorzystana zostanie aplikacja **GreenMail Standalone**, którą można uruchomić na dwa sposoby:

*   **Budując projekt z kodu**

    [link do strony projektu](https://greenmail-mail-test.github.io/greenmail/)

    [link do repozytorium GitHub](https://github.com/greenmail-mail-test/greenmail)
*   **Korzystając z obrazu Docker**

    poniższe polecenie pozwala na uruchomienie serwera GreenMail Standalone, który nie posiada żadnych wiadomości.&#x20;

```python
docker run -d --name greenmail \
  -p 3025:3025 -p 3110:3110 -p 3143:3143 -p 8080:8080 \
  -e GREENMAIL_OPTS='-Dgreenmail.setup.test.all -Dgreenmail.hostname=0.0.0.0 -Dgreenmail.users=student:haslo123@example.com' \
  greenmail/standalone:latest
```

Do w pełni funkcjonalnego działaniaserserwera i praktyczego pracy na zajęciach, należy skrzynkę uzupełnić wiadomościami. Poniżej przedstawiam plik, który uzpełni skrzynkę wiadomoścmiami, które posłużą do pracy na zajęciach.



W ramach zajęć skorzystamy z narzędzia **GreenMail Standalone** do łatwiejszego i bezpieczniejszego zarządzania pocztą. Praca na własnej skrzynce pocztowej jest **nie zalecana i wykonywane jest tylko i wyłącznie na własną odpowiedzialność.**&#x20;
