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
            if self.itemMatchesDiscount(item):
                matched.append(item)
        return matched
    
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
    def __init__(self, item, limit=1e9):
        super().__init__(item)
        self.limit = limit

class BuyNGetMForPercentOffSpecial(Special):
    def __init__(self, item, N, M, percent, limit=1e9):
        self.buyN = N
        self.getM = M
        self.percentOff = percent
        super().__init__(item, limit)
        
    def applyTo(self, scannedItems):
        nPurchased = 0
                
        for index in range(scannedItems.getSize()):
            item = scannedItems.getAt(index)
            if self.itemMatchesDiscount(item) and nPurchased < self.limit:
                if nPurchased % (self.buyN + self.getM) < self.buyN:
                    item.discountPrice = item.markdownPrice
                else:
                    item.discountPrice = item.markdownPrice*(1.0 - self.percentOff*0.01)
                nPurchased += 1


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


        
class BuyNWeightedGetMEqualOrLesserPercentOff(Special):
    def __init__(self, item, N, M, percent, limit=10000):
        self.buyN = N
        self.getM = M
        self.percentOff = percent
        super().__init__(item, limit)
        
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
            