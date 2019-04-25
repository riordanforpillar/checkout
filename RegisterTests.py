import unittest
import checkout.Register


class RegisterTest(unittest.TestCase):


    def setUp(self):
        inventory = checkout.Items.Inventory()
        markdowns = checkout.Discounts.DiscountContainer()
        specials  = checkout.Discounts.DiscountContainer()
        self.register  = checkout.Register.Register(inventory, markdowns, specials)


    def tearDown(self):
        pass


    def testRegisterConstruction(self):
        inventory = checkout.Items.Inventory()
        markdowns = checkout.Discounts.DiscountContainer()
        specials  = checkout.Discounts.DiscountContainer()
        register  = checkout.Register.Register(inventory, markdowns, specials)
        
    def testRegisterGetTotal(self):
        self.assertAlmostEqual(0.0, self.register.getTotal(), 3, "Empty register total not 0")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()