from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
import os

#Wrapper class to help with common use case when going through a page

class WebBotter:

    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36" # Note: Version can change
    poxyServer = "127.0.0.1:8080"

    def __init__(self, website = None, with_profile = False, profil_path = "\\User Data"):
        #Start
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        #ignore-certificates
        options.add_argument("--ignore-certificate-errors")
        #Test arugments----
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-accelerated-2d-canvas")
        options.add_argument("--disable-java")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-device-discovery-notifications")
        options.add_argument('--cryptauth-http-host ""')
        options.add_argument('--disable-features=site-per-process')
        options.add_argument('--no-first-run')
        #/Test arugments----
        #Keep browser open when script ends
        options.add_experimental_option("detach", True)
        #Add in poxy server
        options.add_argument(f'--proxy-server={self.poxyServer}')
        # specify the desired user agent
        options.add_argument(f'user-agent={self.useragent}')
        #Path to a chrome profile
        if with_profile:
            options.add_argument("user-data-dir="+profil_path+"")

        #Init Chrome Driver
        self.driver = webdriver.Chrome(options=options) #Note: driver might need update if your using an newer version of chrome

        if website != None:
            self.driver.get(website)

        self.actions = ActionChains(self.driver)


    #Go to the given url
    def go_to_url (self, link):
        self.driver.get(link)

    def Change_Current_Tab_Title(self, text):
        self.driver.execute_script("document.title = arguments[0]", text)

    #Finds a element with wait and presses the enter key (string). Returns element
    def click_element(self, by, selector):
        element = self.driver.find_element(by, selector)
        element.send_keys(Keys.ENTER)
        return element

    #Find  clicks on an element. Returns element
    def click_link_element(self, by, selector):
        element = self.driver.find_element(by, selector)
        element.click()
        return element

    #Click on an elelment using a JS click
    def click_link_element_JS(self, by, selector):
        ele = self.driver.find_elements(by, selector)
        self.driver.execute_script("arguments[0].click();", ele[1])

    #Finds a element with wait and presses the enter key (string). Returns element
    def click_element_wait(self, by, selector):
        element = self.wait_find_element(by, selector)
        element.send_keys(Keys.ENTER)
        return element

    #Find element and enter the given text. Selector is css
    def input_text(self, by, selector, text):
        element = self.driver.find_element(by, selector)
        element.send_keys(text)
        return element

    #Find element and enter the given text with JS. Selector is css
    def input_text_JS(self, by, selector, text):
        element = self.driver.find_element(by, selector)
        self.driver.execute_script("arguments[0].value=arguments[1];", element, text)
        # element.send_keys(Keys.ENTER)
        return element

    #Find element with wait and enter the given text. Selector is css, Returns element
    def input_text_wait(self, by, selector, text):
        element = self.wait_find_element(by, selector)
        element.send_keys(text)
        return element

    #Find element with wait and enter the given text, then submits it. Selector is css, Returns element
    def input_text_enter_wait(self, by, selector, text):
        element = self.wait_find_element(by, selector)
        element.send_keys(text)
        element.send_keys(Keys.ENTER)
        return element

    #Page down an element
    def page_down_wait(self, by, element):
        # if isinstance(element, str):
        #     element = self.wait_find_element(by, element)
        # element.send_keys(Keys.PAGE_DOWN)
        self.driver.execute_script("window.scrollTo(0, 200)")

    #Wait until element is loaded then find
    def wait_find_element(self, by, locator, time = 10):
        WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located((by, locator))
        )
        element = self.driver.find_element(by, locator)
        return element

    #Wait until the given element is gone
    def wait_unitl_element_gone(self, element, time = 10):
        WebDriverWait(self.driver, time).until(
            EC.invisibility_of_element(element)
        )
    #Check if element exist
    def does_element_exist(self, by, locator):
        element_exist = True
        try:
            self.driver.find_element(by, locator)
        except NoSuchElementException:
            element_exist = False
        return element_exist

    #Check if element exist
    def does_element_exist_wait(self, by, locator, time = 2):
        element_exist = True
        try:
            self.wait_find_element(by, locator, time)
        except TimeoutException:
            element_exist = False
        return element_exist

    #Select a dropdown list base on the attribute value
    def Dropdown_Select_Value(self, by, locator, value):
        s = Select(self.driver.find_element(by, locator))
        s.select_by_value(value)

    #Select a dropdown list base on visible text
    def Dropdown_Select_Text(self, by, locator, text):
        s = Select(self.driver.find_element(by, locator))
        s.select_by_visible_text(text)

    def Key_Space(self, element):
        element.send_keys(Keys.SPACE)
