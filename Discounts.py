
class Discount(object):

    def __init__(self):
        pass
     
    def applyTo(self, scannedItems):
        pass
    
class Markdown(Discount):
    def __init__(self, item, value):
        self.item = item
        self.value = value
        
    def applyTo(self, scannedItems):
        pass