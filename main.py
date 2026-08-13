"""Punkt wejścia do aplikacji OrderFlow."""

from customers import load_customers
from orders import display_order_list, load_orders


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

        print("Ta opcja nie jest jeszcze dostępna.\n")


if __name__ == "__main__":
    main()
