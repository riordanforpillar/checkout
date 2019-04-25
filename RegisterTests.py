import unittest
import checkout.Register
import checkout.Items


class RegisterTest(unittest.TestCase):


    def setUp(self):
        self.singleItemName = "Soup"
        self.singleItemPPU = 1.25
        self.singleItem = checkout.Items.Item(self.singleItemName, self.singleItemPPU)
        
        inventory = checkout.Items.Inventory()
        inventory.addItem(self.singleItem)
        
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

    def testRegisterScanItem(self):
        self.register.scanItemByName(self.singleItemName)
        
    def testRegisterScanItemWithWeight(self):
        aWeight = 1.3
        self.register.scanItemByNameWithWeight(self.singleItemName, aWeight)
        
        
    def testRegisterGetTotal(self):
        self.assertAlmostEqual(0.0, self.register.getTotal(), 3, "Empty register total not 0")
        self.register.scanItemByName(self.singleItemName)
        self.assertAlmostEqual(self.singleItemPPU, self.register.getTotal(), 3, "Scanned item not totaling")


    def testRegisterScanItemAndItemIsMissing(self):
        with self.assertRaises(checkout.Items.NotFoundInInventoryException):
            self.register.scanItemByName("No item here")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()