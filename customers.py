"""Operacje na danych klientów."""

from storage import load_json


CUSTOMERS_FILE = "customers.json"


def load_customers():
    """Wczytuje wszystkich klientów."""
    return load_json(CUSTOMERS_FILE)


def find_customer_by_id(customers, customer_id):
    """Zwraca klienta o podanym ID albo None."""
    normalized_id = customer_id.strip().upper()
    for customer in customers:
        if customer["id"] == normalized_id:
            return customer
    return None


def get_customer_name(customer):
    """Buduje imię i nazwisko klienta do prezentacji."""
    return f'{customer["first_name"]} {customer["last_name"]}'


def format_customer(customer):
    """Zwraca czytelny opis podstawowych danych klienta."""
    return (
        f'ID: {customer["id"]}\n'
        f'Klient: {get_customer_name(customer)}\n'
        f'E-mail: {customer["email"]}'
    )


def display_customer(customer):
    """Wyświetla podstawowe dane klienta."""
    print(format_customer(customer))

