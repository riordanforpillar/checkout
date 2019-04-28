import unittest
import checkout.Register
import checkout.Items
import checkout.Discounts


class RegisterTest(unittest.TestCase):
    
    def setUp(self):
        self.countableItemName = "Soup"
        self.countableItemPPU = 1.25
        countableItem = checkout.Items.Item(self.countableItemName, self.countableItemPPU)
 
        self.weightedItemName = "Beef"
        self.weightedItemPPU = 4.09
        weightedItem = checkout.Items.WeightedItem(self.weightedItemName, self.weightedItemPPU)
   
        self.countableMarkdownValue = 0.40
        self.countableMarkdown = checkout.Discounts.Markdown(countableItem, self.countableMarkdownValue)   
   
        self.buy2Get1FreeSpecial = checkout.Discounts.BuyNGetMForPercentOffSpecial(countableItem, 2, 1, 100.0)
               
        inventory = checkout.Items.Inventory()
        inventory.addItem(countableItem)
        inventory.addItem(weightedItem)
       
        self.markdowns = checkout.Discounts.DiscountContainer()
        self.specials  = checkout.Discounts.DiscountContainer()
        self.register  = checkout.Register.Register(inventory, self.markdowns, self.specials)

    def tearDown(self):
        pass

    def testRegisterConstruction(self):
        inventory = checkout.Items.Inventory()
        markdowns = checkout.Discounts.DiscountContainer()
        specials  = checkout.Discounts.DiscountContainer()
        checkout.Register.Register(inventory, markdowns, specials)

    def testRegisterScanItem(self):
        self.register.scanItemByName(self.countableItemName)
        self.assertAlmostEqual(self.countableItemPPU, self.register.getTotal(), 3, "Register scanned item not totaling")
       
    def testRegisterScanItemWithWeight(self):
        aWeight = 1.3
        expectedPrice = round(aWeight*self.weightedItemPPU,2)
        self.register.scanItemByNameWithWeight(self.weightedItemName, aWeight)
        self.assertAlmostEqual(expectedPrice, self.register.getTotal(), 3, "Register scanned weighted item not totaling")      
  
    def testRegisterScanNonWeightedItemWithWeight(self):
        with self.assertRaises(checkout.Items.ScannedNonWeightedItemWithWeight):
            self.register.scanItemByNameWithWeight(self.countableItemName, 4.0)
            
    def testScanItemLimitTotalPrecision(self):
        highPrecisionWeight = 0.501
        lowPrecisionPrice = round(highPrecisionWeight*self.weightedItemPPU,2)
        self.register.scanItemByNameWithWeight(self.weightedItemName, highPrecisionWeight)
        self.assertAlmostEqual(lowPrecisionPrice, self.register.getTotal(), 3, "Register returned too much precision in total price")
        
    def testRegisterGetTotal(self):
        self.assertAlmostEqual(0.0, self.register.getTotal(), 3, "Empty register total price not 0")

    def testRegisterScanItemAndItemIsMissing(self):
        with self.assertRaises(checkout.Items.NotFoundInInventoryException):
            self.register.scanItemByName("No named item")
            
    def testRegisterWithMarkdown(self):
        self.markdowns.addDiscount(self.countableMarkdown)
        self.register.scanItemByName(self.countableItemName)
        markedDownPrice = self.countableItemPPU-self.countableMarkdownValue
        self.assertAlmostEqual(self.register.getTotal(), markedDownPrice, 3, "Markdown from Register not applied")
        
    def testRegisterWithSpecial(self):
        self.specials.addDiscount(self.buy2Get1FreeSpecial)
        for _ in range(3):
            self.register.scanItemByName(self.countableItemName)
        self.assertAlmostEqual(self.register.getTotal(), self.countableItemPPU*2, 3, "Special from Register not applied")
        
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
        self.assertAlmostEqual(self.register.getTotal(), self.countableItemPPU, 3, "Register removed wrong item")       

       
    def testRegisterRemoveLastScanned(self):
        self.register.scanItemByName(self.countableItemName)
        self.register.removeLastScanned()
        self.assertAlmostEqual(self.register.getTotal(), 0.0, 3, "Register Special not applied to updated smaller scanned set")
            
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()