

import unittest
import checkout.Discounts
import checkout.Items

class DiscountsTest(unittest.TestCase):


    def setUp(self):
        self.discount = checkout.Discounts.Discount()
        
        applesItem = checkout.Items.Item("Apples", 0.60)
        beefItem   = checkout.Items.Item("Beef", 2.49)
        
        scannedApples = checkout.Items.ScannedItem(applesItem, 4)
        scannedBeef = checkout.Items.ScannedWeightedItem(beefItem, 4.02)
        
        self.scannedItems = checkout.Items.ScannedItemContainer()
        
        self.scannedItems.addScannedItem(scannedApples)
        self.scannedItems.addScannedItem(scannedBeef)


    def tearDown(self):
        pass


    def testDiscountConstructor(self):
        aDiscount = checkout.Discounts.Discount()
    
    def testDiscountApply(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()