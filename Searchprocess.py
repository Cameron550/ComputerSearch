
from bs4 import BeautifulSoup as bs
import requests


class search():
    def __init__(self, budget, goodreviewschoice, bchoices, websitelinks):

        # Grabs HTML from chosen sites
        self.hsn_soup = bs(requests.get(websitelinks[0]).text, "html.parser")
        self.microcenter_soup = bs(requests.get(websitelinks[1]).text, "html.parser")
        self.tigerdirect_soup = bs(requests.get(websitelinks[2]).text, "lxml")

        self.computerbudget = budget
        self.reviewswitch = goodreviewschoice
        self.computerbrandchoices = bchoices

        # Computer listing variables
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


    def hsn(self):
        for g in self.hsn_soup("li", class_="item product-item module violated"):
            self.titleposition += 1

            hsnstringtitles = g.find("span", itemprop="name").text
            hsnrawtitles = hsnstringtitles.split()

            for hsntitlekeywords in hsnrawtitles:
                if hsntitlekeywords in self.computerbrandchoices:
                    # adds the title to the title list
                    if len(hsnrawtitles) > 25:  # splits the title in half if its too long.
                        try:
                            cut = len(hsnrawtitles) / 2
                            tdtitle_firsthalf = str(" ".join(hsnrawtitles[:cut]))
                            tdtitle_secondhalf = str(" ".join(hsnrawtitles[cut:]))
                            self.titles.append(tdtitle_firsthalf + '\n' + tdtitle_secondhalf)

                        except:  # Unicode error, happens every 1/300, appends the not cut title
                            print "unicode error"
                            self.titles.append(hsnstringtitles)

                    else:
                        self.titles.append(hsnstringtitles)

                    self.titleposition_compare.append(self.titleposition)
                    # gets hsn link
                    hsnlink = "https://www.hsn.com" + str(g["data-product-url"])
                    self.rawlinks.append(hsnlink)
                    # gets hsn photo link
                    try:
                        hsnphotolink = str(g.find("img", class_="lazy")["data-original"])
                        self.imglist.append(hsnphotolink)

                    except:
                        self.imglist.append(
                            "https://abtsmoodle.org/abtslebanon.org/wp-content/uploads/2017/10/image_unavailable.jpg")

                    try:
                        hsnrawprice = str(g.find("span", itemprop="price").text)

                        if len(hsnrawprice) == 6:
                            hsnprice = hsnrawprice[0:3]

                        elif len(hsnrawprice) == 7:
                            hsnprice = hsnrawprice[0:4]

                        else:
                            hsnprice = 2001

                        self.price.append(int(hsnprice))

                    except:
                        # appends an invalid price canceling out the listing if above code doesnt work on HTML
                        self.price.append(2001)

                    try:  # Try because some listings dont have html if there are no reviews.
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
        for m in self.microcenter_soup.find_all("li", class_="product_wrapper"):
            self.titleposition += 1
            mcstringtitles = str(m.find("div", class_="normal").text)
            mcrawtitles = mcstringtitles.split()
            # Gets the products brand
            rawbrandname = m.find("div", class_="normal")
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
                mcrawlink = m.find("div", class_="normal")
                mclink = str(mcrawlink.find("a")["href"])

                self.rawlinks.append("www.microcenter.com" + mclink)

                # adds the listing price to the price list
                mcrawprice = m.find("div", class_="normal")
                mcpricedata = str(mcrawprice.find("a")["data-price"])

                try:
                    print len(mcpricedata)
                    if len(mcpricedata) == 5:
                        mcprice = int(mcpricedata[0:2])

                    elif len(mcpricedata) == 6:
                        mcprice = int(mcpricedata[0:3])

                    elif len(mcpricedata) == 7:
                        mcprice = int(mcpricedata[0:4])

                    else:  # 1 dollar above max budget
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

                    mcrawimg = mcimagesoup.find("div", class_="image-slide")
                    mcimg = mcrawimg.find("img", class_="productImageZoom")["src"]
                    self.imglist.append(mcimg)

                except:
                    # Adds image unavailable image when unicode error or listing has no image.
                    self.imglist.append(
                        "https://abtsmoodle.org/abtslebanon.org/wp-content/uploads/2017/10/image_unavailable.jpg")

                #
                # Formats then adds the star rating
                try:
                    rawstars = m.find("div", class_="ratingstars")

                    mc_starrating = int(rawstars.text[:3])
                    print mc_starrating
                    self.starlist.append(mc_starrating)

                except:
                    self.starlist.append(0)

    def tigerdirect(self):
        # Gets tigerdirect titles and links
        for d in self.tigerdirect_soup.find_all("div", class_="product"):

            tdstringtitles = d.find("a", class_="itemImage")["title"]
            tdrawtitles = tdstringtitles.split()

            for tdtitlekeywords in tdrawtitles:
                if tdtitlekeywords in self.computerbrandchoices:
                    # splits the title
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
                    tdlink = str(d.find("a", class_="itemImage")["href"][2:])
                    self.rawlinks.append("http://www.tigerdirect.com/applications" + tdlink)
                    # gets tigerdirect images
                    tdimage = str(d.find("img")["data-yo-src"])
                    self.imglist.append(tdimage)

                    # Gets price
                    try:
                        tdrawprice_parenttag = d.find("div", class_="productAction")
                        tdrawprice = tdrawprice_parenttag.find("div", class_="salePrice").text

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

                    # gets tigerdirect star rating for listing
                    try:
                        tdrawstars = d.find("a", class_="itemRating")["title"]

                        if str(tdrawstars) == "Be the first to write a review":
                            tdstars = 0
                        else:

                            tdstars = str(tdrawstars[0:1])
                            print tdstars

                        self.starlist.append(tdstars)

                    except:
                        self.starlist.append(0)
                        print "td starlist error"

    def compare(self):
        # Loop through the techbargain title and price lists and adds the collected values to the dictionary
        # if the price is less or equal to the set budget

        for c in range(len(self.titles)):

            if self.reviewswitch == True:
                extracompare = self.starlist[c]
            else:
                # makes the star comparison 4 if good reviews switch is off to include the listing
                extracompare = 4

            if self.price[c] <= self.computerbudget and extracompare > 3:
                self.laptoplistings[self.titles[c]] = [self.price[c], self.imglist[c], self.rawlinks[c],
                                                       self.starlist[c]]

        return self.laptoplistings
