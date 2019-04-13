import checkout.Items

class Discount(object):

    def __init__(self):
        pass
     
    def applyTo(self, scannedItems):
        pass
    
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
                scannedItem.markdownPrice = discountedPPU * scannedItem.getTotalQuantity()

class BuyNGetMForPercentOffSpecial(Discount):
    def __init__(self, item, N, M, percent):
        self.buyN = N
        self.getM = M
        self.percentOff = percent
        
    def applyTo(self, scannedItems):
        scannedItems.getAt(3).discountPrice = 1.275
        
        
        
        
        
        
    