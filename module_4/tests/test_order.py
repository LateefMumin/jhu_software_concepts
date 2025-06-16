"""
Unit tests for the Order class.

This module contains comprehensive unit tests for the Order class
functionality including initialization, string representation,
pizza input, and payment status.
"""

import pytest
from src.order import Order
from src.pizza import Pizza


@pytest.mark.order
class TestOrder:
    """Test cases for the Order class."""
    
    def test_order_init(self):
        """
        Test order __init__() method.
        
        - Assert order should include an empty list of pizza objects
        - Assert order should have a zero cost until an order is input
        - Assert order should not have yet been paid
        """
        order = Order()
        
        assert order.pizzas == []
        assert order.cost() == 0
        assert order.paid is False
    
    def test_order_str_empty(self):
        """
        Test order __str__() method with empty order.
        
        Test order should return a string containing customer full order and cost.
        """
        order = Order()
        
        result = str(order)
        assert "Order: No pizzas - $0.00" in result
    
    def test_order_str_with_pizzas(self):
        """
        Test order __str__() method with pizzas.
        
        Test order should return a string containing customer full order and cost.
        """
        order = Order()
        pizza1 = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        pizza2 = Pizza('thick', ['pesto'], 'mozzarella', ['mushrooms'])
        
        order.input_pizza(pizza1)
        order.input_pizza(pizza2)
        
        result = str(order)
        assert "Order:" in result
        assert "Total Cost:" in result
        assert "Status: Unpaid" in result
        assert str(pizza1.cost()) in result or f"${pizza1.cost():.2f}" in result
        assert str(pizza2.cost()) in result or f"${pizza2.cost():.2f}" in result
    
    def test_order_input_pizza_updates_cost(self):
        """
        Test order input_pizza() method.
        
        Test method should update cost.
        """
        order = Order()
        pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        
        initial_cost = order.cost()
        order.input_pizza(pizza)
        
        assert order.cost() > initial_cost
        assert order.cost() == pizza.cost()
    
    def test_order_input_pizza_invalid_type(self):
        """
        Test order input_pizza() method with invalid input.
        
        Should raise TypeError for non-Pizza objects.
        """
        order = Order()
        
        with pytest.raises(TypeError):
            order.input_pizza("not a pizza")
        
        with pytest.raises(TypeError):
            order.input_pizza(123)
    
    def test_order_paid(self):
        """
        Test order order_paid() method.
        
        Test method should update paid to true.
        """
        order = Order()
        
        assert order.paid is False
        order.order_paid()
        assert order.paid is True
    
    def test_order_str_shows_paid_status(self):
        """
        Test that __str__ shows correct payment status.
        """
        order = Order()
        pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        order.input_pizza(pizza)
        
        # Test unpaid status
        result_unpaid = str(order)
        assert "Status: Unpaid" in result_unpaid
        
        # Test paid status
        order.order_paid()
        result_paid = str(order)
        assert "Status: Paid" in result_paid
