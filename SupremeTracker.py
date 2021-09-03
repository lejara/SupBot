
from Locators import Locators
from Item import Item
from SupremeDecision import SupremeDecision
from multiprocessing import Process
from bs4 import BeautifulSoup
import json
import threading
import time
import datetime
import requests
import os

#
# Keeps Track of items in the supreme website. If item is not in the item list bank, then this class will notify a new item has been added
#
class SupremeTracker:

    keepPolling = True
    processes = []

    def __init__(self, supbot):
        self.itemList = []
        self.supbot = supbot
        self.LoadItems()
        self.StartPolling()

    #Wille refresh the page and check if a new item has been added
    def StartPolling(self):

        while self.keepPolling:
            hasNewFoundItem = False
            print("[{}] Polling...".format(datetime.datetime.now()))
            #Fetch page
            shop_page = requests.get(Locators.shop_page)
            self.soup_shop = BeautifulSoup(shop_page.content, "html5lib")
            #Get listing elements
            listingElements = self.soup_shop.find("div", {"class" : Locators.shopListing_class})
            listingElements = listingElements.findAll(Locators.listingName_tag)
            #Populate base info
            for ele in listingElements:
                catagory = ele["class"][0]
                a_tag = ele.find(Locators.listingLink_tag)
                id = a_tag['href'].split('/')[-1]
                link = Locators.main_website + a_tag['href']

                new_item  = Item(id, catagory, link)

                #Check if item is already in the list
                exist = False
                for item in self.itemList:
                    if new_item.id_hash == item.id_hash:
                        exist = True
                if not exist:
                    # New Item, not found in list
                    self.NewItemFound(new_item)
                    hasNewFoundItem = True

            #Save Item list
            if hasNewFoundItem:
                print("Save new found items? (y/n)")
                i = input()
                if i == "y":
                    self.SaveItems()
                self.StopPolling()
            else:
                time.sleep(self.supbot.delayTime)

    def StopPolling(self):
        #Wait for completed Processes. including the main process will shop
        self.Joiner()
        self.keepPolling = False

    def NewItemFound(self, item):
        print("[{}] Poll Update: New Item Found: {}".format(datetime.datetime.now(), item.link))
        supDec = SupremeDecision(item, self.supbot)
        #Check if sup dec passed the first check before spawning a process
        if supDec.check_1 == True:
            p = Process(target=supDec.Start)
            p.start()
            self.processes.append(p)
        self.AddToItemList(item)



    def AddToItemList(self, item):
        self.itemList.append(item)

    #Join for completed Processes
    def Joiner(self):
        for pro in self.processes:
            pro.join()

    def SaveItems(self):
        #Encode
        en_itemList = []
        for item in self.itemList:
            en_itemList.append(item.__dict__)
        #Write
        with open('TrackerList.json', 'w') as outfile:
            json.dump(en_itemList, outfile)
        print("\n[Tracker] Tracker List Saved")

    def LoadItems(self):
        #Check if file exist
        if os.path.isfile("TrackerList.json"):
            #Read
            de_itemList = None
            with open('TrackerList.json') as json_data:
                de_itemList = json.load(json_data)
            #Decode
            for item_dist in de_itemList:
                self.itemList.append( Item.from_json(item_dist))

            print("\n[Tracker] Tracker List Loaded")
            # for item in self.itemList:
            #     print(item)
        else:
            self.itemList = []
