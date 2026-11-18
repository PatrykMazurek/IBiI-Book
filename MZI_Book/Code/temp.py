import pandas as pd
import numpy as np
import seaborn as sns
import os
import requests


# url = "https://api.nbp.pl/api/exchangerates/tables/A/"
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m&timezone=Europe%2FLondon&forecast_days=3"
# Parametry doklejane do adresu URL
# query_params = {
#     "apikey": "d8ad4e9f",
#     "t" : "Game of Thrones"
# }

# Nagłówki zawierające m.in. klucz API
# headers = {
#     "Accept": "application/json"
# }

response = requests.get(url)
if response.status_code ==200:
    print("Zapytanie ok")
    print(response.text)