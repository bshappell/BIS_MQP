RASP_PI = 0 # used to toggle between working on the pi and on a PC

from Tkinter import *
import ttk
import time

if RASP_PI:
    import BIS

BUTTON_COLOR = '#BFBFBF'
FONT_COLOR = "black"
BLISK_ID_P01 = "2468M19P01"
BLISK_ID_P02 = "2468M17P02"
BLISK_ID_G02 "2468M18G02"

""" **************************************** Controller Classes **************************************** """

""" Activated when the first start button is choosen """
class StartAppController(object):   

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        if RASP_PI:
            self.bis.start()

        self.bisApp.selectBliskView.run()
        print 'start app controller ' + str(self.bisApp.currentView)


""" Used when the instruction button is clicked """
class InstructionsController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        self.bisApp.instructionsView.run()
        print 'instructions button controller' + str(self.bisApp.currentView)


""" Used when a blisk is selected """
class SelectBliskController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis 

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        blisk = self.bisApp.selectBliskView.blisk.get()
        print "blisk: " + blisk

        bliskNum = -1
        if blisk == BLISK_ID_P01:
            bliskNum = 0
        elif blisk == BLISK_ID_P02:
            bliskNum = 1
        elif blisk == BLISK_ID_G02:
            bliskNum = 2
        else:
            print "ERROR INCORRECT BLISK NUMBER RECEIVED"

        if RASP_PI:
            self.bis.selectBlisk(blisk)

        self.bisApp.roughArmPositionView.run()
        print "select blisk controller " + str(self.bisApp.currentView)


""" Used when the back button is clicked """
class BackController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "back button press, current view = " + str(self.bisApp.currentView)
        
        """ Send the view to the screen before """
        if self.bisApp.currentView == 1:
            self.bisApp.startScreenView.run()
        elif self.bisApp.currentView == 2:
            self.bisApp.selectBliskView.run()
        elif self.bisApp.currentView == 3:
            self.bisApp.roughArmPositionView.run()
        elif self.bisApp.currentView == 4:
            self.bisApp.armPositionView.run()
        elif self.bisApp.currentView == 5:
            self.bisApp.turnBliskView.run()
        elif self.bisApp.currentView == 6:
            self.bisApp.startInspectionView.run()
        elif self.bisApp.currentView == 7:
            self.bisApp.inspectionProgressView.run()
        elif self.bisApp.currentView == 8:
            self.bisApp.inspectionResultsView.run()

        print "new current view: " + str(self.bisApp.currentView)


""" Used when the user select to position the arm outside of the blisk radius """
class RoughArmPositionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        if RASP_PI:
            self.bis.positionArmFar()

        self.bisApp.armPositionView.run()
        print "rough arm position button press " + str(self.bisApp.currentView)


""" Used when the user select to position the arm inside the blisk radius """
class ArmPositionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        #self.bisApp.armPositionView.load()
        #print "Arm Move Button press"
        #cont = LoadingScreenController(self.bis, self.bisApp)
        #cont.run()

        if RASP_PI:
            self.bis.positionArmClose()

        time.sleep(5)
        self.bisApp.turnBliskView.run()
        print "arm position button press " + str(self.bisApp.currentView)


""" Used when the user select to position the arm inside the blisk radius """
class TurnBliskController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        if RASP_PI:
            self.bis.positionBlisk()

        self.bisApp.startInspectionView.run()
        print "turn blisk button press " + str(self.bisApp.currentView)


""" Used when the user chooses to start the blisk inspection """
class StartInspectionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        if RASP_PI:
            self.bisApp.inspectBlisk()

        # REPLACED PROGRESS VIEW WITH INSPECTION VIEW
        #self.bisApp.inspectionProgressView.run()
        self.bisApp.inspectionResultsView.run()
        print "start inspection button press " + str(self.bisApp.currentView)


""" Controller for when the user chooses to view the inspection results """
class InspectionResultsController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        self.bisApp.inspectionResultsView.run()
        print "view inspection results button press " + str(self.bisApp.currentView)

""" Controller to handle the loading screens """
class LoadingScreenController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def run(self):

        print "Loading Screen Controller Running"

        """ Handle which controller to call based on ... """
        self.bisApp.loadingScreenView.run()


""" ********************************************** BIS App ********************************************** """

""" The Top Level BIS Application Boundary Class """
class BisApp(object):

    def __init__(self):

        """ BIS Entity Class """
        self.bis = None #BIS.BIS()

        """ Root Application Screen """
        self.root = Tk()
        #self.root.geometry('638x410')
        #self.root.resizable(width=False, height=False)
        self.root.title("Blisk Inspection System Application")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.configure(bg="light grey")

        """ Copy of all of the View Classes """
        self.startScreenView = StartScreenView(self.bis,self)
        self.selectBliskView = SelectBliskView(self.bis,self)
        self.roughArmPositionView = RoughArmPositionView(self.bis,self)
        self.armPositionView = ArmPositionView(self.bis,self)
        self.turnBliskView = TurnBliskView(self.bis,self)
        self.startInspectionView = StartInspectionView(self.bis,self)
        self.inspectionProgressView = InspectionProgressView(self.bis,self)
        self.inspectionResultsView = InspectionResultsView(self.bis,self)
        self.instructionsView = InstructionsView(self.bis,self)
        self.loadingScreenView = LoadingScreenView(self.bis,self)

        """ Current View Screen (Initially set at opening screen) """
        self.currentView = 0 

    """ Run the Blisk Inspection System Application """
    def run(self):

        self.startScreenView.run()
        self.root.mainloop()
        
    
""" ******************************************** View Classes ******************************************** """    

class StartScreenView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Screen Text Explanation """
        explanation = "Welcome to the Blisk Inspection System Application\n Instructions on how to use the application can be found below"

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root) #, bg="black")
        self.frame.grid(column=0, row=0, sticky=('N', 'S', 'E', 'W'))

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        #Label(self.frame, compound = CENTER, text=explanation, fg = "blue",font = "Helvetica 16 bold").pack()
        self.upperFrame = Frame(self.frame, borderwidth=2, relief='flat')
        self.upperFrame.grid(row=1, column=0, sticky=('N', 'S', 'E', 'W'))
        self.upperFrame.columnconfigure(0, weight=1)
        self.upperFrame.rowconfigure(0, weight=1)

        descript = ""
        desc = Label(self.upperFrame, height=8,  font=('Futura', 12))
        desc.grid(row=0, column=0, sticky=('N', 'S', 'E', 'W'), padx=10, pady=10)

        self.lowerFrame = Frame(self.frame,  borderwidth=2, relief='flat')
        self.lowerFrame.grid(row=2, column=0, sticky=('N', 'S', 'E', 'W'))
        self.lowerFrame.columnconfigure(0, weight=1)
        self.lowerFrame.rowconfigure(0, weight=1)

        banner = Label(self.frame, background='dark grey', text="Blisk Inspection System", font=('Futura', 32), fg='white')
        banner.grid(row=0, column=0, sticky=('N', 'S', 'E', 'W'), padx=10, pady=10)

        """ Start Application Button """
        self.startButton = Button(self.lowerFrame, text = 'Start', bg='#BFBFBF', command = StartAppController(bis,bisApp).buttonPress)
        #self.startButton.pack(pady=20, padx = 20)
        self.startButton.grid(row=0, column=0, sticky=('N', 'S', 'E', 'W'), padx=10, pady=10)

        """ Instructions Button """
        self.instructionsButton = Button(self.lowerFrame, text = 'Instructions', bg='#BFBFBF',command = InstructionsController(bis,bisApp).buttonPress)
        #self.instructionsButton.pack(pady=20, padx = 20)
        self.instructionsButton.grid(row=1, column=0, sticky=('N', 'S', 'E', 'W'), padx=10, pady=10)

    def run(self):

        self.bisApp.currentView = 0
        self.frame.tkraise()
        self.lowerFrame.tkraise()


""" View class of screen to select a blisk from the list of three blisks """
class SelectBliskView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        explanation = "Select a Blisk Part Number to Inspect"
        Label(self.frame, compound = CENTER, text=explanation, fg = "black",font = 16).pack(pady=20)

        """ Drop Down Menu """
        self.blisk = StringVar(self.frame)
        self.blisk.set(BLISK_ID_P01) # initial value

        """ Add Blisk Selection Drop Down Menu """
        option = OptionMenu(self.frame, self.blisk, BLISK_ID_P01, BLISK_ID_P02, BLISK_ID_G02)
        option.config(bg='#BFBFBF')
        option.pack(pady=20, padx =20)

        """ Select Blisk Button """
        self.selectButton = Button(self.frame, text = 'Select Blisk', bg=BUTTON_COLOR,command = SelectBliskController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=10, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', bg=BUTTON_COLOR,command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT, pady=20, padx = 20)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR, command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

    def run(self):

        self.bisApp.currentView = 1
        self.frame.tkraise()


""" Screen where the user chooses to move the arm outside of the radius of the blisk """
class RoughArmPositionView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ Position Arm Button """
        self.posArmButton = Button(self.frame, text = 'Position Arm', bg=BUTTON_COLOR,command = RoughArmPositionController(bis,bisApp).buttonPress)
        self.posArmButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', bg=BUTTON_COLOR,command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT, pady=20, padx = 20)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR,command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

    def run(self):

        self.bisApp.currentView = 2
        self.frame.tkraise()

""" Loading Screen """
class LoadingScreenView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ Loading Progress Bar """
        self.progressbar = ttk.Progressbar(self.frame, orient=HORIZONTAL, length=200, mode='determinate')
        self.progressbar.pack(padx=20, pady=20) #side="bottom")
        self.progressbar.start()

    """ Run the page """
    def run(self):

        self.frame.tkraise()


""" Screen where the user chooses to move the arm inside the radius of the blisk """
class ArmPositionView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ Position Arm Button """
        self.posArmButton = Button(self.frame, text = 'Position Arm', bg=BUTTON_COLOR,command = ArmPositionController(bis,bisApp).buttonPress)
        self.posArmButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', bg=BUTTON_COLOR,command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT, pady=20, padx = 20)

        """ Loading Progress Bar """
        #self.progressbar = ttk.Progressbar(self.frame, orient=HORIZONTAL, length=200, mode='determinate')
        #self.progressbar.pack(padx=20) #side="bottom")
        
        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR,command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

    """ Run the page """
    def run(self):

        self.bisApp.currentView = 3
        self.frame.tkraise()


""" Screen where the user selects to turn the blisk until contact with the EOAT is made """
class TurnBliskView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ Turn Blisk Button """
        self.turnBliskButton = Button(self.frame, text = 'Turn Blisk', bg=BUTTON_COLOR,command = TurnBliskController(bis,bisApp).buttonPress)
        self.turnBliskButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', bg=BUTTON_COLOR,command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT, pady=20, padx = 20)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR,command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

    def run(self):

        self.bisApp.currentView = 4
        self.frame.tkraise()


""" Screen to choose to start the blisk inspection """
class StartInspectionView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ Start Inspection Button """
        self.startButton = Button(self.frame, text = 'Start Inspection', bg=BUTTON_COLOR,command = StartInspectionController(bis,bisApp).buttonPress)
        self.startButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', bg=BUTTON_COLOR,command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT, pady=20, padx = 20)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR,command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

    def run(self):

        self.bisApp.currentView = 5
        self.frame.tkraise()


""" Screen to show the instrucitons on how to use the system """
class InstructionsView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR,command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

        """ Display the Instructions """
        explanation = "In order to use the system please follow these steps:\n 1.) Blah\n 2.) Blah\n 3.) etc.\n"
        Label(self.frame, compound = CENTER, text=explanation, fg = "blue",font = "Helvetica 16 bold").pack()


    def run(self):

        print "in instructions run function, current view = " + str(self.bisApp.currentView)
        self.bisApp.currentView += 1
        self.frame.tkraise()


""" Screen for viewing the inspection progress and choosing to view the results when complete """
class InspectionProgressView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ View Inspection Results Button """
        self.resultsButton = Button(self.frame, text = 'View Results', bg=BUTTON_COLOR,command = InspectionResultsController(bis,bisApp).buttonPress)
        self.resultsButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', bg=BUTTON_COLOR,command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT, pady=20, padx = 20)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR,command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

    def run(self):

        self.bisApp.currentView = 6
        self.frame.tkraise()


""" View to display the inspection results """
class InspectionResultsView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        """ Make a new frame """
        self.frame = Frame(self.bisApp.root)
        self.frame.grid(row=0, column=0, sticky='news')

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', bg=BUTTON_COLOR,command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT, pady=20, padx = 20)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', bg=BUTTON_COLOR,command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT, pady=20, padx = 20)

        """ Button to start a new inspection """
        self.resultsButton = Button(self.frame, text = 'Finish', bg=BUTTON_COLOR,command = StartAppController(bis,bisApp).buttonPress)
        self.resultsButton.pack(pady=20, padx = 20)

        """ Button to Quit the application """
        self.resultsButton = Button(self.frame, text = 'Quit Application', bg=BUTTON_COLOR,command = self.bisApp.root.destroy)
        self.resultsButton.pack(pady=20, padx = 20)

    def run(self):

        self.bisApp.currentView = 7
        self.frame.tkraise()


""" ************************************************ Main ************************************************ """

if __name__=="__main__":
    BisApp().run()


