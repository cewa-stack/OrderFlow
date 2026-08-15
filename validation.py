"""Proste reguły walidacji danych wejściowych."""

import re


def require_text(value, field_name):
    """Zwraca tekst bez skrajnych spacji albo zgłasza błąd."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Pole {field_name} nie może być puste.")
    return value.strip()


def is_valid_identifier(value, prefix):
    """Sprawdza identyfikator, np. ORD-0001 albo CUS-001."""
    if not isinstance(value, str):
        return False
    pattern = rf"{re.escape(prefix)}-\d{{3,4}}"
    return re.fullmatch(pattern, value.strip().upper()) is not None


def parse_positive_integer(value, field_name="Wartość"):
    """Zamienia tekst na dodatnią liczbę całkowitą."""
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} musi być liczbą całkowitą.") from error

    if number <= 0:
        raise ValueError(f"{field_name} musi być większa od zera.")
    return number


def require_choice(value, allowed_values, field_name="Wartość"):
    """Normalizuje i sprawdza wartość z zamkniętej listy."""
    normalized_value = require_text(value, field_name).upper()
    if normalized_value not in allowed_values:
        allowed = ", ".join(allowed_values)
        raise ValueError(f"{field_name} musi mieć jedną z wartości: {allowed}.")
    return normalized_value


def is_valid_email(value):
    """Wykonuje podstawowe sprawdzenie formatu adresu e-mail."""
    if not isinstance(value, str):
        return False
    pattern = r"[^\s@]+@[^\s@]+\.[^\s@]+"
    return re.fullmatch(pattern, value.strip()) is not None


def validate_order_items(items):
    """Sprawdza podstawową strukturę pozycji zamówienia."""
    if not isinstance(items, list) or not items:
        raise ValueError("Zamówienie musi zawierać co najmniej jeden produkt.")

    required_keys = {"product_id", "quantity", "unit_price"}
    for item in items:
        if not isinstance(item, dict) or not required_keys.issubset(item):
            raise ValueError("Pozycja zamówienia ma niepoprawną strukturę.")
        if not is_valid_identifier(item["product_id"], "PRD"):
            raise ValueError("Pozycja zawiera niepoprawne ID produktu.")
        if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
            raise ValueError("Ilość produktu musi być dodatnią liczbą całkowitą.")
        if not isinstance(item["unit_price"], (int, float)) or item["unit_price"] < 0:
            raise ValueError("Cena jednostkowa nie może być ujemna.")

