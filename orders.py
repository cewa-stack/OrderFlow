"""Podstawowe operacje na zamówieniach."""

from storage import load_json, save_json


ORDERS_FILE = "orders.json"
KNOWN_ORDER_STATUSES = [
    "NEW",
    "PAID",
    "PROCESSING",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
]
PAYMENT_METHODS = ["CARD", "TRANSFER", "CASH_ON_DELIVERY"]
DELIVERY_METHODS = ["COURIER", "PARCEL_LOCKER", "PICKUP_POINT", "STORE_PICKUP"]


def load_orders():
    """Wczytuje wszystkie zamówienia."""
    return load_json(ORDERS_FILE)


def save_orders(orders):
    """Zapisuje wszystkie zamówienia."""
    save_json(ORDERS_FILE, orders)


def find_order_by_id(orders, order_id):
    """Zwraca zamówienie o podanym ID albo None."""
    normalized_id = order_id.strip().upper()
    for order in orders:
        if order["id"] == normalized_id:
            return order
    return None


def calculate_order_total(items):
    """Oblicza łączną wartość pozycji zamówienia."""
    total = sum(item["quantity"] * item["unit_price"] for item in items)
    return round(total, 2)


def get_next_order_id(orders):
    """Wyznacza kolejny identyfikator w formacie ORD-0001."""
    numbers = []
    for order in orders:
        try:
            numbers.append(int(order["id"].split("-")[1]))
        except (KeyError, IndexError, ValueError):
            continue

    next_number = max(numbers, default=0) + 1
    return f"ORD-{next_number:04d}"


def sort_orders_by_date(orders, descending=True):
    """Zwraca zamówienia posortowane według daty utworzenia."""
    return sorted(orders, key=lambda order: order["created_at"], reverse=descending)

