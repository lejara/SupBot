import tkinter as tk
from tkinter import *
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO

# Pillow dos: https://pillow.readthedocs.io/en/stable/
# tkinter docs: https://docs.python.org/3/library/tkinter.html
class NotifyForum(tk.Frame):
    def __init__(self, item, supDec, master=None, title = None):
        super().__init__(master)

        self.item = item
        self.supDec = supDec
        self.master = master
        self.buy_f = self.supDec.Start_Buy
        self.refillForum = self.supDec.RefillForum

        self.itemSize = None
        self.itemStyle = None

        if title == None:
            self.master.title("New Item Found")
        else:
            self.master.title(title)

        self.master.minsize(500, 850)
        self.fm = Frame(master)
        self.pack()

        self.add_Product_Name()
        self.add_Price()
        self.load_image(self.item.imagesLinks[0])
        self.create_buy_exit()
        self.style_options()
        self.add_options()
        self.BuyToolOptions()
        self.fm.pack(fill=BOTH, expand=YES)

    def add_Product_Name(self):
        product_name = tk.Label(self.master, text=self.item.product_Name, font="Verdana 18 bold")
        product_name.pack(side="top")

    def add_Price(self):
        price = tk.Label(self.master, text=self.item.price, font="Verdana 10 bold")
        price.pack()

    def create_buy_exit(self):
        #Buy Button
        self.hi_there = tk.Button(self, bg="green", height=4, width=20, font="Verdana 15 bold")
        self.hi_there["text"] = "Buy"
        self.hi_there["command"] = self.Buy
        self.hi_there.pack(side=TOP)
        #Exit Button
        self.quit = tk.Button(self, text="Exit", bg="red", height=4, width=20, font="Verdana 15 bold", command=self.Exit_Forum)
        self.quit.pack(side=TOP)

    def load_image(self, url):
        image_pro = urlopen(url)
        image_raw = image_pro.read()
        image_pro.close()

        im = Image.open(BytesIO(image_raw))
        photo = ImageTk.PhotoImage(im)

        label = tk.Label(image=photo)
        label.image = photo
        label.pack(side="top")

    def style_options(self):
        if self.item.styles != None:
            sizeO_text = tk.Label(self.master, text="Item Style", font="Verdana 10 bold")
            sizeO_text.pack(side="top")
            #Make tk var
            variable = StringVar(self.master)
            # default value
            variable.set(next(iter(self.item.styles)))
            self.itemStyle = self.item.styles[variable.get()]

            #Option menu listing
            w = OptionMenu(self.master, variable, *list(self.item.styles.keys()))
            w.pack(side="top")

            # on change dropdown value
            def change_dropdown(*args):
                self.itemStyle = self.item.styles[variable.get()]

            # link function to change dropdown
            variable.trace('w', change_dropdown)

    def add_options(self):

        #Size Option, check if we did found a size option
        if self.item.sizes != None:
            sizeO_text = tk.Label(self.master, text="Item Size", font="Verdana 10 bold")
            sizeO_text.pack(side="top")
            #Make tk var
            variable = StringVar(self.master)
            # default value
            variable.set(self.item.sizes[0])
            self.itemSize = variable.get()

            #Option menu listing
            w = OptionMenu(self.master, variable, *self.item.sizes)
            w.pack(side="top")

            # on change dropdown value
            def change_dropdown(*args):
                self.itemSize = variable.get()

            # link function to change dropdown
            variable.trace('w', change_dropdown)

    def BuyToolOptions(self):
            label = tk.Label(self.fm, text="Buying Tools", font="Verdana 10 bold")
            label.pack(side="top")
            #Refill fourm button
            self.buyOp = tk.Button(self.fm, height=2, width=10, font="Verdana 7 bold")
            self.buyOp["text"] = "Refill Forum"
            self.buyOp["command"] = self.refillForum
            self.buyOp.pack(side=TOP)

    def Exit_Forum(self):
        self.master.destroy()

    def Buy(self):
        # self.master.destroy()
        self.buy_f(self.itemSize, self.itemStyle)

def Run_Forum(item, supDec, title = None):
    root = tk.Tk()
    app = NotifyForum(item, supDec, master=root, title=title)
    app.mainloop()
