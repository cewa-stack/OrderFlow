# Dokumentacja sprintu — rozszerzone raportowanie zamówień

> Autor: Łukasz Szymankiewicz (34562) · Grupa: INF 3-4 26_27Z · Data: 25.10.2026 · Gałąź: `feature/order-reporting`

Dokumentacja laboratorium *Inżynieria programowania* (OrderFlow Sprint Workshop, lekcje 1–3).
Zgodnie z instrukcją zajęć na tym etapie **kod aplikacji nie jest zmieniany** — powstaje analiza
systemu, analiza wymagania biznesowego i wynik refinementu, które są wejściem do User Story
i Acceptance Criteria.

| Lekcja | Temat | Plik |
|---|---|---|
| 1 | Analiza istniejącego systemu | [lekcja-1-analiza-systemu.md](lekcja-1-analiza-systemu.md) |
| 2 | Analiza wymagania biznesowego | [lekcja-2-analiza-wymagania.md](lekcja-2-analiza-wymagania.md) |
| 3 | Refinement z Product Ownerem | [lekcja-3-refinement.md](lekcja-3-refinement.md) |

## Punkt startowy

```bash
git switch -c feature/order-reporting v1.0-student-base
python -m pytest        # 9 passed
python main.py
```

## Najważniejsze ustalenia

- Raport liczy `orders.build_order_report()` zawsze na pełnej liście zamówień — brak filtra po dacie.
- Raport okresowy wybiera zamówienia po `created_at`; oba dni zakresu włącznie (do potwierdzenia przez PO).
- `CANCELLED` nie wchodzą do wartości sprzedaży, ale są pokazane osobno (do potwierdzenia przez PO).
- System nie przechowuje historii statusów — raport pokazuje status bieżący.
