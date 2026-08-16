import pytest

from validation import (
    is_valid_email,
    is_valid_identifier,
    parse_positive_integer,
    validate_order_items,
)


def test_accepts_valid_identifier():
    assert is_valid_identifier("ord-0042", "ORD") is True


def test_rejects_invalid_identifier():
    assert is_valid_identifier("42", "ORD") is False


def test_parses_positive_integer():
    assert parse_positive_integer("3", "Ilość") == 3


def test_rejects_zero_quantity():
    with pytest.raises(ValueError):
        parse_positive_integer("0", "Ilość")


def test_validates_order_items_and_email():
    items = [{"product_id": "PRD-001", "quantity": 1, "unit_price": 29.90}]

    validate_order_items(items)
    assert is_valid_email("anna@example.com") is True

