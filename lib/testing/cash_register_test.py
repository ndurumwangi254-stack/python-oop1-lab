#!/usr/bin/env python3

from lib.cash_register import CashRegister

import io
import sys

class TestCashRegister:
    '''CashRegister in cash_register.py'''

    def test_has_discount_total_items_and_previous_transactions(self):
        '''has discount, total, items, and previous_transactions attributes initialized.'''
        register = CashRegister()
        assert hasattr(register, 'discount')
        assert hasattr(register, 'total')
        assert hasattr(register, 'items')
        assert hasattr(register, 'previous_transactions')
        assert register.discount == 0
        assert register.total == 0
        assert register.items == []
        assert register.previous_transactions == []

    def test_can_initialize_with_discount(self):
        '''can initialize with a discount.'''
        register = CashRegister(discount=20)
        assert register.discount == 20

    def test_can_add_item_with_quantity(self):
        '''can add items with price and quantity.'''
        register = CashRegister()
        register.add_item("eggs", 0.98, 2)
        assert len(register.items) == 2
        assert register.total == 1.96

    def test_can_add_multiple_items(self):
        '''can add multiple different items.'''
        register = CashRegister()
        register.add_item("eggs", 0.98, 2)
        register.add_item("bread", 1.50, 1)
        assert len(register.items) == 3
        assert register.total == 3.46

    def test_add_item_tracks_transactions(self):
        '''tracks transactions in previous_transactions.'''
        register = CashRegister()
        register.add_item("eggs", 0.98, 2)
        assert len(register.previous_transactions) == 1
        assert register.previous_transactions[0]['item'] == "eggs"
        assert register.previous_transactions[0]['quantity'] == 2

    def test_can_apply_discount(self):
        '''applies discount to total when apply_discount() is called.'''
        register = CashRegister(discount=20)
        register.add_item("eggs", 10, 1)
        register.apply_discount()
        assert register.total == 8.0

    def test_apply_discount_with_no_discount(self):
        '''prints "There is no discount to apply." when discount is 0.'''
        register = CashRegister()
        register.add_item("eggs", 10, 1)
        captured_out = io.StringIO()
        sys.stdout = captured_out
        register.apply_discount()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "There is no discount to apply.\n"
        assert register.total == 10

    def test_can_void_last_transaction(self):
        '''removes last transaction and updates total.'''
        register = CashRegister()
        register.add_item("eggs", 0.98, 2)
        register.add_item("bread", 1.50, 1)
        assert register.total == 3.46
        register.void_last_transaction()
        assert register.total == 1.96
        assert len(register.items) == 2
        assert len(register.previous_transactions) == 1

    def test_void_last_transaction_removes_correct_items(self):
        '''removes the correct items from items list when voiding.'''
        register = CashRegister()
        register.add_item("eggs", 0.98, 2)
        register.add_item("bread", 1.50, 3)
        register.void_last_transaction()
        assert register.items.count("eggs") == 2
        assert register.items.count("bread") == 0

    def test_void_with_no_transactions(self):
        '''prints "There are no previous transactions to void." when no transactions exist.'''
        register = CashRegister()
        captured_out = io.StringIO()
        sys.stdout = captured_out
        register.void_last_transaction()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "There are no previous transactions to void.\n"

    def test_add_item_default_quantity_is_one(self):
        '''defaults quantity to 1 if not provided.'''
        register = CashRegister()
        register.add_item("eggs", 0.98)
        assert len(register.items) == 1
        assert register.total == 0.98
