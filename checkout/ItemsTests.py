import unittest
import checkout.Items

class ItemsTest(unittest.TestCase):
    
    def setUp(self):
        self.countableItemName = "Soup"
        self.countableItemPPU = 1.25
        self.countableItem = checkout.Items.Item(self.countableItemName, self.countableItemPPU)
        self.countableScanned = checkout.Items.ScannedItem(self.countableItem)

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

    def testItemBaseConstruction(self):
        self.assertEqual(self.countableItem.name, self.countableItemName, "ItemBase name not set")
        self.assertEqual(self.countableItem.pricePerUnit, self.countableItemPPU, "ItemBase Price per unit not set")
        
    def testItemConstruction(self):
        self.assertIsInstance(self.countableItem, checkout.Items.ItemBase, "Item does not derive from ItemBase")
        
    def testInventoryConstruct(self):
        emptyInventory = checkout.Items.Inventory()
        self.assertEqual(emptyInventory.getSize(), 0, "Initial Inventory not empty")
    
    def testInventoryAddition(self):
        # Need to add unique item to avoid collision of adding existing item
        # which will not increment inventory
        uniqueItem = checkout.Items.Item("Some unique name", 4.0)
        
        sizeBeforeAdding = self.inventory.getSize()
        self.inventory.addItem(uniqueItem)
        self.assertEqual(self.inventory.getSize(), sizeBeforeAdding+1, 
                         "Inventory size not incremented on unique item addition")
        
        self.inventory.addItem(uniqueItem)
        self.assertEqual(self.inventory.getSize(), sizeBeforeAdding+1, 
                         "Inventory size not maintained with identical item addition")      
        
    def testInventoryGetByNameForMissingItem(self):
        with self.assertRaises(checkout.Items.NotFoundInInventoryException):
            self.inventory.getItemByName("Nonsense Item")

    def testInventoryGetByNameForExistingItem(self):
        returnedItem = self.inventory.getItemByName(self.countableItemName)
        self.assertEqual(returnedItem.name, self.countableItemName, 
                         "Inventory did not return %s" % (self.countableItemName))

    def testScannedItemTotalQuantity(self):  
        testCases = [(self.countableScanned,                         1,           "countable"), 
                     ( self.weightedScanned,   self.weightedItemWeight,    "item with weight")]
        
        for (item, expectedTotalQuantity, caseName) in testCases:
            failMessage = "Unexpected Scanned getQuantity() for %s" % (caseName)
            self.assertEqual(item.getQuantity(), expectedTotalQuantity, failMessage)

    def testScannedItemConstruction(self):
        self.assertIsInstance(self.countableScanned, checkout.Items.ScannedItem,     "No such class as ScannedItem")
        self.assertIsInstance(self.countableScanned, checkout.Items.ScannedItemBase, 
                              "ScannedItem does not derive from ScannedItemBase")

    def testWeightedItemConstruction(self):
        weightedItem = checkout.Items.WeightedItem("Chicken", 4.9)
        self.assertIsInstance(weightedItem, checkout.Items.ItemBase, "WeightedItem not a subclass of ItemBase")

    def testScannedItemByWeightConstruction(self):
        checkout.Items.ScannedWeightedItem(self.weightedItem, weight = 1.09)
    
    def testScannedItemByWeightConstructionFailsWithIntegerWeight(self):
        with self.assertRaises(checkout.Items.ScannedWeightNotFloatException):
            checkout.Items.ScannedWeightedItem(self.weightedItem, weight = 1)

    def testScanNonWeightedItemWithWeightConstruction(self):
        with self.assertRaises(checkout.Items.ScannedNonWeightedItemWithWeight):        
            checkout.Items.ScannedWeightedItem(self.countableItem, weight = 4.09)
            
    def testScanWeightedItemWithoutWeight(self):
        with self.assertRaises(checkout.Items.ScannedWeightedItemWithoutWeight):
            checkout.Items.ScannedItem(self.weightedItem)

    def testScannedItemByWeightGetWeight(self):
        errorMessage = "Weight %f not close enough to %f " % (self.weightedItemWeight, self.weightedScanned.getWeight())
        self.assertAlmostEqual(self.weightedScanned.getWeight(), self.weightedItemWeight, 3, errorMessage )

    def testScannedItemNameAndPrices(self):
        nameMessageForm  = "ScannedItem name %s not set"
        priceMessageForm = "ScannedItem basePrice %f not returned"

        testCases = [(self.countableScanned, self.countableItemName, self.countableItemPPU),
                     ( self.weightedScanned,  self.weightedItemName,  self.weightedItemPPU)]
        
        for scanned, name, price in testCases:
            self.assertEqual(scanned.getName(),       name,  nameMessageForm %(name))
            self.assertEqual(scanned.getBasePrice(), price, priceMessageForm %(price))

    def testScannedMarkdownPrice(self):
        messageForm = "ScannedItem markdown price %f not set"
        
        testCases = [ (self.countableScanned, self.countableItemPPU),
                      ( self.weightedScanned, self.weightedItemPPU*self.weightedItemWeight) ]
        
        for scanned, markdown in testCases:
            self.assertEqual(scanned.getMarkdownPrice(), markdown, messageForm % markdown)
            
    def testScannedDiscountPrice(self):
        messageForm = "ScannedItem discount price %f not set"
        
        testCases = [ (self.countableScanned,  self.countableItemPPU),
                      ( self.weightedScanned,  self.weightedItemPPU*self.weightedItemWeight)]
        
        for scanned, discountPrice in testCases:
            self.assertEqual(scanned.getDiscountPrice(), discountPrice, messageForm % discountPrice)
            
    def testScannedItemContainer(self):
        checkout.Items.ScannedItemContainer()

    def testScannedItemContainerGetSize(self):
        self.assertEqual(self.scannedItemContainer.getSize(), 0, "Initial ScannedItemContainer not empty")
        
    def testScannedItemContainerGetIndex(self):
        testCaseItems = [self.weightedScanned, self.countableScanned, self.countableScanned]
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
        self.scannedItemContainer.addScannedItem(self.countableScanned)
        sizeAfter = self.scannedItemContainer.getSize()
        self.assertEqual(sizeAfter, sizeBefore+1, "ScannedItemContainer size not incremented on add")

    def testGetLastItemFromScannedItemContainer(self):
        itemsToAdd = [self.weightedScanned, self.countableScanned, self.countableScanned]
        
        for item in itemsToAdd:
            self.scannedItemContainer.addScannedItem(item)
            lastItem = self.scannedItemContainer.getLastItem()
            self.assertEqual(item.getName(), lastItem.getName(), "ScannedItemContainer incorrect last item returned")


    def testScannedItemContainerRemoveLast(self):
        targetName = self.countableScanned.getName()
        
        self.scannedItemContainer.addScannedItem(self.countableScanned)
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
        self.scannedItemContainer.addScannedItem(self.countableScanned)
        self.scannedItemContainer.addScannedItem(self.weightedScanned)
        self.scannedItemContainer.removeAt(0)

        lastItem = self.scannedItemContainer.getLastItem()
        self.assertEqual(lastItem.getName(), self.weightedItemName, 
                         "ScannedItemContainer removeAt Did not remove correct item")

    def testScannedItemContainerUsesDeepCopyOfScannedItems(self):
        mutableScannedItem = checkout.Items.ScannedItem(self.countableItem)
        self.scannedItemContainer.addScannedItem(mutableScannedItem)
        originalItem = self.scannedItemContainer.getLastItem()
        
        adjustedDiscountPrice = 0.01
        mutableScannedItem.discountPrice = adjustedDiscountPrice
        self.scannedItemContainer.addScannedItem(mutableScannedItem)

        self.assertNotEqual(originalItem.getDiscountPrice(), adjustedDiscountPrice, 
                            "ScannedItemContainer item with adjusted price propagated to other items")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()