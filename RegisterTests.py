import unittest
import checkout.Register


class RegisterTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testRegisterConstruction(self):
        inventory = checkout.Items.Inventory()
        markdowns = checkout.Discounts.DiscountContainer()
        specials = checkout.Discounts.DiscountContainer()
        register = checkout.Register.Register(inventory, markdowns, specials)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()