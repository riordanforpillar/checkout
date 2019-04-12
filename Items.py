
class Item(object):

    def __init__(self, name, pricePerUnit):
        self.name = name
        self.pricePerUnit = pricePerUnit
        
class ScannedItem():
    def __init__(self, item, quantity=1):
        self.baseItem = item
    
    def getName(self):
        return self.baseItem.name
    
    def getBasePrice(self):
        return self.baseItem.pricePerUnit
    
    def getMarkdownPrice(self):
        return self.baseItem.pricePerUnit

    def getDiscountPrice(self):
        return self.baseItem.pricePerUnit
        
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
            raise InventoryException
        return foundItem
    
class ScannedItemContainer():
    def __init__(self):
        self.itemStack = []
    
    def getSize(self):
        return len(self.itemStack)
    
    def addScannedItem(self, scannedItem):
        self.itemStack.append(scannedItem)
    
class InventoryException(Exception):
    pass