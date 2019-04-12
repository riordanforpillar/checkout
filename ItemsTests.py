'''
Created on Apr 12, 2019

@author: seamus
'''
import unittest
import checkout.Items


class ItemsTest(unittest.TestCase):


    def setUp(self):
        self.itemName = "Soup"
        self.itemPricePerUnit = 1.25
        self.anItem = checkout.Items.Item(self.itemName, self.itemPricePerUnit)


    def tearDown(self):
        pass


    def testItemConstruction(self):
        
        self.assertEqual(self.anItem.name, self.itemName, "Name not set")
        self.assertEqual(self.anItem.pricePerUnit, self.itemPricePerUnit, "Price per unit not set")
        
    def testInventoryAddition(self):
        inventory = checkout.Items.Inventory()
        self.assertEqual(inventory.getSize(), 0, "Initial inventory not empty")
        
        inventory.addItem(self.anItem)
        self.assertEqual(inventory.getSize(), 1, "Inventory size not incremented")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()