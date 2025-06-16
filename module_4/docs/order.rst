Order Module
============

The order module contains the Order class that manages customer orders containing one or more pizzas.

.. automodule:: order
   :members:
   :undoc-members:
   :show-inheritance:

Order Class
-----------

.. autoclass:: order.Order
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __str__

Usage Examples
--------------

Creating an Order
~~~~~~~~~~~~~~~~~

::

    from order import Order
    from pizza import Pizza
    
    # Create a new order
    order = Order()
    print(f"Initial cost: ${order.cost():.2f}")  # $0.00
    print(f"Paid status: {order.paid}")  # False

Adding Pizzas to Order
~~~~~~~~~~~~~~~~~~~~~~

::

    # Create pizzas
    pizza1 = Pizza('thin', ['marinara'], 'mozzarella', ['pineapple'])
    pizza2 = Pizza('thick', ['pesto'], 'mozzarella', ['mushrooms'])
    
    # Add to order
    order.input_pizza(pizza1)
    order.input_pizza(pizza2)
    
    print(f"Total cost: ${order.cost():.2f}")

Processing Payment
~~~~~~~~~~~~~~~~~~

::

    # Mark order as paid
    order.order_paid()
    print(f"Payment status: {order.paid}")  # True

Order Display
~~~~~~~~~~~~~

::

    # Display complete order details
    print(order)
    
    # Output example:
    # Order:
    #   1. Pizza: Thin crust, Marinara sauce, Mozzarella cheese, with Pineapple - $9.00
    #   2. Pizza: Thick crust, Pesto sauce, Mozzarella cheese, with Mushrooms - $10.00
    # Total Cost: $19.00
    # Status: Paid

Order Workflow
--------------

Complete Order Process
~~~~~~~~~~~~~~~~~~~~~~

::

    from order import Order
    from pizza import Pizza
    
    # 1. Create order
    order = Order()
    
    # 2. Add pizzas
    pizza1 = Pizza('thin', ['marinara'], 'mozzarella', ['pepperoni'])
    pizza2 = Pizza('gluten_free', ['pesto', 'liv_sauce'], 'mozzarella', ['mushrooms', 'pineapple'])
    
    order.input_pizza(pizza1)
    order.input_pizza(pizza2)
    
    # 3. Review order
    print("Order Summary:")
    print(order)
    
    # 4. Process payment
    order.order_paid()
    print("Order has been paid!")

Multiple Pizza Management
~~~~~~~~~~~~~~~~~~~~~~~~~

The Order class automatically handles multiple pizzas:

* Cost calculation is additive across all pizzas
* Each pizza maintains its individual cost
* Order tracks total cost dynamically
* String representation lists all pizzas with numbering

Error Handling
~~~~~~~~~~~~~~

::

    # Only Pizza objects can be added to orders
    try:
        order.input_pizza("not a pizza")
    except TypeError as e:
        print(f"Error: {e}")
    
    # Empty orders are valid
    empty_order = Order()
    print(empty_order)  # Shows "Order: No pizzas - $0.00"

Order States
~~~~~~~~~~~~

An order can be in various states:

* **Empty**: No pizzas added, cost is $0.00
* **Active**: Has pizzas, unpaid status
* **Paid**: Has pizzas, payment processed

The order maintains state consistency throughout its lifecycle.
