import checkout.Items
from checkout.Items import ScannedItem, Item


class Discount(object):

    def __init__(self, item):
        self.itemToDiscount = item
     
    def applyTo(self, scannedItems):
        pass
    
    def getMatchedItems(self, scannedItems):
        matchedSet = []
        for index in range(scannedItems.getSize()):
            item = scannedItems.getAt(index)
            self.appendIfMatchedItem(matchedSet, item)
        return matchedSet
    
    def appendIfMatchedItem(self, arrayOfMatched, item):
        if self.itemMatchesDiscount(item):
            arrayOfMatched.append(item)
    
    def itemMatchesDiscount(self, scannedItem):
        if scannedItem.getName() == self.itemToDiscount.name:
            return True
        else:
            return False
    
class Markdown(Discount):
    def __init__(self, item, value):
        super().__init__(item)
        self.value = value

    def applyTo(self, scannedItems):
        matchedItems = self.getMatchedItems(scannedItems)
        for item in matchedItems:
            self.markdownItem(item)
            
    def markdownItem(self, item):
        discountedPPU      = item.getBasePrice() - self.value
        item.markdownPrice = discountedPPU * item.getQuantity()        

class Special(Discount):
    def __init__(self, item, limit=None):
        super().__init__(item)
        self.limit = limit
        
    def partitionAroundLimit(self, listToParition):
        if self.limit == None:
            return (listToParition, [])
        else:
            belowLimit = listToParition[:self.limit]
            aboveLimit = listToParition[self.limit:]
            return (belowLimit,aboveLimit)
     
    def applyTo(self, scannedItems):
        matchedItems = self.getMatchedItems(scannedItems)
        self.partitionAndApplyDiscounts(matchedItems)
    
    def partitionAndApplyDiscounts(self, items):     
        (belowLimitItems, aboveLimitItems) = self.partitionAroundLimit(items)        
        self.applyDiscountBelowLimit(belowLimitItems)
        self.applyDiscountAboveLimit(aboveLimitItems)
        
    def applyDiscountAboveLimit(self, aboveLimitItems):
        for item in aboveLimitItems:
            item.discountPrice = item.getMarkdownPrice()
        
class PercentOffSpecial(Special):
    def __init__(self, item, percentOff, limit=None):
        self.percentOff = percentOff
        super().__init__(item, limit)
        
    def calculateDiscount(self, item):
        markdownPrice  = item.getMarkdownPrice()
        discountFactor = 1.0 - self.percentOff*0.01
        return markdownPrice*discountFactor

    def applyDiscountBelowLimit(self, belowLimitItems):
        for index in range(len(belowLimitItems)):
            item = belowLimitItems[index]
            if self.isDiscountPosition(index):
                item.discountPrice = self.calculateDiscount(item)
            else:
                item.discountPrice = item.markdownPrice
                
    def isDiscountPosition(self, index):
        nInDiscountSet = self.buyN + self.getM
        if index % nInDiscountSet < self.buyN:
            return False
        else:
            return True
        
class BuyNGetMForPercentOffSpecial(PercentOffSpecial):
    def __init__(self, item, N, M, percent, limit=None):
        self.buyN = N
        self.getM = M
        super().__init__(item, percent, limit)
    

class BuyNForXSpecial(Special):
    def __init__(self, item, N, price, limit=None):
        self.buyN  = N
        self.price = price
        super().__init__(item, limit)

    def applyDiscountBelowLimit(self, belowLimitItems):        
        lastN = []
        for item in belowLimitItems:
            lastN.append(item)
            if self.haveFullSet(lastN):
                self.applyDiscountToSet(lastN)
                lastN.clear()
                
    def calcNumberOfFullSets(self, matchedItems):
        length = len(matchedItems)
        return int(length/self.buyN)
    
    def isPricePosition(self, index):
        if (index+1) % self.buyN == 0:
            return True
        else:
            return False
        
    def partitionFullAndLeftovers(self, items):
        nFullSetItems = self.calcNumberOfFullSets(items)*self.buyN
        fullSetItems = items[:nFullSetItems]
        leftoverSetItems = items[nFullSetItems:]
        return (fullSetItems, leftoverSetItems)
        
    def haveFullSet(self, discountSet):
        if len(discountSet) == self.buyN:
            return True
        else:
            return False
              
    def applyDiscountToSet(self, discountSet):
        self.zeroOutDiscountPriceExceptLast(discountSet)
        self.setPriceAtEndOfSet(discountSet)        
        
    def zeroOutDiscountPriceExceptLast(self, discountSet):
        for item in discountSet[:-1]:
            item.discountPrice = 0.0
            
    def setPriceAtEndOfSet(self, discountSet):
        discountSet[-1].discountPrice = self.price
        
        
class BuyNWeightedGetMEqualOrLesserPercentOff(PercentOffSpecial):
    def __init__(self, item, N, M, percent, limit=None):
        self.buyN = N
        self.getM = M
        super().__init__(item, percent, limit)
        
    def applyTo(self, scannedItems):
        sortedItems = self.getMatchedItemsSortedByWeight(scannedItems)
        self.partitionAndApplyDiscounts(sortedItems)
        
    def getMatchedItemsSortedByWeight(self, scannedItems):
        matchedItems = self.getMatchedItems(scannedItems)      
        
        itemQuantitySortKey= lambda item: item.getQuantity()
        sortedItems = sorted(matchedItems, key=itemQuantitySortKey, reverse=True) 
               
        return sortedItems