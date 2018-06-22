from PIL import Image, ImageTk
import Tkinter
from bs4 import BeautifulSoup as bs
import requests
import urllib
import random
import os
import webbrowser


# I know this my code format is probably confusing.Id also advise reading the code from the bottom to the top
#  This is the first program I spent a lot of time trying to
# figure out how to arrange. This is also my first gui program.  :) - Cameron


class search():  # brandchoices
    def __init__(self, budget, bchoices):

        self.searchscreen_root = Tkinter.Toplevel()
        self.searchscreen_root.geometry("600x300")
        self.searchscreen_root.title("searchresults")

        self.searchtitle = Tkinter.Label(self.searchscreen_root, text="Search Results", bg="white", font="fixedsys")
        self.searchtitle.pack(fill=Tkinter.X)

        if Interface1.laptopordesktop == "laptop":
            self.url = "https://www.techbargains.com/category/359/computers/laptops"
            geturl_microcenter = requests.get("http://www.microcenter.com/category/4294967288/Laptops-Notebooks").text
            geturl_tigerdirect = requests.get("http://www.tigerdirect.com/applications/category/category_tlc.asp?CatId=17").text

        elif Interface1.laptopordesktop == "desktop":
            self.url = "https://www.techbargains.com/category/357/computers/desktops"
            geturl_microcenter = requests.get("http://www.microcenter.com/category/4294967292/All-Desktops").text
            geturl_tigerdirect = requests.get("http://www.tigerdirect.com/applications/category/category_tlc.asp?CatId=6").text

        self.microcenter_soup = bs(geturl_microcenter, "html.parser")
        self.tigerdirect_soup = bs(geturl_tigerdirect, "lxml")

        self.computerbudget = budget
        self.computerbrandchoices = bchoices

        #listing variables
        self.titles = []
        self.titleposition = 0
        self.titleposition_compare = []

        self.price = []
        self.priceposition = 0

        self.rawlinks = []
        self.links = []

        self.imglist = []

        # variable for the compare object
        self.laptoplistings = {}
        #variables for the searchscreen object
        self.listingposition = 0

    def microcenter(self):
        for m in self.microcenter_soup.find_all("a", class_ = "image"):
            self.titleposition += 1
            brandname = m["data-brand"]
            mcstringtitles = m.text
            mcrawtitles = mcstringtitles.split()
            print mcrawtitles

            for mctitlekeywords in brandname:
                if brandname in self.computerbrandchoices:
                    #adds the title to the title list
                    if len(mcrawtitles) > 25:
                        cut = len(mcrawtitles) / 2
                        mctitle_firsthalf = str(" ".join(mcrawtitles[:cut]))
                        mctitle_secondhalf = str(" ".join(mcrawtitles[cut:]))
                        self.titles.append(mctitle_firsthalf + '\n' + mctitle_secondhalf)

                    #adds the link to the link list
                    self.rawlinks.append("www.microcenter.com" + str(m["href"]))
                    #adds the listing price to the price list
                    mcrawprice = str(m["data-price"])

                    if len(mcrawprice) == 5:
                        self.price.append(len(mcrawprice[0:2]))

                    elif len(mcrawprice) == 6:
                        self.price.append(len(mcrawprice[0:3]))

                    elif len(mcrawprice) == 7:
                        self.price.append(len(mcrawprice[0:4]))

                    # adds the photo to the photo list
                    mcphoto = m.find("img", class_ = "SearchResultProductImage")["src"]
                    self.imglist.append(mcphoto)


    def tigerdirect(self):
        #gets tigerdirect titles and links
        for d in self.tigerdirect_soup.find_all("div", class_ = "productImage"):
            self.titleposition += 1

            tdstringtitles = d.find("a")["title"]
            tdrawtitles = tdstringtitles.split()

            for tdtitlekeywords in tdrawtitles:
                if tdtitlekeywords in self.computerbrandchoices:
                    if len(tdrawtitles) > 25:
                        cut = len(tdrawtitles) / 2
                        tdtitle_firsthalf = str(" ".join(tdrawtitles[:cut]))
                        tdtitle_secondhalf = str(" ".join(tdrawtitles[cut:]))
                        self.titles.append(tdtitle_firsthalf + '\n' + tdtitle_secondhalf)

                    else:
                        self.titles.append(tdstringtitles)

                    #gets tigerdirect link minus the first two characters.
                    self.rawlinks.append("http://www.tigerdirect.com/applications" + str(d.find("a")["href"][2:]))
                    self.titleposition_compare.append(self.titleposition)
                    #gets tigerdirect images
                    self.imglist.append(str(d.find("img")["data-yo-src"]))

        #gets price
        for f in self.tigerdirect_soup.find_all("div", class_ = "salePrice"):
            self.priceposition += 1
            if self.priceposition in self.titleposition_compare:
                try:
                    tdrawprice = f.text

                    if len(tdrawprice) == 14:
                        self.price.append(int(f.text[7:10]))

                    elif len(tdrawprice) == 15:
                        self.price.append(int(f.text[8:11]))

                    elif len(tdrawprice) == 16:
                        self.price.append(int(f.text[9:12]))

                    elif len(tdrawprice) == 17:
                        self.price.append(int(f.text[10:13]))

                    elif len(tdrawprice) == 18:
                        self.price.append(int(f.text[11:14]))

                    elif len(tdrawprice) == 19:
                        self.price.append(int(f.text[12:15]))

                    else:
                        self.price.append(0)

                except:
                    print "unicode error"
                    self.price.append(0)

    def compare(self):
        # loop through the techbargain title and price lists and adds the title and photo to the dictionary
        # if the price is less or equal to the set budget
        for c in range(len(self.titles)):
            print len(self.titles), len(self.price)
            if self.price[c] <= self.computerbudget:
                self.laptoplistings[self.titles[c]] = [self.imglist[c], self.rawlinks[c]]


    def searchscreen(self):
        self.tigerdirect()
        self.microcenter()
        self.compare()

        def openlink():
            # link to listings
            webbrowser.open_new(self.laptoplistings.values()[self.listingposition][1])


        linkbutton = Tkinter.Button(self.searchscreen_root,
                                    text=self.laptoplistings.values()[0][1],
                                    fg="darkgrey", bd=0, command=openlink)
        linkbutton.pack(side = Tkinter.BOTTOM)


        def link():
            linkbutton.config(text = str(self.laptoplistings.values()[self.listingposition][1]))

        def fontsize():
            titlelength = len(self.laptoplistings.keys()[self.listingposition].split())

            if titlelength < 10:
                return 12
            elif titlelength < 20:
                return 10
            else:
                return 8


        result_title = Tkinter.Label(self.searchscreen_root, text=str(self.laptoplistings.keys()[0]),
                                        fg="darkgrey", font=("arial", fontsize()), width=0)
        result_title.pack()

        urllib.urlretrieve(self.laptoplistings.values()[self.listingposition][0], "firstphoto" + ".jpg")

        # loads and displays the first image and title then deletes the image so its not saved on the hard drive
        firstphotoLd = ImageTk.PhotoImage(Image.open("firstphoto" + ".jpg"))
        photo = Tkinter.Label(self.searchscreen_root, image=firstphotoLd, bg="darkgrey", bd=2)
        photo.image = firstphotoLd


        photo.pack()
        photo.place(x=100, y=65)
        # Removes the photo from laptopfinder file.
        os.remove("firstphoto" + ".jpg")

        #loads and displays the listing position
        position = Tkinter.Label(self.searchscreen_root, text = "0/" + str(len(self.laptoplistings.keys()) - 1),
                                 fg = "darkgrey", font = "fixedsys")
        position.pack()
        position.place(x = 290, y = 260)

        link()


        def getphoto():
            try:
                randomphotoname = str(random.randint(1, 1000000))
                #downloads the image file from techbargain.com
                urllib.urlretrieve(str(self.laptoplistings.values()[self.listingposition][0]), randomphotoname + ".jpg")
                #loads and displays the image
                photoLd = ImageTk.PhotoImage(Image.open(randomphotoname + ".jpg"))
                photo.config(image=photoLd)
                photo.image = photoLd
                photo.pack()
                photo.place(x=100, y=65)
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
            #changes photo forward
            getphoto()
            #change listings title forward
            result_title.config(text=str(self.laptoplistings.keys()[self.listingposition]), font = ("arial", fontsize()))
            #change listing number label forward
            position.config(text = str(self.listingposition) + "/" + str(len(self.laptoplistings.keys()) - 1))
            #change listing link forward
            link()

        def lesslistings():
            self.listingposition -= 1
            # if scrolled to the start of the listings switch back to the last listing
            if self.listingposition < 0:
                self.listingposition = len(self.laptoplistings.keys()) - 1
            #changes photo backward
            getphoto()
            #change listings title backward
            result_title.config(text=self.laptoplistings.keys()[self.listingposition], font = ("arial", fontsize()))
            # change listing number label backward
            position.config(text=str(self.listingposition) + "/" + str(len(self.laptoplistings.keys()) - 1))
            # change listing link backward
            link()


        #loads and displays the left and right arrows
        moreresultsimgld = ImageTk.PhotoImage(Image.open(r"programphotos\rightarrow.png"))
        moreresultsarrow = Tkinter.Button(self.searchscreen_root, image=moreresultsimgld, bd=0, command=morelistings)
        moreresultsarrow.pack()
        moreresultsarrow.place(x=560, y=130)

        lessresultsimgld = ImageTk.PhotoImage(Image.open(r"programphotos\leftarrow.png"))
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
                                        sliderlength=18, bd=1, font="fixedsys",
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
                hpselected = ImageTk.PhotoImage(Image.open(r"programphotos\hphover.jpg"))
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
        self.hpimg = ImageTk.PhotoImage(Image.open(r"programphotos\hp.jpg"))
        self.hpbrand = Tkinter.Button(self.p_root, image=self.hpimg, bd=0, command=hpimgchg)
        self.hpbrand.image = self.hpimg
        self.hpbrand.pack()
        self.hpbrand.place(x=140, y=80)

        # Same as above. Repeats 4 more times
        def dellimgchg():
            if self.dellbrand.image == self.dellimg:
                dellselected = ImageTk.PhotoImage(Image.open(r"programphotos\dellselected.png"))
                self.dellbrand.config(image=dellselected)
                self.dellbrand.image = dellselected

                self.brandchoices.extend(("dell", "Dell", "DELL"))

            elif self.dellbrand.image != self.dellimg:
                self.dellbrand.config(image=self.dellimg)
                self.dellbrand.image = self.dellimg

                for hpremove in ["dell", "Dell", "DELL"]:
                    self.brandchoices.remove(hpremove)

        self.dellimg = ImageTk.PhotoImage(Image.open(r"programphotos\dell.png"))
        self.dellbrand = Tkinter.Button(self.p_root, image=self.dellimg, bd=0, command=dellimgchg)
        self.dellbrand.image = self.dellimg
        self.dellbrand.pack()
        self.dellbrand.place(x=210, y=80)

        def appleimgchg():
            if self.applebrand.image == self.appleimg:
                appleselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\appleselected.png"))
                self.applebrand.config(image=appleselected)
                self.applebrand.image = appleselected

                self.brandchoices.extend(("apple", "Apple", "APPLE"))

            elif self.applebrand.image != self.appleimg:
                self.applebrand.config(image=self.appleimg)
                self.applebrand.image = self.appleimg

                for hpremove in ["apple", "Apple", "APPLE"]:
                    self.brandchoices.remove(hpremove)

        self.appleimg = ImageTk.PhotoImage(Image.open(r"programphotos\apple.png"))
        self.applebrand = Tkinter.Button(self.p_root, image=self.appleimg, bd=0, command=appleimgchg)
        self.applebrand.image = self.appleimg
        self.applebrand.pack()
        self.applebrand.place(x=280, y=80)

        def microsoftimgchg():
            if self.microsoftbrand.image == self.microsoftimg:
                microsoftselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\microsoftselected.png"))
                self.microsoftbrand.config(image=microsoftselected)
                self.microsoftbrand.image = microsoftselected

                self.brandchoices.extend(("microsoft", "Microsoft", "MICROSOFT"))

            elif self.microsoftbrand.image != self.microsoftimg:
                self.microsoftbrand.config(image=self.microsoftimg)
                self.microsoftbrand.image = self.microsoftimg

                for hpremove in ["microsoft", "Microsoft", "MICROSOFT"]:
                    self.brandchoices.remove(hpremove)

        self.microsoftimg = ImageTk.PhotoImage(
            Image.open(r"programphotos\microsoft.png"))
        self.microsoftbrand = Tkinter.Button(self.p_root, image=self.microsoftimg, bd=0, command=microsoftimgchg)
        self.microsoftbrand.image = self.microsoftimg
        self.microsoftbrand.pack()
        self.microsoftbrand.place(x=350, y=80)

        def lenovoimgchg():
            if self.lenovobrand.image == self.lenovoimg:
                lenovoselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\lenovoselected.png"))
                self.lenovobrand.config(image=lenovoselected)
                self.lenovobrand.image = lenovoselected

                self.brandchoices.extend(("lenovo", "Lenovo", "LENOVO"))

            elif self.lenovobrand.image != self.lenovoimg:
                self.lenovobrand.config(image=self.lenovoimg)
                self.lenovobrand.image = self.lenovoimg

                for hpremove in ["lenovo", "Lenovo", "LENOVO"]:
                    self.brandchoices.remove(hpremove)

        self.lenovoimg = ImageTk.PhotoImage(Image.open(r"programphotos\lenovo.png"))
        self.lenovobrand = Tkinter.Button(self.p_root, image=self.lenovoimg, bd=0, command=lenovoimgchg)
        self.lenovobrand.image = self.lenovoimg
        self.lenovobrand.pack()
        self.lenovobrand.place(x=140, y=150)

        def acerimgchg():
            if self.acerbrand.image == self.acerimg:
                acerselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\acerselected.jpg"))
                self.acerbrand.config(image=acerselected)
                self.acerbrand.image = acerselected

                self.brandchoices.extend(("acer", "Acer", "ACER"))

            elif self.acerbrand.image != self.acerimg:
                self.acerbrand.config(image=self.acerimg)
                self.acerbrand.image = self.acerimg

                for hpremove in ["acer", "Acer", "ACER"]:
                    self.brandchoices.remove(hpremove)

        self.acerimg = ImageTk.PhotoImage(Image.open(r"programphotos\acer.jpg"))
        self.acerbrand = Tkinter.Button(self.p_root, image=self.acerimg, bd=0, command=acerimgchg)
        self.acerbrand.image = self.acerimg
        self.acerbrand.pack()
        self.acerbrand.place(x=210, y=150)

        def razerimgchg():
            if self.razerbrand.image == self.razerimg:
                razerselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\razerselected.jpg"))
                self.razerbrand.config(image=razerselected)
                self.razerbrand.image = razerselected

                self.brandchoices.extend(("razer", "Razer", "RAZER"))

            elif self.razerbrand.image != self.razerimg:
                self.razerbrand.config(image=self.razerimg)
                self.razerbrand.image = self.razerimg

                for hpremove in ["razer", "Razer", "RAZER"]:
                    self.brandchoices.remove(hpremove)

        self.razerimg = ImageTk.PhotoImage(Image.open(r"programphotos\razer.png"))
        self.razerbrand = Tkinter.Button(self.p_root, image=self.razerimg, bd=0, command=razerimgchg)
        self.razerbrand.image = self.razerimg
        self.razerbrand.pack()
        self.razerbrand.place(x=280, y=150)

        def msiimgchg():
            if self.msibrand.image == self.msiimg:
                self.msiselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\msiselected.jpg"))
                self.msibrand.config(image=self.msiselected)
                self.msibrand.image = self.msiselected

                self.brandchoices.extend(("msi", "Msi", "MSI"))

            elif self.msibrand.image != self.msiimg:
                self.msibrand.config(image=self.msiimg)
                self.msibrand.image = self.msiimg

                for hpremove in ["msi", "Msi", "MSI"]:
                    self.brandchoices.remove(hpremove)

        self.msiimg = ImageTk.PhotoImage(Image.open(r"programphotos\msi.png"))
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
        self.dtImageLd = ImageTk.PhotoImage(Image.open(r"programphotos\desktop.png"))
        dtImage = Tkinter.Label(self.root, image=self.dtImageLd)
        dtImage.pack(side=Tkinter.LEFT)
        dtImage.place(x=45, y=45)
        #loads and displays the laptop image
        self.ltImageLd = ImageTk.PhotoImage(Image.open(r"programphotos\laptop.png"))
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
