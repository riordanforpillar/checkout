import unittest
import checkout.Register
import checkout.Items


class RegisterTest(unittest.TestCase):
    
    def setUp(self):
        self.countableItemName = "Soup"
        self.countableItemPPU = 1.25
        self.countableItem = checkout.Items.Item(self.countableItemName, self.countableItemPPU)
 
        self.weightedItemName = "Beef"
        self.weightedItemPPU = 4.09
        self.weightedItemWeight = 1.59
        self.weightedItem = checkout.Items.WeightedItem(self.weightedItemName, self.weightedItemPPU)
   
        self.countableMarkdownValue = 0.40
        self.countableMarkdown = checkout.Discounts.Markdown(self.countableItem, self.countableMarkdownValue)   
   
        self.buy2Get1FreeSpecial = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, 2, 1, 100.0)
               
        inventory = checkout.Items.Inventory()
        inventory.addItem(self.countableItem)
        inventory.addItem(self.weightedItem)
       
        self.markdowns = checkout.Discounts.DiscountContainer()
        self.specials  = checkout.Discounts.DiscountContainer()
        self.register  = checkout.Register.Register(inventory, self.markdowns, self.specials)


    def tearDown(self):
        pass


    def testRegisterConstruction(self):
        inventory = checkout.Items.Inventory()
        markdowns = checkout.Discounts.DiscountContainer()
        specials  = checkout.Discounts.DiscountContainer()
        register  = checkout.Register.Register(inventory, markdowns, specials)

    def testRegisterScanItem(self):
        self.register.scanItemByName(self.countableItemName)
        self.assertAlmostEqual(self.countableItemPPU, self.register.getTotal(), 3, "Scanned item not totaling")
       
    def testRegisterScanItemWithWeight(self):
        aWeight = 1.3
        expectedPrice = aWeight*self.weightedItemPPU
        self.register.scanItemByNameWithWeight(self.weightedItemName, aWeight)
        self.assertAlmostEqual(expectedPrice, self.register.getTotal(), 3, "Scanned weighted item not totaling")      
  
    def testRegisterScanNonWeightedItemWithWeight(self):
        with self.assertRaises(checkout.Items.ScannedNonWeightedItemWithWeight):
            self.register.scanItemByNameWithWeight(self.countableItemName, 4.0)
        
    def testRegisterGetTotal(self):
        self.assertAlmostEqual(0.0, self.register.getTotal(), 3, "Empty register total not 0")

    def testRegisterScanItemAndItemIsMissing(self):
        with self.assertRaises(checkout.Items.NotFoundInInventoryException):
            self.register.scanItemByName("No item here")
            
    def testRegisterWithMarkdown(self):
        self.markdowns.addDiscount(self.countableMarkdown)
        self.register.scanItemByName(self.countableItemName)
        markedDownPrice = self.countableItemPPU-self.countableMarkdownValue
        self.assertAlmostEqual(self.register.getTotal(), markedDownPrice, 3, "Markdown not applied")
        
    def testRegisterWithSpecial(self):
        self.specials.addDiscount(self.buy2Get1FreeSpecial)
        for _ in range(3):
            self.register.scanItemByName(self.countableItemName)
        self.assertAlmostEqual(self.register.getTotal(), self.countableItemPPU*2, 3, "Special not applied")
        
    def testRegisterRemoveLastScannedWithNoScanned(self):
        with self.assertRaises(IndexError):
            self.register.removeLastScanned()
            
    def testRegisterRemoveItemAtWithNoScanned(self):
        with self.assertRaises(IndexError):
            self.register.removeScannedAt(3)        

    def testRegisterRemoveItemAt(self):
        weight = 1.03
        self.register.scanItemByNameWithWeight(self.weightedItemName, weight)
        self.register.scanItemByName(self.countableItemName)
        self.register.removeScannedAt(0)
        self.assertAlmostEqual(self.register.getTotal(), self.countableItemPPU, 3, "Removed wrong item")       

       
    def testRegisterRemoveLastScanned(self):
        self.register.scanItemByName(self.countableItemName)
        self.register.removeLastScanned()
        self.assertAlmostEqual(self.register.getTotal(), 0.0, 3, "Special not applied")
            
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()