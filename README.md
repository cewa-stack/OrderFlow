# OrderFlow

OrderFlow to konsolowy system obsługi zamówień sklepu internetowego. Aplikacja
pozwala pracownikowi przeglądać zamówienia i ich szczegóły, wyszukiwać rekordy,
tworzyć zamówienia, aktualizować ich bieżący status oraz wyświetlać podstawowy
raport operacyjny. Dane klientów, produktów i zamówień są przechowywane w
lokalnych plikach JSON.

## Wymagania

- Python 3.10 lub nowszy,
- `pip`,
- terminal obsługujący UTF-8.

Projekt nie wymaga serwera aplikacji ani zewnętrznej bazy danych.

## Instalacja

Po sklonowaniu repozytorium utwórz wirtualne środowisko i zainstaluj zależności.

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Linux lub macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Jedyną zależnością deweloperską projektu jest `pytest`.

## Uruchomienie aplikacji

W aktywnym środowisku wirtualnym wykonaj w katalogu głównym projektu:

```bash
python main.py
```

Menu prowadzi przez dostępne operacje. Identyfikatory mają format `ORD-0001`,
`CUS-001` oraz `PRD-001`. Nowe zamówienie otrzymuje status `NEW`, a jego ceny
jednostkowe są kopiowane z bieżącego katalogu produktów.

## Uruchamianie testów

Pełny zestaw testów uruchom poleceniem:

```bash
python -m pytest
```

Konfiguracja w `pytest.ini` automatycznie wskazuje katalog `tests`.

## Struktura projektu

```text
OrderFlow/
├── main.py                 # menu i obsługa interakcji w konsoli
├── orders.py               # logika zamówień i raport
├── customers.py            # odczyt i prezentacja klientów
├── products.py             # katalog produktów
├── storage.py              # wspólny odczyt i zapis plików JSON
├── validation.py           # podstawowe reguły walidacji
├── time_utils.py           # wspólny mechanizm pobierania czasu
├── data/
│   ├── orders.json
│   ├── customers.json
│   └── products.json
├── tests/
│   ├── test_orders.py
│   └── test_validation.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Dokumentacja sprintu

Analiza systemu, analiza wymagania biznesowego "Rozszerzone raportowanie
zamówień" oraz wynik refinementu z Product Ownerem znajdują się w katalogu
[`docs/`](docs/README.md). Wypełnione pakiety zajęć (.docx) są w
[`docs/pakiety/`](docs/pakiety/).

## Moduły i dane

`main.py` jest punktem wejścia i odpowiada wyłącznie za przebieg operacji
konsolowych. Funkcje biznesowe znajdują się w modułach domenowych. `storage.py`
ustala ścieżki względem katalogu projektu, dzięki czemu aplikację można uruchomić
również spoza jego katalogu roboczego, oraz zapisuje dane przez plik tymczasowy.

Pliki w katalogu `data` zawierają deterministyczny zestaw demonstracyjny.
Zamówienie przechowuje cenę jednostkową każdej pozycji, dlatego późniejsza
zmiana ceny katalogowej nie modyfikuje wartości już istniejących zamówień.
