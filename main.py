"""Punkt wejścia do aplikacji OrderFlow."""

from customers import find_customer_by_id, get_customer_name, load_customers
from orders import (
    DELIVERY_METHODS,
    MANAGEABLE_ORDER_STATUSES,
    PAYMENT_METHODS,
    add_order,
    build_order_item,
    change_order_status,
    create_order,
    display_order_details,
    display_order_list,
    find_order_by_id,
    load_orders,
    save_orders,
)
from products import (
    display_products,
    find_product_by_id,
    format_price,
    get_available_products,
    load_products,
)
from validation import is_valid_identifier, parse_positive_integer


def show_menu():
    print("=" * 40)
    print("              ORDERFLOW")
    print("       Order Management System")
    print("=" * 40)
    print("1. Lista zamówień")
    print("2. Wyszukaj zamówienie")
    print("3. Utwórz zamówienie")
    print("4. Zmień status zamówienia")
    print("5. Raport zamówień")
    print("0. Zakończ")


def handle_order_list():
    """Obsługuje wyświetlanie listy zamówień."""
    print("\nLISTA ZAMÓWIEŃ")
    print("=" * 82)
    display_order_list(load_orders(), load_customers())
    print()


def handle_order_search():
    """Obsługuje wyszukiwanie i wyświetlanie szczegółów zamówienia."""
    order_id = input("Podaj ID zamówienia: ").strip()
    if not is_valid_identifier(order_id, "ORD"):
        print("ID zamówienia powinno mieć format ORD-0001.\n")
        return

    order = find_order_by_id(load_orders(), order_id)

    if order is None:
        print(f"Nie znaleziono zamówienia o ID {order_id.upper()}.\n")
        return

    customers = load_customers()
    customer = find_customer_by_id(customers, order["customer_id"])
    if customer is None:
        print("Zamówienie odwołuje się do nieistniejącego klienta.\n")
        return

    print("\nSZCZEGÓŁY ZAMÓWIENIA")
    print("=" * 74)
    display_order_details(order, customer, load_products())
    print()


def choose_from_list(label, values):
    """Pozwala wybrać jedną wartość z krótkiej listy."""
    print(f"\n{label}:")
    for number, value in enumerate(values, start=1):
        print(f"{number}. {value}")

    while True:
        value = input("Wybierz numer (Enter, aby przerwać): ").strip()
        if not value:
            return None
        try:
            selected_number = parse_positive_integer(value, "Numer opcji")
        except ValueError as error:
            print(error)
            continue
        if selected_number > len(values):
            print(f"Wybierz numer od 1 do {len(values)}.")
            continue
        return values[selected_number - 1]


def collect_order_items(products):
    """Pobiera od użytkownika produkty nowego zamówienia."""
    items = []
    print("\nDOSTĘPNE PRODUKTY")
    print("-" * 90)
    display_products(products, only_available=True)
    print("\nWpisz ID produktu. Pusta wartość kończy dodawanie.")

    while True:
        product_id = input("ID produktu: ").strip()
        if not product_id:
            return items

        if not is_valid_identifier(product_id, "PRD"):
            print("ID produktu powinno mieć format PRD-001.")
            continue

        product = find_product_by_id(products, product_id)
        if product is None or not product["available"]:
            print("Produkt nie istnieje albo jest niedostępny.")
            continue

        try:
            quantity = parse_positive_integer(input("Ilość: "), "Ilość")
        except ValueError as error:
            print(error)
            continue

        existing_item = next(
            (item for item in items if item["product_id"] == product["id"]),
            None,
        )
        if existing_item:
            existing_item["quantity"] += quantity
        else:
            items.append(build_order_item(product, quantity))
        print(f'Dodano: {product["name"]} x {quantity}')


def handle_order_creation():
    """Obsługuje utworzenie i zapis nowego zamówienia."""
    customers = load_customers()
    products = load_products()
    orders = load_orders()

    print("\nNOWE ZAMÓWIENIE")
    print("=" * 70)
    for customer in customers:
        print(f'{customer["id"]:<9} {get_customer_name(customer):<25} {customer["email"]}')

    customer_id = input("\nPodaj ID klienta: ").strip()
    if not is_valid_identifier(customer_id, "CUS"):
        print("ID klienta powinno mieć format CUS-001.\n")
        return

    customer = find_customer_by_id(customers, customer_id)
    if customer is None:
        print("Nie znaleziono klienta.\n")
        return

    available_products = get_available_products(products)
    items = collect_order_items(available_products)
    if not items:
        print("Zamówienie musi zawierać co najmniej jeden produkt.\n")
        return

    payment_method = choose_from_list("Metoda płatności", PAYMENT_METHODS)
    if payment_method is None:
        print("Niepoprawna metoda płatności.\n")
        return

    delivery_method = choose_from_list("Sposób dostawy", DELIVERY_METHODS)
    if delivery_method is None:
        print("Niepoprawny sposób dostawy.\n")
        return

    order = create_order(
        orders,
        customer["id"],
        items,
        payment_method,
        delivery_method,
    )
    add_order(orders, order)
    print(f'\nUtworzono zamówienie {order["id"]} o wartości {format_price(order["total"])}.\n')


def handle_status_change():
    """Obsługuje podstawową zmianę statusu zamówienia."""
    order_id = input("Podaj ID zamówienia: ").strip()
    if not is_valid_identifier(order_id, "ORD"):
        print("ID zamówienia powinno mieć format ORD-0001.\n")
        return

    orders = load_orders()
    order = find_order_by_id(orders, order_id)

    if order is None:
        print("Nie znaleziono zamówienia.\n")
        return

    print(f'Aktualny status: {order["status"]}')
    new_status = choose_from_list("Nowy status", MANAGEABLE_ORDER_STATUSES)
    if new_status is None:
        print("Niepoprawny wybór statusu.\n")
        return

    try:
        change_order_status(order, new_status)
    except ValueError as error:
        print(f"{error}\n")
        return

    save_orders(orders)
    print(f'Status zamówienia {order["id"]} zmieniono na {new_status}.\n')


def main():
    actions = {
        "1": handle_order_list,
        "2": handle_order_search,
        "3": handle_order_creation,
        "4": handle_status_change,
    }

    while True:
        show_menu()
        choice = input("Wybierz opcję: ").strip()

        if choice == "0":
            print("Do zobaczenia.")
            break

        action = actions.get(choice)
        if action is None:
            print("Wybierz jedną z dostępnych opcji.\n")
            continue

        try:
            action()
        except RuntimeError as error:
            print(f"Błąd danych: {error}\n")


if __name__ == "__main__":
    main()
