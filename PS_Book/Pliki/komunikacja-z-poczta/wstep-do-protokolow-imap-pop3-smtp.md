# Wstęp do protokołów IMAP, POP3, SMTP

W przypadku projektów, które wykorzystują komunikację z pocztą elektroniczną, programiści mają do dyspozycji protokoły pozwalające na pełne zarządzanie taką komunikacją. W tym celu można wykorzystać takie protokoły jak: IMAP/POP3 do pobierania i zarządzania wiadomościami w skrzynce pocztowej oraz SMTP do wysyłania wiadomości. Większość serwerów pocztowych do bezpiecznej komunikacji wykorzystuje szyfrowania oraz protokoły OAuth aby bezpiecznie potwierdzić tożsamość użytkownika.&#x20;

#### Historia

Protokół POP -Historia protokołu POP (Post Office Protocol) sięga 1984 roku, kiedy to opublikowano jego pierwszą wersję (POP1) w dokumencie RFC 918. Powstał on jako odpowiedź na realny problem tamtych czasów: komputery osobiste i stacje robocze nie miały stałego dostępu do sieci, więc potrzebowały prostego mechanizmu do pobierania poczty z centralnego serwera podczas krótkich połączeń, np. przez modem. Już rok później, w 1985 roku, pojawiła się ulepszona wersja POP2 (RFC 937), ale prawdziwy przełom przyniósł rok 1988 i debiut POP3 (RFC 1081). Zaprojektowano go tak, by działał w prostym modelu „pobierz wiadomości na dysk i usuń je z serwera”, co idealnie pasowało do epoki drogiej i bardzo ograniczonej przestrzeni dyskowej na serwerach pocztowych.
Przez lata 90. i początek XXI wieku POP3 – ostatecznie ustandaryzowany w 1996 roku w dokumencie RFC 1939 – stał się absolutnym fundamentem internetowej poczty, wspieranym przez niemal każdego klienta e-mail. Z czasem rozszerzono go o mechanizmy bezpieczeństwa, takie jak szyfrowanie połączeń przez SSL/TLS (POP3S) oraz nowoczesne metody uwierzytelniania.

Protokół IMAP - Historia protokołu IMAP (Internet Message Access Protocol) rozpoczęła się w 1986 roku na Uniwersytecie Stanforda, gdzie Mark Crispin zaprojektował go jako nowoczesną alternatywę dla raczkującego wówczas POP. Od samego początku IMAP opierał się na zupełnie innej filozofii: wiadomości miały na stałe pozostawać na serwerze, a programy pocztowe jedynie się z nim synchronizowały. Po wczesnych iteracjach, takich jak IMAP2 z 1988 roku (RFC 1064) oraz niezbyt popularnym IMAP3, prawdziwy przełom nastąpił w 1994 roku wraz z premierą wersji IMAP4 (RFC 1730). Wprowadziła ona zaawansowane zarządzanie folderami, flagowanie wiadomości oraz możliwość ich przeszukiwania bezpośrednio po stronie serwera, bez konieczności pobierania całych załączników.
W 2003 roku protokół doczekał się kluczowej standaryzacji jako IMAP4rev1 (RFC 3501), która przez niemal dwie dekady stanowiła główny fundament poczty elektronicznej. Jego prawdziwy rozkwit przyniosła jednak era smartfonów, tabletów i pracy na wielu urządzeniach jednocześnie, gdzie model „pobierz i usuń” znany z POP3 przestał się sprawdzać.
W 2021 roku opublikowano jego nowoczesną aktualizację – IMAP4rev2 (RFC 9051), która uporządkowała protokół i włączyła do jego rdzenia najważniejsze ulepszenia wypracowane przez lata.

Protokół SMTP - Historia protokołu SMTP (Simple Mail Transfer Protocol) sięga 1982 roku, kiedy to Jon Postel opublikował jego oficjalną specyfikację w dokumencie RFC 821. Powstał on jako następca wcześniejszych, mniej elastycznych mechanizmów przesyłania wiadomości w sieci ARPANET i od samego początku odpowiadał wyłącznie za wysyłanie oraz przekazywanie poczty między serwerami. Pierwotny SMTP był niezwykle prosty – opierał się na czytelnych dla człowieka poleceniach tekstowych w 7-bitowym kodowaniu ASCII i nie posiadał żadnych mechanizmów uwierzytelniania ani szyfrowania. W realiach wczesnego internetu, ograniczonego głównie do środowisk akademickich i wojskowych, opierano się bowiem na wzajemnym zaufaniu użytkowników.
W 1995 roku wprowadzono rozszerzoną wersje ESMTP (później zaktualizowanej w kluczowych dokumentach RFC 2821 z 2001 roku oraz RFC 5321 z 2008 roku), która umożliwiła dodawanie nowych funkcji, takich jak uwierzytelnianie nadawcy (SMTP-AUTH), szyfrowanie transmisji (STARTTLS) czy obsługa załączników i znaków spoza podstawowego alfabetu (dzięki standardowi MIME). Współcześnie SMTP – wspierany dodatkowo przez nowoczesne mechanizmy weryfikacji tożsamości, takie jak SPF, DKIM i DMARC – pozostaje niekwestionowanym kręgosłupem globalnej poczty elektronicznej, przez który codziennie przechodzą miliardy wiadomości.

#### Środowisko pracy

W ramach zajęć skorzystamy z narzędzia **GreenMail Standalone** do łatwiejszego i bezpieczniejszego zarządzania pocztą. Dostęp do aplikacji można uzyskać na dwa sposoby:

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

Niezależnie od wybranej wersji polecam zapoznać się z oficjalną stroną projektu w celu uzyskania szczegółów dotyczących projektu. [Oficjalna Strona GreenMail](https://greenmail-mail-test.github.io/greenmail/)

Do w pełni funkcjonalnego działania serserwera i praktyczego pracy na zajęciach, należy skrzynkę uzupełnić wiadomościami. Poniżej przedstawiam plik, który uzpełni skrzynkę wiadomoścmiami, które posłużą do pracy na zajęciach.

### Uwaga

Praca na własnej skrzynce pocztowej jest **nie zalecana i wykonywane jest tylko i wyłącznie na własną odpowiedzialność.**&#x20;
