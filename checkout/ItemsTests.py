import unittest
import checkout.Items

class ItemsTest(unittest.TestCase):
    
    def setUp(self):
        self.countableItemName = "Soup"
        self.countableItemPPU = 1.25
        self.countableItem = checkout.Items.Item(self.countableItemName, self.countableItemPPU)
        self.singleScanned = checkout.Items.ScannedItem(self.countableItem)

        self.weightedItemName = "Beef"
        self.weightedItemPPU = 4.09
        self.weightedItemWeight = 1.59
        self.weightedItem = checkout.Items.WeightedItem(self.weightedItemName, self.weightedItemPPU)
        self.weightedScanned = checkout.Items.ScannedWeightedItem(self.weightedItem, self.weightedItemWeight)

        self.inventory = checkout.Items.Inventory()
        self.inventory.addItem(self.countableItem)

        self.scannedItemContainer = checkout.Items.ScannedItemContainer()

    def tearDown(self):
        pass


    def testItemConstruction(self):
        self.assertEqual(self.countableItem.name, self.countableItemName, "Name not set")
        self.assertEqual(self.countableItem.pricePerUnit, self.countableItemPPU, "Price per unit not set")
        
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
        
        self.inventory.addItem(uniqueItem)
        self.assertEqual(self.inventory.getSize(), beforeSize+1, "Inventory size not maintained with identical item")      
        
    def testInventoryGet(self):
        with self.assertRaises(checkout.Items.NotFoundInInventoryException):
            self.inventory.getItemByName("Nonsense Item")
        itemNameToGet = "Soup"
        returnedItem = self.inventory.getItemByName(itemNameToGet)
        self.assertEqual(returnedItem.name, itemNameToGet, "Inventory did not return %s" % (itemNameToGet))

            
    def testScannedItemTotalQuantity(self):  
        testCases = [ (self.singleScanned,      1,                          "single"), 
                      (self.weightedScanned,    self.weightedItemWeight,    "item with weight")]
        
        for (item, expectedTotalQuantity, caseName) in testCases:
            failMessage = "Unexpected TotalQuantity for %s" % (caseName)
            self.assertEqual(item.getQuantity(), expectedTotalQuantity, failMessage)

    def testWeightedItemConstruction(self):
        weightedItem = checkout.Items.WeightedItem("Chicken", 4.9)
        self.assertIsInstance(weightedItem, checkout.Items.Item, "WeightedItem not a subclass")


    def testScannedItemByWeightConstruction(self):
        weight = 1.09
        checkout.Items.ScannedWeightedItem(self.weightedItem, weight)
        with self.assertRaises(checkout.Items.ScannedWeightNotFloatException):
            checkout.Items.ScannedWeightedItem(self.weightedItem, 1)

    def testScanUnweightedItemByWeightConstruction(self):
        weight = 4.09
        with self.assertRaises(checkout.Items.ScannedNonWeightedItemWithWeight):        
            checkout.Items.ScannedWeightedItem(self.countableItem, weight)

    def testScannedItemByWeightGetWeight(self):
        errorMessage = "Weight %f not close enough to %f " % (self.weightedItemWeight, self.weightedScanned.getWeight())
        self.assertAlmostEqual(self.weightedScanned.getWeight(), self.weightedItemWeight, 1e-3, errorMessage )
        

    def testScannedBaseItemNameAndPrices(self):
        nameMessageForm = "%s not found"
        priceMessageForm = "Price %f not returned"

        testCases = [ (self.singleScanned,   self.countableItemName,   self.countableItemPPU),
                      (self.weightedScanned, self.weightedItemName, self.weightedItemPPU) ]
        
        for scanned, name, price in testCases:
            self.assertEqual(scanned.getName(),      name,  nameMessageForm %(name))
            self.assertEqual(scanned.getBasePrice(), price, priceMessageForm %(price))

    def testScannedMarkdownPrice(self):
        messageForm = "Markdown price %f not found"
        
        testCases = [ (self.singleScanned,    self.countableItemPPU),\
                      (self.weightedScanned,  self.weightedItemPPU*self.weightedItemWeight) ]
        
        for scanned, markdown in testCases:
            self.assertEqual(scanned.getMarkdownPrice(), markdown, messageForm % markdown)
            
    def testScannedDiscountPrice(self):
        messageForm = "Discount price %f not found"
        
        testCases = [ (self.singleScanned,   self.countableItemPPU),\
                      (self.weightedScanned,   self.weightedItemPPU*self.weightedItemWeight)]
        
        for scanned, discountPrice in testCases:
            self.assertEqual(scanned.getDiscountPrice(), discountPrice, messageForm % discountPrice)
            
    def testScannedItemContainer(self):
        checkout.Items.ScannedItemContainer()

    def testScannedItemContainerGetSize(self):
        self.assertEqual(self.scannedItemContainer.getSize(), 0, "ScannedItemContainer not empty")
        
    def testScannedItemContainerGetIndex(self):
        testCaseItems = [self.weightedScanned, self.singleScanned, self.singleScanned]
        testCaseNames = [item.getName() for item in testCaseItems]
        
        aScannedItemContainer = checkout.Items.ScannedItemContainer()
        for testItem in testCaseItems:
            aScannedItemContainer.addScannedItem(testItem)

        messageForm =  "Scanned item name at index %d not %s"
                
        for i in range(len(testCaseItems)):   
            scannedItem = aScannedItemContainer.getAt(i)
            caseName    = testCaseNames[i]
            self.assertEqual(scannedItem.getName(), caseName, messageForm % (i,caseName))
        
    def testScannedItemContainerAdd(self):
        sizeBefore = self.scannedItemContainer.getSize()
        self.scannedItemContainer.addScannedItem(self.singleScanned)
        sizeAfter = self.scannedItemContainer.getSize()
        self.assertEqual(sizeAfter, sizeBefore+1, "ScannedItemContainer size not incremented")

    def testGetLastItemFromScannedItemContainer(self):
        itemsToAdd = [self.weightedScanned, self.singleScanned, self.singleScanned]
        
        for item in itemsToAdd:
            self.scannedItemContainer.addScannedItem(item)
            lastItem = self.scannedItemContainer.getLastItem()
            self.assertEqual(item.getName(), lastItem.getName(), "Incorrect last item returned")


    def testScannedItemContainerRemoveLast(self):
        targetName = self.singleScanned.getName()
        
        self.scannedItemContainer.addScannedItem(self.singleScanned)
        self.scannedItemContainer.addScannedItem(self.weightedScanned)
        self.scannedItemContainer.removeLastItem()
        
        lastItem = self.scannedItemContainer.getLastItem()
        self.assertEqual(lastItem.getName(), targetName, "ScannedItemContainer not removing last item correctly")
 
    def testScannedItemContainerRemoveLastWithEmptyContainer(self):       
        with self.assertRaises(IndexError):
            self.scannedItemContainer.removeLastItem()
            
    def testScanedItemContainerRemoveAtEmptyContainer(self):
        with self.assertRaises(IndexError):
            self.scannedItemContainer.removeAt(4)
            
    def testScanedItemContainerRemoveAt(self):
        self.scannedItemContainer.addScannedItem(self.singleScanned)
        self.scannedItemContainer.addScannedItem(self.weightedScanned)
        self.scannedItemContainer.removeAt(0)

        lastItem = self.scannedItemContainer.getLastItem()
        self.assertEqual(lastItem.getName(), self.weightedItemName, "removeAt Did not remove correct item")

    def testScannedItemContainerUniqueScannedItems(self):
        mutableScannedItem = checkout.Items.ScannedItem(self.countableItem)
        self.scannedItemContainer.addScannedItem(mutableScannedItem)
        originalItem = self.scannedItemContainer.getLastItem()
        
        adjustedDiscountPrice = 0.01
        mutableScannedItem.discountPrice = adjustedDiscountPrice
        self.scannedItemContainer.addScannedItem(mutableScannedItem)

        self.assertNotEqual(originalItem.getDiscountPrice(), adjustedDiscountPrice, "Adjusted price propagated to other items")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()