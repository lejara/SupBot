from WebBot.WebBotter import WebBotter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from Locators import Locators
from Item import BuyItem
import json
import datetime
import os
import time
import traceback
import logging


class SupremeBuy:

    def __init__(self, buy_Item, item, supbot):
        print("[Buy] Buying.....")
        self.supbot = supbot
        self.buyItem = buy_Item
        self.item = item
        self.webbot = WebBotter()

    def Start(self):
        try:
            self.Start_URL()
            self.Checkout()
        except Exception as e:
            print(f"[Supbot] Error for {self.item.product_Name}, Retrying in {(self.supbot.delayTime + 2)}")
            logging.error(traceback.format_exc())
            # self.Start()

    def Start_URL(self):
        #Check if we can start stright from the style
        if self.buyItem.buyingStyle_URL !=None:
            self.webbot.go_to_url(self.buyItem.buyingStyle_URL)
        else:
            self.webbot.go_to_url(self.buyItem.link)

    def select_options(self):
        #Select size if there is a value
        if self.buyItem.buyingSize != None:
            self.webbot.Dropdown_Select_Text(By.ID, Locators.sizeOption_id, self.buyItem.buyingSize)

    def Checkout(self):
        #Check if sold out
        isNotSoldOut = self.SoldOutCheck()

        if isNotSoldOut:
            self.select_options()
            #Click add to cart
            self.webbot.click_element_wait(By.CSS_SELECTOR, Locators.addToCart_css)
            #Click checkout
            self.webbot.click_element_wait(By.LINK_TEXT , Locators.button_checkout_linkT)
            #Call fill forum
            self.PayoutFormFill()
            #SaveBoughtItem to list
            self.SaveBoughtItem()
        else:
            print(f"\n[Buy] ITEM SOLD OUT IN THIS STYLE! {self.item.product_Name}")
            self.RepollItem()

    def RepollItem(self):
        self.keepPolling = True
        while self.keepPolling:
            print(f'[SupBuy][{datetime.datetime.now()}] Repolling Item: {self.item.product_Name}')
            self.Start_URL()
            soldCheck = self.SoldOutCheck()
            if soldCheck:
                print(f'[SupBuy] Item repolled no longer sold out! {self.item.product_Name}')
                self.Checkout()
                self.keepPolling = False
            time.sleep(self.supbot.delayTime)

    def SoldOutCheck(self):
        return self.webbot.does_element_exist_wait(By.CSS_SELECTOR, Locators.addToCart_css)

    def PayoutFormFill(self):
        time.sleep(0.2)
        #Name
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["name"], self.supbot.buyInfo["name"])
        #Country
        self.webbot.Dropdown_Select_Value(By.ID, Locators.formFieldIds["country"], self.supbot.buyInfo["country"])
        #email
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["email"], self.supbot.buyInfo["email"])
        #tele
        ele = self.webbot.input_text_JS(By.ID, Locators.formFieldIds["tel"], self.supbot.buyInfo["tel"])
        self.webbot.Key_Space(ele)
        #address
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["address"], self.supbot.buyInfo["address"])
        #unit
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["unit"], self.supbot.buyInfo["unit"])
        #zip
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["zip"], self.supbot.buyInfo["zip"])
        #city
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["city"], self.supbot.buyInfo["city"])
        #state (depends on country)
        self.webbot.Dropdown_Select_Value(By.ID, Locators.formFieldIds["state"], self.supbot.buyInfo["state"])
        #Number
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["number"], self.supbot.buyInfo["number"])
        self.webbot.Key_Space(ele)
        #Credit month
        self.webbot.Dropdown_Select_Value(By.ID, Locators.formFieldIds["credit_month"], self.supbot.buyInfo["credit_month"])
        #credit year
        self.webbot.Dropdown_Select_Value(By.ID, Locators.formFieldIds["credit_year"], self.supbot.buyInfo["credit_year"])
        #c
        self.webbot.input_text_JS(By.ID, Locators.formFieldIds["cvv"], self.supbot.buyInfo["cvv"])
        #Check mark terms
        self.webbot.click_link_element_JS(By.CLASS_NAME, Locators.formFieldIds["terms_spec"])
        #submit
        self.webbot.click_element(By.CSS_SELECTOR, Locators.formFieldIds["submit_css"])
        #Change title
        self.webbot.Change_Current_Tab_Title(f'{self.item.price} - {self.item.product_Name}')

    def RefillFourm(self):
        self.webbot.driver.refresh()
        self.PayoutFormFill()

    def ConfirmPayment(self):
        pass

    def SaveBoughtItem(self):

        if os.path.isfile('Bought.json'):
            with open('Bought.json') as json_data:
                bought = json.load(json_data)
        else:
            bought = []

        bought.append(self.buyItem.link)
        with open('Bought.json', 'w') as outfile:
            json.dump(bought, outfile, indent=4)

        print("[Buy] Bought.json Saved. Item: " + self.buyItem.link)
