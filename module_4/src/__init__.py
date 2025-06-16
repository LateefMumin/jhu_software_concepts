"""
Pizza Ordering System

A comprehensive pizza ordering application that allows customers to create
orders with customizable pizzas and manage the ordering process.
"""

__version__ = "1.0.0"
__author__ = "JHU EP 605.256 - Advanced Python"

from .pizza import Pizza
from .order import Order

__all__ = ['Pizza', 'Order']
