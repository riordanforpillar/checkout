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
        self.cerealQuantity = 2
        self.cerealScanned = checkout.Items.ScannedItem(self.cerealItem,2)

        self.beefName = "Beef"
        self.beefPricePerUnit = 4.09
        self.beefWeight = 1.59
        self.beefItem = checkout.Items.Item(self.beefName, self.beefPricePerUnit)
        self.beefScanned = checkout.Items.ScannedWeightedItem(self.beefItem, self.beefWeight)

        self.inventory = checkout.Items.Inventory()
        self.inventory.addItem(self.soupItem)

        self.soupScanned = checkout.Items.ScannedItem(self.soupItem)

        self.scannedItemContainer = checkout.Items.ScannedItemContainer()

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
        with self.assertRaises(checkout.Items.NotFoundInInventoryException):
            self.inventory.getItemByName("Nonsense Item")
        returnedItem = self.inventory.getItemByName("Soup")
        self.assertEqual(returnedItem.name, "Soup", "Did not return Soup")

    def testScannedItemWithQuantityConstruction(self):
        quantity = 2
        item = checkout.Items.ScannedItem(self.cerealItem, quantity)
        with self.assertRaises(checkout.Items.ScannedQuantityNotIntegerException):
            checkout.Items.ScannedItem(self.cerealItem, 1.2)
        
    def testScannedItemByWeightConstruction(self):
        weight = 1.09
        weightItem = checkout.Items.ScannedWeightedItem(self.beefItem, weight, 1)
        with self.assertRaises(checkout.Items.ScannedWeightNotFloatException):
            checkout.Items.ScannedWeightedItem(self.beefItem, 2)

    def testScannedItemByWeightGetWeight(self):
        self.assertAlmostEqual(self.beefScanned.getWeight(), self.beefWeight, 1e-3, "Weight %f not close enough" % self.beefWeight)
        
    def testScannedItemQuantityRetreival(self):
        messageForm = "Quantity %f not found"
        
        testCases = [ (self.soupScanned, 1), (self.beefScanned, 1)]
        
        for scanned, quantity in testCases:
            self.assertEqual(scanned.getQuantity(), quantity, messageForm % quantity)

    def testScannedBaseItemNameAndPrices(self):
        nameMessageForm = "%s not found"
        priceMessageForm = "Price %f not returned"

        testCases = [ (self.soupScanned,   self.soupName,   self.soupPricePerUnit),\
                      (self.cerealScanned, self.cerealName, self.cerealPricePerUnit)]
        for scanned, name, price in testCases:
            self.assertEqual(scanned.getName(),      name,  nameMessageForm %(name))
            self.assertEqual(scanned.getBasePrice(), price, priceMessageForm %(price))

    def testScannedMarkdownPrice(self):
        messageForm = "Markdown price %f not found"
        
        testCases = [ (self.soupScanned,   self.soupPricePerUnit),\
                      (self.cerealScanned, self.cerealPricePerUnit*self.cerealQuantity),
                      (self.beefScanned,   self.beefPricePerUnit*self.beefWeight) ]
        
        for scanned, markdown in testCases:
            self.assertEqual(scanned.getMarkdownPrice(), markdown, messageForm % markdown)
            
    def testScannedDiscountPrice(self):
        messageForm = "Discount price %f not found"
        
        testCases = [ (self.soupScanned,   self.soupPricePerUnit),\
                      (self.cerealScanned, self.cerealPricePerUnit*self.cerealQuantity),
                      (self.beefScanned,   self.beefPricePerUnit*self.beefWeight)]
        
        for scanned, discountPrice in testCases:
            self.assertEqual(scanned.getDiscountPrice(), discountPrice, messageForm % discountPrice)
            
    def testScannedItemContainer(self):
        scannedItemContainer = checkout.Items.ScannedItemContainer()

    def testScannedItemContainerGetSize(self):
        self.assertEqual(self.scannedItemContainer.getSize(), 0, "ScannedItemContainer not empty")
        
    def testScannedItemContainerAdd(self):
        sizeBefore = self.scannedItemContainer.getSize()
        self.scannedItemContainer.addScannedItem(self.soupScanned)
        sizeAfter = self.scannedItemContainer.getSize()
        self.assertEqual(sizeAfter, sizeBefore+1, "ScannedItemContainer size not incremented")

    def testScannedItemContainerRemoveLast(self):
        self.scannedItemContainer.addScannedItem(self.cerealScanned)
        self.scannedItemContainer.addScannedItem(self.soupScanned)
        beforeSize = self.scannedItemContainer.getSize()
        self.scannedItemContainer.removeLastItem()
        afterSize = self.scannedItemContainer.getSize()
        self.assertEqual(afterSize, beforeSize-1, "Scanned item size not decremented")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()