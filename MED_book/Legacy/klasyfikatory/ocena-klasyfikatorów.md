# Ocena klasyfikatorów 


Ważnym etapem w pracy z danymi jest sprawdzenie, jak klasyfikatory radzą sobie z przygotowanymi danymi przed wdrożeniem do realnych systemów. 

Biblioteka `scikit-learn` oferuje różne metryki do oceny skuteczności modeli, takie jak:
- *macierz pomyłek (confusion matrix)*;
- *dokładność (accuracy)*;
- *precyzja (precision)*;
- *czułość (recall)*;
- *wskaźnik F1 (F1-score)*.

### Confusion matrix (Macierz pomyłek)

Jest to jedna z najpopularniejszych metod do weryfikacji wyników klasyfikacji. W wyniku otrzymujemy macierz 2 x 2, która zawiera:

* *Prawdziwie pozytywne (**TP**)*
    Przypadki, w których:
    - Model przewiduje wartość **Tak**,
    - Rzeczywista wartość również wynosi **Tak**.<br>

* *Prawdziwie negatywne (**TN**)*
    Przypadki, w których:
    - Model przewiduje wartość **Nie**,
    - Rzeczywista wartość również wynosi **Nie**.<br>

* *Fałszywie pozytywne (**FP**)*
    Przypadki, w których:
    - Model przewiduje wartość **Tak**,
    - Rzeczywista wartość wynosi **Nie**.<br>

* *Fałszywie negatywne (**FN**)*
    Przypadki, w których:
    - Model przewiduje wartość **Nie**,
    - Rzeczywista wartość wynosi **Tak**.<br>

Macierz potrafi pokazać, gdzie występuje problem w klasyfikacji.

Przykładowy kod, przedstawiający wyniki macierzy pomyłek:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

sns.heatmap(confusion_matrix(target_test, predictions), annot = True, cmap='Blues', fmt='g')
plt.show()
```

#### Accuracy - dokładność klasyfikacji

Dokładność modelu (accuracy) można wyrazić za pomocą pojęć TN (True Negative), TP (True Positive), FN (False Negative) i FP (False Positive) za pomocą następującego wzoru:
$$
\mbox{accuracy} = \frac{TP+TN}{TP+TN+FP+FN}
$$

#### Precision - precyzja

Określa, jaka część wyników wskazanych przez klasyfikator jako pozytywne/negatywne jest faktycznie pozytywna/negatywna.

$$
\mbox{precision} = \frac{TP}{TP+FP}
$$

#### Recall - czułość

Określa, jaką część próbek pozytywnej/negatywnej klasy (ze wszystkich, które powinien był wykryć) wykrył klasyfikator.
$$
\mbox{Recall} = \frac{TP}{TP+FN}
$$

#### F1 - score

Wskaźnik F1 jest miarą harmoniczną precyzji (precision) i czułości (recall), który zapewnia zrównoważone spojrzenie na skuteczność modelu, szczególnie w przypadku niezrównoważonych klas. Wzór na F1-score to:
$$
F1 = 2 * \frac{Precission * Recal}{Precission + Recal}
$$

Do przeprowadzenia kompletnej oceny klasyfikatora w uczeniu maszynowym wykorzystuje się różne miary, które pomagają zrozumieć jego skuteczność. Narzędzie, które to automatyzuje w Pythonie, to funkcja `classification_report` z biblioteki `scikit-learn`.

```python
from sklearn.metrics import classification_report

c_report = classification_report(target_test, predictions, output_dict=True)
pd.DataFrame(c_report)
```
