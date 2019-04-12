'''
Created on Apr 12, 2019

@author: seamus
'''
import unittest
import checkout.Items
from distutils.command.check import check


class ItemsTest(unittest.TestCase):


    def setUp(self):
        self.itemName = "Soup"
        self.itemPricePerUnit = 1.25
        self.anItem = checkout.Items.Item(self.itemName, self.itemPricePerUnit)

        self.inventory = checkout.Items.Inventory()
        self.inventory.addItem(self.anItem)

        self.scannedItem = checkout.Items.ScannedItem(self.anItem)


    def tearDown(self):
        pass


    def testItemConstruction(self):
        
        self.assertEqual(self.anItem.name, self.itemName, "Name not set")
        self.assertEqual(self.anItem.pricePerUnit, self.itemPricePerUnit, "Price per unit not set")
        
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
            self.inventory.getItemByName("Cereal")
        returnedItem = self.inventory.getItemByName("Soup")
        self.assertEqual(returnedItem.name, "Soup", "Did not return Soup")

    def testScannedItemName(self):
        self.assertEqual(self.scannedItem.getName(), "Soup", "Soup not found")

    def testScannedItemPrice(self):
        self.assertEqual(self.scannedItem.getPrice(), self.itemPricePerUnit, "Price %f not returned" % self.itemPricePerUnit)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()