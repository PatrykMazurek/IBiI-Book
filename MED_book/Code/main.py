import numpy as np
import pandas as pd
import seaborn as sns

matrix = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

# # Przekazujemy macierz i definiujemy nazwy kolumn oraz indeksy
# df_matrix = pd.DataFrame(
#     data=matrix,
#     columns=['Kolumna_A', 'Kolumna_B', 'Kolumna_C']
# )
#
# flights = sns.load_dataset('flights')
# tips = sns.load_dataset('tips')
# iris = sns.load_dataset('iris')

# for i in flights:
#     print(i)
#
# v = np.array([-5, 6, 7, 8, 2, 1])
# m = np.array([(2, 4, 6, 8),
#             (12, 14, 16, 18),
#             (22, 24, 26, 28)])

n = np.arange(0,40, 5)
# print(n)
# print(type(n))
#
# print("size\t shape\t len()")
# print(f"{m.size}\t\t {m.shape}\t {len(m)}")
# print("-"*25)
# print(f"{v.size}\t\t {v.shape}\t {len(v)}")
#
# print(f"dtype = {np.array([3,6,3,50]).dtype}")
# print(f"dtype.name = {np.array([3.0, 0.6, 0.6, 5.1, 8.4]).dtype.name}")
# print(f"dtype = {np.array(["Warszawa", "Kraków", "Katowice"]).dtype}")
# print(f"dtype.name = {np.array(["Warszawa", "Kraków", "Katowice", "Radom"]).dtype.name}")

print(f"typ = {n.dtype} : {n}")
n = np.astype(n, np.float16)
print(f"typ = {n.dtype} : {n}")

