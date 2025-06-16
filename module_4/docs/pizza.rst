Pizza Module
============

The pizza module contains the Pizza class that represents a customizable pizza with various crust, sauce, cheese, and topping options.

.. automodule:: pizza
   :members:
   :undoc-members:
   :show-inheritance:

Pizza Class
-----------

.. autoclass:: pizza.Pizza
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __str__

Usage Examples
--------------

Creating a Simple Pizza
~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pizza import Pizza
    
    # Create a basic pizza
    pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
    print(pizza)  # Shows pizza details and cost

Creating a Complex Pizza
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Pizza with multiple sauces and toppings
    pizza = Pizza(
        crust='gluten_free',
        sauce=['marinara', 'pesto'],
        cheese='mozzarella',
        toppings=['pepperoni', 'mushrooms']
    )
    
    print(f"Cost: ${pizza.cost():.2f}")

Pricing Calculation
~~~~~~~~~~~~~~~~~~~

The cost calculation is additive across all components:

* **Example 1**: Thin crust ($5) + Marinara sauce ($2) + Mozzarella cheese ($1) + Pineapple topping ($1) = $9
* **Example 2**: Gluten-free crust ($7) + Pesto sauce ($3) + Mozzarella cheese ($1) + Pepperoni ($2) + Mushrooms ($3) = $16

Validation
~~~~~~~~~~

The Pizza class validates all inputs:

* Crust must be one of: 'thin', 'thick', 'gluten_free'
* Sauce must be a non-empty list containing valid sauce types
* Cheese must be 'mozzarella' (only supported option)
* Toppings must be a non-empty list containing valid topping types

Error Handling
~~~~~~~~~~~~~~

::

    # This will raise a ValueError
    try:
        pizza = Pizza('invalid_crust', ['marinara'], 'mozzarella', ['pineapple'])
    except ValueError as e:
        print(f"Error: {e}")
    
    # This will also raise a ValueError (empty toppings)
    try:
        pizza = Pizza('thin', ['marinara'], 'mozzarella', [])
    except ValueError as e:
        print(f"Error: {e}")
