import checkout.Items
from checkout.Items import ScannedItem, Item

class Discount(object):

    def __init__(self):
        pass
     
    def applyTo(self, scannedItems):
        pass
    
    def itemMatchesDiscount(self, scannedItem):
        if scannedItem.getName() == self.itemToDiscount.name:
            return True
        else:
            return False
    
class Markdown(Discount):
    def __init__(self, item, value):
        self.itemToDiscount = item
        self.value = value

    def applyTo(self, scannedItems):
        for index in range(scannedItems.getSize()):
            scannedItem = scannedItems.getAt(index)
            if self.itemMatchesDiscount(scannedItem):
                discountedPPU = scannedItem.getBasePrice() - self.value
                scannedItem.markdownPrice = discountedPPU * scannedItem.getQuantity()

class BuyNGetMForPercentOffSpecial(Discount):
    def __init__(self, item, N, M, percent, limit=1e9):
        self.buyN = N
        self.getM = M
        self.percentOff = percent
        self.itemToDiscount = item
        self.limit = limit
        
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


class BuyNForXSpecial(Discount):
    def __init__(self, item, N, price, limit=1e9):
        self.buyN = N
        self.price = price
        self.itemToDiscount = item
        self.limit = limit

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


        
class BuyNWeightedGetMEqualOrLesserPercentOff():
    def __init__(self, item, N, M, percent):
        self.buyN = 3
        self.getM = 2
        self.percentOff = 40.0
        
        
    