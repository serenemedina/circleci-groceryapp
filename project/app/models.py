"""
Database models for the grocery list application.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class GroceryItem(db.Model):
    # Represents a grocery item in the database
    __tablename__ = "grocery_item"
    
    id = db.Column(db.Integer, primary_key=True) #primary key
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False, default="Other")  

    #  Return a string of representation of the GroceryItem, i.e. "milk (dairy)"
    def __repr__(self):
        return f'{self.name} ({self.category})'
