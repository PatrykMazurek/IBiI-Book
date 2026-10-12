import numpy as np
import pandas as pd
import seaborn as sns

data = {
    'Imie': ['Anna', 'Jan', 'Piotr', 'Kasia', 'Marek', 'Ewa', 'Kamil'],
    'Dzial': ['IT', 'HR', 'IT', 'Sprzedaz', 'HR', 'IT', np.nan],
    'Wiek': [28, 34, 29, 42, 25, 31, np.nan],
    'Pensja': [8000, 6000, 8500, 9000, 5500, 9200, np.nan],
    'Lata_Pracy': [3, 7, 4, 12, 1, 5, np.nan]
}

df = pd.DataFrame(data)

print(df.nlargest(2, "Wiek"))
print(("-"*15))
print(df.nsmallest(2, "Pensja"))
