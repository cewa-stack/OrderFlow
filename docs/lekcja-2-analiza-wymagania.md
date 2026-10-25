# Lekcja 2 - Analiza wymagania biznesowego

> Autor: Łukasz Szymankiewicz (34562), Grupa: INF 3-4 26_27Z, Data: 25.10.2026, Gałąź: `feature/order-reporting`

Dokument wejściowy: *Business Request - Rozszerzone raportowanie zamówień* (wersja A).

## Karta pracy zespołu

Pracujcie na pełnym Business Requeście. Nie twórzcie jeszcze User Story, Acceptance Criteria ani projektu rozwiązania.

| Zespół | Data | Role Studentów (imię i nazwisko) |
|---|---|---|
| Łukasz Szymankiewicz (nr albumu 34562), INF 3-4 26_27Z | 25.10.2026 | Moderator: Łukasz Szymankiewicz<br>Analityk: Łukasz Szymankiewicz<br>Sekretarz: Łukasz Szymankiewicz |

## Problem i rezultat

**Problem biznesowy w maksymalnie dwóch zdaniach:** Kierownik operacyjny nie może uzyskać w OrderFlow podsumowania zamówień dla wybranego okresu, bo obecny raport obejmuje całą historię, więc dane okresowe zbiera i sumuje ręcznie poza systemem. Wydłuża to przygotowanie podsumowań i grozi pominięciem zamówień lub błędnym zsumowaniem wartości.

**Oczekiwany rezultat biznesowy w maksymalnie dwóch zdaniach:** Pracownik wskazuje w OrderFlow początek i koniec okresu i dostaje czytelne podsumowanie (liczba, wartość, podział na statusy) albo jasną informację, dlaczego raportu nie da się przygotować. Wynik jest powtarzalny, nie zmienia danych i pozwala zaufać temu, które zamówienia zostały policzone.

## Użytkownik i kontekst

| Element | Odpowiedź zespołu | Dowód w dokumencie |
|---|---|---|
| Użytkownik | Kierownik operacyjny (główny odbiorca); z raportu korzystają też pracownicy obsługi zamówień. | BR - nagłówek "ODBIORCA"; pkt 1 Kontekst biznesowy |
| Sytuacja pracy | Krótkie odprawy (np. poranna - raport z poprzedniego dnia) oraz przygotowanie podsumowań dziennych, tygodniowych, miesięcznych i dla okresów kampanii dla osób od sprzedaży i realizacji. | pkt 1, pkt 6, pkt 10; przypadki 1, 2 i 7 (pkt 13) |
| Decyzja wspierana raportem | Ocena skali i wartości sprzedaży w okresie oraz stanu realizacji zamówień (struktura statusów) - np. czy kampania przyniosła sprzedaż i czy zamówienia nie utknęły w realizacji. | pkt 2, pkt 3, pkt 14 ("ocenić skalę aktywności... strukturę... wartości istotne operacyjnie i sprzedażowo") |

## Kontrola jakości

- [x] Nie opisaliśmy jeszcze konkretnego ekranu ani rozwiązania technicznego
- [x] Każdy kluczowy fakt ma źródło w Business Requeście lub analizie OrderFlow
- [x] Potrafimy wyjaśnić różnicę między problemem a proponowaną funkcją

## Stan obecny i docelowy

| Krok | Stan obecny | Stan docelowy |
|---|---|---|
| 1 | Pracownik wybiera "5. Raport zamówień". | Pracownik wybiera operację raportu okresowego. |
| 2 | System liczy raport ze wszystkich zamówień - nie da się wskazać okresu. | Pracownik podaje datę początkową i końcową okresu. |
| 3 | Pracownik przegląda listę zamówień i ręcznie wybiera te z interesujących go dat. | System sprawdza zakres; przy błędzie podaje powód i jak go poprawić. |
| 4 | Ręcznie sumuje liczbę i wartości poza OrderFlow. | System wybiera zamówienia wg daty utworzenia i oblicza podsumowanie. |
| 5 | Przygotowuje podsumowanie w niejednolitej formie; trudno sprawdzić, które zamówienia policzono. | Pracownik otrzymuje czytelny wynik z jawnym okresem albo informację "brak zamówień"; dane nie są zmieniane. |

## Tablica analizy

| Nr | Stwierdzenie lub pytanie | Typ F Z P | Dowód albo wpływ |
|---|---|---|---|
| 1 | Raport okresowy jest przygotowywany na podstawie daty utworzenia zamówienia; każde zamówienie najwyżej raz. | F | BR pkt 5; pole created_at w orders.json |
| 2 | Zakres musi mieć początek i koniec; dla zakresu niemożliwego do zinterpretowania raport nie powstaje. | F | BR pkt 5, pkt 9, przypadek 6 |
| 3 | Wartości pochodzą z wartości zapisanych w zamówieniu, nie z bieżącego cennika. | F | BR pkt 5, pkt 11; kod: build_order_report() sumuje pole total |
| 4 | Generowanie raportu nie zmienia danych, a ponowne uruchomienie na niezmienionych danych daje ten sam wynik. | F | BR pkt 3, pkt 11 |
| 5 | Poprawny okres bez zamówień nie jest błędem i ma dostać jednoznaczny komunikat. | F | BR pkt 9, przypadek 3 |
| 6 | Zamówienia anulowane nie mogą być ukryte w raporcie. | F | BR pkt 7, przypadek 4 |
| 7 | Data końcowa jest liczona włącznie (cały ostatni dzień do 23:59:59). | Z | Przypadek 5 tylko sugeruje ("zwykłe rozumienie"); zmienia, które zamówienia wejdą do raportu -> pytanie 2 |
| 8 | Podział na statusy pokazuje status bieżący (z chwili generowania), a nie z końca okresu. | Z | System nie ma historii statusów; przypadek 7 może oczekiwać innej interpretacji -> pytanie 4 |
| 9 | Użytkownik wpisuje daty w formacie RRRR-MM-DD. | Z | BR nie określa formatu; wpływa na walidację i komunikaty błędów -> pytanie 6 |
| 10 | Czy CANCELLED wchodzą do głównej wartości raportu? | P | Zmienia sposób liczenia najważniejszej liczby raportu -> pytanie 1 |

**Instrukcja:** F oznacza fakt, Z oznacza założenie, a P oznacza pytanie. Każde założenie powinno zostać potwierdzone, odrzucone albo zamienione w pytanie na refinement.

Podsumowanie: 6 faktów (F), 3 założenia (Z), 1 pytanie (P) w tablicy + 10 pytań na refinement poniżej.

## Pytania na refinement

| Nr | Pytanie do Product Ownera | Co zmieni odpowiedź | Priorytet |
|---|---|---|---|
| 1 | Czy zamówienia CANCELLED wliczamy do łącznej wartości okresu, czy pokazujemy je osobno (liczba i wartość anulowanych)? | Sposób liczenia głównej wartości raportu | Wysoki |
| 2 | Czy data końcowa jest włącznie (do 23:59:59)? Czy raport dzienny to ta sama data początkowa i końcowa? | Które zamówienia z granic okresu wejdą do raportu | Wysoki |
| 3 | Które statusy tworzą "wartość sprzedaży"? Czy liczymy też NEW (np. nieopłacone, pobranie przy odbiorze)? | Definicja głównej wartości; ewentualnie dwie różne wartości w raporcie | Wysoki |
| 4 | Czy raport pokazuje status bieżący, czy z końca okresu? Czy akceptujemy, że ponowny raport za ten sam okres po zmianie statusów da inny podział? | Zakres zmiany - historia statusów oznaczałaby przebudowę modelu danych (poza zakresem wg pkt 15) | Wysoki |
| 5 | Co zrobić z rekordem o brakującej/niepoprawnej dacie, statusie lub wartości: przerwać raport czy pominąć z ostrzeżeniem? | Zachowanie przy danych niespójnych (pkt 11) i treść komunikatu | Średni |
| 6 | W jakim formacie wpisujemy daty? Czy potrzebne są skróty: dziś, wczoraj, bieżący tydzień/miesiąc? | Walidacja wejścia, komunikaty, zakres funkcji | Średni |
| 7 | Czy obowiązują ograniczenia zakresu: data w przyszłości, maksymalna długość okresu, daty sprzed uruchomienia systemu? | Reguły walidacji - granica między ochroną przed błędem a blokowaniem analiz historycznych (pkt 6) | Wysoki |
| 8 | Czy w podziale pokazywać wszystkie 6 statusów (także z zerem), czy tylko występujące? | Format i czytelność wyniku | Niski |
| 9 | Co musi zawierać nagłówek wyniku: okres, datę wygenerowania, liczbę dni? Czy pokazać ID policzonych zamówień? | Prezentacja i weryfikowalność wyniku (pkt 8, pkt 10) bez kopiowania listy zamówień (pkt 5) | Średni |
| 10 | Czy raport okresowy ma być osobną operacją obok obecnego raportu, czy go zastąpić (np. pusty zakres = całość)? | Wpływ na istniejącą funkcję (pkt 12) i układ menu | Średni |

## Pięć pytań priorytetowych

Test wpływu: czy odpowiedź zmienia sposób liczenia wyniku, zbiór zamówień w raporcie albo możliwość napisania jednoznacznych AC.

| Miejsce | Numer pytania | Uzasadnienie |
|---|---|---|
| 1 | 1 | Zmienia sposób liczenia głównej wartości - bez odpowiedzi nie da się napisać AC dla podsumowania. |
| 2 | 2 | Zmienia, które zamówienia z granic okresu wchodzą do raportu (przypadki 1, 2 i 5). |
| 3 | 3 | Definiuje "wartość sprzedaży"; odbiorcy raportu rozumieją ją różnie (pkt 7). |
| 4 | 4 | Decyduje o zakresie: status bieżący vs. historia statusów (przebudowa modelu danych). |
| 5 | 7 | Bez reguł zakresu nie da się jednoznacznie opisać, kiedy raport zostaje odrzucony (pkt 6, przypadek 6). |

## Gotowość zespołu

- [x] Mamy co najmniej 10 pytań z opisanym wpływem
- [x] Wybraliśmy 5 pytań, które mogą zmienić zakres lub wynik
- [x] Nie pytamy o informacje, które dokument już podaje
- [x] Potrafimy rozpocząć refinement bez prezentowania gotowego rozwiązania

## Exit tickets

### Exit ticket numer 1

**1. Które pytanie może najbardziej zmienić zakres funkcji i dlaczego?**

Pytanie 4 (status bieżący czy z końca okresu): jeśli PO oczekuje statusów historycznych, trzeba by przechowywać historię zmian statusów, czyli przebudować model danych - coś, co BR w pkt 15 wyłącza z zakresu.

**2. Jakie założenie było najłatwiej pomylić z faktem?**

Że data końcowa jest włącznie do końca dnia - brzmi oczywiście, ale BR mówi tylko o "zwykłym rozumieniu zakresu dat", a created_at zawiera godzinę, więc to wymaga potwierdzenia.

### Exit ticket numer 2

**1. Które pytanie może najbardziej zmienić zakres funkcji i dlaczego?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

**2. Jakie założenie było najłatwiej pomylić z faktem?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

### Exit ticket numer 3

**1. Które pytanie może najbardziej zmienić zakres funkcji i dlaczego?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

**2. Jakie założenie było najłatwiej pomylić z faktem?**

Nie dotyczy - praca indywidualna (zespół jednoosobowy).

