import copy

class ItemBase(object):

    def __init__(self, name, pricePerUnit):
        self.name = name
        self.pricePerUnit = pricePerUnit
        
class Item(ItemBase):
    def __init__(self, name, pricePerUnit):
        super(Item, self).__init__(name, pricePerUnit)

class WeightedItem(ItemBase):
    def __init__(self, name, pricePerUnit):
        super(WeightedItem, self).__init__(name, pricePerUnit)

class ScannedBaseItem():
    def __init__(self, item):
        self.baseItem = item
        self.markdownPrice = self.baseItem.pricePerUnit*self.getQuantity()
        self.discountPrice = self.markdownPrice
    
    def getName(self):
        return self.baseItem.name
    
    def getQuantity(self):
        return 1
    
    def getBasePrice(self):
        return self.baseItem.pricePerUnit
    
    def getMarkdownPrice(self):
        return self.markdownPrice

    def getDiscountPrice(self):
        return self.discountPrice
    
class ScannedItem(ScannedBaseItem):
    def __init__(self, item):
        super().__init__(item)
    
class ScannedWeightedItem(ScannedBaseItem):
    def __init__(self, item, weight):
        if type(weight) != float:
            raise ScannedWeightNotFloatException
        if type(item) != WeightedItem:
            raise ScannedNonWeightedItemWithWeight
        self.weight = weight
        super().__init__(item)

    def getWeight(self):
        return self.weight
    
    def getQuantity(self):
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
        
    def removeAt(self, index):
        self.itemStack.pop(index)
    
class NotFoundInInventoryException(Exception):
    pass

class ScannedWeightNotFloatException(Exception):
    pass

class ScannedNonWeightedItemWithWeight(Exception):
    pass

class ScannedWeightedItemWithoutWeight(Exception):
    pass
