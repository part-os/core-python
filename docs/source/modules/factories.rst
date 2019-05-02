Mock Data Factories
===================

The Paperless Parts SDK comes with pre-made entity factories for the purpose of allowing developers to develop third party apps rapidly with realistic looking data.

**Note: These factories are intended purely for making testing easy and should never be used as part of a production solution.**

Basic Usage
-----------

See the following example for a demonstration on how to use factories:

.. code-block:: python

    from tests.factories.orders import OperationFactory, OrderFactory

    # Generating a dummy entity
    dummy_order1 = OrderFactory.build()
    print(dummy_order1.number)

    # Generating a dummy entity with defined values
    number = 404
    dummy_order2 = OrderFactory.build(number=number)
    print(dummy_order2.number)
    assert dummy_order2.number == number

    # Generating a batch of dummy entities
    dummy_operations = OperationFactory.build_batch(10)
    print(dummy_operations)

    # Generating a dummy entity using other dummy entities
    dummy_operations = OperationFactory.build_batch(10)
    print(dummy_operations)
    dummy_order_item = OrderItemFactory.build(operations=dummy_operations)
    print(dummy_order_item)

Available Factories
-------------------
TODO: ADD REFS LINKING THESE ALL TO THE CLASSES THEY ARE FACTORIES FOR

.. autoclass:: tests.factories.address.AddressFactory

.. autoclass:: tests.factories.orders.OperationFactory

.. autoclass:: tests.factories.orders.OrderItemFactory

.. autoclass:: tests.factories.orders.PaymentDetailsFactory

.. autoclass:: tests.factories.orders.ShippingOptionFactory

.. autoclass:: tests.factories.orders.OrderCustomerFactory

.. autoclass:: tests.factories.orders.OrderFactory


