"""
Integration tests for the pizza ordering system.

This module contains integration tests that verify the interaction
between Order and Pizza classes, particularly testing multiple
pizza objects per order.
"""

import pytest
from src.order import Order
from src.pizza import Pizza


@pytest.mark.order
@pytest.mark.pizza
class TestIntegration:
    """Integration test cases for Order and Pizza interaction."""
    
    def test_multiple_pizzas_per_order(self):
        """
        Test that code can handle multiple pizza objects per order.
        
        Ensure multiple pizza objects within a given order result in 
        an additively larger cost.
        """
        order = Order()
        
        # Create first pizza: Thin Crust, Marinara, Mozzarella, Pineapple
        # Cost: $5 + $2 + $1 + $1 = $9
        pizza1 = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        
        # Create second pizza: Thick Crust, Pesto, Mozzarella, Mushrooms
        # Cost: $3 + $3 + $1 + $3 = $10
        pizza2 = Pizza('thick', ['pesto'], 'mozzarella', ['mushrooms'])
        
        # Add pizzas to order
        order.input_pizza(pizza1)
        assert order.cost() == pizza1.cost()
        
        order.input_pizza(pizza2)
        expected_total = pizza1.cost() + pizza2.cost()
        assert order.cost() == expected_total
        
        # Verify individual pizza costs are maintained
        assert pizza1.cost() == 9
        assert pizza2.cost() == 10
        assert order.cost() == 19
    
    def test_complex_order_scenario(self):
        """
        Test the complex order scenario from the assignment.
        
        Order 1:
        - Pizza(thin, pesto, mozzarella, mushrooms) = $5 + $3 + $1 + $3 = $12
        - Pizza(thick, marinara, mozzarella, mushrooms) = $3 + $2 + $1 + $3 = $9
        Total: $21
        
        Order 2:
        - Pizza(gluten_free, marinara, mozzarella, pineapple) = $7 + $2 + $1 + $1 = $11
        - Pizza(thin, liv_sauce, pesto, mozzarella, mushrooms, pepperoni) = $5 + $5 + $3 + $1 + $3 + $2 = $19
        Total: $30
        """
        # Order 1
        order1 = Order()
        pizza1_1 = Pizza('thin', ['pesto'], 'mozzarella', ['mushrooms'])
        pizza1_2 = Pizza('thick', ['marinara'], 'mozzarella', ['mushrooms'])
        
        order1.input_pizza(pizza1_1)
        order1.input_pizza(pizza1_2)
        
        assert pizza1_1.cost() == 12  # 5 + 3 + 1 + 3
        assert pizza1_2.cost() == 9   # 3 + 2 + 1 + 3
        assert order1.cost() == 21
        
        # Order 2
        order2 = Order()
        pizza2_1 = Pizza('gluten_free', ['marinara'], 'mozzarella', ['pineapple'])
        pizza2_2 = Pizza('thin', ['liv_sauce', 'pesto'], 'mozzarella', ['mushrooms', 'pepperoni'])
        
        order2.input_pizza(pizza2_1)
        order2.input_pizza(pizza2_2)
        
        assert pizza2_1.cost() == 11  # 7 + 2 + 1 + 1
        assert pizza2_2.cost() == 19  # 5 + 5 + 3 + 1 + 3 + 2
        assert order2.cost() == 30
    
    def test_order_string_with_multiple_pizzas(self):
        """
        Test order string representation with multiple pizzas.
        """
        order = Order()
        pizza1 = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        pizza2 = Pizza('thick', ['pesto'], 'mozzarella', ['mushrooms'])
        
        order.input_pizza(pizza1)
        order.input_pizza(pizza2)
        
        order_str = str(order)
        
        # Check that both pizzas are listed
        assert "1." in order_str
        assert "2." in order_str
        assert "Total Cost:" in order_str
        assert f"${order.cost():.2f}" in order_str
        assert "Status: Unpaid" in order_str
    
    def test_payment_workflow_integration(self):
        """
        Test complete order and payment workflow.
        """
        order = Order()
        pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
        
        # Initial state
        assert order.cost() == 0
        assert not order.paid
        
        # Add pizza
        order.input_pizza(pizza)
        assert order.cost() == pizza.cost()
        assert not order.paid
        
        # Process payment
        order.order_paid()
        assert order.paid
        assert order.cost() == pizza.cost()  # Cost should remain same after payment
    
    def test_empty_order_workflow(self):
        """
        Test workflow with empty order.
        """
        order = Order()
        
        # Empty order should have zero cost
        assert order.cost() == 0
        
        # Can mark empty order as paid
        order.order_paid()
        assert order.paid
        
        # String representation should handle empty order
        order_str = str(order)
        assert "No pizzas" in order_str
        assert "$0.00" in order_str
