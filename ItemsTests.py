

import unittest
import checkout.Items
from sqlalchemy.testing.util import fail

class ItemsTest(unittest.TestCase):
    
    def setUp(self):
        self.singleItemName = "Soup"
        self.singleItemPPU = 1.25
        self.singleItem = checkout.Items.Item(self.singleItemName, self.singleItemPPU)
        self.singleScanned = checkout.Items.ScannedItem(self.singleItem)

        self.countableItemName = "Cereal"
        self.countableItemPPU = 5.25
        self.countableItem = checkout.Items.Item(self.countableItemName, self.countableItemPPU)
        self.countableItemQuantity = 2
        self.countableScanned = checkout.Items.ScannedItem(self.countableItem,2)

        self.weightedItemName = "Beef"
        self.weightedItemPPU = 4.09
        self.weightedItemWeight = 1.59
        self.weightedItem = checkout.Items.Item(self.weightedItemName, self.weightedItemPPU)
        self.weightedScanned = checkout.Items.ScannedWeightedItem(self.weightedItem, self.weightedItemWeight)
        
        self.weightedQtyName = "Apples"
        self.weightedQtyPPU = 0.69
        self.weightedQtyItemWeight = 1.59
        self.weightedQtyItemQuantity = 4
        self.weightedQtyItemTotal = self.weightedQtyItemWeight*self.weightedQtyItemQuantity
        self.weightedQtyItem = checkout.Items.Item(self.weightedQtyName, self.weightedQtyPPU)
        self.weightedQtyScanned = checkout.Items.ScannedWeightedItem(self.weightedQtyItem, self.weightedQtyItemWeight, self.weightedQtyItemQuantity)

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
        checkout.Items.ScannedItem(self.countableItem, quantity)
        with self.assertRaises(checkout.Items.ScannedQuantityNotIntegerException):
            checkout.Items.ScannedItem(self.countableItem, 1.2)
            
    def testScannedItemTotalQuantity(self):  
        testCases = [ (self.singleScanned,      1,                          "single"), 
                      (self.countableScanned,   self.countableItemQuantity, "item with quantity"),
                      (self.weightedScanned,    self.weightedItemWeight,    "item with weight"),
                      (self.weightedQtyScanned, self.weightedQtyItemTotal,  "item with weight and quantity" )]
        
        for (item, expectedTotalQuantity, caseName) in testCases:
            failMessage = "Unexpected TotalQuantity for %s" % (caseName)
            self.assertEqual(item.getTotalQuantity(), expectedTotalQuantity, failMessage)


    def testScannedItemByWeightConstruction(self):
        weight = 1.09
        checkout.Items.ScannedWeightedItem(self.weightedItem, weight, 1)
        with self.assertRaises(checkout.Items.ScannedWeightNotFloatException):
            checkout.Items.ScannedWeightedItem(self.weightedItem, 2)

    def testScannedItemByWeightGetWeight(self):
        errorMessage = "Weight %f not close enough to %f " % (self.weightedItemWeight, self.weightedScanned.getWeight())
        self.assertAlmostEqual(self.weightedScanned.getWeight(), self.weightedItemWeight, 1e-3, errorMessage )
        
    def testScannedItemQuantityRetreival(self):        
        testCases = [ (self.singleScanned,      1,                            "single item"), 
                      (self.countableScanned,   self.countableItemQuantity,   "countable itmes"),
                      (self.weightedQtyScanned, self.weightedQtyItemQuantity, "weighted countable") ]

        messageForm = "Quantity %d for %s not found"
        
        for (scanned, quantity, caseName) in testCases:
            errorMessage = messageForm % (quantity, caseName)
            self.assertEqual(scanned.getQuantity(), quantity, errorMessage)

    def testScannedBaseItemNameAndPrices(self):
        nameMessageForm = "%s not found"
        priceMessageForm = "Price %f not returned"

        testCases = [ (self.singleScanned,   self.singleItemName,   self.singleItemPPU),\
                      (self.countableScanned, self.countableItemName, self.countableItemPPU)]
        for scanned, name, price in testCases:
            self.assertEqual(scanned.getName(),      name,  nameMessageForm %(name))
            self.assertEqual(scanned.getBasePrice(), price, priceMessageForm %(price))

    def testScannedMarkdownPrice(self):
        messageForm = "Markdown price %f not found"
        
        testCases = [ (self.singleScanned,    self.singleItemPPU),\
                      (self.countableScanned, self.countableItemPPU*self.countableItemQuantity),
                      (self.weightedScanned,  self.weightedItemPPU*self.weightedItemWeight) ]
        
        for scanned, markdown in testCases:
            self.assertEqual(scanned.getMarkdownPrice(), markdown, messageForm % markdown)
            
    def testScannedDiscountPrice(self):
        messageForm = "Discount price %f not found"
        
        testCases = [ (self.singleScanned,   self.singleItemPPU),\
                      (self.countableScanned, self.countableItemPPU*self.countableItemQuantity),
                      (self.weightedScanned,   self.weightedItemPPU*self.weightedItemWeight)]
        
        for scanned, discountPrice in testCases:
            self.assertEqual(scanned.getDiscountPrice(), discountPrice, messageForm % discountPrice)
            
    def testScannedItemContainer(self):
        checkout.Items.ScannedItemContainer()

    def testScannedItemContainerGetSize(self):
        self.assertEqual(self.scannedItemContainer.getSize(), 0, "ScannedItemContainer not empty")
        
    def testScannedItemContainerGetIndex(self):
        aScannedItemContainer = checkout.Items.ScannedItemContainer()
        aScannedItemContainer.addScannedItem(self.weightedScanned)
        aScannedItemContainer.addScannedItem(self.countableScanned)
        
        testCases = [self.weightedScanned.getName(), self.countableScanned.getName()]
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
        targetName = self.countableScanned.getName()
        self.scannedItemContainer.addScannedItem(self.countableScanned)
        self.scannedItemContainer.addScannedItem(self.singleScanned)
        self.scannedItemContainer.removeLastItem()
        nItems = self.scannedItemContainer.getSize()
        lastItem = self.scannedItemContainer.getAt(nItems-1)
        self.assertEqual(lastItem.getName(), targetName, "ScannedItemContainer not removing last item correctly")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()