import pandas as pd
import numpy as np
import random

# Ustawiamy ziarno losowości, aby za każdym razem generowały się te same dane (ważne na laboratoriach)
np.random.seed(42)
random.seed(42)

print("Rozpoczynam generowanie danych dla studentów...")

# ==========================================
# 1. ZBIÓR LOGOWAŃ (Dla Zadania 1: Drzewa Decyzyjne)
# ==========================================
n_logins = 2000
wiek_konta = np.random.randint(1, 730, n_logins)
# Większość użytkowników wpisuje hasło bezbłędnie lub myli się raz/dwa. Atakujący próbują wielokrotnie.
nieudane_proby = np.random.choice([0, 1, 2, 3, 4, 5, 8, 12], n_logins, p=[0.6, 0.15, 0.1, 0.05, 0.03, 0.03, 0.02, 0.02])
ip_zagraniczne = np.random.choice([0, 1], n_logins, p=[0.8, 0.2])

zablokowany = []
for i in range(n_logins):
    # Logika dla drzewa: zablokuj jeśli (konto bardzo młode i >2 błędy) LUB (zagraniczne IP i >3 błędy) LUB (>5 błędów w ogóle)
    if (wiek_konta[i] < 30 and nieudane_proby[i] > 2) or \
       (ip_zagraniczne[i] == 1 and nieudane_proby[i] > 3) or \
       (nieudane_proby[i] > 5):
        zablokowany.append(1)
    else:
        # Dodajemy odrobinę szumu losowego (1% szans na dziwną decyzję admina), żeby drzewo nie miało w 100% łatwego zadania
        zablokowany.append(np.random.choice([0, 1], p=[0.99, 0.01]))

df_logowania = pd.DataFrame({
    'wiek_konta_w_dniach': wiek_konta,
    'liczba_nieudanych_prob': nieudane_proby,
    'czy_ip_zagraniczne': ip_zagraniczne,
    'zablokowany': zablokowany
})
df_logowania.to_csv('logowania.csv', index=False)
print(f"✅ Wygenerowano 'logowania.csv' ({len(df_logowania)} wierszy, {sum(zablokowany)} blokad).")

# ==========================================
# 2. ZBIÓR TRANSAKCJI / FRAUDÓW (Dla Zadań 2 i 4: Lasy Losowe, Starcie Tytanów)
# Ekstremalne niezbalansowanie: 0.5% ataków
# ==========================================
n_normal = 9950
n_fraud = 50

# Normalne transakcje (mniejsze kwoty, bliżej domu, standardowe odstępy czasu)
normal_kwota = np.random.exponential(scale=150, size=n_normal) # Większość to małe zakupy, rzadko duże
normal_odleglosc = np.random.lognormal(mean=1.5, sigma=1.0, size=n_normal) # Zazwyczaj w okolicy
normal_czas = np.random.normal(loc=24, scale=10, size=n_normal) # Zazwyczaj co ok. 24 godziny (abs() żeby nie było na minusie)
normal_czas = np.abs(normal_czas)

# Fraudy (duże kwoty, na drugim końcu kraju/świata, wykonywane tuż po sobie w krótkim czasie)
fraud_kwota = np.random.normal(loc=3000, scale=1000, size=n_fraud)
fraud_odleglosc = np.random.normal(loc=500, scale=200, size=n_fraud)
fraud_czas = np.random.exponential(scale=0.5, size=n_fraud) # Bardzo mały czas od ostatniej transakcji

df_normal = pd.DataFrame({
    'kwota_przelewu': normal_kwota,
    'odleglosc_od_domu': normal_odleglosc,
    'czas_od_ostatniej_transakcji': normal_czas,
    'is_fraud': 0
})

df_fraud = pd.DataFrame({
    'kwota_przelewu': fraud_kwota,
    'odleglosc_od_domu': fraud_odleglosc,
    'czas_od_ostatniej_transakcji': fraud_czas,
    'is_fraud': 1
})

df_transakcje = pd.concat([df_normal, df_fraud]).sample(frac=1, random_state=42).reset_index(drop=True)
# Zaokrąglamy dla realizmu
df_transakcje = df_transakcje.round(2)
df_transakcje.to_csv('transakcje.csv', index=False)
print(f"✅ Wygenerowano 'transakcje.csv' ({len(df_transakcje)} wierszy, {df_transakcje['is_fraud'].sum()} oszustw).")

# ==========================================
# 3. ZBIÓR MAILI (Dla Zadania 3: Naiwny Bayes)
# ==========================================
# Szablony tekstów
szablony_ham = [
    "Czesc, o ktorej jutro mamy to spotkanie biznesowe?",
    "W zalaczeniu przesylam raport finansowy za ubiegly miesiac. Pozdrawiam.",
    "Czy mozesz mi podeslac notatki z wczorajszego wykladu?",
    "Kup po drodze chleb i maslo, zapomnialem rano.",
    "Projekt zostal zaakceptowany przez klienta. Zaczynamy wdrazanie.",
    "Zycze udanego urlopu, do zobaczenia za dwa tygodnie!",
    "Twoje zamowienie nr {id} zostalo wyslane i jest w drodze.",
    "Przypominam o dzisiejszym szkoleniu z zasad BHP o 14:00."
]

szablony_phishing = [
    "Pilne! Zablokowano twoje konto w banku. Kliknij link aby zresetowac haslo.",
    "Wygrales nowego iPhone! Odbierz nagrode pod tym linkiem natychmiast.",
    "Twoja paczka zostala wstrzymana z powodu niedoplaty 2 PLN. Zaplac teraz klikajac tutaj.",
    "Twoje haslo wygaslo. Zresetuj je w ciagu 24 godzin albo stracisz dostep do konta.",
    "Wykryto nieautoryzowane logowanie. Zaloguj sie na ponizszej stronie aby potwierdzic tozsamosc.",
    "Gratulacje! Zostales wylosowany w loterii kryptowalut. Odbierz swoje bitcoiny.",
    "Konto zawieszone. Twoje dane logowania wyciekly. Zmien haslo pilnie!"
]

maile = []
etykiety = []

# Generujemy 300 normalnych maili (Ham)
for _ in range(300):
    tresc = random.choice(szablony_ham)
    if "{id}" in tresc:
        tresc = tresc.replace("{id}", str(random.randint(1000, 9999)))
    maile.append(tresc)
    etykiety.append(0)

# Generujemy 100 maili phishingowych (Phishing) - zależy nam na widocznym powtarzaniu słów-kluczy
for _ in range(100):
    maile.append(random.choice(szablony_phishing))
    etykiety.append(1)

df_maile = pd.DataFrame({
    'tresc_wiadomosci': maile,
    'etykieta': etykiety
})

# Mieszamy wiadomości
df_maile = df_maile.sample(frac=1, random_state=42).reset_index(drop=True)
df_maile.to_csv('maile.csv', index=False)
print(f"✅ Wygenerowano 'maile.csv' ({len(df_maile)} wierszy, 100 wiadomości phishingowych).")
print("\nDane są gotowe. Studenci mogą zaczynać pracę!")