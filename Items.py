import copy

class Item(object):

    def __init__(self, name, pricePerUnit):
        self.name = name
        self.pricePerUnit = pricePerUnit
        
class ScannedItem():
    def __init__(self, item):
        self.baseItem = item
        
        self.markdownPrice = self.baseItem.pricePerUnit*self.getTotalQuantity()
        self.discountPrice = self.markdownPrice

    
    def getName(self):
        return self.baseItem.name
    
    def getTotalQuantity(self):
        return 1
    
    def getBasePrice(self):
        return self.baseItem.pricePerUnit
    
    def getMarkdownPrice(self):
        return self.markdownPrice

    def getDiscountPrice(self):
        return self.discountPrice
    
class ScannedWeightedItem(ScannedItem):
    def __init__(self, item, weight):
        if type(weight) != float:
            raise ScannedWeightNotFloatException
        self.weight = weight
        super().__init__(item)

    def getWeight(self):
        return self.weight
    
    def getTotalQuantity(self):
        return self.weight
                
        
class Inventory():
    def __init__(self):
        self.storedItems = {}
    
    def getSize(self):
        return len(self.storedItems.keys())
    
    def addItem(self, item):
        self.storedItems[item.name] = item
        
    def getItemByName(self, itemName):
        try:
            foundItem = self.storedItems[itemName]
        except:
            raise NotFoundInInventoryException
        return foundItem
    
class ScannedItemContainer():
    def __init__(self):
        self.itemStack = []
    
    def getSize(self):
        return len(self.itemStack)
    
    def addScannedItem(self, scannedItem):
        self.itemStack.append(copy.copy(scannedItem))
        
    def getAt(self, index):
        return self.itemStack[index]
    
    def getLastItem(self):
        return self.itemStack[-1]
        
    def removeLastItem(self):
        self.itemStack.pop()
    
class NotFoundInInventoryException(Exception):
    pass

class ScannedWeightNotFloatException(Exception):
    pass