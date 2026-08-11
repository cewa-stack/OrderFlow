"""Pomocnicze operacje odczytu i zapisu danych JSON."""

import json
from pathlib import Path


PROJECT_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = PROJECT_DIRECTORY / "data"


def get_data_path(file_name):
    """Zwraca pełną ścieżkę pliku znajdującego się w katalogu data."""
    return DATA_DIRECTORY / file_name


def load_json(file_name):
    """Wczytuje listę rekordów z pliku JSON.

    Błędy techniczne są zamieniane na komunikaty zrozumiałe dla użytkownika
    aplikacji, a szczegóły pierwotnego wyjątku pozostają dostępne w tracebacku.
    """
    path = get_data_path(file_name)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise RuntimeError(f"Nie znaleziono pliku danych: {path}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Plik {path.name} zawiera niepoprawny JSON.") from error
    except OSError as error:
        raise RuntimeError(f"Nie można odczytać pliku {path.name}.") from error

    if not isinstance(data, list):
        raise RuntimeError(f"Plik {path.name} powinien zawierać listę rekordów.")

    return data


def save_json(file_name, records):
    """Zapisuje listę rekordów do pliku JSON w bezpieczny sposób."""
    path = get_data_path(file_name)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
            file.write("\n")
        temporary_path.replace(path)
    except OSError as error:
        raise RuntimeError(f"Nie można zapisać pliku {path.name}.") from error


def data_file_exists(file_name):
    """Sprawdza, czy wskazany plik danych istnieje."""
    return get_data_path(file_name).is_file()

