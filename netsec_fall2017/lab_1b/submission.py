import unittest

from mypackets import RequestMenu, Menu, Order, Result


class MyPacketsTestCase(unittest.TestCase):

    def test_RequestMenu(self):
        request_menu_before = RequestMenu()
        request_menu_ser = request_menu_before.__serialize__()
        request_menu_after = RequestMenu.Deserialize(request_menu_ser)
        self.assertEqual(request_menu_before, request_menu_after)

    def test_Menu(self):
        menu_before = Menu()

        menu_before.ID = 1
        menu_before.setMealA = 'A'
        menu_before.setMealB = 'B'
        menu_before.setMealC = 'C'

        menu_ser = menu_before.__serialize__()
        menu_after = Menu.Deserialize(menu_ser)
        self.assertEqual(menu_before, menu_after)

    def test_Order(self):
        order_before = Order()

        order_before.ID = 1
        order_before.setMeal = 'B'

        order_ser = order_before.__serialize__()
        order_after = Order.Deserialize(order_ser)
        self.assertEqual(order_before, order_after)

    def test_Result(self):
        result_before = Result()

        result_before.ID = 1
        result_before.price = 10

        result_ser = result_before.__serialize__()
        result_after = Result.Deserialize(result_ser)
        self.assertEqual(result_before, result_after)


if __name__ == '__main__':
    unittest.main()
