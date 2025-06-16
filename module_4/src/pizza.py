"""
Pizza module for the pizza ordering system.

This module defines the Pizza class that represents a customizable pizza
with various crust, sauce, cheese, and topping options.
"""

from typing import List


class Pizza:
    """
    A class representing a pizza with customizable options.
    
    The pizza pricing structure:
    - Crust: Thin ($5), Thick ($3), Gluten-free ($7)
    - Sauce: Marinara ($2), Pesto ($3), Liv Sauce ($5)
    - Cheese: Mozzarella ($1)
    - Toppings: Pepperoni ($2), Mushrooms ($3), Pineapple ($1)
    
    Each pizza must have exactly one crust, at least one sauce, 
    cheese (only Mozzarella), and at least one topping.
    """
    
    # Pricing constants
    CRUST_PRICES = {
        'thin': 5,
        'thick': 3,
        'gluten_free': 7
    }
    
    SAUCE_PRICES = {
        'marinara': 2,
        'pesto': 3,
        'liv_sauce': 5
    }
    
    CHEESE_PRICES = {
        'mozzarella': 1
    }
    
    TOPPING_PRICES = {
        'pepperoni': 2,
        'mushrooms': 3,
        'pineapple': 1
    }
    
    def __init__(self, crust: str, sauce: List[str], cheese: str, toppings: List[str]):
        """
        Initialize a pizza with specified ingredients.
        
        Args:
            crust (str): The crust type (thin, thick, or gluten_free)
            sauce (List[str]): List of sauces (at least one required)
            cheese (str): The cheese type (only mozzarella supported)
            toppings (List[str]): List of toppings (at least one required)
            
        Raises:
            ValueError: If invalid ingredients are provided or requirements not met
        """
        # Validate crust
        if crust not in self.CRUST_PRICES:
            raise ValueError(f"Invalid crust type: {crust}")
        
        # Validate sauce (at least one required)
        if not sauce or not isinstance(sauce, list):
            raise ValueError("At least one sauce is required")
        
        for s in sauce:
            if s not in self.SAUCE_PRICES:
                raise ValueError(f"Invalid sauce type: {s}")
        
        # Validate cheese (only mozzarella supported)
        if cheese not in self.CHEESE_PRICES:
            raise ValueError(f"Invalid cheese type: {cheese}")
        
        # Validate toppings (at least one required)
        if not toppings or not isinstance(toppings, list):
            raise ValueError("At least one topping is required")
        
        for t in toppings:
            if t not in self.TOPPING_PRICES:
                raise ValueError(f"Invalid topping type: {t}")
        
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings
    
    def cost(self) -> float:
        """
        Calculate the total cost of the pizza.
        
        Returns:
            float: The total cost of the pizza
        """
        total = 0.0
        
        # Add crust cost
        total += self.CRUST_PRICES[self.crust]
        
        # Add sauce costs
        for s in self.sauce:
            total += self.SAUCE_PRICES[s]
        
        # Add cheese cost
        total += self.CHEESE_PRICES[self.cheese]
        
        # Add topping costs
        for t in self.toppings:
            total += self.TOPPING_PRICES[t]
        
        return total
    
    def __str__(self) -> str:
        """
        Return a string representation of the pizza and its cost.
        
        Returns:
            str: A formatted string describing the pizza and cost
        """
        sauce_str = ", ".join(self.sauce)
        toppings_str = ", ".join(self.toppings)
        
        return (f"Pizza: {self.crust.replace('_', ' ').title()} crust, "
                f"{sauce_str.replace('_', ' ').title()} sauce, "
                f"{self.cheese.title()} cheese, "
                f"with {toppings_str.replace('_', ' ').title()} - "
                f"${self.cost():.2f}")
