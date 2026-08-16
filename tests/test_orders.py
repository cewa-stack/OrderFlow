from orders import calculate_order_total, find_order_by_id, get_next_order_id, load_orders


def test_finds_existing_order():
    orders = load_orders()

    order = find_order_by_id(orders, "ORD-0001")

    assert order is not None
    assert order["customer_id"] == "CUS-001"


def test_returns_none_for_unknown_order():
    orders = load_orders()

    order = find_order_by_id(orders, "ORD-9999")

    assert order is None


def test_calculates_total_from_items():
    items = [
        {"product_id": "PRD-001", "quantity": 2, "unit_price": 10.50},
        {"product_id": "PRD-002", "quantity": 1, "unit_price": 5.25},
    ]

    assert calculate_order_total(items) == 26.25


def test_generates_next_order_id():
    orders = [{"id": "ORD-0003"}, {"id": "ORD-0011"}]

    assert get_next_order_id(orders) == "ORD-0012"

