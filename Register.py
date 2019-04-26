import checkout.Discounts
import checkout.Items

class Register(object):
    def __init__(self, inventory, markdowns, specials):
        self.inventory = inventory
        self.scannedItems = checkout.Items.ScannedItemContainer()
        self.markdowns = markdowns
        self.specials = specials
    
    def getTotal(self):
        self.applyMarkdownsAndSpecialsInOrder()
        return self.calculateSumOfDiscountPrices()
    
    def applyMarkdownsAndSpecialsInOrder(self):
        self.applyDiscounts(self.markdowns)
        self.applyDiscounts(self.specials)          
    
    def calculateSumOfDiscountPrices(self):
        total = 0.0
        nScannedItems = self.scannedItems.getSize()
        for index in range(nScannedItems):
            scannedItem = self.scannedItems.getAt(index)
            total += scannedItem.getDiscountPrice()
        return total        
        
    def applyDiscounts(self, discounts):
        for index in range(discounts.getSize()):
            discount = discounts.getAt(index)
            discount.applyTo(self.scannedItems)    
    
    
    def scanItemByName(self, name):
        item = self.inventory.getItemByName(name)
        scannedItem = checkout.Items.ScannedItem(item)
        self.scannedItems.addScannedItem(scannedItem)
        
    def scanItemByNameWithWeight(self, name, weight):
        item = self.inventory.getItemByName(name)
        scannedItem = checkout.Items.ScannedWeightedItem(item, weight)
        self.scannedItems.addScannedItem(scannedItem)
        
    def removeLastScanned(self):
        pass
        
