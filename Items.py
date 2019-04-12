
class Item(object):

    def __init__(self, name, pricePerUnit):
        self.name = name
        self.pricePerUnit = pricePerUnit
        
        
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
    
    
class InventoryException(Exception):
    pass