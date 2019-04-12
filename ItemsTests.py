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
            self.inventory.getItemByName("Cereal")
        returnedItem = self.inventory.getItemByName("Soup")
        self.assertEqual(returnedItem.name, "Soup", "Did not return Soup")
        

    def testScannedItemName(self):
        self.assertEqual(self.scannedItem.getName(), self.soupItem.name, "%s not found" %(self.soupItem.name))
        self.assertEqual(self.cerealScanned.getName(), self.cerealItem.name, "%s not found" %(self.cerealItem.name))


    def testScannedItemPrice(self):
        self.assertEqual(self.scannedItem.getBasePrice(), self.soupPricePerUnit, "Price %f not returned" % self.soupPricePerUnit)
        self.assertEqual(self.cerealScanned.getBasePrice(), self.cerealPricePerUnit, "Price %f not returned" %(self.cerealPricePerUnit))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()