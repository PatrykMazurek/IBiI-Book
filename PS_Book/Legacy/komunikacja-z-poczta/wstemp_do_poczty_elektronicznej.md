# Wprowadzenie do komunikacji

W projektach wykorzystujących pocztę elektroniczną programiści mają do dyspozycji rozwiązania pozwalające na pełne zarządzanie wymianą wiadomości. W tym celu stosuje się protokoły: **IMAP** lub **POP3** do pobierania i obsługi wiadomości w skrzynce pocztowej oraz **SMTP** do ich wysyłania. Większość serwerów pocztowych wykorzystuje ponadto szyfrowanie oraz protokół OAuth, aby bezpiecznie potwierdzić tożsamość użytkownika.

## Historia

### Protokół POP

Historia protokołu POP (Post Office Protocol) sięga 1984 roku, kiedy to opublikowano jego pierwszą wersję (POP1) w dokumencie RFC 918. Powstał on jako odpowiedź na realny problem tamtych czasów: komputery osobiste i stacje robocze nie miały stałego dostępu do sieci, więc potrzebowały prostego mechanizmu do pobierania poczty z centralnego serwera podczas krótkich połączeń, np. przez modem. Już rok później, w 1985 roku, pojawiła się ulepszona wersja POP2 (RFC 937), ale prawdziwy przełom przyniósł rok 1988 i debiut POP3 (RFC 1081). Zaprojektowano go tak, by działał w prostym modelu „pobierz wiadomości na dysk i usuń je z serwera”, co idealnie pasowało do epoki drogiej i bardzo ograniczonej przestrzeni dyskowej na serwerach pocztowych.

Przez lata 90. i początek XXI wieku POP3 – ostatecznie ustandaryzowany w 1996 roku w dokumencie RFC 1939 – stał się absolutnym fundamentem internetowej poczty, wspieranym przez niemal każdego klienta e-mail. Z czasem rozszerzono go o mechanizmy bezpieczeństwa, takie jak szyfrowanie połączeń przez SSL/TLS (POP3S) oraz nowoczesne metody uwierzytelniania.

### Protokół IMAP

Historia protokołu IMAP (Internet Message Access Protocol) rozpoczęła się w 1986 roku na Uniwersytecie Stanforda, gdzie Mark Crispin zaprojektował go jako nowoczesną alternatywę dla raczkującego wówczas POP. Od samego początku IMAP opierał się na zupełnie innej filozofii: wiadomości miały na stałe pozostawać na serwerze, a programy pocztowe jedynie się z nim synchronizowały. Po wczesnych iteracjach, takich jak IMAP2 z 1988 roku (RFC 1064) oraz niezbyt popularnym IMAP3, prawdziwy przełom nastąpił w 1994 roku wraz z premierą wersji IMAP4 (RFC 1730). Wprowadziła ona zaawansowane zarządzanie folderami, flagowanie wiadomości oraz możliwość ich przeszukiwania bezpośrednio po stronie serwera, bez konieczności pobierania całych załączników.

W 2003 roku protokół doczekał się kluczowej standaryzacji jako IMAP4rev1 (RFC 3501), która przez niemal dwie dekady stanowiła główny fundament poczty elektronicznej. Jego prawdziwy rozkwit przyniosła jednak era smartfonów, tabletów i pracy na wielu urządzeniach jednocześnie, gdzie model „pobierz i usuń” znany z POP3 przestał się sprawdzać.

W 2021 roku opublikowano jego nowoczesną aktualizację – IMAP4rev2 (RFC 9051), która uporządkowała protokół i włączyła do jego rdzenia najważniejsze ulepszenia wypracowane przez lata.

### Protokół SMTP

Historia protokołu SMTP (Simple Mail Transfer Protocol) sięga 1982 roku, kiedy to Jon Postel opublikował jego oficjalną specyfikację w dokumencie RFC 821. Powstał on jako następca wcześniejszych, mniej elastycznych mechanizmów przesyłania wiadomości w sieci ARPANET i od samego początku odpowiadał wyłącznie za wysyłanie oraz przekazywanie poczty między serwerami. Pierwotny SMTP był niezwykle prosty – opierał się na czytelnych dla człowieka poleceniach tekstowych w 7-bitowym kodowaniu ASCII i nie posiadał żadnych mechanizmów uwierzytelniania ani szyfrowania. W realiach wczesnego internetu, ograniczonego głównie do środowisk akademickich i wojskowych, opierano się bowiem na wzajemnym zaufaniu użytkowników.

W 1995 roku wprowadzono rozszerzoną wersję ESMTP (później zaktualizowaną w kluczowych dokumentach RFC 2821 z 2001 roku oraz RFC 5321 z 2008 roku), która umożliwiła dodawanie nowych funkcji, takich jak uwierzytelnianie nadawcy (SMTP-AUTH), szyfrowanie transmisji (STARTTLS) czy obsługa załączników i znaków spoza podstawowego alfabetu (dzięki standardowi MIME). Współcześnie SMTP – wspierany dodatkowo przez nowoczesne mechanizmy weryfikacji tożsamości, takie jak SPF, DKIM i DMARC – pozostaje niekwestionowanym kręgosłupem globalnej poczty elektronicznej, przez który codziennie przechodzą miliardy wiadomości.

## Środowisko pracy

## Uwaga

Praca na własnej skrzynce pocztowej jest **niezalecana i odbywa się wyłącznie na własną odpowiedzialność.**

W ramach zajęć skorzystamy z narzędzia **GreenMail Standalone** do łatwiejszego i bezpieczniejszego zarządzania pocztą. Dostęp do aplikacji można uzyskać na dwa sposoby:

* **Budując projekt z kodu**
  * [Strona projektu](https://greenmail-mail-test.github.io/greenmail/)
  * [Repozytorium GitHub](https://github.com/greenmail-mail-test/greenmail)
*   **Korzystając z obrazu Docker**

    Poniższe polecenie pozwala na uruchomienie serwera GreenMail Standalone, który nie posiada żadnych wiadomości:

```bash
docker run -d --name greenmail \
  -p 3025:3025 -p 3110:3110 -p 3143:3143 -p 8080:8080 \
  -e GREENMAIL_OPTS='-Dgreenmail.setup.test.all -Dgreenmail.hostname=0.0.0.0 -Dgreenmail.users=student:haslo123@example.com' \
  greenmail/standalone:latest
```

```yml
  GNU nano 7.2                                       docker-compose.yml
services:
  greenmail:
    image: greenmail/standalone:latest
    container_name: greenmail
    restart: unless-stopped
    environment:
      # Usunięto -Dgreenmail.auth.disabled -> serwer wymaga teraz autoryzacji
      # Format konta: login:haslo@domena -> tworzy admin@ps-uken.pl z loginem "admin" i hasłem "amin"
      - GREENMAIL_OPTS=-Dgreenmail.setup.test.all -Dgreenmail.hostname=0.0.0.0 -Dgreenmail.users=admin:admin@ps-uken.pl>
    ports:
      - "0.0.0.0:3025:3025" # SMTP
      - "0.0.0.0:3465:3465" # SMTPS (SSL/TLS)
      - "0.0.0.0:3110:3110" # POP3
      - "0.0.0.0:3995:3995" # POP3S (SSL/TLS)
      - "0.0.0.0:3143:3143" # IMAP
      - "0.0.0.0:3993:3993" # IMAPS (SSL/TLS)
      - "0.0.0.0:8080:8080" # GreenMail REST API

  roundcube:
    image: roundcube/roundcubemail:latest
    container_name: roundcube
    restart: unless-stopped
    depends_on:
      - greenmail
    ports:
      - "0.0.0.0:8081:80" # Interfejs WWW Roundcube
```

Niezależnie od wybranej metody polecam zapoznać się z [oficjalną stroną GreenMail](https://greenmail-mail-test.github.io/greenmail/), aby uzyskać bardziej szczegółowe informacje.

Do w pełni funkcjonalnego działania serwera i praktycznej pracy na zajęciach należy uzupełnić skrzynkę wiadomościami. Poniżej znajdziesz plik z przykładowymi wiadomościami do zaimportowania:

_\[Miejsce na link do pliku lub skryptu uzupełniającego skrzynkę]_
