
from PIL import Image, ImageTk, ImageOps
import Tkinter
from bs4 import BeautifulSoup as bs
import requests
import urllib
import random
import time
import os
import webbrowser


class search():                # brandchoices
    def __init__(self, budget, bchoices):

        self.searchscreen_root = Tkinter.Toplevel()
        self.searchscreen_root.geometry("600x300")
        self.searchscreen_root.title("searchresults")

        self.searchtitle = Tkinter.Label(self.searchscreen_root, text="Search Results", bg="white", font="fixedsys")
        self.searchtitle.pack(fill=Tkinter.X)

        if Interface1.laptopordesktop == "laptop":

            geturl_hsn = requests.get("https://www.hsn.com/shop/laptops/ec0033").text
            geturl_microcenter = requests.get("http://www.microcenter.com/category/4294967288/Laptops-Notebooks").text
            geturl_tigerdirect = requests.get("http://www.tigerdirect.com/applications/category/category_tlc.asp?CatId=17").text

        elif Interface1.laptopordesktop == "desktop":

            geturl_hsn = requests.get("https://www.hsn.com/shop/desktop-computers/ec0031?akamai-feo=off").text
            geturl_microcenter = requests.get("http://www.microcenter.com/category/4294967292/All-Desktops").text
            geturl_tigerdirect = requests.get("http://www.tigerdirect.com/applications/category/category_tlc.asp?CatId=6").text

        self.hsn_soup = bs(geturl_hsn, "html.parser")
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
        self.imgposition = 0

        self.starlist = []
        self.starposition = 0

        # variable for the compare object
        self.laptoplistings = {}
        # variables for the searchscreen object
        self.listingposition = 0

    def hsn(self):
        for g in self.hsn_soup("li", class_ = "item product-item module violated"):
            self.titleposition += 1

            hsnstringtitles = g.find("span", itemprop = "name").text
            hsnrawtitles = hsnstringtitles.split()

            for hsntitlekeywords in hsnrawtitles:
                if hsntitlekeywords in self.computerbrandchoices:
                    # adds the title to the title list
                    if len(hsnrawtitles) > 25: #splits the title in half if its too long.
                        try:
                            cut = len(hsnrawtitles) / 2
                            tdtitle_firsthalf = str(" ".join(hsnrawtitles[:cut]))
                            tdtitle_secondhalf = str(" ".join(hsnrawtitles[cut:]))
                            self.titles.append(tdtitle_firsthalf + '\n' + tdtitle_secondhalf)

                        except:  # Unicode error, happens every 1/300
                            print "unicode error"
                            self.titles.append(hsnstringtitles)

                    else:
                        self.titles.append(hsnstringtitles)

                    self.titleposition_compare.append(self.titleposition)
                    #gets hsn link
                    hsnlink = "https://www.hsn.com" + str(g["data-product-url"])
                    self.rawlinks.append(hsnlink)
                    #gets hsn photo link
                    try:
                        hsnphotolink = str(g.find("img", class_ = "lazy")["data-original"])
                        self.imglist.append(hsnphotolink)

                    except:
                        self.imglist.append("https://abtsmoodle.org/abtslebanon.org/wp-content/uploads/2017/10/image_unavailable.jpg")



                    try:
                        hsnrawprice = str(g.find("span", itemprop = "price").text)

                        if len(hsnrawprice) == 6:
                            hsnprice = hsnrawprice[0:3]

                        elif len(hsnrawprice) == 7:
                            hsnprice = hsnrawprice[0:4]

                        else:
                            hsnprice = 2001


                        self.price.append(int(hsnprice))

                    except:
                        self.price.append(2001)


                    try:  # Try because some listings dont have html if there is no reviews.
                        raw_hsn_starrating = g.find("span", itemprop="ratingValue").text

                        # Asks if the length is equal to that of a float or a interger.
                        if len(raw_hsn_starrating) == 3:
                            # changes it from unicode to back to a float then rounds it.
                            hsn_starrating = int(round(float(raw_hsn_starrating)))
                            self.starlist.append(hsn_starrating)

                        elif len(raw_hsn_starrating) == 1:
                            hsn_starrating = int(raw_hsn_starrating)
                            self.starlist.append(hsn_starrating)

                        else:
                            self.starlist.append(0)

                    except:
                        self.starlist.append(0)



    # Any efforts to increase the speed of the microcenter search process are appreciated
    def microcenter(self):
        # Gets the main product tag
        for m in self.microcenter_soup.find_all("li", class_ = "product_wrapper"):
            self.titleposition += 1
            mcstringtitles = str(m.find("div", class_="normal").text)
            mcrawtitles = mcstringtitles.split()
            # Gets the products brand
            rawbrandname = m.find("div", class_= "normal")
            brandname = rawbrandname.find("a")["data-brand"]

            if brandname in self.computerbrandchoices:
                # adds the title to the title list
                if len(mcrawtitles) > 15:
                    cut = len(mcrawtitles) / 2
                    mctitle_firsthalf = str(" ".join(mcrawtitles[:cut]))
                    mctitle_secondhalf = str(" ".join(mcrawtitles[cut:]))

                    self.titles.append(mctitle_firsthalf + "\n" + mctitle_secondhalf)

                else:
                    self.titles.append(mcstringtitles)

                self.titleposition_compare.append(self.titleposition)

                # adds the link to the link list
                mcrawlink = m.find("div", class_ = "normal")
                mclink = str(mcrawlink.find("a")["href"])

                self.rawlinks.append("www.microcenter.com" + mclink)

                # adds the listing price to the price list
                mcrawprice = m.find("div", class_ = "normal")
                mcpricedata = str(mcrawprice.find("a")["data-price"])

                try:
                    print len(mcpricedata)
                    if len(mcpricedata) == 5:
                        mcprice = int(mcpricedata[0:2])

                    elif len(mcpricedata) == 6:
                        mcprice = int(mcpricedata[0:3])

                    elif len(mcpricedata) == 7:
                        mcprice = int(mcpricedata[0:4])

                    else:              # 1 dollar above max budget
                                            # to phase out listing
                        mcprice = 2001

                    self.price.append(mcprice)
                except:
                    print "unicode error in microcenter price"
                    self.price.append(2001)

                # Gets the image

                # Opens the listing page to get the image
                mcimageurl = requests.get("http://www.microcenter.com" + mclink).text
                mcimagesoup = bs(mcimageurl, "html.parser")

                try:

                    mcrawimg = mcimagesoup.find("div", class_ = "image-slide")
                    mcimg = mcrawimg.find("img", class_ = "productImageZoom")["src"]
                    self.imglist.append(mcimg)

                except:
                    # Adds image unavailable image when unicode error or listing has no image.
                    self.imglist.append("https://abtsmoodle.org/abtslebanon.org/wp-content/uploads/2017/10/image_unavailable.jpg")

                #
                # Formats then adds the star rating
                try:
                    rawstars = m.find("div", class_="ratingstars")

                    mc_starrating = int(rawstars.text[:3])
                    print mc_starrating
                    self.starlist.append(mc_starrating)

                except:
                    self.starlist.append(0)

        print len(self.titles), len(self.price), len(self.rawlinks), len(self.imglist), len(self.starlist)

    def tigerdirect(self):
        # Gets tigerdirect titles and links
        for d in self.tigerdirect_soup.find_all("div", class_="product"):

            tdstringtitles = d.find("a", class_ = "itemImage")["title"]
            tdrawtitles = tdstringtitles.split()

            for tdtitlekeywords in tdrawtitles:
                if tdtitlekeywords in self.computerbrandchoices:
                    #splits the title
                    if len(tdrawtitles) > 25:
                        try:
                            cut = len(tdrawtitles) / 2
                            tdtitle_firsthalf = str(" ".join(tdrawtitles[:cut]))
                            tdtitle_secondhalf = str(" ".join(tdrawtitles[cut:]))
                            self.titles.append(tdtitle_firsthalf + '\n' + tdtitle_secondhalf)
                        # Unicode error, happens every 1/300
                        except:
                            print "unicode error"
                            self.titles.append(tdstringtitles)

                    else:
                        self.titles.append(tdstringtitles)


                    # gets tigerdirect link minus the first two characters.
                    tdlink = str(d.find("a", class_ = "itemImage")["href"][2:])
                    self.rawlinks.append("http://www.tigerdirect.com/applications" + tdlink)
                    # gets tigerdirect images
                    tdimage = str(d.find("img")["data-yo-src"])
                    self.imglist.append(tdimage)

                    # Gets price
                    try:
                        tdrawprice_parenttag = d.find("div", class_ = "productAction")
                        tdrawprice = tdrawprice_parenttag.find("div", class_= "salePrice").text

                        if len(tdrawprice) == 14:
                            tdprice = int(tdrawprice[7:10])

                        elif len(tdrawprice) == 15:
                            tdprice = int(tdrawprice[8:11])

                        elif len(tdrawprice) == 16:
                            tdprice = int(tdrawprice[9:12])

                        elif len(tdrawprice) == 17:
                            tdprice = int(tdrawprice[10:13])

                        elif len(tdrawprice) == 18:
                            tdprice = int(tdrawprice[11:14])

                        elif len(tdrawprice) == 19:
                            tdprice = int(tdrawprice[12:15])
                        else:
                            tdprice = 2001

                        self.price.append(tdprice)

                    except:
                        self.price.append(2001)
                        print "td price error"

                    #gets tigerdirect star rating for listing
                    try:
                        tdrawstars = d.find("a", class_ = "itemRating")["title"]

                        if str(tdrawstars) == "Be the first to write a review":
                            tdstars = 0
                        else:

                            tdstars = str(tdrawstars[0:1])
                            print tdstars

                        self.starlist.append(tdstars)

                    except:
                        self.starlist.append(0)
                        print "td starlist error"

        print len(self.titles), len(self.price), len(self.rawlinks), len(self.imglist), self.starlist


    def compare(self):
        # Loop through the techbargain title and price lists and adds the collected values to the dictionary
        # if the price is less or equal to the set budget
        for c in range(len(self.titles)):
            if self.price[c] <= self.computerbudget:
                self.laptoplistings[self.titles[c]] = [self.price[c], self.imglist[c], self.rawlinks[c], self.starlist[c]]


    def searchscreen(self):
        # Starts the data-collection process through all the websites.
        self.hsn()
        self.microcenter()
        self.tigerdirect()
        # Starts the process to store all the data together in a dictionary
        self.compare()


        if len(self.laptoplistings) == 0:
            Noresultstext = Tkinter.Label(self.searchscreen_root,text = "Sorry, there are no results available.",
                                          fg = "darkgrey",font = "fixedsys" )
            Noresultstext.pack()
            Noresultstext.place(x = 140, y = 170)

            Noresultsphotold = ImageTk.PhotoImage(Image.open(r"programphotos\sad.jpg"))
            Noresultsphoto = Tkinter.Label(self.searchscreen_root, image = Noresultsphotold)
            Noresultsphoto.Image = Noresultsphotold
            Noresultsphoto.pack()
            Noresultsphoto.place(x = 260, y = 90)

        else:
            def openlink():
                # link to listings
                webbrowser.open_new(self.laptoplistings.values()[self.listingposition][2])


            linkbutton = Tkinter.Button(self.searchscreen_root,
                                    text=self.laptoplistings.values()[0][2],
                                    fg="darkgrey", bd=0, command=openlink)
            linkbutton.pack(side = Tkinter.BOTTOM)


            def fontsize():
                titlelength = len(self.laptoplistings.keys()[self.listingposition].split())

                if titlelength < 10:
                    return 12
                elif titlelength < 20:
                    return 10
                else:
                    return 8

            result_title = Tkinter.Label(self.searchscreen_root, text=self.laptoplistings.keys()[0],
                                    fg="darkgrey", font=("arial", fontsize()))

            result_title.pack()

            urllib.urlretrieve(self.laptoplistings.values()[0][1], "firstphoto" + ".jpg")

            # Loads and displays the first image and title then deletes the image so its not saved on the hard drive
            PILfirstphotold = Image.open("firstphoto" + ".jpg")
            # Configures the size of the image
            PILfirstphotoconfig = PILfirstphotold.resize((240, 170), Image.ANTIALIAS)
            firstphotoLd = ImageTk.PhotoImage(PILfirstphotoconfig)

            photo = Tkinter.Label(self.searchscreen_root, image=firstphotoLd, bg="darkgrey", bd=2)
            photo.image = firstphotoLd


            photo.pack()
            photo.place(x=80, y=75)
            # Removes the photo from laptopfinder file.
            os.remove("firstphoto" + ".jpg")


            def starrating():

                if int(self.laptoplistings.values()[self.listingposition][3]) != 0:
                    starlength = "programphotos" + "/" + str(self.laptoplistings.values()[self.listingposition][3]) + "star.png"

                else:
                    starlength = "programphotos/0star.png"

                return starlength

            starget = starrating()
            starimgLd = ImageTk.PhotoImage(Image.open(starget))

            starimg = Tkinter.Label(self.searchscreen_root, image = starimgLd, bg = "darkgrey",  bd = 2)
            starimg.pack()
            starimg.place(x = 350, y = 90)


            def seereviews_visible():
                # Asks if the star rating isnt 0
                if int(self.laptoplistings.values()[self.listingposition][3]) != 0:
                    seereviews_text = "(See Reviews)"

                else:
                    seereviews_text = ""

                return seereviews_text


            def seereviews_link():
                webbrowser.open_new(self.laptoplistings.values()[self.listingposition][2])


            seereviews = Tkinter.Button(self.searchscreen_root, font = "fixedsys", bd = 0,
                                       fg = "darkgrey", text = seereviews_visible(),
                                        command = seereviews_link)
            seereviews.pack()
            seereviews.place(x = 373, y = 147)


            # Loads and displays the listing position
            position = Tkinter.Label(self.searchscreen_root, text = "0/" + str(len(self.laptoplistings.keys()) - 1),
                                 fg = "darkgrey", font = "fixedsys")
            position.pack()
            position.place(x = 290, y = 260)

            # Loads and displays the price
            pricelabel = Tkinter.Label(self.searchscreen_root, text = "Price: " + "$" +
                                        str(self.laptoplistings.values()[0][0]),
                                        font = ("fixedsys", 15), fg = "darkgrey")

            pricelabel.pack()
            pricelabel.place(x = 370, y = 200)


            def getphoto():
                try:
                    randomphotoname = str(random.randint(1, 1000000))
                    # Downloads the image file from techbargain.com
                    photolink = self.laptoplistings.values()[self.listingposition][1]
                    urllib.urlretrieve(photolink, randomphotoname + ".jpg")
                    # Loads and displays the image
                    PILphotold = Image.open(randomphotoname + ".jpg")
                                         # Changes img size to a default
                    PILphotold_config = PILphotold.resize((240, 170), Image.ANTIALIAS)
                    listingphoto = ImageTk.PhotoImage(PILphotold_config)

                    photo.config(image=listingphoto)
                    photo.image = listingphoto
                    photo.pack()
                    photo.place(x=80, y=75)
                    # Removes the photo from laptopfinder file.
                    os.remove(randomphotoname + ".jpg")

                except:
                    print "download error"


            def morelistings():
                self.listingposition += 1
                # If scrolled to the end of the listings switch back to the first listing
                if self.listingposition > len(self.laptoplistings.keys()) - 1:
                    self.listingposition = 0

                print self.listingposition
                # Changes photo forward
                getphoto()
                # Change listings title forward
                result_title.config(text=self.laptoplistings.keys()[self.listingposition], font = ("arial", fontsize()))
                # Change listing number label forward
                position.config(text = str(self.listingposition) + "/" + str(len(self.laptoplistings.keys()) - 1))
                #   Change listing link forward
                linkbutton.config(text=str(self.laptoplistings.values()[self.listingposition][2]))

                # Change price label forward
                pricelabel.config(text="Price: " + "$" +
                                   str(self.laptoplistings.values()[self.listingposition][0]))

                starimgLd_config = ImageTk.PhotoImage(Image.open(starrating()))
                starimg.config(image=starimgLd_config)
                starimg.image = starimgLd_config
                # Configures the See Reviews link to be visible or invisible
                seereviews.config(text = seereviews_visible())

            def lesslistings():
                self.listingposition -= 1
                # If scrolled to the start of the listings switch back to the last listing
                if self.listingposition < 0:
                    self.listingposition = len(self.laptoplistings.keys()) - 1
                # Changes photo backward
                getphoto()
                # Change listings title backward
                result_title.config(text=self.laptoplistings.keys()[self.listingposition], font = ("arial", fontsize()))
                # Change listing number label backward
                position.config(text=str(self.listingposition) + "/" + str(len(self.laptoplistings.keys()) - 1))
                # Change listing link backward
                linkbutton.config(text=str(self.laptoplistings.values()[self.listingposition][2]))

                starimgLd_config = ImageTk.PhotoImage(Image.open(starrating()))
                starimg.config(image=starimgLd_config)
                starimg.image = starimgLd_config
                # Change price label backward
                pricelabel.config(text="Price: " + "$" +
                                   str(self.laptoplistings.values()[self.listingposition][0]))
                # Configures the See Reviews link to be visible or invisible
                seereviews.config(text=seereviews_visible())


            # Loads and displays the left and right arrows
            moreresultsimgld = ImageTk.PhotoImage(Image.open(r"programphotos\rightarrow.png"))
            moreresultsarrow = Tkinter.Button(self.searchscreen_root, image=moreresultsimgld, bd=0, command=morelistings)
            moreresultsarrow.pack()
            moreresultsarrow.place(x=560, y=130)

            lessresultsimgld = ImageTk.PhotoImage(Image.open(r"programphotos\leftarrow.png"))
            lessresultsarrow = Tkinter.Button(self.searchscreen_root, image=lessresultsimgld, bd=0, command=lesslistings)
            lessresultsarrow.pack()
            lessresultsarrow.place(x=0, y=130)

            self.searchscreen_root.mainloop()


class parameterscreen():

    def __init__(self, txt):
        # If i use Tkinter.Tk() for the parameter screen root the images dont work?
        self.p_root = Tkinter.Toplevel()
        self.p_root.title("Pc finder")
        self.p_root.geometry("540x300")

        self.budget1 = 0

        self.brandchoices = []
        #loads and displays the parameterscreen title
        paramlabel = Tkinter.Label(self.p_root, font="fixedsys", text=txt, bg="white")
        paramlabel.pack(fill = Tkinter.BOTH)

        # Loads the wait label but doesnt display it until search button is clicked
        self.loadtimelabel = Tkinter.Label(self.p_root, text="Please wait 30 seconds to 1 minute for results to load.",
                                      font="fixedsys", fg=self.p_root.cget("bg"))
        self.loadtimelabel.pack()
        self.loadtimelabel.place(x=370, y=260)


    # Function for the parameter screen budget scale
    def range(self):
        self.pricerange = Tkinter.Scale(self.p_root, from_=0, to=2000, label="Budget", fg="darkgrey",
                                        orient=Tkinter.VERTICAL, length=250,                   #used root background
                                        sliderlength=14, bd=1, font="fixedsys", troughcolor = self.p_root.cget("bg"),
                                        )

        self.pricerange.pack()
        self.pricerange.place(x=5, y=32)

    def choosecomputerbrand(self):

        def hpimgchg():
            # Changes button to a different image to let user know brand is selected.

            # Is  there a better solution for changing the images when I click on the button?
            # I would make this into a function so i dont have to add an extra 75 lines but
            # tkinters command doesnt let me pass.

            if self.hpbrand.image == self.hpimg:
                hpselected = ImageTk.PhotoImage(Image.open(r"programphotos\hphover.jpg"))
                self.hpbrand.config(image=hpselected)
                self.hpbrand.image = hpselected
                # Adds keywords to brand choices
                self.brandchoices.extend(("hp", "Hp", "HP"))

            elif self.hpbrand.image != self.hpimg:
                self.hpbrand.config(image=self.hpimg)
                self.hpbrand.image = self.hpimg

                for hpremove in ["hp", "Hp", "HP"]:  # I guess just using 3 .removes would be easier to read but
                    self.brandchoices.remove(hpremove)  # I gotta save that 1 line of code :)

            print self.brandchoices

        # Read this before hpimgchg
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
                appleselected = ImageTk.PhotoImage(Image.open(r"programphotos\appleselected.png"))
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
                self.msiselected = ImageTk.PhotoImage(Image.open(r"programphotos\msiselected.jpg"))
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

        loadtimelabel = Tkinter.Label(self.p_root, text="Please wait 30 seconds to 1 minute for results to load.",
                                      font=("Arial", 8), fg="lightgrey")
        loadtimelabel.pack()
        loadtimelabel.place(x=130, y=265)

        def buttoncommand():

            self.searchtrigger = search(self.pricerange.get(), self.brandchoices)
            self.searchtrigger.searchscreen()

        # Button that triggers the search class in the search file
        searchbutton = Tkinter.Button(self.p_root, text="FIND", font="fixedsys", fg="darkgrey",
                                      width=8, command=buttoncommand)

        searchbutton.pack()
        searchbutton.place(x=450, y=260)

    def paramterwidgets(self):
        #starts all parameter screen widgets
        self.choosecomputerbrand()
        self.range()
        self.findbutton()


class screen():
    def __init__(self):
        print "tacos"
        self.laptopordesktop = ""

    # Startup screen and its widgets
    def startscreen(self):
        self.root = Tkinter.Tk()
        self.root.title("Pc finder")
        self.root.geometry("440x200")

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
            # Starts parameter screen(desktop version).
            self.laptopordesktop = "desktop"
            parameterscreen1 = parameterscreen("What kind of desktop would you like to find?")
            parameterscreen1.paramterwidgets()

        # Buttons
        b1 = Tkinter.Button(self.root, font="fixedsys", text="Desktops",
                            bg=self.root.cget("bg"), command=Dtchangescreen
                            )   #gets default background
        b1.pack()
        b1.place(x=65, y=160)

        def Ltchangescreen():
            # Starts parameter screen(laptop version)
            self.laptopordesktop = "laptop"
            parameterscreen1 = parameterscreen("What kind of laptop would you like to find?")
            parameterscreen1.paramterwidgets()

        b2 = Tkinter.Button(self.root, font="fixedsys", text="Laptops",
                            bg=self.root.cget("bg"), command=Ltchangescreen
                            )

        b2.pack()
        b2.place(x=305, y=160)

        #

# Starts the startup screen
Interface1 = screen()
Interface1.startscreen()
Interface1.root.mainloop()
