<div align="center">

# Evoluční algoritmy
</div>

Přehled výsledků vyhledávání minim jde najít v souboru `statistics_output.xlsx`,
kde je přehled iterací pro jednotlivé funkce a dimenzionalitu,
nalezená minima a populace poslední generace, ze které bylo toto minimum získáno.
Dále je pak pro každý algoritmus, funkci a dimenzionalitu uveden průměr, medián,
maximum, minimum a standardní odchylka.

Vykreslené grafy dle zadání jde najít v adresáři [/plots](/plots), jejich pojmenování
vždy udává testovací funkci, dimenzi a typ grafu:

* `iterations` podává přehled průběhů nejlepšího výsledku z každé generace pro jednotlivé iterace v dané dimenzionalitě 
* `stats` podává přehled statistických ukazatelů, opět navázaných na generace, ale přeze všechny iterace

Grafy byly vykresleny pomocí knihovny `matplotlib`.

Implementace algoritmů je v souboru `optim.py`. Pokud máte nainstalovaný
Python 3.x, jde skript spustit následovně:

```
py -m pip install -r requirements.txt
py optim.py
```

Výstup skiptu se uloží do souboru `raw_output.xlsx`.

Pokud budeme chtít vykreslit i grafy pro jednotlivé vstupy, je potřeba skript
spustit s touto možností povolenou:

```
py optim.py --enable-plots
NEBO
py optim.py -p
```

### Řešení funkce Schwefel

Pro funkci Schwefel jsou výsledky DE nepříliš uspokojivé. Na rozdíl od ostatních
funkcí zde algoritmus váznul v lokálních minimech a pouze v některých iteracích
a až po více generacích dokázal najít i lepší minimum. Tento problém jsem zkusil
odstranit zvolením metody kontroly hranic random, tedy výměnou za náhodnou novou
souřadnici, která může zvýšit pravděpodobnost, že z lokálního minima
vyvázneme, vnesením nového "skoku" v pohybu jednotlivých bodů.
