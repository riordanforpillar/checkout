import checkout.Discounts
import checkout.Items

class Register(object):
    def __init__(self, inventory, specials, markdowns):
        self.inventory = inventory
    
    def getTotal(self):
        return 0.0
    
    def scanItemByName(self, name):
        self.inventory.getItemByName(name)