"""
Order module for the pizza ordering system.

This module defines the Order class that manages customer orders
containing one or more pizzas.
"""

from typing import List
try:
    from .pizza import Pizza
except ImportError:
    from pizza import Pizza


class Order:
    """
    A class representing a customer order containing pizzas.
    
    An order must contain at least one pizza and tracks the total cost
    and payment status.
    """
    
    def __init__(self):
        """
        Initialize an empty order.
        
        The order starts with an empty list of pizzas, zero cost,
        and unpaid status.
        """
        self.pizzas: List[Pizza] = []
        self.paid: bool = False
    
    def input_pizza(self, pizza: Pizza) -> None:
        """
        Add a pizza to the order.
        
        Args:
            pizza (Pizza): The pizza object to add to the order
            
        Raises:
            TypeError: If the input is not a Pizza object
        """
        if not isinstance(pizza, Pizza):
            raise TypeError("Only Pizza objects can be added to an order")
        
        self.pizzas.append(pizza)
    
    def order_paid(self) -> None:
        """
        Mark the order as paid.
        
        Updates the paid status to True.
        """
        self.paid = True
    
    def cost(self) -> float:
        """
        Calculate the total cost of the order.
        
        Returns:
            float: The sum of all pizza costs in the order
        """
        return sum(pizza.cost() for pizza in self.pizzas)
    
    def __str__(self) -> str:
        """
        Return a string representation of the complete order and cost.
        
        Returns:
            str: A formatted string describing the full order and total cost
        """
        if not self.pizzas:
            return "Order: No pizzas - $0.00"
        
        order_details = []
        order_details.append("Order:")
        
        for i, pizza in enumerate(self.pizzas, 1):
            order_details.append(f"  {i}. {pizza}")
        
        total_cost = self.cost()
        order_details.append(f"Total Cost: ${total_cost:.2f}")
        
        if self.paid:
            order_details.append("Status: Paid")
        else:
            order_details.append("Status: Unpaid")
        
        return "\n".join(order_details)
