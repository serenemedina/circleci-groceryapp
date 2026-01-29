"""
Unit tests for the Grocery Flask application
"""

import pytest
from project.app import create_app, db
from project.app.models import GroceryItem

# Test that an item can be added and retrieved from the database
def test_add_grocery_item(client, app):
    with app.app_context():
        item = GroceryItem(name="Milk", quantity=2)
        db.session.add(item)
        db.session.commit()

        fetched = GroceryItem.query.filter_by(name="Milk").first()
        assert fetched is not None
        assert fetched.quantity == 2

# Test updating the quantity in the database
def test_update_grocery_item(app):
    with app.app_context():
        item = GroceryItem(name="Eggs", quantity=12)
        db.session.add(item)
        db.session.commit()

        # Update the quantity
        item.quantity = 24
        db.session.commit()

        fetched = GroceryItem.query.filter_by(name="Eggs").first()
        assert fetched.quantity == 24

 # Test deleting an item from the database
def test_delete_grocery_item(app):
    with app.app_context():
        item = GroceryItem(name="Bread", quantity=1)
        db.session.add(item)
        db.session.commit()

        db.session.delete(item)
        db.session.commit()

        fetched = GroceryItem.query.filter_by(name="Bread").first()
        assert fetched is None