Vaším úkolem bude implementace libovolného evolučního algoritmu a vytvoření jednoduchých statistických a grafických výstupů.

Algoritmy (vyberte libovolný jeden z totoho seznamu):

* DE/jDE
* SOMA (AllToOne strategie)
* PSO

Testovací funkce (Dimenze D=10 a D=30):

* 1st DeJong function
* 2nd DeJong function
* Schweffel function
* Rastrigin (správná definice fce Rastrigin viz [zde](http://www.sfu.ca/~ssurjano/rastr.html))

Funkce - definice v níže přiloženém souboru

FES bude nastaven na 5 000 x D. Algoritmus se musí spustit opakovaně 30x pro každou zkušební funkci - 
pro získání nějakého statistického základu - vypočítáte (z 30 nejlepších výsledků) Min, Max, Mean, Median a Std. Dev.

Musíte také potvrdit vaše výsledky vykreslením nejlepších řešení z každé iterace - tj. Konvergenční graf.
Vaším úkolem bude vykreslit:

* Konvergenční graf všech 30 běhů v jednom grafu (30 čar v 1 grafu) - celkem 8 grafů (1 algoritmus x 4 funkce x 2 nastavení D)
* Konvergenční graf průměrného nejlepšího výsledků - tj. průměrné nejlepší řešení v každé iteraci (z 30 běhů) - celkem 8 grafů ( 1 algoritmus x 4 funkce x 2 nastavení D).

Berte v úvahu následující a nastavení parametrů:

* Nelze opustit vyhledávací prostor - při vytváření nových řešení - zkontrolujte hranice typické pro každou testovací funkci. Pokud opustíte vyhledávací prostor - aplikujte libovolnou zvolenou funkci pro kontrolu hranic (random, periodic, reflection...).

Nastavení –

* pro DE/jDE (NP = 50, F = 0.5, CR = 0.9 (pro jDE je to pouze init nastavení, zbytek dle článku J. Brest et. al),
* pro SOMA (NP = 50, prt = 0.3, PathLength = 3, step = 0.33),
* pro PSO (NP = 50, c1 a c2 = 2.0, inertia weight (lineární pokles): wstart = 0.9, wend = 0.4).

kde NP = počet jedinců (velikost populace).
