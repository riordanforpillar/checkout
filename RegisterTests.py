import unittest
import checkout.Register
import checkout.Items


class RegisterTest(unittest.TestCase):


    def setUp(self):
        self.singleItemName = "Soup"
        self.singleItemPPU = 1.25
        self.singleItem = checkout.Items.Item(self.singleItemName, self.singleItemPPU)
 
        self.weightedItemName = "Beef"
        self.weightedItemPPU = 4.09
        self.weightedItemWeight = 1.59
        self.weightedItem = checkout.Items.Item(self.weightedItemName, self.weightedItemPPU)
                
        inventory = checkout.Items.Inventory()
        inventory.addItem(self.singleItem)
        inventory.addItem(self.weightedItem)
       
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
        self.assertAlmostEqual(self.singleItemPPU, self.register.getTotal(), 3, "Scanned item not totaling")
       
    def testRegisterScanItemWithWeight(self):
        aWeight = 1.3
        expectedPrice = aWeight*self.weightedItemPPU
        self.register.scanItemByNameWithWeight(self.weightedItemName, aWeight)
        self.assertAlmostEqual(expectedPrice, self.register.getTotal(), 3, "Scanned weighted item not totaling")
        
        
    def testRegisterGetTotal(self):
        self.assertAlmostEqual(0.0, self.register.getTotal(), 3, "Empty register total not 0")


    def testRegisterScanItemAndItemIsMissing(self):
        with self.assertRaises(checkout.Items.NotFoundInInventoryException):
            self.register.scanItemByName("No item here")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()