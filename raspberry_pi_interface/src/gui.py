from tkinter import *
import time
from time import sleep
from take_picture import *
from classify import *
from score import *
from constants import *

class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        #initialize window
        Tk.__init__(self, *args, **kwargs)
        self.title("Waste Classifier")

        #make full screen
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

        # this container contains all the pages
        container = Frame(self)
        #make the grid cover the entire window
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #object to store the multiple pages
        self.frames = {}

        #initialize all pages
        for F in (StartPage, ClassificationPage, ThankYouPage, NoPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #show the start page at the beginning
        self.show_frame(StartPage)

    #show_frame event handler, used to switch between pages
    def show_frame(self, name, classification=None):
        frame = self.frames[name]
        if(frame == self.frames[ClassificationPage] and classification != None):
            waste_type = classification.split()[0]
            pred_class = classification.split()[2]
            frame.set_label(waste_type,pred_class)
        frame.tkraise()
        if(frame == self.frames[ThankYouPage]):
            frame.start_countdown()


class ThankYouPage(Frame):

    #switches to starting page after countdown
    def start_countdown(self):
        (num_correct,num_wrong,perc_correct) = get_score()
        self.score_label.configure(text = "Correct: "+str(num_correct) + " Wrong: " + str(num_wrong) + " Accuracy: " + str(perc_correct) + "%" )
        self.after(THANK_YOU_TIME,
                   lambda: self.controller.show_frame(StartPage))

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        thank_you_label = Label(
            self, text='Thank you. Happy wasting!', font=LARGE_FONT)
        # center button on page
        thank_you_label.grid(row=0)
        self.score_label = Label(
            self, text='Score: ', font=SM_FONT)
        self.score_label.grid(row=1)


class NoPage(Frame):

    #event handlers for the buttons:
    def handle_trash(self, controller):
        print("handling trash")
        store_in_folder("Trash")
        append_score(False)
        controller.show_frame(ThankYouPage)

    def handle_recycling(self, controller):
        print("handling recycling")
        store_in_folder("Recycling")
        append_score(False)
        controller.show_frame(ThankYouPage)

    def handle_compost(self, controller):
        print("handling compost")
        store_in_folder("Compost")
        append_score(False)
        controller.show_frame(ThankYouPage)
    
    def handle_other(self, controller):
        print("handling other")
        store_in_folder("Other")
        controller.show_frame(ThankYouPage)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        #set up the columns and rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #set up the no question and the buttons
        no_question = Label(
            self, text='What is the correct classification?', font=MED_FONT)
        no_question.grid(row=0, columnspan=4)

        trash_button = Button(self, text='Trash',
                              command=lambda: self.handle_trash(controller), font=MED_FONT
                              )
        trash_button.grid(row=1, column=0)

        recycling_button = Button(self, text='Recycling',
                                  command=lambda: self.handle_recycling(controller), font=MED_FONT
                                  )
        recycling_button.grid(row=1, column=1)

        compost_button = Button(self, text='Compost',
                              command=lambda: self.handle_compost(controller), font=MED_FONT
                              )
        compost_button.grid(row=1, column=2)
        
        other_button = Button(self, text='Other',
                              command=lambda: self.handle_other(controller), font=MED_FONT
                              )
        other_button.grid(row=1, column=3)


class StartPage(Frame):
    #classify images and then send to the classification page
    def handle_classify_button_click(self, controller):
        print('classifying')
        img = take_waste_pic()
        (waste_type, pred_class) = predict_single_img(img)
        classification = waste_type + " - " + pred_class
        controller.show_frame(ClassificationPage, classification)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        classify_button = Button(self, text='Classify Waste',
                                 command=lambda: self.handle_classify_button_click(controller), font=LARGE_FONT
                                 )
        # center button on page
        classify_button.place(relx=0.5, rely=0.5, anchor=CENTER)


class ClassificationPage(Frame):
	#page that displays the classification
    def go_back(self, controller):
        controller.show_frame(StartPage)

    def handle_yes(self, controller):
        print("yes")
        append_score(True)
        store_in_folder(self.waste_type)
        controller.show_frame(ThankYouPage)

    def handle_no(self, controller):
        print("no")
        
        controller.show_frame(NoPage)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        #set up the grid layout for this page
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

        #classification variables
        self.classification = ""
        self.waste_type = ""

        classification_header = Label(
            self, text='Classification: ', font=SM_FONT)
        classification_header.grid(row=1, columnspan=2)

        #create the label that will show the classfication of the object
        self.classification_label = Label(self, text="", font=LARGE_FONT)
        self.classification_label.grid(row=2, columnspan=2)
        self.pred_class_label = Label(self, text="", font=XS_FONT)
        self.pred_class_label.grid(row=3, columnspan=2)

        #create the label to ask the user whether or not the classification is correct
        question_label = Label(
            self, text='Is the classification correct?', font=SM_FONT)
        question_label.grid(row=4, columnspan=2)

        #create yes and no buttons
        yes_button = Button(self, text='Yes',
                            command=lambda: self.handle_yes(controller), font=MED_FONT
                            )
        yes_button.grid(row=5, column=0, sticky=E, padx=(0, 40))

        no_button = Button(self, text='No',
                           command=lambda: self.handle_no(controller), font=MED_FONT)
        no_button.grid(row=5, column=1, sticky=W, padx=(40, 0))

    #setter method to set the classification label
    def set_label(self, waste_type, pred_class):
        print("classification", waste_type+"-"+pred_class)
        self.waste_type = waste_type
        self.pred_class = pred_class
        self.classification_label.configure(text=waste_type)
        self.pred_class_label.configure(text=pred_class)


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
