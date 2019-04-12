'''
Created on Apr 12, 2019

@author: seamus
'''
import unittest
import checkout.Items


class ItemsTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testItemConstruction(self):
        name = "Soup"
        pricePerUnit = 1.25
        anItem = checkout.Items.Item(name, pricePerUnit)
        self.assertEqual(anItem.name, name, "Name not set")
        self.assertEqual(anItem.pricePerUnit, pricePerUnit, "Price per unit not set")
        
    def testInventory(self):
        inventory = checkout.Items.Inventory()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()