"""Operacje na katalogu produktów."""

from storage import load_json


PRODUCTS_FILE = "products.json"


def load_products():
    """Wczytuje cały katalog produktów."""
    return load_json(PRODUCTS_FILE)


def find_product_by_id(products, product_id):
    """Zwraca produkt o podanym ID albo None."""
    normalized_id = product_id.strip().upper()
    for product in products:
        if product["id"] == normalized_id:
            return product
    return None


def get_available_products(products):
    """Zwraca produkty, które można dodać do nowego zamówienia."""
    return [product for product in products if product["available"]]


def format_price(value):
    """Formatuje kwotę w złotych."""
    return f"{value:.2f} zł"


def format_product(product):
    """Buduje pojedynczy wiersz katalogu produktów."""
    availability = "dostępny" if product["available"] else "niedostępny"
    return (
        f'{product["id"]:<8} {product["name"]:<30} '
        f'{product["category"]:<18} {format_price(product["price"]):>12}  '
        f'{availability}'
    )


def display_products(products, only_available=False):
    """Wyświetla katalog albo wyłącznie dostępne produkty."""
    records = get_available_products(products) if only_available else products
    for product in records:
        print(format_product(product))

