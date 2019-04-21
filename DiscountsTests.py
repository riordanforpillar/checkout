import unittest
import checkout.Discounts
import checkout.Items
from checkout.Discounts import PercentOffSpecial

class DiscountsTest(unittest.TestCase):
    
    def setUp(self):
        self.countableMarkdownValue = 0.40
        self.countableItem = checkout.Items.Item("Cereal", 4.25)
        self.countableScanned = checkout.Items.ScannedItem(self.countableItem)
        self.countableMarkdown = checkout.Discounts.Markdown(self.countableItem, self.countableMarkdownValue)
        
        self.weightedMarkdownValue = 0.1
        self.weightedItemWeight = 3.5
        self.weightedItem = checkout.Items.Item("Beef", 2.0)
        self.weightedScanned = checkout.Items.ScannedWeightedItem(self.weightedItem, self.weightedItemWeight)
        self.weightedMarkdown = checkout.Discounts.Markdown(self.weightedItem, self.weightedMarkdownValue)
        
        self.scannedItems = self.makeScannedSet(1, 1)
        self.addNToScanned(self.scannedItems, self.countableScanned, 6)
        
        self.discount = checkout.Discounts.Discount(self.countableItem)
        
        self.buy3 = 3
        self.get1 = 1
        self.seventyPercentOff = 70.0
        self.buy3get1Special = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, self.buy3, self.get1, self.seventyPercentOff)

        self.buy2Get1FreeSpecial = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, 2, 1, 100.0)

        self.buy3price = 5.0
        self.buy3For5DollarsSpecial = checkout.Discounts.BuyNForXSpecial(self.countableItem, self.buy3, self.buy3price)

    def tearDown(self):
        pass
    
    def makeScannedSet(self, nCountable, nWeighted):
        scannedSet = checkout.Items.ScannedItemContainer()
        
        self.addNToScanned(scannedSet, self.countableScanned, nCountable)
        self.addNToScanned(scannedSet, self.weightedScanned, nWeighted)
                
        return scannedSet
    
    def addNToScanned(self, scannedItems, itemToAdd, nToAdd ):
        for _ in range(nToAdd):
            scannedItems.addScannedItem(itemToAdd)
    
    def testDiscountConstructor(self):
        checkout.Discounts.Discount(self.countableItem)
    
    def testDiscountApply(self):
        self.discount.applyTo(self.scannedItems)
        
    def testMarkdownConstructor(self):
        checkout.Discounts.Markdown(self.countableItem, 5.00)
        checkout.Discounts.Markdown(self.countableItem, 0.30)
        
    def MarkdownConstructionTest(self, value):
        aMarkdown = checkout.Discounts.Markdown(self.countableItem, value)
        self.assertEqual(aMarkdown.value, value, "Markdown value not set")
        self.assertEqual(aMarkdown.itemToDiscount.name, self.countableItem.name, "Markdown name not set")
        self.assertIsInstance(aMarkdown, checkout.Discounts.Discount, "Markdown is not a Discount subclass")
        
    def testGetMatchedItems(self):
        scanned = self.makeScannedSet(7,3)
        self.compareGetMatchedItems(scanned, 7)
        
        emptyScanned = checkout.Items.ScannedItemContainer()        
        self.compareGetMatchedItems(emptyScanned, 0)
        

    def compareGetMatchedItems(self, scannedSet, expectedMatchedLength):
        matchedItems = self.discount.getMatchedItems(scannedSet)
        self.assertEqual(len(matchedItems), expectedMatchedLength, "Matched items length doesn't match expected")       
        

    def testSpecialMatchItem(self):
        self.assertTrue(self.buy2Get1FreeSpecial.itemMatchesDiscount(self.countableScanned), "Markdown did not match scanned item")
        self.assertFalse(self.buy2Get1FreeSpecial.itemMatchesDiscount(self.weightedScanned), "Markdown matched scanned item incorrectly")
        
    def testMarkdownApplicationOnItem(self):
        self.countableMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(0)
        targetPrice = self.calculateDiscountedPrice(self.countableScanned.getBasePrice(), self.countableMarkdownValue, 1.0)
        self.assertEqual(scannedItem.getMarkdownPrice(), targetPrice, "Countable markdown not applied")
        
    def testMarkdownApplicationNotOnItem(self):
        self.countableMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(1)
        targetPrice = self.calculateDiscountedPrice(self.weightedScanned.getBasePrice(), 0.0, self.weightedItemWeight)
        self.assertEqual(scannedItem.getMarkdownPrice(), targetPrice, "Markdown misapplied")
        
    def testMultipleMarkdownApplicationNotUndoingPreviousMarkdowns(self):
        self.countableMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(0)
        unchangedPrice = scannedItem.getMarkdownPrice()
        
        self.weightedMarkdown.applyTo(self.scannedItems)        
        self.assertEqual(scannedItem.getMarkdownPrice(), unchangedPrice, "Countable markdown undone")
        
    def testMarkdownOnWeighted(self):
        self.weightedMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(1)
        newPrice = self.calculateDiscountedPrice(self.weightedScanned.getBasePrice(), self.weightedMarkdownValue, self.weightedItemWeight)
        self.assertEqual(scannedItem.getMarkdownPrice(), newPrice, "Weighted markdown misapplied")
        
    def calculateDiscountedPrice(self, basePrice, discountToApply, weight=1):
        discountedPPU = basePrice-discountToApply
        discountedPrice = discountedPPU*weight
        return discountedPrice
    
    def testSpecialPartitionAroundLimit(self):
        self.partitionTestRun(3, 8, "7")
        self.partitionTestRun(7, 8, "a")


    def partitionTestRun(self, limit, length, objectInList):
        special = checkout.Discounts.Special(self.countableScanned, limit)
        listToParition = [objectInList]*length
        
        (below, above) = special.partitionAroundLimit(listToParition)
        self.assertEqual(len(below), limit,        "Paritioned number below limit not equal to limit")
        self.assertEqual(len(above), length-limit, "Paritioned number above limit not equal to remaining")
        self.assertEqual(below[0],   objectInList, "List returned not original")
  
    def testSpecialPartitionAroundLimitWithEmptySpecial(self):
        limit = 4
        special = checkout.Discounts.Special(self.countableScanned, limit)
        (below, _) = special.partitionAroundLimit([])
        self.assertEqual(len(below), 0, "Paritioned number of empty list not zero")
        
    def testPercentOffSpecialConstruction(self):
        percentOff = 40.0
        limit = 3
        special = checkout.Discounts.PercentOffSpecial(self.countableItem, percentOff, limit)
        self.assertEqual(special.seventyPercentOff, percentOff, "PercentOff Special percent off not set")
        self.assertEqual(special.limit, limit, "PercentOff Special limit not set")
        
        self.assertIsInstance(special, checkout.Discounts.Special, "PercentOff not a subclass of Special")
        
    def testCalculateDiscountInPercentOffSpecial(self):
        self.PercentOffTestFactory(40.0)
        self.PercentOffTestFactory(10.0)
        
    def PercentOffTestFactory(self, percentOff):
        special = checkout.Discounts.PercentOffSpecial(self.countableItem, percentOff)
        discountPrice = special.calculateDiscount(self.countableScanned)
        expectedDiscountPrice = self.countableScanned.getMarkdownPrice()*(1.0-0.01*percentOff)
        self.assertEqual(discountPrice, expectedDiscountPrice, "PercentOffSpecial discount calculator gives wrong price")
        
    def testBuyNGetMForPercentOffConstruction(self):
        self.BuyNGetMForPercentOffConstructCheck(1, 1, 100.0)
        self.BuyNGetMForPercentOffConstructCheck(3, 4, 100.0)
        self.assertIsInstance(self.buy2Get1FreeSpecial, checkout.Discounts.PercentOffSpecial, "Not subclass of PercentOffSpecial")

        
    def BuyNGetMForPercentOffConstructCheck(self, buyN, getM, percentOff):
        special = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, buyN, getM, percentOff)
        self.assertEqual(special.buy3, buyN, "Buy N not set correctly")
        self.assertEqual(special.get1, getM, "Get M not set correctly")
        self.assertEqual(special.seventyPercentOff, percentOff, "Percent off not set correctly")        

    def testBuy3Get1ForPercentOffApplication(self):
        self.buy3get1Special.applyTo(self.scannedItems)
        specialItem = self.scannedItems.getAt(4)
        self.assertAlmostEqual(specialItem.getMarkdownPrice()*(1.0-self.seventyPercentOff*0.01), specialItem.getDiscountPrice(), 3, "Buy3Get1For70PercentOff Special not applied")
    
    def testBuy2Get1FreeApplication(self):    
        self.buy2Get1FreeSpecial.applyTo(self.scannedItems)
        specialItem = self.scannedItems.getAt(3)
        self.assertAlmostEqual(0.0, specialItem.getDiscountPrice(), 3, "Buy2Get1Free Special not applied")
        
    def testBuyNGetMForPercentOffApplicationRecalculateNonSpecialItem(self):
        modifiedSpecialItem = self.scannedItems.getAt(0)
        self.mangleDiscountPrice(modifiedSpecialItem)
        self.buy3get1Special.applyTo(self.scannedItems)       
        self.assertAlmostEqual(modifiedSpecialItem.getMarkdownPrice(), modifiedSpecialItem.getBasePrice(), 3, "Undiscounted price not recalculated")
 
    def testBuyNGetMForPercentOffApplicationOnNonSpecialItem(self):
        self.buy3get1Special.applyTo(self.scannedItems)     
        unSpecialItem = self.scannedItems.getAt(5)
        self.assertEqual(unSpecialItem.getMarkdownPrice(), unSpecialItem.getDiscountPrice(), "Markdown and special price do not match for nonspecial item")

    def testBuyNGetMForPercentOffPastLimitApplication(self):
        buy2Get1FreeLimit3Special = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, 2, 1, 100.0, 3)
        nonDiscountedItem = self.scannedItems.getAt(6)
        
        self.mangleDiscountPrice(nonDiscountedItem)

        buy2Get1FreeLimit3Special.applyTo(self.scannedItems)
        self.assertEqual(nonDiscountedItem.getMarkdownPrice(), nonDiscountedItem.getDiscountPrice(), "Markdown and special price do not match for discounted item but past limit")

    def mangleDiscountPrice(self, item):
        item.discountPrice = item.discountPrice*5.21
       

    def testBuyNGetMForPercentOffValidDiscountCheck(self):
        self.assertTrue( self.buy2Get1FreeSpecial.isDiscountPosition(2))
        self.assertFalse(self.buy2Get1FreeSpecial.isDiscountPosition(0))

        self.assertFalse(self.buy3get1Special.isDiscountPosition(2))

    def testBuyNForXConstruction(self):
        self.BuyNForXConstructCheck(3, 5.0)
        self.BuyNForXConstructCheck(5, 2.2)
        self.assertIsInstance(self.buy3For5DollarsSpecial, checkout.Discounts.Special, "BuyNForX not a subclass of Special")
        
    def BuyNForXConstructCheck(self, buyN, price):
        special = checkout.Discounts.BuyNForXSpecial(self.countableItem, buyN, price )
        self.assertEqual(special.buy3, buyN, "Buy N not set correctly")
        self.assertEqual(special.price, price, "Price not set correctly")
        
    def testBuyNForXApplicationZeroingOut(self):
        self.buy3For5DollarsSpecial.applyTo(self.scannedItems)
        zeroedItem = self.scannedItems.getAt(0)
        self.assertEqual(zeroedItem.getDiscountPrice(), 0.0, "Zeroed item not zeroed")

    def testBuyNForXApplicationSetPrice(self):
        self.buy3For5DollarsSpecial.applyTo(self.scannedItems)
        sumPriceItem = self.scannedItems.getAt(3)
        self.assertEqual(sumPriceItem.getDiscountPrice(), self.buy3price, "Summed discount not applied")

    def testBuyNForXApplicationToPartialSet(self):
        subThresholdScan = self.makeScannedSet(2, 3)
        
        nonZeroedItem = subThresholdScan.getAt(0)
        self.mangleDiscountPrice(nonZeroedItem)
        self.buy3For5DollarsSpecial.applyTo(subThresholdScan)
        
        self.assertEqual(nonZeroedItem.getDiscountPrice(), nonZeroedItem.getMarkdownPrice(), "Nonzeroed item wrong price")
        
    def testBuyNForXLimitApplication(self):
        limit = 3
        price = 5.00
        buy3ForXLimit3Special = checkout.Discounts.BuyNForXSpecial(self.countableItem, self.buy3, price, limit)
        buy3ForXLimit3Special.applyTo(self.scannedItems)
        nonDiscountedItem = self.scannedItems.getAt(4)
        self.assertAlmostEqual(nonDiscountedItem.getDiscountPrice(), nonDiscountedItem.getMarkdownPrice(), 3, "BuyNForX Limit not used")
    
    def testGetNFullSetsForBuyNForXSpecial(self):
        self.runFullSetCalcForN(10)
        self.runFullSetCalcForN(20)
        
    def runFullSetCalcForN(self, nMatched):
        dummySet = [0]*nMatched
        nSets = self.buy3For5DollarsSpecial.calcNumberOfFullSets(dummySet)
        self.assertEqual(nSets, int(nMatched/self.buy3), "Number of sets incorrect")
        
    def testIsPricePositionForBuyNForXSpecial(self):
        self.assertFalse(self.buy3For5DollarsSpecial.isPricePosition(0),           "Zeroed position for BuyNForXSpecial misidentified")
        self.assertTrue( self.buy3For5DollarsSpecial.isPricePosition(self.buy3-1), "Price position for BuyNForXSpecial misidentified")
        self.assertFalse(self.buy3For5DollarsSpecial.isPricePosition(4),           "Zeroed position for BuyNForXSpecial misidentified")
    
    def testPartitionFullAndLeftoversforBuyNForXSpecial(self):
        self.runPartitionForFullAndLeftovers(3, 8, 'a')
        self.runPartitionForFullAndLeftovers(2, 3, 'b')
        
    def runPartitionForFullAndLeftovers(self, buyN, testLength, itemObject):
        special = checkout.Discounts.BuyNForXSpecial(self.countableItem, buyN, 0.0)
        dummy = [itemObject]*testLength
        (full, left) = special.partitionFullAndLeftovers(dummy)
        self.assertEqual(len(full), buyN*int(testLength/buyN), "Full set not right size")
        self.assertEqual(len(left), testLength - buyN*int(testLength/buyN), "Leftover set not right size")
        self.assertEqual(full[0], itemObject, "Full set item output not equal to input")        
        self.assertEqual(left[0], itemObject, "Leftover set item output not equal to input")        
              
    def testBuyNWeightedGetMLesserPercentOffConstruction(self):
        self.BuyNWeightedGetMLesserConstructCheck(3,2,40.0)
        self.BuyNWeightedGetMLesserConstructCheck(2,1,10.0)
        
    def BuyNWeightedGetMLesserConstructCheck(self, buyN, getM, percent):
        special = checkout.Discounts.BuyNWeightedGetMEqualOrLesserPercentOff(self.weightedItem, buyN, getM, percent)
        self.assertEqual(special.buy3, buyN, "Buy N for weighted special not set")
        self.assertEqual(special.get1, getM, "Get M for weighted special not set")
        self.assertEqual(special.seventyPercentOff, percent, "Percent off for weighted special not set") 
        self.assertIsInstance(special, PercentOffSpecial, "BuyN for weighted not a subclass of PercentOffSpecial")   
            
    def testBuyNWeightedGetMLesserPercentOffApplication(self):
        discount = 40.0
        special = checkout.Discounts.BuyNWeightedGetMEqualOrLesserPercentOff(self.weightedItem, 3, 2, discount)
        
        scannedItems = checkout.Items.ScannedItemContainer()
        
 #      [MMMMHLMM]
        for _ in range(4):
            scannedItems.addScannedItem(self.weightedScanned)
        
        
        heavyScannedItem = checkout.Items.ScannedWeightedItem(self.weightedItem, 5.5)
        scannedItems.addScannedItem(heavyScannedItem)
        
        lightScannedItem = checkout.Items.ScannedWeightedItem(self.weightedItem, 0.5)
        scannedItems.addScannedItem(lightScannedItem)
        
        for _ in range(2):
            scannedItems.addScannedItem(self.weightedScanned)     
        special.applyTo(scannedItems)
        
        discountedItem = scannedItems.getAt(2)
        self.assertEqual(discountedItem.getDiscountPrice(), discountedItem.getMarkdownPrice()*(1.0-discount*0.01), "Discount not applied")
        
        special = checkout.Discounts.BuyNWeightedGetMEqualOrLesserPercentOff(self.weightedItem, 2, 1, discount)
        special.applyTo(scannedItems)
        discountedItem = scannedItems.getAt(1)
        self.assertEqual(discountedItem.getDiscountPrice(), discountedItem.getMarkdownPrice()*(1.0-discount*0.01), "Discount not applied")        
        
        nonDiscountedItem = scannedItems.getAt(2)
        self.assertEqual(nonDiscountedItem.getDiscountPrice(), nonDiscountedItem.getMarkdownPrice(), "Discount misapplied")
        discountedItem = scannedItems.getAt(5)
        self.assertEqual(discountedItem.getDiscountPrice(), discountedItem.getMarkdownPrice(), "Discount misapplied")

    def testBuyNWeightedGetMLesserPercentOffLimit(self):
        discount = 40.0
        limit = 5
        buy2 = 3
        get1 = 2
        special = checkout.Discounts.BuyNWeightedGetMEqualOrLesserPercentOff(self.weightedItem, buy2, get1, discount, limit)
        self.assertEqual(special.limit, limit, "limit not set")
      
        scannedItems = self.makeScannedSet(0, 10)
        special.applyTo(scannedItems)
            
        lastItem = scannedItems.getLastItem()
        self.assertEqual(lastItem.getDiscountPrice(), lastItem.getMarkdownPrice(), "Limit in weighted special not imposed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    
    
    
    