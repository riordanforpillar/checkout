import checkout.Discounts
import checkout.Items
from checkout.Items import ScannedItemContainer

class Register(object):
    def __init__(self, inventory, specials, markdowns):
        self.inventory = inventory
        self.scannedItems = checkout.Items.ScannedItemContainer()
    
    def getTotal(self):
        sum = 0.0
        nScannedItems = self.scannedItems.getSize()
        for index in range(nScannedItems):
            scannedItem = self.scannedItems.getAt(index)
            sum += scannedItem.getDiscountPrice()
        return sum
    
    def scanItemByName(self, name):
        item = self.inventory.getItemByName(name)
        scannedItem = checkout.Items.ScannedItem(item)
        self.scannedItems.addScannedItem(scannedItem)