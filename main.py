"""Punkt wejścia do aplikacji OrderFlow."""

from customers import find_customer_by_id, load_customers
from orders import (
    display_order_details,
    display_order_list,
    find_order_by_id,
    load_orders,
)
from products import load_products


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


def main():
    while True:
        show_menu()
        choice = input("Wybierz opcję: ").strip()

        if choice == "0":
            print("Do zobaczenia.")
            break

        if choice == "1":
            handle_order_list()
            continue

        if choice == "2":
            handle_order_search()
            continue

        print("Ta opcja nie jest jeszcze dostępna.\n")


if __name__ == "__main__":
    main()
