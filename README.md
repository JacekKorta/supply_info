# supply_info
Supply info (django)

Założenia: 
Prosta strona na której nasi klienci będą mogli zobaczyć dostępność produktów (niedokładną). 

Niezalogowani użytkownicy powinni widzieć tylko listę maszyn.

Po zalogowaniu dostępna będzie wyszukiwarka za pomocą której będzie można wyszukać produkty (po kodzie) oraz uzyskać informację o cenie 
(w zależności od cennika przypisanego do klienta).

Dane zostaną zaimportowane z dwóch raportów tekstowych wygenerowanych z programu symfonia Handel 2.0

Oba raporty będą importowane ze schowka. Jeden raport (rzadko używany) będzie dodawał produkty i informacje o nich. 
Drugi raport będzie aktualizował informacje o stanach.

ActiveProductList ma mi dać możliwość włączania i wyłączania widoczności poszczególnych produktów w wyszukiwarce. 
Może istnieć potrzeba czasowego wyłączenia informacji o produkcie, chcę mieć do tego proste i szybkie narzędzie. 
W tym wypadku listę ukrytych (nieaktywnych) produktów. 
