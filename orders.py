"""Podstawowe operacje na zamówieniach."""

from customers import get_customer_name
from products import format_price
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


def format_order_date(created_at):
    """Skraca datę ISO do formatu czytelnego w tabeli."""
    return created_at.replace("T", " ")[:16]


def format_order_summary(order, customer=None):
    """Buduje wiersz podsumowania zamówienia."""
    customer_name = get_customer_name(customer) if customer else order["customer_id"]
    return (
        f'{order["id"]:<10} {format_order_date(order["created_at"]):<17} '
        f'{customer_name:<25} {order["status"]:<12} '
        f'{format_price(order["total"]):>12}'
    )


def format_order_details(order, customer, products):
    """Buduje wielowierszowy widok zamówienia, klienta i produktów."""
    product_index = {product["id"]: product for product in products}
    lines = [
        f'Zamówienie: {order["id"]}',
        f'Data: {format_order_date(order["created_at"])}',
        f'Status: {order["status"]}',
        f'Płatność: {order["payment_method"]}',
        f'Dostawa: {order["delivery_method"]}',
        "",
        "Klient:",
        f'  {get_customer_name(customer)} ({customer["id"]})',
        f'  {customer["email"]}',
        "",
        "Produkty:",
    ]

    for item in order["items"]:
        product = product_index.get(item["product_id"])
        product_name = product["name"] if product else item["product_id"]
        item_total = item["quantity"] * item["unit_price"]
        lines.append(
            f'  {product_name:<30} {item["quantity"]:>3} x '
            f'{format_price(item["unit_price"]):>11} = {format_price(item_total):>11}'
        )

    lines.extend(["-" * 74, f'Wartość zamówienia: {format_price(order["total"])}'])
    return "\n".join(lines)


def display_order_list(orders, customers):
    """Wyświetla tabelę wszystkich zamówień."""
    customer_index = {customer["id"]: customer for customer in customers}
    print(f'{"ID":<10} {"DATA":<17} {"KLIENT":<25} {"STATUS":<12} {"WARTOŚĆ":>12}')
    print("-" * 82)
    for order in sort_orders_by_date(orders):
        customer = customer_index.get(order["customer_id"])
        print(format_order_summary(order, customer))


def display_order_details(order, customer, products):
    """Wyświetla pełne informacje o zamówieniu."""
    print(format_order_details(order, customer, products))
