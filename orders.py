"""Podstawowe operacje na zamówieniach."""

from customers import get_customer_name
from products import format_price
from storage import load_json, save_json
from time_utils import get_current_datetime
from validation import require_choice, validate_order_items


ORDERS_FILE = "orders.json"
KNOWN_ORDER_STATUSES = [
    "NEW",
    "PAID",
    "PROCESSING",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
]
MANAGEABLE_ORDER_STATUSES = ["NEW", "PAID", "PROCESSING", "SHIPPED", "DELIVERED"]
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


def build_order_item(product, quantity):
    """Buduje pozycję zamówienia na podstawie bieżącej ceny produktu."""
    return {
        "product_id": product["id"],
        "quantity": quantity,
        "unit_price": product["price"],
    }


def create_order(orders, customer_id, items, payment_method, delivery_method):
    """Tworzy kompletny rekord nowego zamówienia."""
    validate_order_items(items)
    payment_method = require_choice(payment_method, PAYMENT_METHODS, "Metoda płatności")
    delivery_method = require_choice(delivery_method, DELIVERY_METHODS, "Sposób dostawy")
    return {
        "id": get_next_order_id(orders),
        "customer_id": customer_id,
        "created_at": get_current_datetime().isoformat(timespec="seconds"),
        "status": "NEW",
        "payment_method": payment_method,
        "delivery_method": delivery_method,
        "items": items,
        "total": calculate_order_total(items),
    }


def add_order(orders, order):
    """Dodaje zamówienie do kolekcji i zapisuje dane."""
    orders.append(order)
    save_orders(orders)


def change_order_status(order, new_status):
    """Zmienia status na jedną z wartości obsługiwanych przez podstawowy proces."""
    normalized_status = require_choice(
        new_status,
        MANAGEABLE_ORDER_STATUSES,
        "Status zamówienia",
    )
    if order["status"] == "CANCELLED":
        raise ValueError("Statusu zamówienia anulowanego nie można zmienić.")

    order["status"] = normalized_status


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
    if not orders:
        print("Brak zamówień do wyświetlenia.")
        return

    customer_index = {customer["id"]: customer for customer in customers}
    print(f'{"ID":<10} {"DATA":<17} {"KLIENT":<25} {"STATUS":<12} {"WARTOŚĆ":>12}')
    print("-" * 82)
    for order in sort_orders_by_date(orders):
        customer = customer_index.get(order["customer_id"])
        print(format_order_summary(order, customer))


def display_order_details(order, customer, products):
    """Wyświetla pełne informacje o zamówieniu."""
    print(format_order_details(order, customer, products))


def build_order_report(orders):
    """Oblicza podstawowe zestawienie liczby i wartości zamówień."""
    status_counts = {status: 0 for status in KNOWN_ORDER_STATUSES}
    status_values = {status: 0.0 for status in KNOWN_ORDER_STATUSES}

    for order in orders:
        status = order["status"]
        if status not in status_counts:
            status_counts[status] = 0
            status_values[status] = 0.0
        status_counts[status] += 1
        status_values[status] += order["total"]

    return {
        "order_count": len(orders),
        "total_value": round(sum(order["total"] for order in orders), 2),
        "status_counts": status_counts,
        "status_values": status_values,
    }


def format_order_report(report):
    """Formatuje raport zamówień do wyświetlenia w konsoli."""
    lines = [
        f'Liczba zamówień: {report["order_count"]}',
        f'Łączna wartość: {format_price(report["total_value"])}',
        "",
        f'{"STATUS":<15} {"LICZBA":>8} {"WARTOŚĆ":>16}',
        "-" * 41,
    ]

    for status, count in report["status_counts"].items():
        value = report["status_values"][status]
        lines.append(f'{status:<15} {count:>8} {format_price(value):>16}')
    return "\n".join(lines)


def display_order_report(orders):
    """Wyświetla podstawowy raport zamówień."""
    print(format_order_report(build_order_report(orders)))
