Pizza Ordering System Documentation
====================================

Welcome to the Pizza Ordering System documentation! This is a comprehensive Test-Driven Development (TDD) pizza ordering application built for JHU EP 605.256 - Advanced Python coursework.

Overview
--------

The Pizza Ordering System provides an extensible and scalable pizza ordering service that allows customers to create customized pizza orders. The system features:

* Object-oriented design with clean separation of concerns
* Flexible pizza customization with multiple options
* Automatic cost calculation based on selected ingredients
* Order management supporting multiple pizzas per order
* Payment tracking functionality
* Comprehensive test coverage using pytest
* Full API documentation

Quick Start
-----------

Creating a simple pizza::

    from src.pizza import Pizza
    
    # Create a pizza with thin crust, marinara sauce, mozzarella cheese, and pineapple
    pizza = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
    print(f"Pizza cost: ${pizza.cost():.2f}")

Creating an order::

    from src.order import Order
    from src.pizza import Pizza
    
    # Create an order and add pizzas
    order = Order()
    pizza1 = Pizza('thin', ['pesto'], 'mozzarella', ['mushrooms'])
    pizza2 = Pizza('thick', ['marinara'], 'mozzarella', ['pepperoni'])
    
    order.input_pizza(pizza1)
    order.input_pizza(pizza2)
    
    print(f"Total order cost: ${order.cost():.2f}")
    
    # Process payment
    order.order_paid()

Pricing Structure
-----------------

**Crust Options:**
  * Thin: $5.00
  * Thick: $3.00
  * Gluten-free: $7.00

**Sauce Options:**
  * Marinara: $2.00
  * Pesto: $3.00
  * Liv Sauce: $5.00

**Cheese Options:**
  * Mozzarella: $1.00 (only option available)

**Topping Options:**
  * Pepperoni: $2.00
  * Mushrooms: $3.00
  * Pineapple: $1.00

Requirements
------------

* Each pizza must have exactly one crust
* Each pizza must have at least one sauce
* Each pizza must have cheese (only Mozzarella supported)
* Each pizza must have at least one topping
* Costs are additive across all selected ingredients

API Reference
=============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   pizza
   order

Testing
-------

The project uses pytest for comprehensive testing with custom markers:

* Run all tests: ``pytest``
* Run only order-related tests: ``pytest -m order``
* Run only pizza-related tests: ``pytest -m pizza``

Development
-----------

This project follows Test-Driven Development (TDD) principles where tests are written first to define expected behavior, implementation follows to satisfy the tests, and code is refactored while maintaining test compliance.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
