from PIL import Image, ImageTk
import Tkinter
from bs4 import BeautifulSoup as bs
import requests

#I know this my code format is probably confusing.Id also advise reading the code from the bottom to the top
#  This is the first program I spent a lot of time trying to
#figure out how to arrange. This is also my first gui program so bear with.  :) - Cameron



class search():
    def __init__(self, budget, bchoices):
        geturl = requests.get("https://www.techbargains.com/category/359/computers/laptops").text
        self.soup = bs(geturl, "html.parser")

        self.computerbudget = budget
        self.computerbrandchoices = bchoices

        self.tbtitles = []
        self.tbtitleposition = 0
        self.tb_titleposition_compare = []

        self.tbprice = []
        self.tbpriceposition = 0

        self.laptoplistings = {}

    def techbargain(self):
        #gets techbargain titles
        for t in self.soup.find_all("a", class_ = "details hidden-xs"):
            self.tbtitleposition += 1

            stringtitles = str(t["title"])
            rawtitles = stringtitles.split()

            for titles in rawtitles:
                if titles in self.computerbrandchoices:
                    self.tbtitles.append(t["title"])
                    self.tb_titleposition_compare.append(self.tbtitleposition)


        #gets techbargain prices
        for y in self.soup.find_all("span", class_ = "final-price"):
            self.tbpriceposition += 1

            if self.tbpriceposition in self.tb_titleposition_compare:
                tbrawprice = y.text[2:]

                if len(tbrawprice) == 6:
                    self.tbprice.append(int(tbrawprice[0:3]))

                elif len(tbrawprice) == 8:
                    #deletes the comma
                    self.tbprice.append(int(tbrawprice[0] + tbrawprice[2:5]))

                else:
                    self.tbprice.append("price unavailable")


    def compare(self):
        #loop through the techbargain title and price lists and adds there values to a dictionary
        # if the price is less or equal to the set budget
        for c in range(len(self.tbtitles)):
            if self.tbprice[c] <= self.computerbudget:
                self.laptoplistings[self.tbtitles[c]] = self.tbprice[c]


        print self.laptoplistings


    def searchscreen(self):
        self.searchscreen = Tkinter.Tk()
        self.searchscreen.geometry("550x300")
        self.searchscreen.title("searchresults")

        self.searchtitle = Tkinter.Label(self.searchscreen, text="Search Results", bg="white", font="fixedsys")
        self.searchtitle.pack(fill=Tkinter.X)

        self.techbargain()
        self.compare()
        self.searchscreen.mainloop()



class parameterscreen:

    def __init__(self, txt="What brand of Desktop would you like to find?"):
        #if i use Tkinter.Tk() for the parameter screen root the images dont work?
        self.p_root = Tkinter.Toplevel()
        self.p_root.title("Pc finder")
        self.p_root.geometry("540x300")
        self.budget1 = 0

        self.brandchoices = []

        paramlabel = Tkinter.Label(self.p_root, font="fixedsys", text=txt, bg="white")
        paramlabel.pack(side=Tkinter.TOP, fill=Tkinter.X)


    def range(self):
        self.pricerange = Tkinter.Scale(self.p_root, from_=0, to=2500, label="Budget", fg="darkgrey",
                                        orient=Tkinter.VERTICAL, length=250,
                                        sliderlength=20, bd=1, font="fixedsys",
                                        )

        self.pricerange.pack()
        self.pricerange.place(x=5, y=32)


    def choosecomputerbrand(self):


        def hpimgchg():
            #changes button to a different image to let user know brand is selected.

            # Is  there a better solution for changing the images when I click on the button?
            # I would make this into a function so i dont have to add an extra 75 lines but
            # tkinters command doesnt let me pass.


            if self.hpbrand.image == self.hpimg:
                hpselected = ImageTk.PhotoImage(Image.open("programphotos/hphover.jpg"))
                self.hpbrand.config(image=hpselected)
                self.hpbrand.image = hpselected
                #adds keywords to brand choices
                self.brandchoices.extend(("hp","Hp", "HP"))

            elif self.hpbrand.image != self.hpimg:
                self.hpbrand.config(image=self.hpimg)
                self.hpbrand.image = self.hpimg

                for hpremove in ["hp","Hp","HP"]:        #I guess just using 3 .removes would be easier to read but
                    self.brandchoices.remove(hpremove)   # I gotta save that 1 line of code :)

            print self.brandchoices

        #read this before hpimgchg
        self.hpimg = ImageTk.PhotoImage(Image.open("programphotos/hp.jpg"))
        self.hpbrand = Tkinter.Button(self.p_root, image=self.hpimg, bd = 0, command = hpimgchg)
        self.hpbrand.image = self.hpimg
        self.hpbrand.pack()
        self.hpbrand.place(x=140, y=70)

        #Same as above. Repeats 4 more times
        def dellimgchg():
            if self.dellbrand.image == self.dellimg:
                dellselected = ImageTk.PhotoImage(Image.open("programphotos/dellselected.png"))
                self.dellbrand.config(image=dellselected)
                self.dellbrand.image = dellselected

                self.brandchoices.extend(("dell","Dell","DELL"))

            elif self.dellbrand.image != self.dellimg:
                self.dellbrand.config(image=self.dellimg)
                self.dellbrand.image = self.dellimg

                for hpremove in ["dell","Dell","DELL"]:
                    self.brandchoices.remove(hpremove)

        self.dellimg = ImageTk.PhotoImage(Image.open("programphotos/dell.png"))
        self.dellbrand = Tkinter.Button(self.p_root, image=self.dellimg, bd=0, command=dellimgchg)
        self.dellbrand.image = self.dellimg
        self.dellbrand.pack()
        self.dellbrand.place(x=210, y=70)


        def appleimgchg():
            if self.applebrand.image == self.appleimg:
                appleselected = ImageTk.PhotoImage(Image.open("programphotos/appleselected.png"))
                self.applebrand.config(image=appleselected)
                self.applebrand.image = appleselected

                self.brandchoices.extend(("apple","Apple","APPLE"))

            elif self.applebrand.image != self.appleimg:
                self.applebrand.config(image=self.appleimg)
                self.applebrand.image = self.appleimg

                for hpremove in ["apple","Apple","APPLE"]:
                    self.brandchoices.remove(hpremove)

        self.appleimg = ImageTk.PhotoImage(Image.open("programphotos/apple.png"))
        self.applebrand = Tkinter.Button(self.p_root, image=self.appleimg, bd=0, command=appleimgchg)
        self.applebrand.image = self.appleimg
        self.applebrand.pack()
        self.applebrand.place(x=280, y=70)


        def microsoftimgchg():
            if self.microsoftbrand.image == self.microsoftimg:
                microsoftselected = ImageTk.PhotoImage(Image.open("programphotos/microsoftselected.png"))
                self.microsoftbrand.config(image=microsoftselected)
                self.microsoftbrand.image = microsoftselected

                self.brandchoices.extend(("microsoft","Microsoft","MICROSOFT"))

            elif self.microsoftbrand.image != self.microsoftimg:
                self.microsoftbrand.config(image=self.microsoftimg)
                self.microsoftbrand.image = self.microsoftimg

                for hpremove in ["microsoft","Microsoft","MICROSOFT"]:
                    self.brandchoices.remove(hpremove)

        self.microsoftimg = ImageTk.PhotoImage(Image.open("programphotos/microsoft.png"))
        self.microsoftbrand = Tkinter.Button(self.p_root, image=self.microsoftimg, bd=0, command=microsoftimgchg)
        self.microsoftbrand.image = self.microsoftimg
        self.microsoftbrand.pack()
        self.microsoftbrand.place(x=350, y=70)


        def lenovoimgchg():
            if self.lenovobrand.image == self.lenovoimg:
                lenovoselected = ImageTk.PhotoImage(Image.open("programphotos/lenovoselected.png"))
                self.lenovobrand.config(image=lenovoselected)
                self.lenovobrand.image = lenovoselected

                self.brandchoices.extend(("lenovo","Lenovo","LENOVO"))

            elif self.lenovobrand.image != self.lenovoimg:
                self.lenovobrand.config(image=self.lenovoimg)
                self.lenovobrand.image = self.lenovoimg

                for hpremove in ["lenovo","Lenovo","LENOVO"]:
                    self.brandchoices.remove(hpremove)

        self.lenovoimg = ImageTk.PhotoImage(Image.open("programphotos/lenovo.png"))
        self.lenovobrand = Tkinter.Button(self.p_root, image=self.lenovoimg, bd=0, command=lenovoimgchg)
        self.lenovobrand.image = self.lenovoimg
        self.lenovobrand.pack()
        self.lenovobrand.place(x=140, y=140)


        def acerimgchg():
            if self.acerbrand.image == self.acerimg:
                acerselected = ImageTk.PhotoImage(Image.open("programphotos/acerselected.jpg"))
                self.acerbrand.config(image=acerselected)
                self.acerbrand.image = acerselected

                self.brandchoices.extend(("acer","Acer","ACER"))

            elif self.acerbrand.image != self.acerimg:
                self.acerbrand.config(image=self.acerimg)
                self.acerbrand.image = self.acerimg

                for hpremove in ["acer","Acer","ACER"]:
                    self.brandchoices.remove(hpremove)

        self.acerimg = ImageTk.PhotoImage(Image.open("programphotos/acer.jpg"))
        self.acerbrand = Tkinter.Button(self.p_root, image=self.acerimg, bd=0, command=acerimgchg)
        self.acerbrand.image = self.acerimg
        self.acerbrand.pack()
        self.acerbrand.place(x=210, y=140)


        def razerimgchg():
            if self.razerbrand.image == self.razerimg:
                razerselected = ImageTk.PhotoImage(Image.open("programphotos/razerselected.jpg"))
                self.razerbrand.config(image=razerselected)
                self.razerbrand.image = razerselected

                self.brandchoices.extend(("razer","Razer","RAZER"))

            elif self.razerbrand.image != self.razerimg:
                self.razerbrand.config(image=self.razerimg)
                self.razerbrand.image = self.razerimg

                for hpremove in ["razer","Razer","RAZER"]:
                    self.brandchoices.remove(hpremove)

        self.razerimg = ImageTk.PhotoImage(Image.open("programphotos/razer.png"))
        self.razerbrand = Tkinter.Button(self.p_root, image=self.razerimg, bd=0, command=razerimgchg)
        self.razerbrand.image = self.razerimg
        self.razerbrand.pack()
        self.razerbrand.place(x=280, y=140)


        def msiimgchg():
            if self.msibrand.image == self.msiimg:
                self.msiselected = ImageTk.PhotoImage(Image.open("programphotos/msiselected.jpg"))
                self.msibrand.config(image=self.msiselected)
                self.msibrand.image = self.msiselected

                self.brandchoices.extend(("msi","Msi","MSI"))

            elif self.msibrand.image != self.msiimg:
                self.msibrand.config(image=self.msiimg)
                self.msibrand.image = self.msiimg

                for hpremove in ["msi","Msi","MSI"]:
                    self.brandchoices.remove(hpremove)

        self.msiimg = ImageTk.PhotoImage(Image.open("programphotos/msi.png"))
        self.msibrand = Tkinter.Button(self.p_root, image=self.msiimg, bd=0, command=msiimgchg)
        self.msibrand.image = self.msiimg
        self.msibrand.pack()
        self.msibrand.place(x=350, y=140)


    def paramterwidgets(self):
        self.choosecomputerbrand()
        self.range()
        self.findbutton()


    def findbutton(self):

        def buttoncommand():
            self.searchtrigger = search(self.pricerange.get(), self.brandchoices)
            self.searchtrigger.searchscreen()

        #Button that triggers the search class in the search file
        searchbutton = Tkinter.Button(self.p_root, text="FIND", font="fixedsys",  fg="darkgrey",
                                      width=8, command = buttoncommand)

        searchbutton.pack()
        searchbutton.place(x=450, y=260)



    # how does this class work without me calling self.p_root.mainloop() ?



class screen:
    #startupscreen and its widgets
    def startscreen(self):
        self.root = Tkinter.Tk()
        self.root.title("Pc finder")
        self.root.geometry("440x200")

        self.defaultbg = self.root.cget("bg")

        self.Lttxt = "What kind of Laptop would you like to find?"

        self.dtImageLd = ImageTk.PhotoImage(Image.open("programphotos/desktop.png"))
        self.ltImageLd = ImageTk.PhotoImage(Image.open("programphotos/laptop.png"))

        label1 = Tkinter.Label(self.root, font="fixedsys", text="What kind of computer would you like to find?",
                               width=40, bg="white")
        label1.pack(side=Tkinter.TOP, fill=Tkinter.X)

        dtImage = Tkinter.Label(self.root, image=self.dtImageLd)
        dtImage.pack(side=Tkinter.LEFT)
        dtImage.place(x=45, y=45)

        ltImage = Tkinter.Label(self.root, image=self.ltImageLd)
        ltImage.pack(side=Tkinter.RIGHT)
        ltImage.place(x=275, y=40)

        def Dtchangescreen():
            #starts parameter screen(desktop version).
            parameterscreen1 = parameterscreen()
            parameterscreen1.paramterwidgets()

        # Buttons
        b1 = Tkinter.Button(self.root, font="fixedsys", text = "Desktops",
                            bg=self.defaultbg, command=Dtchangescreen
                            )
        b1.pack()
        b1.place(x=65, y=160)

        def Ltchangescreen():
            #starts parameter screen(laptop version)
            parameterscreen1 = parameterscreen()
            parameterscreen1.paramterwidgets()

        b2 = Tkinter.Button(self.root, font="fixedsys", text="Laptops",
                            bg=self.defaultbg, command=Ltchangescreen
                            )

        b2.pack()
        b2.place(x=305, y=160)
        #



#starts the startup screen
Interface1 = screen()
Interface1.startscreen()
Interface1.root.mainloop()
