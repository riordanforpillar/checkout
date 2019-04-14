import unittest
import checkout.Discounts
import checkout.Items
from checkout.Discounts import PercentOffSpecial

class DiscountsTest(unittest.TestCase):


    def setUp(self):
        
        self.scannedItems = checkout.Items.ScannedItemContainer()

        self.countableMarkdownValue = 0.40
        self.countableItem = checkout.Items.Item("Cereal", 4.25)
        self.countableScanned = checkout.Items.ScannedItem(self.countableItem)
        self.countableMarkdown = checkout.Discounts.Markdown(self.countableItem, self.countableMarkdownValue)
        
        self.weightedMarkdownValue = 0.1
        self.weightedItemWeight = 3.5
        self.weightedItem = checkout.Items.Item("Beef", 2.0)
        self.weightedScanned = checkout.Items.ScannedWeightedItem(self.weightedItem, self.weightedItemWeight)
        self.weightedMarkdown = checkout.Discounts.Markdown(self.weightedItem, self.weightedMarkdownValue)
        
        self.scannedItems.addScannedItem(self.countableScanned)
        self.scannedItems.addScannedItem(self.weightedScanned)
        for _ in range(6):
            self.scannedItems.addScannedItem(self.countableScanned)
        
        
        self.discount = checkout.Discounts.Discount(self.countableItem)

        
        self.buyN = 3
        self.getM = 1
        self.percentOff = 70.0
        self.buyNgetMSpecial = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, self.buyN, self.getM, self.percentOff)

        self.buy2Get1FreeSpecial = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, 2, 1, 100.0)

        self.buyNprice = 5.0
        self.buyNForXSpecial = checkout.Discounts.BuyNForXSpecial(self.countableItem, self.buyN, self.buyNprice)

    def tearDown(self):
        pass

    def testDiscountConstructor(self):
        aDiscount = checkout.Discounts.Discount(self.countableItem)
    
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
        matchedItems = self.discount.getMatchedItems(self.scannedItems)
        self.assertEqual(len(matchedItems), 7, "Matched items length doesn't match expected")
        
        emptyScanned = checkout.Items.ScannedItemContainer()
        matchedItems = self.discount.getMatchedItems(emptyScanned)
        self.assertEqual(len(matchedItems), 0, "Matched items length doesn't match expected")        
        

    def testSpecialMatchItem(self):
        self.assertTrue(self.buy2Get1FreeSpecial.itemMatchesDiscount(self.countableScanned), "Markdown did not match scanned item")
        self.assertFalse(self.buy2Get1FreeSpecial.itemMatchesDiscount(self.weightedScanned), "Markdown matched scanned item incorrectly")
        
    def testMarkdownApplication(self):
        self.countableMarkdown.applyTo(self.scannedItems)
        scannedItem = self.scannedItems.getAt(0)
        targetPrice = self.countableScanned.getBasePrice() - self.countableMarkdownValue
        self.assertEqual(scannedItem.getMarkdownPrice(), targetPrice, "Countable  markdown not applied")
        scannedItem = self.scannedItems.getAt(1)
        self.assertEqual(scannedItem.getMarkdownPrice(), self.weightedScanned.getBasePrice()*self.weightedItemWeight, "Markdown misapplied")
        
        scannedItem = self.scannedItems.getAt(0)
        unchangedPrice = scannedItem.getMarkdownPrice()
        self.weightedMarkdown.applyTo(self.scannedItems)
        
        self.assertEqual(scannedItem.getMarkdownPrice(), unchangedPrice, "Countable markdown undone")
        
        scannedItem = self.scannedItems.getAt(1)
        
        newPrice = (self.weightedScanned.getBasePrice()-self.weightedMarkdownValue)*self.weightedItemWeight
        self.assertEqual(scannedItem.getMarkdownPrice(), newPrice, "Beef markdown misapplied")
    
    def testSpecialPartitionAroundLimit(self):
        self.partitionTestRun(3, 8, "7")
        self.partitionTestRun(7, 8, "a")

        limit = 4
        special = checkout.Discounts.Special(self.countableScanned, limit)
        (below, _) = special.partitionAroundLimit([])
        self.assertEqual(len(below), 0, "Paritioned number of empty list not zero")

    def partitionTestRun(self, limit, length, objectInList):
        special = checkout.Discounts.Special(self.countableScanned, limit)
        listToParition = [objectInList]*length
        
        (below, above) = special.partitionAroundLimit(listToParition)
        self.assertEqual(len(below), limit,        "Paritioned number below limit not equal to limit")
        self.assertEqual(len(above), length-limit, "Paritioned number above limit not equal to remaining")
        self.assertEqual(below[0],   objectInList, "List returned not original")
        
    def testPercentOffSpecialConstruction(self):
        percentOff = 40.0
        limit = 3
        special = checkout.Discounts.PercentOffSpecial(self.countableItem, percentOff, limit)
        self.assertEqual(special.percentOff, percentOff, "PercentOff Special percent off not set")
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
        self.assertEqual(special.buyN, buyN, "Buy N not set correctly")
        self.assertEqual(special.getM, getM, "Get M not set correctly")
        self.assertEqual(special.percentOff, percentOff, "Percent off not set correctly")        

    def testBuyNGetMForPercentOffApplication(self):
        changedDiscountPrice = 0.01
        modifiedSpecialItem = self.scannedItems.getAt(0)
        modifiedSpecialItem.discountPrice = changedDiscountPrice

        self.buyNgetMSpecial.applyTo(self.scannedItems)
        specialItem = self.scannedItems.getAt(4)
        self.assertAlmostEqual(specialItem.getMarkdownPrice()*(1.0-self.percentOff*0.01), specialItem.getDiscountPrice(), 3, "Special not applied")

        self.assertAlmostEqual(modifiedSpecialItem.getMarkdownPrice(), modifiedSpecialItem.getBasePrice(), 3, "Undiscounted price not recalculated")
        
        unSpecialItem = self.scannedItems.getAt(5)
        self.assertEqual(unSpecialItem.getMarkdownPrice(), unSpecialItem.getDiscountPrice(), "Markdown and special price do not match for nonspecial item")

        self.buy2Get1FreeSpecial.applyTo(self.scannedItems)
        specialItem = self.scannedItems.getAt(3)
        self.assertAlmostEqual(0.0, specialItem.getDiscountPrice(), 3, "Special not applied")


    def testBuyNGetMForPercentOffLimitApplication(self):
        buy2Get1FreeLimit3Special = checkout.Discounts.BuyNGetMForPercentOffSpecial(self.countableItem, 2, 1, 100.0, 3)

        nonDiscountedItem = self.scannedItems.getAt(6)
        changedDiscountPrice = 0.01
        nonDiscountedItem.discountPrice = changedDiscountPrice

        buy2Get1FreeLimit3Special.applyTo(self.scannedItems)
        self.assertEqual(nonDiscountedItem.getMarkdownPrice(), nonDiscountedItem.getDiscountPrice(), "Markdown and special price do not match for nonspecial item past limit")

    def testBuyNGetMForPercentOffValidDiscountCheck(self):
        self.assertTrue( self.buy2Get1FreeSpecial.isDiscountPosition(2))
        self.assertFalse(self.buy2Get1FreeSpecial.isDiscountPosition(0))

        self.assertFalse(self.buyNgetMSpecial.isDiscountPosition(2))



    def testBuyNForXConstruction(self):
        self.BuyNForXConstructCheck(3, 5.0)
        self.BuyNForXConstructCheck(5, 2.2)
        self.assertIsInstance(self.buyNForXSpecial, checkout.Discounts.Special, "BuyNForX not a subclass of Special")
        
    def BuyNForXConstructCheck(self, buyN, price):
        special = checkout.Discounts.BuyNForXSpecial(self.countableItem, buyN, price )
        self.assertEqual(special.buyN, buyN, "Buy N not set correctly")
        self.assertEqual(special.price, price, "Price not set correctly")
        
    def testBuyNForXApplication(self):
        self.buyNForXSpecial.applyTo(self.scannedItems)
        
        zeroedItem = self.scannedItems.getAt(0)
        self.assertEqual(zeroedItem.getDiscountPrice(), 0.0, "Zeroed item not zeroed")

        sumPriceItem = self.scannedItems.getAt(3)

        self.assertEqual(sumPriceItem.getDiscountPrice(), self.buyNprice, "Summed discount not applied")

        subThresholdScan = checkout.Items.ScannedItemContainer()
        subThresholdScan.addScannedItem(self.countableScanned)
        subThresholdScan.addScannedItem(self.countableScanned)
        
        nonZeroedItem = subThresholdScan.getAt(0)
 #       nonZeroedItem.discountPrice = 0.01
        self.buyNForXSpecial.applyTo(subThresholdScan)
        
        self.assertEqual(nonZeroedItem.getDiscountPrice(), nonZeroedItem.getMarkdownPrice(), "Nonzeroed item wrong price")
        
    def testBuyNForXLimitApplication(self):
        price = 5.0
        buy3ForXLimit3Special = checkout.Discounts.BuyNForXSpecial(self.countableItem, 3, price, 3)

 
        buy3ForXLimit3Special.applyTo(self.scannedItems)
        
        nonDiscountedItem = self.scannedItems.getAt(4)

        self.assertAlmostEqual(nonDiscountedItem.getDiscountPrice(), nonDiscountedItem.getMarkdownPrice(), 3, "Limit not used")
    
    def testGetNFullSetsForBuyNForXSpecial(self):
        self.runFullSetCalcForN(10)
        self.runFullSetCalcForN(20)
        
    def runFullSetCalcForN(self, nMatched):
        dummySet = [0]*nMatched
        nSets = self.buyNForXSpecial.calcNumberOfFullSets(dummySet)
        self.assertEqual(nSets, int(nMatched/self.buyN), "Number of sets incorrect")
        
    def testIsPricePositionForBuyNForXSpecial(self):
        self.assertFalse(self.buyNForXSpecial.isPricePosition(0),           "Zeroed position for BuyNForXSpecial misidentified")
        self.assertTrue( self.buyNForXSpecial.isPricePosition(self.buyN-1), "Price position for BuyNForXSpecial misidentified")
        self.assertFalse(self.buyNForXSpecial.isPricePosition(4),           "Zeroed position for BuyNForXSpecial misidentified")
    
    def testPartitionFullAndLeftoversforBuyNForXSpecial(self):
        self.runPartitionForFullAndLeftovers(3, 8, 'a')
        
    def runPartitionForFullAndLeftovers(self, buyN, testLength, itemObject):
        special = checkout.Discounts.BuyNForXSpecial(self.countableItem, buyN, 0.0)
        dummy = [itemObject]*testLength
        (full, left) = special.partitionFullAndLeftovers(dummy)
        self.assertEqual(len(full), buyN*int(testLength/buyN), "Full set not right size")
        self.assertEqual(len(left), testLength - buyN*int(testLength/buyN), "Leftover set not right size")        
              
    def testBuyNWeightedGetMLesserPercentOffConstruction(self):
        self.BuyNWeightedGetMLesserConstructCheck(3,2,40.0)
        self.BuyNWeightedGetMLesserConstructCheck(2,1,10.0)
        
                
        
    def BuyNWeightedGetMLesserConstructCheck(self, buyN, getM, percent):
        special = checkout.Discounts.BuyNWeightedGetMEqualOrLesserPercentOff(self.weightedItem, buyN, getM, percent)
        self.assertEqual(special.buyN, buyN, "Buy N for weighted special not set")
        self.assertEqual(special.getM, getM, "Get M for weighted special not set")
        self.assertEqual(special.percentOff, percent, "Percent off for weighted special not set") 
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
        limit = 3
        special = checkout.Discounts.BuyNWeightedGetMEqualOrLesserPercentOff(self.weightedItem, 2, 1, discount, limit)
        self.assertEqual(special.limit, limit, "limit not set")
      
        scannedItems = checkout.Items.ScannedItemContainer()
        
        for _ in range(6):
            scannedItems.addScannedItem(self.weightedScanned)
        
        special.applyTo(scannedItems)
            
        lastItem = scannedItems.getLastItem()
        self.assertEqual(lastItem.getDiscountPrice(), lastItem.getMarkdownPrice(), "Limit in weighted special not imposed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    
    
    
    