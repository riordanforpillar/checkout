
class Item(object):

    def __init__(self, name, pricePerUnit):
        self.name = name
        self.pricePerUnit = pricePerUnit
        
class ScannedItem():
    def __init__(self, item, quantity=1):
        if type(quantity) != int:
            raise ScannedQuantityNotIntegerException
        self.baseItem = item
        self.quantity = quantity
        
        self.markdownPrice = self.baseItem.pricePerUnit*self.getTotalQuantity()
    
    def getName(self):
        return self.baseItem.name
    
    def getQuantity(self):
        return self.quantity
    
    def getTotalQuantity(self):
        return self.quantity
    
    def getBasePrice(self):
        return self.baseItem.pricePerUnit
    
    def getMarkdownPrice(self):
        return self.markdownPrice

    def getDiscountPrice(self):
        return self.getMarkdownPrice()
    
class ScannedWeightedItem(ScannedItem):
    def __init__(self, item, weight, quantity=1):
        if type(weight) != float:
            raise ScannedWeightNotFloatException
        self.weight = weight
        super().__init__(item, quantity)

    
    def getWeight(self):
        return self.weight
    
    def getTotalQuantity(self):
        return ScannedItem.getTotalQuantity(self)*self.weight
                
        
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
        self.itemStack.append(scannedItem)
        
    def getAt(self, index):
        return self.itemStack[index]
        
    def removeLastItem(self):
        self.itemStack.pop()
    
class NotFoundInInventoryException(Exception):
    pass

class ScannedQuantityNotIntegerException(Exception):
    pass

class ScannedWeightNotFloatException(Exception):
    pass