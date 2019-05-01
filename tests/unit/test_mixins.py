import unittest

from tests.factories.orders import OperationFactory, OrderFactory, OrderItemFactory, PaymentDetailsFactory,\
    ShippingOptionFactory, OrderCustomerFactory


class TestOrderListener(unittest.TestCase):

    def test_example(self):

        op = OperationFactory.build()
        print(op)
        print(op.name)

        oi = OrderItemFactory.build()
        print(oi)

        pd = PaymentDetailsFactory.build()
        print(pd)

        so = ShippingOptionFactory.build()
        print(so)

        cus = OrderCustomerFactory.build()
        print(cus)


        test = OrderFactory.build()
        print(test)



        self.assertFalse(True)