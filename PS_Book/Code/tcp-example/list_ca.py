import ssl
import pprint

# Utworzenie domyślnego kontekstu (automatycznie ładuje systemowe certyfikaty CA)
context = ssl.create_default_context()

# Pobranie listy załadowanych certyfikatów (w czytelnej formie słownika)
ca_certs = context.get_ca_certs(binary_form=False)

print(f"Z systemu załadowano {len(ca_certs)} certyfikatów zaufanych CA.\n")

# Wyświetlenie informacji o pierwszym certyfikacie z brzegu
if ca_certs:
    print("Przykładowy certyfikat (Wystawca / Podmiot):")
    # Zwrócony certyfikat zawiera m.in. klucz 'subject' (kogo dotyczy) i 'issuer' (kto wydał)
    pprint.pprint(ca_certs[0]['subject'])