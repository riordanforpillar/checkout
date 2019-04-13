

import unittest
import checkout.Discounts
import checkout.Items

class DiscountsTest(unittest.TestCase):


    def setUp(self):
        self.discount = checkout.Discounts.Discount()
        
        self.scannedItems = checkout.Items.ScannedItemContainer()

        self.countableMarkdownValue = 0.40
        self.countableItem = checkout.Items.Item("Cereal", 4.25)
        self.countableScanned = checkout.Items.ScannedItem(self.countableItem)
        self.countableMarkdown = checkout.Discounts.Markdown(self.countableItem, self.countableMarkdownValue)
        
        self.weightedMarkdownValue = 0.1
        self.weightedItemWeight = 3.5
        self.weightedItem = checkout.Items.Item("Beef", 2.0)
        self.weighteScanned = checkout.Items.ScannedWeightedItem(self.weightedItem, self.weightedItemWeight)
        self.weightedMarkdown = checkout.Discounts.Markdown(self.weightedItem, self.weightedMarkdownValue)
        
        self.scannedItems.addScannedItem(self.countableScanned)
        self.scannedItems.addScannedItem(self.weighteScanned)
        self.scannedItems.addScannedItem(self.countableScanned)
        self.scannedItems.addScannedItem(self.countableScanned)
        self.scannedItems.addScannedItem(self.countableScanned)
        self.scannedItems.addScannedItem(self.countableScanned)


        
        self.buyN = 3
        self.getM = 1
        self.percentOff = 50.0
        self.buyNgetMSpecial = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, self.buyN, self.getM, self.percentOff)



    def tearDown(self):
        pass

    def testDiscountConstructor(self):
        aDiscount = checkout.Discounts.Discount()
    
    def testDiscountApply(self):
        self.discount.applyTo(self.scannedItems)
        
    def testMarkdownConstructor(self):
        aMarkdown = checkout.Discounts.Markdown(self.countableItem, self.countableMarkdownValue)
        self.assertEqual(aMarkdown.value, self.countableMarkdownValue, "Markdown value not set")
        self.assertEqual(aMarkdown.itemToMarkdown.name, self.countableItem.name, "Markdown name not set")
        
    def testMarkdownMatchItem(self):
        self.assertTrue(self.weightedMarkdown.itemMatchesMarkdown(self.weighteScanned), "Markdown did not match scanned item")
        self.assertFalse(self.countableMarkdown.itemMatchesMarkdown(self.weighteScanned), "Markdown matched scanned item incorrectly")

        
    def testMarkdownApplication(self):
        self.countableMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(0)
        targetPrice = self.countableScanned.getBasePrice() - self.countableMarkdownValue
        self.assertEqual(scannedItem.getMarkdownPrice(), targetPrice, "Countable  markdown not applied")
        scannedItem = self.scannedItems.getAt(1)
        self.assertEqual(scannedItem.getMarkdownPrice(), self.weighteScanned.getBasePrice()*self.weightedItemWeight, "Markdown misapplied")
        
        scannedItem = self.scannedItems.getAt(0)
        unchangedPrice = scannedItem.getMarkdownPrice()
        self.weightedMarkdown.applyTo(self.scannedItems)
        
        self.assertEqual(scannedItem.getMarkdownPrice(), unchangedPrice, "Countable markdown undone")
        
        scannedItem = self.scannedItems.getAt(1)
        
        newPrice = (self.weighteScanned.getBasePrice()-self.weightedMarkdownValue)*self.weightedItemWeight
        self.assertEqual(scannedItem.getMarkdownPrice(), newPrice, "Beef markdown misapplied")

    def testBuyNGetMForPercentOffConstruction(self):
        buyN = 1
        getM = 1
        percentOff = 100.0
        special = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, buyN, getM, percentOff)
        self.assertEqual(special.buyN, buyN, "Buy N not set correctly")
        self.assertEqual(special.getM, getM, "Get M not set correctly")
        self.assertEqual(special.percentOff, percentOff, "Percent off not set correctly")

    def testBuyNGetMForPercentOffApplication(self):
        self.buyNgetMSpecial.applyTo(self.scannedItems)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    
    
    
    