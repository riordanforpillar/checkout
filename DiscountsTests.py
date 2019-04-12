

import unittest
import checkout.Discounts
import checkout.Items
from checkout.Items import ScannedItem

class DiscountsTest(unittest.TestCase):


    def setUp(self):
        self.discount = checkout.Discounts.Discount()
        
        self.scannedItems = checkout.Items.ScannedItemContainer()

        self.cerealMarkdownValue = 0.40
        self.cerealItem = checkout.Items.Item("Cereal", 4.25)
        self.scannedCereal = checkout.Items.ScannedItem(self.cerealItem)
        self.cerealMarkdown = checkout.Discounts.Markdown(self.cerealItem, self.cerealMarkdownValue)
        
        self.beefMarkdownValue = 0.1
        self.beefWeight = 3.25
        self.beefItem = checkout.Items.Item("Beef", 2.35)
        self.scannedBeef = checkout.Items.ScannedWeightedItem(self.beefItem, self.beefWeight)
        self.beefMarkdown = checkout.Discounts.Markdown(self.beefItem, self.beefMarkdownValue)
        
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
        self.assertEqual(aMarkdown.item.name, cerealItem.name, "Markdown name set")

        
    def testMarkdownApplication(self):
        self.cerealMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(0)
        self.assertEqual(scannedItem.getMarkdownPrice(), self.scannedCereal.getBasePrice() - self.cerealMarkdownValue, "Markdown not applied")
        
        scannedItem = self.scannedItems.getAt(1)
        self.assertEqual(scannedItem.getMarkdownPrice(), self.scannedBeef.getBasePrice()*self.beefWeight, "Markdown misapplied")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()