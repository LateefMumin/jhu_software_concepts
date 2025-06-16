"""
Unit tests for the Pizza class.

This module contains comprehensive unit tests for the Pizza class
functionality including initialization, string representation,
and cost calculation.
"""

import pytest
from src.pizza import Pizza


@pytest.mark.pizza
class TestPizza:
    """Test cases for the Pizza class."""
    
    def test_pizza_init_valid(self):
        """
        Test pizza __init__() method with valid inputs.
        
        - Test return an initialized pizza
        - Test pizza should have crust (str), sauce (list of str), cheese (str), toppings (list of str)
        - Test pizza should return a non-zero cost
        """
        pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        
        assert isinstance(pizza.crust, str)
        assert pizza.crust == 'thin'
        
        assert isinstance(pizza.sauce, list)
        assert all(isinstance(s, str) for s in pizza.sauce)
        assert pizza.sauce == ['marinara']
        
        assert isinstance(pizza.cheese, str)
        assert pizza.cheese == 'mozzarella'
        
        assert isinstance(pizza.toppings, list)
        assert all(isinstance(t, str) for t in pizza.toppings)
        assert pizza.toppings == ['pineapple']
        
        assert pizza.cost() > 0
    
    def test_pizza_init_multiple_sauces_toppings(self):
        """
        Test pizza initialization with multiple sauces and toppings.
        """
        pizza = Pizza('thick', ['marinara', 'pesto'], 'mozzarella', ['pepperoni', 'mushrooms'])
        
        assert pizza.sauce == ['marinara', 'pesto']
        assert pizza.toppings == ['pepperoni', 'mushrooms']
    
    def test_pizza_init_invalid_crust(self):
        """
        Test pizza initialization with invalid crust.
        """
        with pytest.raises(ValueError, match="Invalid crust type"):
            Pizza('invalid_crust', ['marinara'], 'mozzarella', ['pineapple'])
    
    def test_pizza_init_invalid_sauce(self):
        """
        Test pizza initialization with invalid sauce.
        """
        with pytest.raises(ValueError, match="Invalid sauce type"):
            Pizza('thin', ['invalid_sauce'], 'mozzarella', ['pineapple'])
    
    def test_pizza_init_empty_sauce(self):
        """
        Test pizza initialization with empty sauce list.
        """
        with pytest.raises(ValueError, match="At least one sauce is required"):
            Pizza('thin', [], 'mozzarella', ['pineapple'])
    
    def test_pizza_init_invalid_cheese(self):
        """
        Test pizza initialization with invalid cheese.
        """
        with pytest.raises(ValueError, match="Invalid cheese type"):
            Pizza('thin', ['marinara'], 'invalid_cheese', ['pineapple'])
    
    def test_pizza_init_invalid_topping(self):
        """
        Test pizza initialization with invalid topping.
        """
        with pytest.raises(ValueError, match="Invalid topping type"):
            Pizza('thin', ['marinara'], 'mozzarella', ['invalid_topping'])
    
    def test_pizza_init_empty_toppings(self):
        """
        Test pizza initialization with empty toppings list.
        """
        with pytest.raises(ValueError, match="At least one topping is required"):
            Pizza('thin', ['marinara'], 'mozzarella', [])
    
    def test_pizza_str(self):
        """
        Test pizza __str__() method.
        
        Test pizza should return a string containing the pizza and cost.
        """
        pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        result = str(pizza)
        
        assert "Pizza:" in result
        assert "Thin" in result
        assert "Marinara" in result
        assert "Mozzarella" in result
        assert "Pineapple" in result
        assert "$" in result
        assert str(pizza.cost()) in result or f"{pizza.cost():.2f}" in result
    
    def test_pizza_cost_simple(self):
        """
        Test pizza cost() method with simple pizza.
        
        Test return of correct cost for an input pizza.
        E.g. a Thin Crust, Marinara, Mozzarella pizza with Pineapple will cost: $5 + $2 + $1 + $1 = $9
        """
        pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        expected_cost = 5 + 2 + 1 + 1  # thin + marinara + mozzarella + pineapple
        
        assert pizza.cost() == expected_cost
    
    def test_pizza_cost_complex(self):
        """
        Test pizza cost() method with complex pizza.
        
        E.g. a Thin Crust, Marinara, Liv Sauce, Mozzarella pizza with Pepperoni and Mushrooms will cost:
        $5 + $2 + $5 + $1 + $2 + $3 = $18
        """
        pizza = Pizza('thin', ['marinara', 'liv_sauce'], 'mozzarella', ['pepperoni', 'mushrooms'])
        expected_cost = 5 + 2 + 5 + 1 + 2 + 3  # thin + marinara + liv_sauce + mozzarella + pepperoni + mushrooms
        
        assert pizza.cost() == expected_cost
    
    def test_pizza_cost_all_crusts(self):
        """
        Test pizza cost calculation for different crust types.
        """
        base_cost = 2 + 1 + 1  # marinara + mozzarella + pineapple
        
        thin_pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        assert thin_pizza.cost() == 5 + base_cost
        
        thick_pizza = Pizza('thick', ['marinara'], 'mozzarella', ['pineapple'])
        assert thick_pizza.cost() == 3 + base_cost
        
        gf_pizza = Pizza('gluten_free', ['marinara'], 'mozzarella', ['pineapple'])
        assert gf_pizza.cost() == 7 + base_cost
    
    def test_pizza_cost_all_sauces(self):
        """
        Test pizza cost calculation for different sauce types.
        """
        base_cost = 5 + 1 + 1  # thin + mozzarella + pineapple
        
        marinara_pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        assert marinara_pizza.cost() == base_cost + 2
        
        pesto_pizza = Pizza('thin', ['pesto'], 'mozzarella', ['pineapple'])
        assert pesto_pizza.cost() == base_cost + 3
        
        liv_pizza = Pizza('thin', ['liv_sauce'], 'mozzarella', ['pineapple'])
        assert liv_pizza.cost() == base_cost + 5
    
    def test_pizza_cost_all_toppings(self):
        """
        Test pizza cost calculation for different topping types.
        """
        base_cost = 5 + 2 + 1  # thin + marinara + mozzarella
        
        pepperoni_pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pepperoni'])
        assert pepperoni_pizza.cost() == base_cost + 2
        
        mushroom_pizza = Pizza('thin', ['marinara'], 'mozzarella', ['mushrooms'])
        assert mushroom_pizza.cost() == base_cost + 3
        
        pineapple_pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        assert pineapple_pizza.cost() == base_cost + 1
