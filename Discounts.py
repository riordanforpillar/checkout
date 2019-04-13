import checkout.Items

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
    def __init__(self, item, N, M, percent):
        self.buyN = N
        self.getM = M
        self.percentOff = percent
        self.itemToDiscount = item
        
    def applyTo(self, scannedItems):
        nPurchased = 0
                
        for index in range(scannedItems.getSize()):
            item = scannedItems.getAt(index)
            if self.itemMatchesDiscount(item):
                if nPurchased % (self.buyN + self.getM) < self.buyN:
                    item.discountPrice = item.markdownPrice
                else:
                    item.discountPrice = item.markdownPrice*(1.0 - self.percentOff*0.01)
                nPurchased += 1


class BuyNForXSpecial(Discount):
    def __init__(self, item, N, price):
        self.buyN = N
        self.price = price

    def applyTo(self, scannedItems):
        scannedItems.getAt(0).discountPrice = 0.0

        
        
        
        
        
    