import checkout.Items

class Register(object):
    def __init__(self, inventory, markdowns, specials):
        self.inventory = inventory
        self.scannedItems = checkout.Items.ScannedItemContainer()
        self.markdowns = markdowns
        self.specials = specials
    
    def getTotal(self):
        self.applyMarkdownsAndSpecialsInOrder()
        return round(self.calculateSumOfDiscountPrices(),2)
    
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
        self.scanAndAdd(name)
        
    def scanItemByNameWithWeight(self, name, weight):
        self.scanAndAdd(name, weight)
        
    def scanAndAdd(self, name, weight = None):
        item = self.inventory.getItemByName(name)
        if weight == None:
            scannedItem = checkout.Items.ScannedItem(item)
        else:
            scannedItem = checkout.Items.ScannedWeightedItem(item, weight)
        self.scannedItems.addScannedItem(scannedItem)
        
    def removeScannedAt(self, index):
        self.scannedItems.removeAt(index)
        
    def removeLastScanned(self):
        self.scannedItems.removeLastItem()
