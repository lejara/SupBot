import hashlib
#
# Product Data Holder
#
class Item:

    def __init__(self, id, catagory, link, id_hash = None):
        self.id = id
        self.catagory  = catagory
        self.link = link
        self.id_hash = id_hash if id_hash != None else int(hashlib.md5(self.id.encode()).hexdigest(), 16)
        self.imagesLinks = []

    def add_more_info(self, first_product_image_link, productName, p, sizes = None, styles = None):
        self.imagesLinks.append(first_product_image_link)
        self.product_Name = productName
        self.price = p
        self.sizes = sizes
        self.styles = styles

    #For Json decodeing
    @classmethod
    def from_json(self, item_dist):
        return self(id=item_dist['id'], catagory=item_dist['catagory'], link=item_dist['link'], id_hash=item_dist['id_hash'])

    def __str__(self):
        return "id_hash {}, id {}, catagory {}, link:{}".format(self.id_hash, self.id, self.catagory, self.link)

# Holder class to store any needed information when buying the item
class BuyItem:

    def __init__(self, link, buyingSize = None, buyingStyle_URL = None):
        self.link = link
        self.buyingSize = buyingSize
        self.buyingStyle_URL = buyingStyle_URL


#will hold defualt values that we think it hold value to us
class ItemInfluence:
    pass


#Testing Only: make a dummy item object with fake values
def DummyItem():
    return Item("d4u2sg1th", "hats", "https://www.supremenewyork.com/shop/hats/gm1xhjab9/qp9dsj628", "d9524b95b27b9a73adff69b0c0924s34")
    #Normal exmaple
    #{"id": "qp9dsj628", "catagory": "hats", "link": "https://www.supremenewyork.com/shop/hats/gm1xhjab9/qp9dsj628", "id_hash": "d9524b95b27b9a73adff69b0c0924a34", "imagesLinks": []}
    #with size example
    #d4u2sg1th, pants, https://www.supremenewyork.com/shop/pants/d4u2sg1th, d9524b95b27b9a73adff69b0c0924s34
