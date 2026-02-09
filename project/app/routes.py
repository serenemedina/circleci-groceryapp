""""
Flask routes for the grocery list application.

Uses a Blueprint to organize routes and handles all CRUD operations
for grocery items.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import GroceryItem
from . import db

# Blueprint setup
main = Blueprint('main', __name__)

# Predefined grocery categories
CATEGORIES = [ "🥬 Produce", "🥛 Dairy","🥩 Meat", "🥖 Bakery","🥫 Pantry","🍪 Snacks","🥤 Drinks"]

# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------

@main.route('/')
def index():
    # Display the main grocery list page:
    # Retrieves all grocery items from the database
    # Orders them by category
    # Passes items and categories to the template
    items = GroceryItem.query.order_by(GroceryItem.category).all()
    return render_template('index.html', items=items, categories=CATEGORIES)

@main.route('/add', methods=['POST'])
def add_item():
    # Add a grocery item to the list:
    # If the item already exists in the same category, increment quantity
    # Otherwise, create a new item
    name = request.form.get('item_name')
    category = request.form.get('category')
    quantity = int(request.form.get('quantity', 1))  # default 1 if empty

    if name:
        # See if item already exists in that category
        existing = GroceryItem.query.filter_by(name=name, category=category).first()
        if existing:
            existing.quantity += quantity
            flash(f"Updated {existing.name} quantity to {existing.quantity} in {category}")
        else:
            item = GroceryItem(name=name, category=category, quantity=quantity)
            db.session.add(item)
            flash(f"Added {quantity} x {name} to {category}")

        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete-selected', methods=['POST'])
def delete_selected():
    # Get list of selected item IDs from the form
    item_ids = request.form.getlist('item_ids')

    if item_ids:
        # Query all items matching the selected IDs
        items_to_delete = GroceryItem.query.filter(GroceryItem.id.in_(item_ids)).all()

        # Delete each item and flash a message with quantity, name, and category
        for item in items_to_delete:
            flash(f"Deleted {item.quantity} x {item.name} from {item.category}")
            db.session.delete(item)

        db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/increment/<int:item_id>', methods=['POST'])
def increment_item(item_id):

    # Increase the quantity of a grocery item by 1
    item = GroceryItem.query.get_or_404(item_id)
    item.quantity += 1
    db.session.commit()
    flash(f"Added 1 x {item.name} to {item.category}")
    return redirect(url_for('main.index'))


@main.route('/decrement/<int:item_id>', methods=['POST'])
def decrement_item(item_id):
    
    #Decrease the quantity of a grocery item by 1
    # If quantity reaches 0, deletes the item

    item = GroceryItem.query.get_or_404(item_id)
    item.quantity -= 1

    if item.quantity <= 0:
        db.session.delete(item)
        db.session.commit()
        flash(f"Removed {item.name} from {item.category}")
    else:
        db.session.commit()
        flash(f"Removed 1 x {item.name} from {item.category}")

    return redirect(url_for('main.index'))




