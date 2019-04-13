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
        self.itemToMarkdown = item
        self.value = value

    def itemMatchesMarkdown(self, scannedItem):
        if scannedItem.getName() == self.itemToMarkdown.name:
            return True
        else:
            return False

    def applyTo(self, scannedItems):
        for index in range(scannedItems.getSize()):
            scannedItem = scannedItems.getAt(index)
            if self.itemMatchesMarkdown(scannedItem):
                discountedPPU = scannedItem.getBasePrice() - self.value
                scannedItem.markdownPrice = discountedPPU * scannedItem.getQuantity()

class BuyNGetMForPercentOffSpecial(Discount):
    def __init__(self, item, N, M, percent):
        self.buyN = N
        self.getM = M
        self.percentOff = percent
        self.itemToDiscount = item
        
    def applyTo(self, scannedItems):
        pass

        
        
        
        
        
    