

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
        self.bisApp.selectBliskView.run()


""" Used when the instruction button is clicked """
class InstructionsController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print 'instructions button controller'
        self.bisApp.instructionsView.run()


""" Used when a blisk is selected """
class SelectBliskController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis 

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "select blisk controller"
        self.bisApp.roughArmPositionView.run()


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


""" Used when the user select to position the arm outside of the blisk radius """
class RoughArmPositionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "rough arm position button press"
        self.bisApp.armPositionView.run()


""" Used when the user select to position the arm inside the blisk radius """
class ArmPositionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "arm position button press"
        self.bisApp.turnBliskView.run()


""" Used when the user select to position the arm inside the blisk radius """
class TurnBliskController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "turn blisk button press"
        self.bisApp.startInspectionView.run()

""" Used when the user chooses to start the blisk inspection """
class StartInspectionController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "start inspection button press"
        self.bisApp.inspectionResultsView.run()


""" Controller for when the user chooses to view the inspection results """
class InspectionResultsController(object):

    def __init__(self, bis, bisApp):

        """ Blisk Inspection System Entity Class """
        self.bis = bis

        """ BIS Application Top Level Boundary Class """
        self.bisApp = bisApp

    def buttonPress(self):

        print "view inspection results button press"


""" ********************************************** BIS App ********************************************** """

""" The Top Level BIS Application Boundary Class """
class BisApp(object):

    def __init__(self):

        """ BIS Entity Class """
        self.bis = None # TO DO: set correctly

        """ Root Application Screen """
        self.root = Tk()
        self.root.geometry('800x610+350+70')
        self.root.title("Blisk Inspection System Application")

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
        self.frame = Frame(self.bisApp.root, bg="light blue")
        self.frame.grid(row=0, column=0, sticky='news')
        Label(self.frame, compound = CENTER, text=explanation, fg = "blue",font = "Helvetica 16 bold").pack()

        """ Start Application Button """
        self.startButton = Button(self.frame, text = 'Start', command = StartAppController(bis,bisApp).buttonPress)
        self.startButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(pady=20, padx = 20)

    def run(self):

        self.bisApp.currentView = 0
        self.frame.tkraise()


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

        """ Select Blisk Button """
        self.selectButton = Button(self.frame, text = 'Select Blisk', command = SelectBliskController(bis,bisApp).buttonPress)
        self.selectButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack()

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack()

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
        self.posArmButton = Button(self.frame, text = 'Position Arm', command = RoughArmPositionController(bis,bisApp).buttonPress)
        self.posArmButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT)

    def run(self):

        self.bisApp.currentView = 2
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
        self.posArmButton = Button(self.frame, text = 'Position Arm', command = ArmPositionController(bis,bisApp).buttonPress)
        self.posArmButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT)

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
        self.turnBliskButton = Button(self.frame, text = 'Turn Blisk', command = TurnBliskController(bis,bisApp).buttonPress)
        self.turnBliskButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT)

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
        self.startButton = Button(self.frame, text = 'Start Inspection', command = StartInspectionController(bis,bisApp).buttonPress)
        self.startButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT)

    def run(self):

        self.bisApp.currentView += 1
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
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT)

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
        self.resultsButton = Button(self.frame, text = 'View Results', command = InspectionResultsController(bis,bisApp).buttonPress)
        self.resultsButton.pack(pady=20, padx = 20)

        """ Instructions Button """
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT)

    def run(self):

        self.bisApp.currentView = 7
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
        self.instructionsButton = Button(self.frame, text = 'Instructions', command = InstructionsController(bis,bisApp).buttonPress)
        self.instructionsButton.pack(side=RIGHT)

        """ Back Button """
        self.backButton = Button(self.frame, text = 'Back', command = BackController(bis,bisApp).buttonPress)
        self.backButton.pack(side=LEFT)

        """ Display the inspection results """

    def run(self):

        self.bisApp.currentView = 8
        self.frame.tkraise()


""" ************************************************ Main ************************************************ """

if __name__=="__main__":
    BisApp().run()

