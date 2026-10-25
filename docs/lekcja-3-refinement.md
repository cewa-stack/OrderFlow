# Lekcja 3 - Refinement z Product Ownerem

> Autor: Łukasz Szymankiewicz (34562), Grupa: INF 3-4 26_27Z, Data: 25.10.2026, Gałąź: `feature/order-reporting`

## Rejestr decyzji zespołu

**Product Owner:** Łukasz Szymankiewicz<br>
**Facylitator, Analityk, Sekretarz:** Łukasz Szymankiewicz

| Nr | Temat i pytanie | Odpowiedź PO | Potwierdzona reguła | Wpływ na zakres lub AC | Otwarte |
|---|---|---|---|---|---|
| 1 | Anulowane: czy CANCELLED wchodzą do łącznej wartości? | Nie są wliczane do wartości sprzedaży, ale raport ma pokazać, że powstały. | CANCELLED liczone w liczbie wszystkich zamówień i widoczne w podziale na statusy (liczba i wartość); wykluczone z wartości sprzedaży. | AC dla podsumowania: wartość sprzedaży bez CANCELLED; CANCELLED widoczne w podziale na statusy. | - |
| 2 | Granice okresu: czy data końcowa jest włącznie? | Tak, oba dni włącznie, cały dzień kalendarzowy. | Okres = od 00:00:00 dnia początkowego do 23:59:59 dnia końcowego; ta sama data = raport dzienny. | AC dla granic (przypadek 5) i raportu dziennego (przypadek 1). | Strefa czasu - otwarte kwestie. |
| 3 | Wartość sprzedaży: które statusy? | Wszystkie poza CANCELLED. NEW też się liczy, bo to złożone zamówienie; jedynym wyjątkiem jest anulowanie. | Wartość sprzedaży = suma total zamówień o statusach NEW, PAID, PROCESSING, SHIPPED, DELIVERED. | Definicja głównej liczby raportu i jej etykieta ("Wartość sprzedaży"). | - |
| 4 | Status w raporcie: bieżący czy z końca okresu? | Bieżący; historia statusów nie jest potrzebna w tej zmianie. | Podział na statusy według bieżącego statusu zamówienia w chwili raportowania, bez historii zmian. | Historia statusów i raport statusu na wskazany dzień poza zakresem; AC: wynik powtarzalny przy niezmienionych danych. | - |
| 5 | Niespójne dane: przerwać raport czy pominąć rekord? | Nie pokazywać wyniku, który tylko wygląda na poprawny. | Rekord z brakującą/niepoprawną datą, statusem lub wartością w danych -> raport nie powstaje, bez częściowego wyniku; komunikat wskazuje ID zamówienia. | AC dla danych niespójnych (pkt 11); aplikacja nie może się zamknąć. | - |
| 6 | Format daty i skróty okresów? | RRRR-MM-DD wystarczy; bez skrótów w tej zmianie. | Dwie wymagane daty kalendarzowe RRRR-MM-DD; brak daty, zły format, nieistniejąca data lub koniec przed początkiem -> komunikat z przykładem poprawnej wartości, brak raportu. Bez dodatkowych limitów długości okresu. | AC dla walidacji (przypadek 6); skróty okresów poza zakresem. | - |
| 7 | Obecny raport: zastąpić czy zostawić? | Zostawić bez zmian, raport okresowy jako osobna operacja. | Opcja "Raport zamówień" działa jak dotąd; raport okresowy to nowa, osobna operacja w menu. | AC regresji dla istniejących funkcji (pkt 12). | - |
| 8 | Pusty okres: jak pokazać wynik? | To nie błąd, użytkownik ma dostać jasną informację. | Poprawny zakres bez zamówień -> czytelny wynik: 0 zamówień, wartość sprzedaży 0.00 zł, wszystkie statusy z zerem i informacja, że w okresie nie ma zamówień. | AC dla przypadku 3. | - |
| 9 | Podział na statusy: wszystkie czy tylko występujące? | Wszystkie znane statusy, także z wynikiem zero. | Raport zawsze pokazuje 6 statusów (NEW, PAID, PROCESSING, SHIPPED, DELIVERED, CANCELLED) z liczbą i wartością, także gdy wynik to 0. | Stały układ wyniku; AC dla podziału na statusy. | - |

## Kontrola jakości zapisu

- [x] Każda ważna odpowiedź została sparafrazowana
- [x] PO potwierdził albo skorygował regułę
- [x] Zapisałem wpływ decyzji na zakres lub przyszłe AC
- [x] Każda niewiadoma ma właściciela i następny krok

## Podsumowanie zakresu

### W zakresie

- Osobny raport okresowy uruchamiany z aplikacji konsolowej (nowa operacja w menu).
- Dwie wymagane daty kalendarzowe w formacie RRRR-MM-DD.
- Obustronnie domknięty zakres oparty na created_at (od 00:00:00 pierwszego dnia do 23:59:59 ostatniego).
- Liczba wszystkich zamówień oraz wartość sprzedaży bez CANCELLED.
- Liczba i wartość dla wszystkich znanych statusów, także z wynikiem zero.
- Bieżący status zamówienia w chwili raportowania.
- Czytelny wynik dla pustego okresu.
- Odrzucenie błędnego zakresu i niespójnych danych bez częściowego raportu.
- Zachowanie dotychczasowego raportu wszystkich zamówień; raport nie modyfikuje danych.

### Poza zakresem

- Panel graficzny, wykresy, dashboard i porównanie wielu okresów.
- Eksport do CSV, PDF albo automatyczna wysyłka.
- Integracje z BI, księgowością i operatorem płatności.
- Historia zmian statusu oraz raport statusu na wskazany dzień.
- Przebudowa modelu danych, ról i uprawnień.
- Prognozowanie sprzedaży i nowe miary analityczne.

## Otwarte kwestie

| Kwestia | Dlaczego blokuje | Właściciel | Termin lub następny krok |
|---|---|---|---|
| Strefa czasu dla created_at (zapis bez strefy, czas lokalny komputera). | Może przesunąć zamówienia z okolic północy między dniami. | Zespół techniczny | Ustalić przed AC dla granic okresu (lekcja 4) |
| Sposób parsowania dat i rodzaje wyjątków. | Potrzebne do testów walidacji zakresu. | Zespół techniczny | Decyzja przy implementacji, po lekcji 4 |
| Układ wyniku w konsoli, numer opcji menu i format kwot. | Wpływa na czytelność wyniku na odprawach (pkt 10). | Zespół techniczny | Projekt przy implementacji; obecny format kwot zostaje |
| Struktura i liczba testów (dane testowe niezależne od data/orders.json). | Bez tego testy raportu mogą zależeć od danych demo. | Zespół techniczny | Ustalić razem z AC na lekcji 4 |

## Potwierdzenie PO

- [x] Potwierdzam sens biznesowy podsumowania
- [ ] Wymagana korekta przed lekcją 4

Korekta: Brak korekty.

## Materiał wejściowy do User Story i Acceptance Criteria (lekcja 4)

- Rola: kierownik operacyjny / pracownik obsługi zamówień.
- Potrzeba: podsumowanie zamówień dla wskazanego okresu bez ręcznych obliczeń.
- Reguły do AC: reguły 1-9 z rejestru decyzji.
- Przypadki do AC: 1 (dzień), 2 (kampania śr-wt), 3 (brak zamówień), 4 (anulowane), 5 (granice), 6 (zły zakres), 7 (miesiąc).
- Przykład kontrolny z danych demo: maj 2026 (od 2026-05-01 do 2026-05-31) -> 12 zamówień, w tym 1 anulowane (ORD-0006, 388.00 zł); wartość sprzedaży 6114.50 zł; wartość wszystkich 6502.50 zł.

## Exit tickets

### Exit ticket numer 1

**1. Która odpowiedź Product Ownera najbardziej zmieniła moje początkowe założenie i dlaczego?**

Odpowiedź o CANCELLED: zakładałem jedną "łączną wartość" jak w obecnym raporcie, a główną wartością jest wartość sprzedaży bez anulowanych; anulowane widać tylko w podziale na statusy, co zmienia sposób liczenia wyniku.

**2. Która reguła nadal wymaga doprecyzowania przed napisaniem Acceptance Criteria?**

Strefa czasu dla created_at i sposób parsowania dat - to decyzje zespołu technicznego, ale bez nich AC dla granic dnia nie będą w pełni jednoznaczne.

