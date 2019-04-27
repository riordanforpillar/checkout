import checkout.Items, checkout.Discounts, checkout.Register

def runScanSequence(register, scanSequence):
    print("%8s %6s" % ("", "Total"))  

    for itemName, weight in scanSequence:
        if weight == None:
            register.scanItemByName(itemName)
        else:
            register.scanItemByNameWithWeight(itemName, weight)
        print("%8s %6.2f" % (itemName, register.getTotal()))  
        
    indexToRemove = 3
    print("Removing item at index %d" % indexToRemove)
    register.removeScannedAt(indexToRemove)
    print("   Total %6.2f" % (register.getTotal()))  
              

if __name__ == '__main__':

        soup   = checkout.Items.ItemBase("Soup", 1.00)
        cereal = checkout.Items.ItemBase("Cereal", 5.71)
        beef   = checkout.Items.WeightedItem("Beef", 4.09)

        soupMarkdown = checkout.Discounts.Markdown(soup, 0.40)   
   
        buy2Get1HalfOffLimit3Special = checkout.Discounts.BuyNGetMForPercentOffSpecial(soup, 2, 1, 50.0,3)
               
        inventory = checkout.Items.Inventory()
        inventory.addItem(soup)
        inventory.addItem(cereal)
        inventory.addItem(beef)
       
        markdowns = checkout.Discounts.DiscountContainer()
        markdowns.addDiscount(soupMarkdown)
        
        specials  = checkout.Discounts.DiscountContainer()
        specials.addDiscount(buy2Get1HalfOffLimit3Special)
        
        register  = checkout.Register.Register(inventory, markdowns, specials)
        
        scanSequence = [ ("Soup", None), ("Soup", None), ("Beef", 2.1), ("Cereal", None),
                        ("Soup", None), ("Soup", None), ("Soup", None), ("Soup", None)]
        
        runScanSequence(register, scanSequence)
        
