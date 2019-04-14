import checkout.Items
from checkout.Items import ScannedItem, Item

class Discount(object):

    def __init__(self, item):
        self.itemToDiscount = item
     
    def applyTo(self, scannedItems):
        pass
    
    def getMatchedItems(self, scannedItems):
        matched = []
        for index in range(scannedItems.getSize()):
            item = scannedItems.getAt(index)
            self.appendIfMatchedItem(matched, item)
        return matched
    
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
        
class PercentOffSpecial(Special):
    def __init__(self, item, percentOff, limit=None):
        self.percentOff = percentOff
        super().__init__(item, limit)
        
    def calculateDiscount(self, item):
        markdownPrice  = item.getMarkdownPrice()
        discountFactor = 1.0 - self.percentOff*0.01
        return markdownPrice*discountFactor

class BuyNGetMForPercentOffSpecial(PercentOffSpecial):
    def __init__(self, item, N, M, percent, limit=None):
        self.buyN = N
        self.getM = M
        super().__init__(item, percent, limit)
        
    def applyTo(self, scannedItems):
        matchedItems = self.getMatchedItems(scannedItems)
        
        (belowLimitItems, aboveLimitItems) = self.partitionAroundLimit(matchedItems)
        
        self.applyDistcountBelowLimit(belowLimitItems)
        self.applyDistcountAboveLimit(aboveLimitItems)


    def applyDistcountBelowLimit(self, belowLimitItems):
        for index in range(len(belowLimitItems)):
            item = belowLimitItems[index]
            if self.isDiscountPosition(index):
                item.discountPrice = self.calculateDiscount(item)
            else:
                item.discountPrice = item.markdownPrice
                
    def applyDistcountAboveLimit(self, aboveLimitItems):
        for item in aboveLimitItems:
            item.discountPrice = item.markdownPrice

                
    def isDiscountPosition(self, index):
        nInDiscountSet = self.buyN + self.getM
        if index % nInDiscountSet < self.buyN:
            return False
        else:
            return True

class BuyNForXSpecial(Special):
    def __init__(self, item, N, price, limit=1e9):
        self.buyN = N
        self.price = price
        super().__init__(item, limit)

    def applyTo(self, scannedItems):
        nPurchased = 0
        lastN = []
        for index in range(scannedItems.getSize()):
            item = scannedItems.getAt(index)
            if self.itemMatchesDiscount(item):
                if nPurchased > self.limit:
                    item.discountPrice = item.markdownPrice
                else:
                    lastN.append(item)
                    if len(lastN) == self.buyN:
                        for lastItem in lastN[:-1]:
                            lastItem.discountPrice = 0.0
                        lastN[-1].discountPrice = self.price
                        lastN.clear()
                nPurchased += 1


        
class BuyNWeightedGetMEqualOrLesserPercentOff(PercentOffSpecial):
    def __init__(self, item, N, M, percent, limit=10000):
        self.buyN = N
        self.getM = M
        super().__init__(item, percent, limit)
        
    def applyTo(self, scannedItems):
        purchased = []
        nInDiscountSet = self.buyN + self.getM
        for index in range(scannedItems.getSize()):
            item = scannedItems.getAt(index)
            if self.itemMatchesDiscount(item):
                purchased.append(item)
                
        sortedPurchased = sorted(purchased, key=lambda item: item.getQuantity(), reverse=True)
        
        pastLimit = sortedPurchased[self.limit:]
        sortedPurchased = sortedPurchased[:self.limit]
                
        while len(sortedPurchased) > 0:
            regularPriceSet = sortedPurchased[0:self.buyN]
            discountSet = sortedPurchased[self.buyN:nInDiscountSet]
            sortedPurchased = sortedPurchased[nInDiscountSet:]
            for item in regularPriceSet:
                item.discountPrice = item.getMarkdownPrice()
            for item in discountSet:
                item.discountPrice = item.getMarkdownPrice()*(1.0-self.percentOff*0.01)
        
        for item in pastLimit:
            item.discountPrice = item.getMarkdownPrice()   
            