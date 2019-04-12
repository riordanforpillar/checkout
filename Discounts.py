
class Discount(object):

    def __init__(self):
        pass
     
    def applyTo(self, scannedItems):
        pass
    
class Markdown(Discount):
    def __init__(self, item, value):
        self.itemtoMarkdown = item
        self.value = value
        
    def applyTo(self, scannedItems):
        for index in range(scannedItems.getSize()):
            scannedItem = scannedItems.getAt(index)
            if scannedItem.getName() == self.itemtoMarkdown.name:
                scannedItem.markdownPrice = (scannedItem.getBasePrice() - self.value)*scannedItem.getTotalQuantity()