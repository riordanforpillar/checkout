
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
    
    def getName(self):
        return self.baseItem.name
    
    def getQuantity(self):
        return self.quantity
    
    def getBasePrice(self):
        return self.baseItem.pricePerUnit
    
    def getMarkdownPrice(self):
        return self.getBasePrice()*self.getQuantity()

    def getDiscountPrice(self):
        return self.getMarkdownPrice()
    
class ScannedWeightedItem(ScannedItem):
    def __init__(self, item, weight, quantity=1):
        super().__init__(item, quantity)
        if type(weight) != float:
            raise ScannedWeightNotFloatException
        self.weight = weight
    
    def getWeight(self):
        return self.weight
                
    def getMarkdownPrice(self):
        return self.getBasePrice()*self.getQuantity()*self.getWeight()
        
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
    
class NotFoundInInventoryException(Exception):
    pass

class ScannedQuantityNotIntegerException(Exception):
    pass

class ScannedWeightNotFloatException(Exception):
    pass