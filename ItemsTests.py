'''
Created on Apr 12, 2019

@author: seamus
'''
import unittest
import checkout.Items
from distutils.command.check import check


class ItemsTest(unittest.TestCase):


    def setUp(self):
        self.soupName = "Soup"
        self.soupPricePerUnit = 1.25
        self.soupItem = checkout.Items.Item(self.soupName, self.soupPricePerUnit)

        self.cerealName = "Cereal"
        self.cerealPricePerUnit = 5.25
        self.cerealItem = checkout.Items.Item(self.cerealName, self.cerealPricePerUnit)
        self.cerealScanned = checkout.Items.ScannedItem(self.cerealItem)


        self.inventory = checkout.Items.Inventory()
        self.inventory.addItem(self.soupItem)

        self.scannedItem = checkout.Items.ScannedItem(self.soupItem)


    def tearDown(self):
        pass


    def testItemConstruction(self):
        
        self.assertEqual(self.soupItem.name, self.soupName, "Name not set")
        self.assertEqual(self.soupItem.pricePerUnit, self.soupPricePerUnit, "Price per unit not set")
        
    def testInventoryConstruct(self):
        inventory = checkout.Items.Inventory()
        self.assertEqual(inventory.getSize(), 0, "Initial inventory not empty")
    
    def testInventoryAddition(self):
        # Need to add unique item to avoid collision of adding existing item
        # which will not increment inventory
        uniqueItem = checkout.Items.Item("Unique", 4.0)
        
        beforeSize = self.inventory.getSize()
        self.inventory.addItem(uniqueItem)
        self.assertEqual(self.inventory.getSize(), beforeSize+1, "Inventory size not incremented")
        
    def testInventoryGet(self):
        with self.assertRaises(checkout.Items.InventoryException):
            self.inventory.getItemByName("Nonsense Item")
        returnedItem = self.inventory.getItemByName("Soup")
        self.assertEqual(returnedItem.name, "Soup", "Did not return Soup")
        

    def testScannedBaseItemNameAndPrices(self):
        nameMessageForm = "%s not found"
        priceMessageForm = "Price %f not returned"

        testCases = [ (self.scannedItem,   self.soupName,   self.soupPricePerUnit),\
                      (self.cerealScanned, self.cerealName, self.cerealPricePerUnit)]
        for scanned, name, price in testCases:
            self.assertEqual(scanned.getName(),      name,  nameMessageForm %(name))
            self.assertEqual(scanned.getBasePrice(), price, priceMessageForm %(price))

    def testScannedMarkdownPrice(self):
        messageForm = "Markdown price %f not found"
        
        testCases = [ (self.scannedItem,   self.soupPricePerUnit),\
                      (self.cerealScanned, self.cerealPricePerUnit)]
        
        for scanned, markdown in testCases:
            self.assertEqual(scanned.getMarkdownPrice(), markdown, messageForm % markdown)
            
    def testScannedDiscountPrice(self):
        messageForm = "Discount price %f not found"
        
        testCases = [ (self.scannedItem,   self.soupPricePerUnit),\
                      (self.cerealScanned, self.cerealPricePerUnit)]
        
        for scanned, discountPrice in testCases:
            self.assertEqual(scanned.getDiscountPrice(), discountPrice, messageForm % discountPrice)
            
    def testScannedItemContainer(self):
        scannedItemContainer = checkout.Items.ScannedItemContainer()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()