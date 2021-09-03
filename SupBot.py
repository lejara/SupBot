from SupremeTracker import SupremeTracker
from multiprocessing import Process
from CryptoInfo import CryptoInfo
import JsonTemplates
import multiprocessing
import threading
import json
import os
import sys


# Import for Testing
from Item import DummyItem
from SupremeDecision import SupremeDecision
from SupremeBuy import SupremeBuy

version = "2.3.3"
auhtor = "Lejara"

class SupBot:

    filter_Out_Categories = []
    filter_In_keywords = []
    insta_buy_keywords = []
    instaBuy = False
    buyInfo = {}
    delayTime = 1

    def __init__(self, initalEncrypt = False, doInstaBuy = False):
        self.instaBuy = doInstaBuy
        self.Load()
        if initalEncrypt == True:
            self.buyInfo = self.Inital_Encrypt_Info().decrypt()
        else:
            self.Decrypt_Info()

    def Start(self):
        SupremeTracker(self)

    def TestFromSupDec(self):
        SupremeDecision(DummyItem(), self)

    def TestFromSupBuy(self):
        SupremeBuy(DummyItem().link, self)

    def Inital_Encrypt_Info(self):
        en = CryptoInfo(self.buyInfo, True)
        self.buyInfo = en.Inital_Encrypt()
        self.Save_Buy_Info()
        return en

    def Decrypt_Info(self):
        self.buyInfo = CryptoInfo(self.buyInfo, False).decrypt()

    def Load(self):
        print("[SupBot] Init: Loading Jsons...")
        self.Load_Filter_Categories()
        # self.Load_Filter_Keywords()
        self.Load_InstaBuy_Keywords()
        self.Load_Buy_Info()

    def Load_Filter_Categories(self):
        if os.path.isfile('CategoriesFilter.json'):
            with open('CategoriesFilter.json') as json_data:
                self.filter_Out_Categories = json.load(json_data)
            print("[SupBot] Category Filter List Loaded")
        else:
            self.filter_Out_Categories = []
            with open('CategoriesFilter.json', 'w') as outfile:
                json.dump(JsonTemplates.CategoryFilter, outfile, indent=4)
            print("[SupBot] CategoriesFilter.json Created")

    # def Load_Filter_Keywords(self):
    #     if os.path.isfile('ItemKeywords.json'):
    #         with open('ItemKeywords.json') as json_data:
    #             self.filter_In_keywords = json.load(json_data)
    #         print("[SupBot] Keyword Filter List Loaded")
    #     else:
    #         self.filter_In_keywords = []
    #         with open('ItemKeywords.json', 'w') as outfile:
    #             json.dump(self.filter_In_keywords, outfile, indent=4)
    #         print("[SupBot] ItemKeywords.json Created.")

    def Load_InstaBuy_Keywords(self):
        if os.path.isfile("InstaBuyKeywords.json"):
            with open('InstaBuyKeywords.json') as json_data:
                self.insta_buy_keywords = json.load(json_data)
            print("[SupBot] Insta Buy Keywords Loaded")
        else:
            self.insta_buy_keywords = []
            with open('InstaBuyKeywords.json', 'w') as outfile:
                json.dump(self.insta_buy_keywords, outfile, indent=4)
            print("[SupBot] InstaBuyKeywords.json Created")

    def Load_Buy_Info(self):
        if os.path.isfile("Info.json"):
            with open('Info.json') as json_data:
                self.buyInfo = json.load(json_data)
            print("[SupBot] Info Loaded")
        else:
            with open('Info.json', 'w') as outfile:
                json.dump(JsonTemplates.Info_Template, outfile, indent=4)
            print("[SupBot] Info.json Created. Please fill out info.json, and / or other json files")
            sys.exit()

    def Save_Buy_Info(self):
        with open('Info.json', 'w') as outfile:
            json.dump(self.buyInfo, outfile, indent=4)
        print("[SupBot] Info Saved")



if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("\n----------------SupBot Beta Version: {}-----------------------".format(version))
    print("\nMade By: {}\n\n".format(auhtor))

    #Normal Start-----
    print("[SupBot] Encrypt Info.Json? (y/n)")
    x = input()
    encrypt = True if x == 'y' else False
    print("[SupBot] Turn on Insta Buy? (y/n)")
    x = input()
    doInsta = True if x == 'y' else False

    s = SupBot(encrypt, doInsta)
    # s = SupBot() # no encrypt, no insta buy
    s.Start()


    #Testing Starts
    # s = SupBot(False, False).TestFromSupDec()
    # s = SupBot().TestFromSupBuy() #Outdated
