

import unittest
import checkout.Discounts
import checkout.Items

class DiscountsTest(unittest.TestCase):


    def setUp(self):
        self.discount = checkout.Discounts.Discount()
        
        self.scannedItems = checkout.Items.ScannedItemContainer()


    def tearDown(self):
        pass


    def testDiscountConstructor(self):
        aDiscount = checkout.Discounts.Discount()
    
    def testDiscountApply(self):
        self.discount.applyTo(self.scannedItems)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()