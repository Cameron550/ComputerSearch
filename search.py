from PIL import Image, ImageTk
import Tkinter
from bs4 import BeautifulSoup as bs
import requests
import urllib
import random
import os


# I know this my code format is probably confusing.Id also advise reading the code from the bottom to the top
#  This is the first program I spent a lot of time trying to
# figure out how to arrange. This is also my first gui program.  :) - Cameron


class search():  # brandchoices
    def __init__(self, budget, bchoices):

        self.searchscreen_root = Tkinter.Toplevel()
        self.searchscreen_root.geometry("700x300")
        self.searchscreen_root.title("searchresults")

        self.searchtitle = Tkinter.Label(self.searchscreen_root, text="Search Results", bg="white", font="fixedsys")
        self.searchtitle.pack(fill=Tkinter.X)

        if Interface1.laptopordesktop == "laptop":
            self.url = "https://www.techbargains.com/category/359/computers/laptops"
            geturl = requests.get("https://www.techbargains.com/category/359/computers/laptops").text

        elif Interface1.laptopordesktop == "desktop":
            self.url = "https://www.techbargains.com/category/357/computers/desktops"
            geturl = requests.get("https://www.techbargains.com/category/357/computers/desktops").text

        self.soup = bs(geturl, "html.parser")

        self.computerbudget = budget
        self.computerbrandchoices = bchoices
        #variables for the techbargain object
        self.tbtitles = []
        self.tbtitleposition = 0
        self.tb_titleposition_compare = []

        self.tbprice = []
        self.tbpriceposition = 0
        #variable for the compare object
        self.laptoplistings = {}

        self.listingposition = 0
        self.listingincrease = 1
        self.listingdecrease = 1

        self.imglist = []
        self.imglistposition = 0

        self.photoposition = 0

    def techbargain(self):
        # gets techbargain titles
        for t in self.soup.find_all("a", class_="details hidden-xs"):

            stringtitles = str(t["title"])
            rawtitles = stringtitles.split()
            #Asks if the last 4 letters of the title is "MORE", This is a fail safe to make sure
            #every title has a price that accompanies it.
            if str(t["title"][-4:]) != "MORE":
                self.tbtitleposition += 1

                for titlekeywords in rawtitles:
                    if titlekeywords in self.computerbrandchoices:
                        self.tbtitles.append(t["title"])
                        self.tb_titleposition_compare.append(self.tbtitleposition)

        # gets techbargain prices
        for y in self.soup.find_all("span", class_="final-price"):
            self.tbpriceposition += 1
            if self.tbpriceposition in self.tb_titleposition_compare:

                tbrawprice = y.text[2:]

                if len(tbrawprice) == 6:
                    self.tbprice.append(int(tbrawprice[0:3]))

                elif len(tbrawprice) == 8:
                    # deletes the comma
                    self.tbprice.append(int(tbrawprice[0] + tbrawprice[2:5]))

                elif len(tbrawprice) == 5:
                    self.tbprice.append(int(tbrawprice[0] + tbrawprice[1:2]))

                else:
                    self.tbprice.append("price unavailable")

        # gets techbargain images
        for u in self.soup.find_all("img"):
            for p in self.tbtitles:
                #if image title is the same as techbargian title add the image to the list of images to load
                try:
                    if p == str(u["alt"]):
                        rawimg = str(u["src"])
                        self.imglist.append(rawimg)
                        print u["alt"]

                except:
                    print "wrong image"

    def compare(self):
        # loop through the techbargain title and price lists and adds the title and photo to the dictionary
        # if the price is less or equal to the set budget
        for c in range(len(self.tbtitles)):
            if self.tbprice[c] <= self.computerbudget:
                self.laptoplistings[self.tbtitles[c]] = self.imglist[c]

    def searchscreen(self):
        self.techbargain()
        self.compare()

        try:
            #loads and displays the first image and title then deletes the image so its not saved on the hard drive
            result_title = Tkinter.Label(self.searchscreen_root, text=str(self.tbtitles[0]),
                                         fg="darkgrey", font=("arial", 10), width=0)
            result_title.pack()

            urllib.urlretrieve("https:" + self.laptoplistings.values()[0], "firstphoto" + ".jpg")

            # loads and displays the starting image
            firstphotoLd = ImageTk.PhotoImage(Image.open("firstphoto" + ".jpg"))
            photo = Tkinter.Label(self.searchscreen_root, image=firstphotoLd, bg="darkgrey", bd=2)
            photo.image = firstphotoLd
            photo.pack()
            photo.place(x=140, y=65)
            # Removes the photo from laptopfinder file.
            os.remove("firstphoto" + ".jpg")


        except:
            #loads and displays a no results image
            noresults = Tkinter.Label(self.searchscreen_root,
                                      text="Sorry, there were no results for your brands within that price range.",
                                      font="fixedsys", fg="darkgrey")
            noresults.pack()
            noresults.place(x=52, y=75)

            sadsmileyLd = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\sad.png"))
            sadsmiley = Tkinter.Label(self.searchscreen_root, image=sadsmileyLd)
            sadsmiley.image = sadsmileyLd
            sadsmiley.pack()
            sadsmiley.place(x=290, y=120)

        def getphoto():
            try:
                randomphotoname = str(random.randint(1, 1000000))
                #downloads the image file from techbargain.com
                urllib.urlretrieve("https:" + self.laptoplistings.values()[self.listingposition], randomphotoname + ".jpg")
                #loads and displays the image
                photoLd = ImageTk.PhotoImage(Image.open(randomphotoname + ".jpg"))
                photo.config(image=photoLd)
                photo.image = photoLd
                photo.pack()
                photo.place(x=140, y=65)
                #Removes the photo from laptopfinder file.
                os.remove(randomphotoname + ".jpg")

            except:
                print "download error"


        def morelistings():
            self.listingposition += 1
            #if scrolled to the end of the listings switch back to the first listing
            if self.listingposition > len(self.laptoplistings.keys()) - 1:
                self.listingposition = 0

            print self.listingposition

            getphoto()
            #change listings forward
            result_title.config(text=str(self.laptoplistings.keys()[self.listingposition]))

        def lesslistings():
            self.listingposition -= 1
            # if scrolled to the start of the listings switch back to the last listing
            if self.listingposition < 0:
                self.listingposition = len(self.laptoplistings.keys()) - 1

            getphoto()
            result_title.config(text=self.laptoplistings.keys()[self.listingposition])

        #loads and displays the left and right arrows
        moreresultsimgld = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\rightarrow.png"))
        moreresultsarrow = Tkinter.Button(self.searchscreen_root, image=moreresultsimgld, bd=0, command=morelistings)
        moreresultsarrow.pack()
        moreresultsarrow.place(x=660, y=130)

        lessresultsimgld = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\leftarrow.png"))
        lessresultsarrow = Tkinter.Button(self.searchscreen_root, image=lessresultsimgld, bd=0, command=lesslistings)
        lessresultsarrow.pack()
        lessresultsarrow.place(x=0, y=130)

        self.searchscreen_root.mainloop()


class parameterscreen:

    def __init__(self, txt):
        # if i use Tkinter.Tk() for the parameter screen root the images dont work?
        self.p_root = Tkinter.Toplevel()
        self.p_root.title("Pc finder")
        self.p_root.geometry("540x300")

        self.budget1 = 0

        self.brandchoices = []
        #loads and displays the parameterscreen title
        paramlabel = Tkinter.Label(self.p_root, font="fixedsys", text=txt, bg="white")
        paramlabel.pack(fill = Tkinter.BOTH)
    #function for the parameter screen budget scale
    def range(self):
        self.pricerange = Tkinter.Scale(self.p_root, from_=0, to=2000, label="Budget", fg="darkgrey",
                                        orient=Tkinter.VERTICAL, length=250,
                                        sliderlength=12, bd=1, font="fixedsys",
                                        )

        self.pricerange.pack()
        self.pricerange.place(x=5, y=32)

    def choosecomputerbrand(self):

        def hpimgchg():
            # changes button to a different image to let user know brand is selected.

            # Is  there a better solution for changing the images when I click on the button?
            # I would make this into a function so i dont have to add an extra 75 lines but
            # tkinters command doesnt let me pass.

            if self.hpbrand.image == self.hpimg:
                hpselected = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\hphover.jpg"))
                self.hpbrand.config(image=hpselected)
                self.hpbrand.image = hpselected
                # adds keywords to brand choices
                self.brandchoices.extend(("hp", "Hp", "HP"))

            elif self.hpbrand.image != self.hpimg:
                self.hpbrand.config(image=self.hpimg)
                self.hpbrand.image = self.hpimg

                for hpremove in ["hp", "Hp", "HP"]:  # I guess just using 3 .removes would be easier to read but
                    self.brandchoices.remove(hpremove)  # I gotta save that 1 line of code :)

            print self.brandchoices

        # read this before hpimgchg
        self.hpimg = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\hp.jpg"))
        self.hpbrand = Tkinter.Button(self.p_root, image=self.hpimg, bd=0, command=hpimgchg)
        self.hpbrand.image = self.hpimg
        self.hpbrand.pack()
        self.hpbrand.place(x=140, y=80)

        # Same as above. Repeats 4 more times
        def dellimgchg():
            if self.dellbrand.image == self.dellimg:
                dellselected = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\dellselected.png"))
                self.dellbrand.config(image=dellselected)
                self.dellbrand.image = dellselected

                self.brandchoices.extend(("dell", "Dell", "DELL"))

            elif self.dellbrand.image != self.dellimg:
                self.dellbrand.config(image=self.dellimg)
                self.dellbrand.image = self.dellimg

                for hpremove in ["dell", "Dell", "DELL"]:
                    self.brandchoices.remove(hpremove)

        self.dellimg = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\dell.png"))
        self.dellbrand = Tkinter.Button(self.p_root, image=self.dellimg, bd=0, command=dellimgchg)
        self.dellbrand.image = self.dellimg
        self.dellbrand.pack()
        self.dellbrand.place(x=210, y=80)

        def appleimgchg():
            if self.applebrand.image == self.appleimg:
                appleselected = ImageTk.PhotoImage(
                    Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\appleselected.png"))
                self.applebrand.config(image=appleselected)
                self.applebrand.image = appleselected

                self.brandchoices.extend(("apple", "Apple", "APPLE"))

            elif self.applebrand.image != self.appleimg:
                self.applebrand.config(image=self.appleimg)
                self.applebrand.image = self.appleimg

                for hpremove in ["apple", "Apple", "APPLE"]:
                    self.brandchoices.remove(hpremove)

        self.appleimg = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\apple.png"))
        self.applebrand = Tkinter.Button(self.p_root, image=self.appleimg, bd=0, command=appleimgchg)
        self.applebrand.image = self.appleimg
        self.applebrand.pack()
        self.applebrand.place(x=280, y=80)

        def microsoftimgchg():
            if self.microsoftbrand.image == self.microsoftimg:
                microsoftselected = ImageTk.PhotoImage(
                    Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\microsoftselected.png"))
                self.microsoftbrand.config(image=microsoftselected)
                self.microsoftbrand.image = microsoftselected

                self.brandchoices.extend(("microsoft", "Microsoft", "MICROSOFT"))

            elif self.microsoftbrand.image != self.microsoftimg:
                self.microsoftbrand.config(image=self.microsoftimg)
                self.microsoftbrand.image = self.microsoftimg

                for hpremove in ["microsoft", "Microsoft", "MICROSOFT"]:
                    self.brandchoices.remove(hpremove)

        self.microsoftimg = ImageTk.PhotoImage(
            Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\microsoft.png"))
        self.microsoftbrand = Tkinter.Button(self.p_root, image=self.microsoftimg, bd=0, command=microsoftimgchg)
        self.microsoftbrand.image = self.microsoftimg
        self.microsoftbrand.pack()
        self.microsoftbrand.place(x=350, y=80)

        def lenovoimgchg():
            if self.lenovobrand.image == self.lenovoimg:
                lenovoselected = ImageTk.PhotoImage(
                    Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\lenovoselected.png"))
                self.lenovobrand.config(image=lenovoselected)
                self.lenovobrand.image = lenovoselected

                self.brandchoices.extend(("lenovo", "Lenovo", "LENOVO"))

            elif self.lenovobrand.image != self.lenovoimg:
                self.lenovobrand.config(image=self.lenovoimg)
                self.lenovobrand.image = self.lenovoimg

                for hpremove in ["lenovo", "Lenovo", "LENOVO"]:
                    self.brandchoices.remove(hpremove)

        self.lenovoimg = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\lenovo.png"))
        self.lenovobrand = Tkinter.Button(self.p_root, image=self.lenovoimg, bd=0, command=lenovoimgchg)
        self.lenovobrand.image = self.lenovoimg
        self.lenovobrand.pack()
        self.lenovobrand.place(x=140, y=150)

        def acerimgchg():
            if self.acerbrand.image == self.acerimg:
                acerselected = ImageTk.PhotoImage(
                    Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\acerselected.jpg"))
                self.acerbrand.config(image=acerselected)
                self.acerbrand.image = acerselected

                self.brandchoices.extend(("acer", "Acer", "ACER"))

            elif self.acerbrand.image != self.acerimg:
                self.acerbrand.config(image=self.acerimg)
                self.acerbrand.image = self.acerimg

                for hpremove in ["acer", "Acer", "ACER"]:
                    self.brandchoices.remove(hpremove)

        self.acerimg = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\acer.jpg"))
        self.acerbrand = Tkinter.Button(self.p_root, image=self.acerimg, bd=0, command=acerimgchg)
        self.acerbrand.image = self.acerimg
        self.acerbrand.pack()
        self.acerbrand.place(x=210, y=150)

        def razerimgchg():
            if self.razerbrand.image == self.razerimg:
                razerselected = ImageTk.PhotoImage(
                    Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\razerselected.jpg"))
                self.razerbrand.config(image=razerselected)
                self.razerbrand.image = razerselected

                self.brandchoices.extend(("razer", "Razer", "RAZER"))

            elif self.razerbrand.image != self.razerimg:
                self.razerbrand.config(image=self.razerimg)
                self.razerbrand.image = self.razerimg

                for hpremove in ["razer", "Razer", "RAZER"]:
                    self.brandchoices.remove(hpremove)

        self.razerimg = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\razer.png"))
        self.razerbrand = Tkinter.Button(self.p_root, image=self.razerimg, bd=0, command=razerimgchg)
        self.razerbrand.image = self.razerimg
        self.razerbrand.pack()
        self.razerbrand.place(x=280, y=150)

        def msiimgchg():
            if self.msibrand.image == self.msiimg:
                self.msiselected = ImageTk.PhotoImage(
                    Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\msiselected.jpg"))
                self.msibrand.config(image=self.msiselected)
                self.msibrand.image = self.msiselected

                self.brandchoices.extend(("msi", "Msi", "MSI"))

            elif self.msibrand.image != self.msiimg:
                self.msibrand.config(image=self.msiimg)
                self.msibrand.image = self.msiimg

                for hpremove in ["msi", "Msi", "MSI"]:
                    self.brandchoices.remove(hpremove)

        self.msiimg = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\msi.png"))
        self.msibrand = Tkinter.Button(self.p_root, image=self.msiimg, bd=0, command=msiimgchg)
        self.msibrand.image = self.msiimg
        self.msibrand.pack()
        self.msibrand.place(x=350, y=150)

    def findbutton(self):

        def buttoncommand():
            self.searchtrigger = search(self.pricerange.get(), self.brandchoices)
            self.searchtrigger.searchscreen()

        # Button that triggers the search class in the search file
        searchbutton = Tkinter.Button(self.p_root, text="FIND", font="fixedsys", fg="darkgrey",
                                      width=8, command=buttoncommand)

        searchbutton.pack()
        searchbutton.place(x=450, y=260)

    def paramterwidgets(self):
        self.choosecomputerbrand()
        self.range()
        self.findbutton()

    # how does this class work without me calling self.p_root.mainloop() ?


class screen:
    def __init__(self):
        print "tacos"
        self.laptopordesktop = ""

    # startupscreen and its widgets
    def startscreen(self):
        self.root = Tkinter.Tk()
        self.root.title("Pc finder")
        self.root.geometry("440x200")
        #
        self.defaultbg = self.root.cget("bg")
        #loads and displays the title for the startup screen
        startscreen_title = Tkinter.Label(self.root, font="fixedsys", text="What kind of computer would you like to find?",
                               width=40, bg="white")
        startscreen_title.pack(side=Tkinter.TOP, fill=Tkinter.X)
        #loads and displats the desktop image
        self.dtImageLd = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\desktop.png"))
        dtImage = Tkinter.Label(self.root, image=self.dtImageLd)
        dtImage.pack(side=Tkinter.LEFT)
        dtImage.place(x=45, y=45)
        #loads and displays the laptop image
        self.ltImageLd = ImageTk.PhotoImage(Image.open(r"C:\Users\Cameron\PycharmProjects\laptopdealfinder\programphotos\laptop.png"))
        ltImage = Tkinter.Label(self.root, image=self.ltImageLd)
        ltImage.pack(side=Tkinter.RIGHT)
        ltImage.place(x=275, y=40)

        def Dtchangescreen():
            # starts parameter screen(desktop version).
            self.laptopordesktop = "desktop"
            parameterscreen1 = parameterscreen("What kind of desktop would you like to find?")
            parameterscreen1.paramterwidgets()

        # Buttons
        b1 = Tkinter.Button(self.root, font="fixedsys", text="Desktops",
                            bg=self.defaultbg, command=Dtchangescreen
                            )
        b1.pack()
        b1.place(x=65, y=160)

        def Ltchangescreen():
            # starts parameter screen(laptop version)
            self.laptopordesktop = "laptop"
            parameterscreen1 = parameterscreen("What kind of laptop would you like to find?")
            parameterscreen1.paramterwidgets()

        b2 = Tkinter.Button(self.root, font="fixedsys", text="Laptops",
                            bg=self.defaultbg, command=Ltchangescreen
                            )

        b2.pack()
        b2.place(x=305, y=160)

        #

# starts the startup screen
Interface1 = screen()
Interface1.startscreen()
Interface1.root.mainloop()
