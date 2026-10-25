# Lekcja 3 - Refinement z Product Ownerem

> Autor: Łukasz Szymankiewicz (34562), Grupa: INF 3-4 26_27Z, Data: 25.10.2026, Gałąź: `feature/order-reporting`

> Praca indywidualna: rolę Product Ownera odgrywał autor na podstawie Business Requestu i dokumentacji biznesowej OrderFlow, zgodnie z podziałem ról z prezentacji do lekcji 3.

## Rejestr decyzji zespołu

**Product Owner:** Łukasz Szymankiewicz, **Facylitator:** Łukasz Szymankiewicz, **Analityk:** Łukasz Szymankiewicz, **Sekretarz:** Łukasz Szymankiewicz

| Nr | Temat i pytanie | Odpowiedź PO | Potwierdzona reguła | Wpływ na zakres lub AC | Otwarte |
|---|---|---|---|---|---|
| 1 | Anulowane: czy CANCELLED wchodzą do łącznej wartości? | Nie wliczamy ich do wartości sprzedaży, ale raport ma pokazać, że powstały. | CANCELLED liczone w liczbie wszystkich zamówień i w podziale na statusy; wykluczone z wartości sprzedaży; osobno liczba i wartość anulowanych. | AC dla podsumowania: dwie wartości - sprzedaż (bez CANCELLED) i anulowane. | - |
| 2 | Granice okresu: czy data końcowa jest włącznie? | Tak, oba dni włącznie, cały dzień kalendarzowy. | Okres = od 00:00:00 dnia początkowego do 23:59:59 dnia końcowego; ta sama data = raport dzienny. | AC dla granic (przypadek 5) i raportu dziennego (przypadek 1). | Strefa czasu - otwarte kwestie. |
| 3 | Wartość sprzedaży: które statusy? | Wszystkie poza CANCELLED. NEW też liczymy, bo to złożone zamówienie; jedynym wyjątkiem jest anulowanie. | Wartość sprzedaży = suma total zamówień o statusach NEW, PAID, PROCESSING, SHIPPED, DELIVERED. | Definicja głównej liczby raportu i jej etykieta ("Wartość sprzedaży"). | - |
| 4 | Status w raporcie: bieżący czy z końca okresu? | Bieżący; historia statusów nie jest potrzebna w tej zmianie. | Podział na statusy według statusu w chwili generowania; raport pokazuje datę i godzinę wygenerowania. | Historia statusów poza zakresem; AC: wynik powtarzalny przy niezmienionych danych. | - |
| 5 | Niespójne dane: przerwać raport czy pominąć rekord? | Nie pokazywać wyniku, który tylko wygląda na poprawny. | Rekord z brakującą/niepoprawną datą, statusem lub wartością w danych -> raport nie powstaje; komunikat wskazuje ID zamówienia. | AC dla danych niespójnych (pkt 11); aplikacja nie może się zamknąć. | - |
| 6 | Format daty i skróty okresów? | RRRR-MM-DD wystarczy; bez skrótów w tej zmianie. | Daty wpisywane jako RRRR-MM-DD; zły format, nieistniejąca data lub koniec przed początkiem -> komunikat z przykładem poprawnej wartości, brak raportu. | AC dla walidacji (przypadek 6); skróty okresów poza zakresem. | Ograniczenia zakresu - otwarte. |
| 7 | Obecny raport: zastąpić czy zostawić? | Zostawić bez zmian, raport okresowy jako osobna operacja. | Opcja "Raport zamówień" działa jak dotąd; raport okresowy to nowa, osobna operacja w menu. | AC regresji dla istniejących funkcji (pkt 12). | - |

## Kontrola jakości zapisu

- [x] Każda ważna odpowiedź została sparafrazowana
- [x] PO potwierdził albo skorygował regułę
- [x] Zapisaliśmy wpływ decyzji na zakres lub przyszłe AC
- [x] Każda niewiadoma ma właściciela i następny krok

## Podsumowanie zakresu

### W zakresie

- Nowa operacja w menu: raport okresowy z datą początkową i końcową (RRRR-MM-DD, oba dni włącznie).
- Walidacja zakresu: format, istniejąca data, data początkowa <= końcowa; czytelny komunikat, brak raportu przy błędzie.
- Wybór zamówień po dacie utworzenia (created_at); każde zamówienie najwyżej raz.
- Wynik: okres i data wygenerowania, liczba wszystkich zamówień, wartość sprzedaży (bez CANCELLED), liczba i wartość anulowanych, liczba i wartość dla każdego statusu.
- Jednoznaczny komunikat dla okresu bez zamówień; obsługa niespójnych rekordów bez pozornie poprawnego wyniku.
- Raport nie modyfikuje danych; dotychczasowe funkcje i obecny raport działają bez zmian.

### Poza zakresem

- Panel analityczny, wykresy, porównywanie wielu okresów, prognozy (BR pkt 15).
- Integracje (BI, księgowość, płatności), wysyłka e-mail, eksport do pliku.
- Historia statusów i przebudowa modelu danych, nowy system ról i uprawnień.
- Skróty okresów (dziś, wczoraj, bieżący miesiąc) oraz filtrowanie po kliencie, produkcie, płatności lub dostawie.

## Otwarte kwestie

| Kwestia | Dlaczego blokuje | Właściciel | Termin lub następny krok |
|---|---|---|---|
| Czy przy anulowanych pokazywać ich numery ID, żeby na odprawie dało się je szybko sprawdzić? | Zmienia zawartość wyniku i AC dla przypadku 4. | Product Owner | Decyzja przed lekcją 4 (User Story i AC) |
| Ograniczenia zakresu: data w przyszłości, maksymalna długość okresu. | Bez reguły AC walidacji jest niejednoznaczne. | Product Owner | Decyzja przed lekcją 4 |
| Strefa czasu: created_at bez strefy, czas lokalny komputera. | Może przesunąć zamówienia z okolic północy między dniami. | Zespół + PO | Potwierdzić: czas lokalny firmy (Europe/Warsaw) - przed AC |
| Format liczb w wyniku (kropka "17333.50 zł" vs. polski "17 333,50 zł"). | Wpływa na czytelność wyniku na odprawach (pkt 10). | Product Owner | Pytanie na lekcji 4; domyślnie zostaje obecny format |

## Potwierdzenie PO

- [x] Potwierdzam sens biznesowy podsumowania
- [ ] Wymagana korekta przed lekcją 4

Korekta: Brak korekty.

## Materiał wejściowy do User Story i Acceptance Criteria (lekcja 4)

- Rola: kierownik operacyjny / pracownik obsługi zamówień.
- Potrzeba: podsumowanie zamówień dla wskazanego okresu bez ręcznych obliczeń.
- Reguły do AC: reguły 1-7 z rejestru decyzji.
- Przypadki do AC: 1 (dzień), 2 (kampania śr-wt), 3 (brak zamówień), 4 (anulowane), 5 (granice), 6 (zły zakres), 7 (miesiąc).
- Przykład kontrolny z danych demo: maj 2026 (od 2026-05-01 do 2026-05-31) -> 12 zamówień, w tym 1 anulowane (ORD-0006, 388.00 zł); wartość sprzedaży 6114.50 zł; wartość wszystkich 6502.50 zł.

## Exit tickets

### Exit ticket numer 1

**1. Która odpowiedź Product Ownera najbardziej zmieniła wasze początkowe założenie i dlaczego?**

Odpowiedź o CANCELLED: zakładałem jedną "łączną wartość" jak w obecnym raporcie, a raport potrzebuje dwóch wartości - sprzedaży bez anulowanych oraz osobno anulowanych - co zmienia sposób liczenia i wygląd wyniku.

**2. Która reguła nadal wymaga doprecyzowania przed napisaniem Acceptance Criteria?**

Ograniczenia zakresu dat (data w przyszłości, maksymalna długość okresu) oraz strefa czasu dla created_at - bez nich AC dla walidacji i granic dnia nie będą jednoznaczne.

### Exit ticket numer 2

**1. Która odpowiedź Product Ownera najbardziej zmieniła wasze początkowe założenie i dlaczego?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

**2. Która reguła nadal wymaga doprecyzowania przed napisaniem Acceptance Criteria?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

### Exit ticket numer 3

**1. Która odpowiedź Product Ownera najbardziej zmieniła wasze początkowe założenie i dlaczego?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

**2. Która reguła nadal wymaga doprecyzowania przed napisaniem Acceptance Criteria?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

