

import unittest
import checkout.Items

class ItemsTest(unittest.TestCase):
    
    def setUp(self):
        self.singleItemName = "Soup"
        self.singleItemPPU = 1.25
        self.singleItem = checkout.Items.Item(self.singleItemName, self.singleItemPPU)
        self.singleScanned = checkout.Items.ScannedItem(self.singleItem)

        self.quantityItemName = "Cereal"
        self.quantityItemPPU = 5.25
        self.quantityItem = checkout.Items.Item(self.quantityItemName, self.quantityItemPPU)
        self.quantityItemQuantity = 2
        self.quantityScanned = checkout.Items.ScannedItem(self.quantityItem,2)

        self.weightItemName = "Beef"
        self.weightItemPPU = 4.09
        self.weightItemWeight = 1.59
        self.weightItem = checkout.Items.Item(self.weightItemName, self.weightItemPPU)
        self.weightScanned = checkout.Items.ScannedWeightedItem(self.weightItem, self.weightItemWeight)
        
        self.weightQtyName = "Apples"
        self.weightQtyPPU = 0.69
        self.weightQtyItemWeight = 1.59
        self.weightQtyItemQuantity = 4
        self.weightQtyItem = checkout.Items.Item(self.weightQtyName, self.weightQtyPPU)
        self.weightQtyScanned = checkout.Items.ScannedWeightedItem(self.weightQtyItem, self.weightQtyItemWeight, self.weightQtyItemQuantity)

        self.inventory = checkout.Items.Inventory()
        self.inventory.addItem(self.singleItem)


        self.scannedItemContainer = checkout.Items.ScannedItemContainer()

    def tearDown(self):
        pass


    def testItemConstruction(self):
        self.assertEqual(self.singleItem.name, self.singleItemName, "Name not set")
        self.assertEqual(self.singleItem.pricePerUnit, self.singleItemPPU, "Price per unit not set")
        
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
        itemNameToGet = "Soup"
        returnedItem = self.inventory.getItemByName(itemNameToGet)
        self.assertEqual(returnedItem.name, itemNameToGet, "Inventory did not return %s" % (itemNameToGet))

    def testScannedItemWithQuantityConstruction(self):
        quantity = 2
        checkout.Items.ScannedItem(self.quantityItem, quantity)
        with self.assertRaises(checkout.Items.ScannedQuantityNotIntegerException):
            checkout.Items.ScannedItem(self.quantityItem, 1.2)
            
    def testScannedItemTotalQuantity(self):
        self.assertEqual(self.singleScanned.getTotalQuantity(), 1, "Single TotalQuantity Failed")
        self.assertEqual(self.quantityScanned.getTotalQuantity(), self.quantityItemQuantity, "Multiple TotalQuantity Failed")
        self.assertEqual(self.weightScanned.getTotalQuantity(), self.weightItemWeight, "Weighted TotalQuantity Failed")
        self.assertEqual(self.weightQtyScanned.getTotalQuantity(), self.weightQtyItemWeight*self.weightQtyItemQuantity, "Multiple Weighted TotalQuantity Failed")

    def testScannedItemByWeightConstruction(self):
        weight = 1.09
        checkout.Items.ScannedWeightedItem(self.weightItem, weight, 1)
        with self.assertRaises(checkout.Items.ScannedWeightNotFloatException):
            checkout.Items.ScannedWeightedItem(self.weightItem, 2)

    def testScannedItemByWeightGetWeight(self):
        self.assertAlmostEqual(self.weightScanned.getWeight(), self.weightItemWeight, 1e-3, "Weight %f not close enough" % self.weightItemWeight)
        
    def testScannedItemQuantityRetreival(self):
        messageForm = "Quantity %f not found"
        
        testCases = [ (self.singleScanned, 1), (self.weightScanned, 1)]
        
        for scanned, quantity in testCases:
            self.assertEqual(scanned.getQuantity(), quantity, messageForm % quantity)

    def testScannedBaseItemNameAndPrices(self):
        nameMessageForm = "%s not found"
        priceMessageForm = "Price %f not returned"

        testCases = [ (self.singleScanned,   self.singleItemName,   self.singleItemPPU),\
                      (self.quantityScanned, self.quantityItemName, self.quantityItemPPU)]
        for scanned, name, price in testCases:
            self.assertEqual(scanned.getName(),      name,  nameMessageForm %(name))
            self.assertEqual(scanned.getBasePrice(), price, priceMessageForm %(price))

    def testScannedMarkdownPrice(self):
        messageForm = "Markdown price %f not found"
        
        testCases = [ (self.singleScanned,   self.singleItemPPU),\
                      (self.quantityScanned, self.quantityItemPPU*self.quantityItemQuantity),
                      (self.weightScanned,   self.weightItemPPU*self.weightItemWeight) ]
        
        for scanned, markdown in testCases:
            self.assertEqual(scanned.getMarkdownPrice(), markdown, messageForm % markdown)
            
    def testScannedDiscountPrice(self):
        messageForm = "Discount price %f not found"
        
        testCases = [ (self.singleScanned,   self.singleItemPPU),\
                      (self.quantityScanned, self.quantityItemPPU*self.quantityItemQuantity),
                      (self.weightScanned,   self.weightItemPPU*self.weightItemWeight)]
        
        for scanned, discountPrice in testCases:
            self.assertEqual(scanned.getDiscountPrice(), discountPrice, messageForm % discountPrice)
            
    def testScannedItemContainer(self):
        checkout.Items.ScannedItemContainer()

    def testScannedItemContainerGetSize(self):
        self.assertEqual(self.scannedItemContainer.getSize(), 0, "ScannedItemContainer not empty")
        
    def testScannedItemContainerGetIndex(self):
        aScannedItemContainer = checkout.Items.ScannedItemContainer()
        aScannedItemContainer.addScannedItem(self.weightScanned)
        aScannedItemContainer.addScannedItem(self.quantityScanned)
        
        testCases = [self.weightScanned.getName(), self.quantityScanned.getName()]
        messageForm =  "Scanned item name at index %d not %s"
        
        for i in range(len(testCases)):   
            scannedItem = aScannedItemContainer.getAt(i)
            caseName = testCases[i]
            self.assertEqual(scannedItem.getName(), caseName, messageForm % (i,caseName))
        
    def testScannedItemContainerAdd(self):
        sizeBefore = self.scannedItemContainer.getSize()
        self.scannedItemContainer.addScannedItem(self.singleScanned)
        sizeAfter = self.scannedItemContainer.getSize()
        self.assertEqual(sizeAfter, sizeBefore+1, "ScannedItemContainer size not incremented")

    def testScannedItemContainerRemoveLast(self):
        targetName = self.quantityScanned.getName()
        self.scannedItemContainer.addScannedItem(self.quantityScanned)
        self.scannedItemContainer.addScannedItem(self.singleScanned)
        self.scannedItemContainer.removeLastItem()
        nItems = self.scannedItemContainer.getSize()
        lastItem = self.scannedItemContainer.getAt(nItems-1)
        self.assertEqual(lastItem.getName(), targetName, "ScannedItemContainer not removing last item correctly")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()