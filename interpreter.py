from tkinter import *
from pypeg2 import *
import actionbuttons
from statements import *
<<<<<<< HEAD
import matrix
=======
import math
>>>>>>> 82879131ffd6e904073b50ee4c51d8da6483ae75

#Binding object has four instance variables
#bType - the type of object with regards to "Gooey" ex) Window, Button
#varname - how we identify the object (a string)
#bObject - the actual tkinter object
#params - an optional argument use to take in the parameters of a user defined function
class Binding:
    bType = None
    varname = None
    bObject = None
    params = None

    def __init__(self,bType,varname,bObject,params):
        '''Sets instance variables: type, name, Tkinter object, and optional parameters'''
        self.bType = bType
        self.varname = varname
        self.bObject = bObject
        self.params = params

    def __repr__(self):
        '''Prints a pretty version of the bindings'''
        prettyStr = "Binding " + str(varname) + " of type " + str(bType) + "."
        return prettyStr

class Interpreter():
    '''Interpreter class: creates GUI based on the expression given by the user.'''
    gRows = 0
    gColumns = 0
    
    def __init__(self, target):
        '''Initializes the GUI window'''
        self.window = target

    def error(self, message):
        '''Generates a popup error message'''
        errorPopup = Toplevel()
        errorPopup.title("Error")
        errorPopup.geometry("%dx%d%+d%+d" % (200, 200, 200, 200))
        msg = Message(errorPopup, text=message)
        msg.pack()
        button = Button(errorPopup, text="Ok", command=errorPopup.destroy)
        button.pack()
        #self.window.destroy()

    def interpret(self, ast, bindings):
        '''Interprets the Gooey code and creates a GUI in the window.  
        It takes in an abstract syntax tree as generated by pypeg, and the current bindings.  
        Returns a new list of bindings. '''
        for expr in ast:
            
            
            #   MAKE
            if(expr.__class__.__name__ == "Make"):
                if hasattr(expr, "type"):
                    if (expr.type == "Window"):
                        self.checkVarname(expr,bindings)
                        w = self.makeWindow(self.window,expr)
                        binding = self.makeBinding("Window", expr.varname, w)
                        bindings = self.addBinding(binding, bindings)

                    elif(expr.type == "Button"):
                        self.checkVarname(expr,bindings)
                        b = self.makeButton(self.window,expr)
                        binding = self.makeBinding("Button", expr.varname, b)
                        bindings = self.addBinding(binding, bindings)

                    elif(expr.type == "Menu"):
                        self.checkVarname(expr,bindings)
                        m = self.makeMenu(self.window,expr,bindings)
                        options = self.getOptions(expr)
                        binding = self.makeBinding("Menu", expr.varname, m, options)
                        bindings = self.addBinding(binding,bindings)

                    elif(expr.type == "MenuItem"):
                        self.checkVarname(expr,bindings)
                        mi = self.makeMenuItem(self.window,expr,bindings)
                        options = self.getOptions(expr)
                        binding = self.makeBinding("MenuItem", expr.varname, mi, options)
                        bindings = self.addBinding(binding,bindings)

                    elif(expr.type == "TextBox"):
                        self.checkVarname(expr,bindings)
                        t = self.makeTextBox(self.window, expr)
                        binding = self.makeBinding("TextBox", expr.varname, t)
                        bindings = self.addBinding(binding,bindings)

                    elif(expr.type == "Image"):
                        self.checkVarname(expr,bindings)
                        i = self.makeImage(self.window, expr)
                        binding = self.makeBinding("Image", expr.varname, i)
                        bindings = self.addBinding(binding,bindings)
                    else:
                        self.error("Error: Object not recognized. Make sure to capitalize the object name.")

                else:
                    self.error("Error: No type recognized.")



            #   SET
            elif(expr.__class__.__name__ == "GooeySet"):
                if hasattr(expr, "varname"):
                    if expr.varname in bindings:
                        obj = bindings[expr.varname]
                        if obj.bType == "Window":
                            win = self.getObject(expr,bindings)
                            assert win.bType == 'Window'
                            wColorBefore = win.bObject.cget('bg')
                            w = self.setWindow(win.bObject,expr)
                            wColorAfter = w.cget('bg')
                            if wColorBefore != wColorAfter:
                                bindings = self.fixButtonPadding(wColorAfter,bindings)
                            w = self.setWindow(win.bObject,expr)

                        elif(obj.bType == "Button"):
                            button = self.getObject(expr,bindings)
                            assert button.bType == 'Button'
                            b = self.setButton(button.bObject,self.window, expr)

                        elif(obj.bType == "Menu"):
                            pass

                        elif(obj.bType == "MenuItem"):
                            pass

                        elif(obj.bType == "TextBox"):
                            t = self.getObject(expr,bindings)
                            assert t.bType == 'TextBox'
                            tbox = t.bObject
                            if hasattr(expr, "attributes"):
                                for item in expr.attributes[0]:
                                    if hasattr(item, 'text'):
                                        tbox.insert(END, item.text.value)
                                        tbox.pack()
                        #print("THIS IS EXPR: ",expr.attributes.text)
                        #tbox.insert(END, expr)
                else:
                    self.error("Error: Undefined variable used.")


            #               FUNCTIONS
            #Interprets all function definition statements
            elif(expr.__class__.__name__ == "FunctionDefinition"):
                if hasattr(expr, "funcname"):
                    #Checks bindings to see if function name is already there
                    for i in range(len(expr.funcaction)):
                        b = self.interpret([expr.funcaction[i]], bindings) #this putting i in a list is stupid and Leah fully admits it
                        # b = self.interpret(expr.funcaction[i], bindings) #this putting i in a list is stupid and Leah fully admits it

                        expr.funcaction[i] = b

                    if expr.funcname in bindings:
                        self.error("Sorry, this function name is already used.")

                    #If function isn't already defined, add it to bindings
                    else:
                        if hasattr(expr, "params"):
                            binding = self.makeBinding("Function", str(expr.funcname), expr.funcaction, expr.params)
                        else:
                            binding = self.makeBinding("Function", str(expr.funcname), expr.funcaction)
                        bindings = self.addBinding(binding,bindings)
                else:
                    self.error("Sorry, you need to give your function a name")

            #Interprets all function calls
            elif(expr.__class__.__name__ == "FunctionCall"):
                #Find function with that name
                function = expr.funcname
                if function in bindings:
                    #Look at params in the bindings
                    #if hasattr(expr, "params"):
                    localBindings = dict()
                    if len(expr.params)>0:
                        #Make set of local bindings

                        #Bind objects passed into parameter with parameter in function

                        #Take param being passed in (params), bind to expected param in function
                        #add this to local binding
                        functionParam = bindings[function].params[0]
                        #functionInput = bindings[functionParam[0]]

                        #Assuming only one parameter
                        functionInput = bindings[expr.params[0]] 

                        #Sets the type of the local to the thing that we're passing in.
                        b = self.makeBinding(functionInput.bType, functionParam, functionInput.bObject) 
                        localBindings = self.addBinding(b, localBindings)
                        newBindings = self.runFunction(bindings,function,localBindings)
                        newB = newBindings[functionParam]
                        newB.varname = functionInput.varname

                        #Binds the returned object to the thing that it modified
                        bindings[functionInput.varname] = newB
                    else:
                        newBindings = self.runFunction(bindings,function,localBindings)
                else:
                    self.error("This function isn't defined.")


            #Interprets each line of a function.
            elif(expr.__class__.__name__ == "Line"):
                return expr.lineAction
            elif(expr.__class__.__name__ == "Return"):
                return expr.param

            else:
                #Invalid first word
                self.error("Error: Invalid command. Please start your command with Make, Set, or other valid start commands.")

        return bindings









    #               WINDOWS
    def makeWindow(self,w,expr):
<<<<<<< HEAD
        print("making window")
        #print(matrix.getDefault("Window","color"))
        w.deiconify() #Show the window
=======
        '''Makes a window given user attributes.
        It should set anything that the user has not specified to the defaults.'''
        #Show the window
        w.deiconify() 
>>>>>>> 82879131ffd6e904073b50ee4c51d8da6483ae75
        if hasattr(expr, "attributes"):
            windowAttributeList = expr.attributes[0]
            for item in windowAttributeList:
                #Here is where we need to check our attributes matrix
                if hasattr(item, 'color'):
                    w.configure(bg=item.color.value)
                elif hasattr(item,'size'):
                    if hasattr(item.size.value, "columns"):
                        rows = int(item.size.value.rows)
                        columns = int(item.size.value.columns)
                        Interpreter.gRows = rows
                        Interpreter.gColumns = columns
                        #fill cells with empty space somehow, so the user gets a sense of it actually being a grid
                        for i in range(0,columns):
                            for j in range(0,rows):
                                l = Frame(w, height=100, width=100, bg="red")
                                l.grid(row = j, column = i)

                    elif item.size.value[0].isdigit():
                        size = item.size.value+"x"+item.size.value
                        w.geometry(size)
                    else:
                        if item.size.value.lower() == "large":
                            w.geometry('500x500')
                        elif item.size.value.lower() == "small":
                            w.geomerty('200x200')
        else: #set the defaults according to our matrix
            pass

        #somewhere in here we need to look and error check that there are only
        #attributes that are supposed to be here
        return w

    def setWindow(self,w,expr):
        '''Sets window attributes to those specified by the user.'''
        if hasattr(expr, "attributes"):
            #here is where we need to check our attributes matrix
            for item in expr.attributes[0]:
                if hasattr(item, 'color'):
                    #self.window.configure(bg=item.color.value)
                    w.configure(bg=item.color.value)
                elif hasattr(item,'size'):
                    if hasattr(item.size.value, "columns"):
                        rows = int(item.size.value.rows)
                        columns = int(item.size.value.columns)
                        for i in range(0,columns):
                            for j in range(0,rows):
                                l = Frame(w, height=100, width=100)
                                l.rowconfigure('all', minsize = 100)
                                l.columnconfigure('all', minsize = 100)
                                l.grid(row = j, column = i)

                    elif item.size.value[0].isdigit():
                        size = item.size.value+"x"+item.size.value
                        w.geometry(size)
                    else:
                        if item.size.value.lower() == "large":
                            w.geometry('500x500')
                        elif item.size.value.lower() == "small":
                            w.geomerty('200x200')
        return w



    #               TEXT BOX
    def makeTextBox(self,w,expr):
        '''Makes a text box with the user defined attributes.'''
        t = Text(w, height=2, width=30)
        r, c = 0, 0
        if hasattr(expr, "attributes"):
            for item in expr.attributes[0]:
                if hasattr(item, 'text'):
                    t.insert(END, self.extractTextValue(item.text.value))
                elif hasattr(item, 'position'):
                    if hasattr(item.position.value, "r"):
                        r = int(item.position.value.r)
                        c = int(item.position.value.c)
                    else:
                        r, c = self.getPositionByKeyword(item.position.value)
                else:
                    self.error("Error: Incorrect attribute.")
        t.grid(row=r, column=c, sticky=N+S+E+W)
        return t



    #               BUTTONS
    def makeButton(self,w,expr):
        '''Makes a button by taking in the window the button should be made in 
        and the expression given by the user.'''
        #This is the current background color of the window
        #We need this to correct for padding issues on the mac
        hB = w.cget('bg')
        b = Button(w, bd=-2, highlightbackground = hB)

        if hasattr(expr, "attributes"):
            r, c = 0, 0
            for item in expr.attributes[0]:
                if hasattr(item, 'color'):
                    b.configure(bg=item.color.value)
                if hasattr(item, 'text'):
                    b.configure(text=self.extractTextValue(item.text.value))
                elif hasattr(item,'size'):
                    b.configure(width=item.size.value)
                    b.configure(height=item.size.value)
                elif hasattr(item,'position'):
                    if hasattr(item.position.value, "r"):
                        r = int(item.position.value.r)
                        c = int(item.position.value.c)
                    else:
                        r, c = self.getPositionByKeyword(item.position.value)
                    
                # These are the action statements
                elif hasattr(item, 'action'):
                    #Cast action to string, otherwise you cannot find right action
                    #This is temporary until I can call the action as a direct line in the command
                    action = str(item.action.value)
                    # print("AKLSJDHFKLAJHFH")
                    # print(item.action.value)
                    # if action == 'write':
                    #     b.configure(command=lambda: actionbuttons.Actions.write(item.action.text))
                    # elif action == 'close':
                    #     b.configure(command=lambda: actionbuttons.Actions.close(w))
                    # elif action == 'colorChange':
                    #     b.configure(command=lambda: actionbuttons.Actions.windowColorChange(w, item.action.color))
                    #     print("interpreter")
                    #a = actionbuttons.Actions.callAction(w,item)
                    a = actionbuttons.findAction(item)
                    #w = a[0]
                    #item = a[1]
                    b.configure(command=lambda: actionbuttons.callAction(w,item,action))
                    # else:
                    #     print("You have entered a command that is not defined")

        b.grid(row=r, column=c, sticky=N+S+E+W)
        return b


    def setButton(self,b,w,expr):
        '''Sets button based on user attributes.'''
        for item in expr.attributes[0]:
            if hasattr(item, 'color'):
                b.configure(bg=item.color.value)
            if hasattr(item, 'text'):
                b.configure(text=self.extractTextValue(item.text.value))
            elif hasattr(item,'size'):
                b.configure(width=item.size.value)
                b.configure(height=item.size.value)
            elif hasattr(item,'position'):
                if hasattr(item.position.value, "r"):
                    r = int(item.position.value.r)
                    c = int(item.position.value.c)
                else:
                    r, c = self.getPositionByKeyword(item.position.value)
                b.grid(row=r, column=c, sticky=N+S+E+W)
            elif hasattr(item, 'action'):
                # print(item)
                action = str(item.action.value)
                # print("AKLSJDHFKLAJHFH")
                # print(item.action.value)
                # if action == 'write':
                #     b.configure(command=lambda: actionbuttons.Actions.write(item.action.text))
                # elif action == 'close':
                #     b.configure(command=lambda: actionbuttons.Actions.close(w))
                # elif action == 'colorChange':
                #     b.configure(command=lambda: actionbuttons.Actions.windowColorChange(w, item.action.color))
                #     print("interpreter")
                #a = actionbuttons.Actions.callAction(w,item)
                a = actionbuttons.findAction(item)
                #w = a[0]
                #item = a[1]
                b.configure(command=lambda: actionbuttons.callAction(w,item,action))
        return b

    def fixButtonPadding(self,color,bindings):
        '''Fixes the padding around the buttons'''
        for i in bindings.keys():
            if bindings[i].bType == "Button":
                bindings[i].bObject.configure(highlightbackground = color)
        return bindings








    #               MENUS
    def makeMenu(self,w,expr,bindings):
        rootMenu = None
        children = w.winfo_children()
        for c in children:
            if type(c).__name__ == "Menu":
                rootMenu = c
        w.config(menu=rootMenu)
        return rootMenu

    def makeMenuItem(self,w,expr,bindings):
        menuItem = None
        rootMenu = None
        children = w.winfo_children()
        for c in children:
            if type(c).__name__ == "Menu":
                rootMenu = c

        #check if menu item has already been defined as a child of some other menu or menuitem
        for key in bindings:
            if bindings[key].bType == "Menu":
                if expr.varname in bindings[key].params:
                    #binding found, add to submenu to rootMenu
                    subMenu = Menu(bindings[key].bObject, tearoff=0)
                    #get the text attribute
                    subMenuText = "Undefined"
                    for item in expr.attributes:
                        if hasattr(item,'text'):
                            subMenuText = item.text.value
                    bindings[key].bObject.add_cascade(label=subMenuText,menu=subMenu)

                    for item in expr.attributes[0]:
                        if hasattr(item, 'options'):							
                            for v in item.options.value:
                                print(v)
                                '''
                                action = str(v)
                                a = actionbuttons.findAction(v)
                                subMenu.add_command(label=v.text,command=lambda: actionbuttons.callAction(w,v,action))
                                '''

                    menuItem = subMenu
                    w.config(menu=bindings[key].bObject)

        return menuItem


    #           IMAGES
    def makeImage(self, w, expr):
        '''Makes a images with the user defined attributes.'''
        r, c = 0, 0
        if hasattr(expr, "attributes"):
            for item in expr.attributes[0]:
                if hasattr(item, 'source'):
                    print(item.source.value)
                    i = PhotoImage(file=item.source.value)
                    l = Label(image=i)
                    l.image = i
                elif hasattr(item, 'position'):
                    if hasattr(item.position.value, "r"):
                        r = int(item.position.value.r)
                        c = int(item.position.value.c)
                    else:
                        r, c = self.getPositionByKeyword(item.position.value)
                else:
                    self.error("Error: Incorrect attribute.")
        l.grid(row=r, column=c, sticky=N+S+E+W)
        return l
        



    #               HELPER METHODS
    def makeBinding(self,t,v,o,p=[]):
        '''Makes a binding for the object.'''
        binding = Binding(t,v,o,p)
        return binding

    def addBinding(self,b,bindings):
        '''Takes a binding and adds to the dictionary of bindings.'''
        bindings[b.varname] = b
        return bindings

    '''#Make the binding associated with this function
    #The object will be the parameters passed in and the function action (in a tuple)
    def makeFunction(self,w, expr):
        pass'''

    #this should maybe take in parameters
    #expects "run" then a user defined function name
    #replaces , separating gooey instructions and adds period at end
    #Makes a temporary binding relating to parameters and then gets rid of that parameter
    def runFunction(self,bindings,function,localBindings):
        #Run function should create local bindings maybe?????????????????
        print("\n\n I'm running runFunction!")
        functionCode = bindings[function].bObject #We need to make this proper gooey code
        newBindings = localBindings
        print("New Bindings: ", newBindings)
        for action in functionCode:
            print("Here's the action", action)
            newBindings = self.interpret([action], newBindings)
            # newBindings = self.interpret(action, newBindings)

            print("New Bindings: ", newBindings)
        return newBindings
        # funStr = ''
        # for i in functionCode:
        #     funStr = funStr + " " + i
        # funStr = funStr[1:] + "."
        # #parse the function code and pass the parsed code as the ast
        # localAst = parse(funStr,Program)
        # newBindings = self.interpret(localAst,localBindings)
        # return newBindings


    def getOptions(self,expr):
        '''Get list of options, ie: make MenuItem with options [red green blue]. '''
        for item in expr.attributes:
            if hasattr(item, 'options'):
                return item.options.value
            else:
                return None

<<<<<<< HEAD
    #Consult the matrix and find the default values for an object
    def getAllDefaults(self, typeName):
        for i in range(0,14):
            defaultAttr = matrix.getDefault(typeName, i)
            #Need to figure out how to return these
=======
    def checkVarname(self,exp,bindings):
        if hasattr(exp, "varname"):
            #if expr.varname in bindings:
            if exp.varname in bindings:
                message = exp.varname, "already defined."
                self.error(message)

    def getObject(self,exp,bindings):
        if exp.varname in bindings:
            return bindings[exp.varname]
        else:
            message = exp.varname, "undefined."
            self.error(message)
            
    def getPositionByKeyword(self, keyword):
        if keyword == "center":
            r = math.floor(float(Interpreter.gRows)/2)
            c = math.floor(float(Interpreter.gColumns)/2)
        elif keyword == "top":
            r = 0
            c = math.floor(float(Interpreter.gColumns)/2)
        elif keyword == "bottom":
            r = Interpreter.gRows
            c = math.floor(float(Interpreter.gColumns)/2)
        elif keyword == "left":
            r = math.floor(float(Interpreter.gRows)/2)
            c = 0
        elif keyword == "right":
            r = math.floor(float(Interpreter.gRows)/2)
            c = Interpreter.gColumns
        elif keyword == "topleft":
            r = 0
            c = 0
        elif keyword == "topright":
            r = 0
            c = Interpreter.gColumns
        elif keyword == "bottomleft":
            r = Interpreter.gRows
            c = 0
        elif keyword == "bottomright":
            r = Interpreter.gRows
            c = Interpreter.gColumns
        return r, c
    
    def extractTextValue(self, value):
        words = re.findall(r'[\w\d\.]+', value)
        return ' '.join(words)
>>>>>>> 82879131ffd6e904073b50ee4c51d8da6483ae75
