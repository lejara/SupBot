
from NotifyForum import Run_Forum
from SupremeBuy import SupremeBuy
from Locators import Locators
from Item import Item
from Item import BuyItem
from bs4 import BeautifulSoup
import time
import requests
import datetime


class SupremeDecision:

    def __init__(self, item, supbot):
        self.item = item
        self.supbot = supbot
        self.BuyingObject = None
        self.instaBuyed = False
        #Do a first Check, before we all it to spawn process
        self.check_1 = self.Filter_One_Check()

    def Start(self):
        self.Populate_Item_WebBot()
        if self.Filter_Two_Check() == True:
            self.Prompt_Forum()


    def Filter_One_Check(self):
        #Check Catagory
        print("[Decision] Checking 1....")
        check_pass = False
        for filter_cat in self.supbot.filter_Out_Categories:
            if filter_cat.lower() == self.item.catagory.lower():
                check_pass = True
                break

        if not check_pass:
            print("[Decision] Catagory no pass " + self.item.link)

        return check_pass

    def Filter_Two_Check(self):
        print(f'[Decision] Checking 2.... {self.item.product_Name}')
        check_pass = True

        isNotSoldOut = self.SoldOutCheck()
        check_pass = isNotSoldOut

        #Check if we can insta buy
        if self.supbot.instaBuy:
            for keyword in self.supbot.insta_buy_keywords:
                if keyword.lower() in self.item.product_Name.lower():

                    print(f"[Decision] Insta Buying... {self.item.product_Name}, {self.item.link}")
                    self.Start_Buy(None, None)
                    # check_pass = False # don't allow the forum to run
                    self.instaBuyed = True

        return check_pass

    def SoldOutCheck(self):
        #check if its sold out
        cart_button = self.soup.find("input", {"value" : "add to cart"})
        if cart_button == None:
            print(f"[Decision] ITEM SOLD OUT! {self.item.product_Name}, {self.item.link}")
            return False
        return True

    # def RepollItem(self):
    #     self.keepPolling = True
    #     while self.keepPolling:
    #         print(f'[Decision][{datetime.datetime.now()}] Repolling Item: {self.item.product_Name}')
    #         self.Get_The_Soup()
    #         soldCheck = self.SoldOutCheck()
    #         if soldCheck:
    #             print(f'[Decision] Item repolled no longer sold out! {self.item.product_Name}')
    #             if self.supbot.instaBuy:
    #                 print("[Decision] Repoll Insta Buying... " + self.item.product_Name)
    #                 self.Start_Buy(None, None)
    #                 self.instaBuyed = True
    #                 self.Prompt_Forum()
    #             else:
    #                 print("[Decision] Repoll Prompting Forum " + self.item.product_Name)
    #                 self.Prompt_Forum()
    #             break
    #         time.sleep(self.supbot.delayTime)

    def Prompt_Forum(self):
        if self.instaBuyed == True:
            Run_Forum(self.item, self, "----------Item Insta Buyed----------")
        elif self.supbot.instaBuy == False:
            Run_Forum(self.item, self)

    def Populate_Item_WebBot(self):

        self.Get_The_Soup()

        #TODO: upate locators here
        #Get Image link
        main_image_url = "https:" + (self.soup.find("img", id=Locators.productImg_Id)['src'])

        #Get Product Name
        product_name = self.soup.find("h1", {"itemprop" : "name"}).text

        #Get price
        price = self.soup.find("span", {"itemprop" : "price"}).text

        #Get size option
        size_options_s = self.soup.find("select", {"name" : "s"})
        size_options = []
        if size_options_s != None:
            size_options_s = size_options_s.findAll("option")
            for op in size_options_s:
                size_options.append(op.text)
        else:
            size_options = None

        #Get styles
        style_s = self.soup.find("ul", {"class" : "styles"})
        if style_s != None:
            style_s = style_s.findAll("li")
            styles = {}
            for li_cat in style_s:
                a_tag = li_cat.findAll("a")[0]
                style_name = a_tag[Locators.style_name_css_key]
                style_url = Locators.main_website + a_tag["href"] #if style break, probs here is way
                styles.update({style_name : style_url})
        else:
            styles = None

        #Add all the info
        self.item.add_more_info(main_image_url, product_name, price, size_options, styles)

    def Get_The_Soup(self):
        item_page = requests.get(self.item.link)
        self.soup = BeautifulSoup(item_page.content, "html5lib")

    #Rerun the forum fill only in the current buy object
    def RefillForum(self):
        if self.BuyingObject != None:
            self.BuyingObject.RefillFourm()
        else:
            print("[Decision] Could not do Refill. No item is being bought!")

    def Start_Buy(self, bS, buyStyle):
        buyingItem = BuyItem(link=self.item.link, buyingSize=bS, buyingStyle_URL=buyStyle)
        self.BuyingObject = SupremeBuy(buyingItem, self.item, self.supbot)
        self.BuyingObject.Start()
