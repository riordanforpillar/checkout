

import unittest
import checkout.Discounts
import checkout.Items
from checkout.Items import ScannedItem

class DiscountsTest(unittest.TestCase):


    def setUp(self):
        self.discount = checkout.Discounts.Discount()
        
        self.scannedItems = checkout.Items.ScannedItemContainer()

        self.cerealMarkdownValue = 0.40
        self.quantityItem = checkout.Items.Item("Cereal", 4.25)
        self.scannedCereal = checkout.Items.ScannedItem(self.quantityItem)
        self.cerealMarkdown = checkout.Discounts.Markdown(self.quantityItem, self.cerealMarkdownValue)
        
        self.beefMarkdownValue = 0.1
        self.weightItemWeight = 3.5
        self.weightItem = checkout.Items.Item("Beef", 2.0)
        self.scannedBeef = checkout.Items.ScannedWeightedItem(self.weightItem, self.weightItemWeight)
        self.beefMarkdown = checkout.Discounts.Markdown(self.weightItem, self.beefMarkdownValue)
        
        self.scannedItems.addScannedItem(self.scannedCereal)
        self.scannedItems.addScannedItem(self.scannedBeef)


    def tearDown(self):
        pass

    def testDiscountConstructor(self):
        aDiscount = checkout.Discounts.Discount()
    
    def testDiscountApply(self):
        self.discount.applyTo(self.scannedItems)
        
    def testMarkdownConstructor(self):
        markdownValue = 0.40
        cerealItem = checkout.Items.Item("Cereal", 4.25)
        aMarkdown = checkout.Discounts.Markdown(cerealItem, markdownValue)
        self.assertEqual(aMarkdown.value, markdownValue, "Markdown value not set")
        self.assertEqual(aMarkdown.itemtoMarkdown.name, cerealItem.name, "Markdown name not set")

        
    def testMarkdownApplication(self):
        self.cerealMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(0)
        targetCerealPrice = self.scannedCereal.getBasePrice() - self.cerealMarkdownValue
        self.assertEqual(scannedItem.getMarkdownPrice(), targetCerealPrice, "Cereal markdown not applied")
        scannedItem = self.scannedItems.getAt(1)
        self.assertEqual(scannedItem.getMarkdownPrice(), self.scannedBeef.getBasePrice()*self.weightItemWeight, "Markdown misapplied")
        
        self.beefMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(0)
        self.assertEqual(scannedItem.getMarkdownPrice(), targetCerealPrice, "Cereal markdown undone")
        scannedItem = self.scannedItems.getAt(1)
        targetBeefPrice = (self.scannedBeef.getBasePrice()-self.beefMarkdownValue)*self.weightItemWeight
        self.assertEqual(scannedItem.getMarkdownPrice(), targetBeefPrice, "Beef markdown misapplied")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()