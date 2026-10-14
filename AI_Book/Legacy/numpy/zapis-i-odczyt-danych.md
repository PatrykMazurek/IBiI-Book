# Zapis i odczyt danych

Pakiet Numpy przygotował odpowiednie metody, które pozwalają na zapis i odczyt danych z takich formatów jak `csv`, `txt` czy `npy`. Format npy to specjalnie przygotowany format binaryn, który pozwala na szybki odczyt i zapis danych przy zachowaniu odpowiednich struktór macierzowych.

### Zapis do plików

Posiadając dane numeryczne w postaci tablicy czy macierzy możemy je zapisać za pomocą funkcji zawartych w pakiecie Numpy.&#x20;

**Zapisywanie do pliku tekstowego**&#x20;

Zakładając że mamy pewną macierz z danymi numerycznymi&#x20;

```python
import numpy as np

dane = np.array([
    [10, 20, 30],
    [45, 55, 65],
    [70, 80, 95]
])
```

Możemy zapisać powyższe dane do pliku `dane.txt` stosując następującą metodę

```python
p.savetxt("dane.txt", dane)
```

&#x20;W wyniku działani metody otrzyamamy plik z zapisaną macierzą, zapis jest w postaci naukowej więc możemy sformatować do bardziej czytelnej formy.

```python
np.savetxt("dane.txt", dane, fmt="%d")
```

Jeżeli dane mają być zapisane w formacie CSV można ustawić odpowiedni separator.

```python
np.savetxt("dane.csv", dane, delimiter=",", fmt="%d")
```

Innym sposobem zapisania danych jest zapisanie do pliku binarnego w odpowiednim formacie `.npy` zaproponowanym przez Numpy. Zapis do takiego plku pozwala na zachowanie struktury macierzy, którą będziemy zapisywać.

```python
np.save("dane.npy", dane)
```
