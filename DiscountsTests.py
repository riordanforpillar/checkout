

import unittest
import checkout.Discounts
import checkout.Items

class DiscountsTest(unittest.TestCase):


    def setUp(self):
        self.discount = checkout.Discounts.Discount()
        
        self.scannedItems = checkout.Items.ScannedItemContainer()

        self.cerealMarkdownValue = 0.40
        self.cerealItem = checkout.Items.Item("Cereal", 4.25)
        self.markdown = checkout.Discounts.Markdown(self.cerealItem, self.cerealMarkdownValue)

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
        
    def testMarkdownApplication(self):
        self.markdown.applyTo(self.scannedItems)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()