import checkout.Discounts
import checkout.Items

class Register(object):
    def __init__(self, inventory, markdowns, specials):
        self.inventory = inventory
        self.scannedItems = checkout.Items.ScannedItemContainer()
        self.markdowns = markdowns
    
    def getTotal(self):
        for index in range(self.markdowns.getSize()):
            markdown = self.markdowns.getAt(index)
            markdown.applyTo(self.scannedItems)
                                                    
        total = 0.0
        nScannedItems = self.scannedItems.getSize()
        for index in range(nScannedItems):
            scannedItem = self.scannedItems.getAt(index)
            total += scannedItem.getDiscountPrice()
        return total
    
    def scanItemByName(self, name):
        item = self.inventory.getItemByName(name)
        scannedItem = checkout.Items.ScannedItem(item)
        self.scannedItems.addScannedItem(scannedItem)
        
    def scanItemByNameWithWeight(self, name, weight):
        item = self.inventory.getItemByName(name)
        scannedItem = checkout.Items.ScannedWeightedItem(item, weight)
        self.scannedItems.addScannedItem(scannedItem)
        
