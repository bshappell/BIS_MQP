

from Tkinter import *

""" **************************************** Controller Classes **************************************** """

""" Activated when the first start button is choosen """
class StartAppController(object):   

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print 'start app controller'


""" Used when the instruction button is clicked """
class InstructionsController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print 'instructions button controller'


""" Used when a blisk is selected """
class SelectBliskController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis 

        """ BIS Application Top Level Boundary Class """
        self.BisApp = bisApp

    def buttonPress(self):

        print "select blisk controller"


""" Used when the back button is clicked """
class BackController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "back button press"

""" Used when the user select to position the arm outside of the blisk radius """
class RoughArmPositionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "rough arm position button press"


""" Used when the user select to position the arm inside the blisk radius """
class ArmPositionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "arm position button press"


""" Used when the user select to position the arm inside the blisk radius """
class TurnBliskController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "turn blisk button press"


""" ********************************************** BIS App ********************************************** """

""" The Top Level BIS Application Boundary Class """
class BisApp(object):

    def __init__(self):

        """ BIS Entity Class """
        self.bis = None # TO DO: set correctly

        self.root = Tk()
        self.root.geometry('100x110+350+70')

    """ Run the Blisk Inspection System Application """
    def run(self):

        StartScreenView(self.bis, self.root)
        
    
""" ******************************************** View Classes ******************************************** """    

class StartScreenView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.startButton = Button(self.bisApp, text = 'Start', command = StartAppController(bis,bisApp).buttonPress)
        self.startButton.pack(pady=20, padx = 20)

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        self.bisApp.mainloop()


""" View class of screen to select a blisk from the list of three blisks """
class SelectBliskView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.selectButton = Button(self.bisApp, text = 'Select Blisk', command = SelectBliskController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=20, padx = 20)

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.bisApp, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()


""" Screen where the user chooses to move the arm outside of the radius of the blisk """
class RoughArmPositionView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.selectButton = Button(self.bisApp, text = 'Position Arm', command = RoughArmPositionController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=20, padx = 20)

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.bisApp, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()


""" Screen where the user chooses to move the arm inside the radius of the blisk """
class ArmPositionView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.selectButton = Button(self.bisApp, text = 'Position Arm', command = ArmPositionController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=20, padx = 20)

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.bisApp, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()


""" Screen where the user selects to turn the blisk until contact with the EOAT is made """
class TurnBliskView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.selectButton = Button(self.bisApp, text = 'Turn Blisk', command = TurnBliskController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=20, padx = 20)

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.bisApp, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()


""" Screen to choose to start the blisk inspection """
class StartInspectionView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.selectButton = Button(self.bisApp, text = 'Start Inspection', command = StartInspectionController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=20, padx = 20)

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.bisApp, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()


""" Screen for viewing the inspection progress and choosing to view the results when complete """
class InspectionProgressView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.selectButton = Button(self.bisApp, text = 'View Results', command = InspectionResultsController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=20, padx = 20)

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.bisApp, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()


""" View to display the inspection results """
class InspectionResultsView(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

        self.instructionsButton = Button(self.bisApp, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.bisApp, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()

        """ Display the inspection results """


""" ************************************************ Main ************************************************ """

if __name__=="__main__":
    BisApp().run()