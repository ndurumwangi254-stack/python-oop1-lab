#!/usr/bin/env python3

class CashRegister:
    def __init__(self, discount=0):
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    def add_item(self, item, price, quantity=1):
        """Add an item to the register and update total."""
        for _ in range(quantity):
            self.items.append(item)
        item_total = price * quantity
        self.total += item_total
        # Store transaction for potential void
        self.previous_transactions.append({
            'item': item,
            'price': price,
            'quantity': quantity,
            'subtotal': item_total
        })

    def apply_discount(self):
        """Apply the discount to the total."""
        if self.discount == 0:
            print("There is no discount to apply.")
            return self.total
        self.total = self.total - (self.total * self.discount / 100)
        return self.total

    def void_last_transaction(self):
        """Remove the last transaction and adjust total."""
        if not self.previous_transactions:
            print("There are no previous transactions to void.")
            return
        
        last_transaction = self.previous_transactions.pop()
        self.total -= last_transaction['subtotal']
        
        # Remove items from items list
        for _ in range(last_transaction['quantity']):
            self.items.remove(last_transaction['item'])
