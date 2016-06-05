'''
Created on 23.12.2015

@author: Christopher Skerra, Dennis Skerra
@contact: Skerra.Christopher@yahoo.de - https://github.com/BuXXe/Cosmic-Spikes-with-Pandas
@license: Licensed under CC BY-NC-SA 4.0 - https://creativecommons.org/licenses/by-nc-sa/4.0/

'''

import Tix
from SplashScreen import SplashScreen
from Tkinter import *
from program_ui import ProgramUI
import tkFileDialog
import pandas as pd
import os
from DataSet import DataSet
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
import TrendlineUnspiking
matplotlib.use('TkAgg')
import ImportHelpers

pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
# text widgets, if disabled, do not allow to select / set focus in order to ctrl+c
# this helps:
# t.bind("<1>", lambda event: t.focus_set())

# This list contains the current items
# the list is corresponding to the list box
activeDataList = []

figu = None
canvas =None

class Program(ProgramUI):
    pass

    # Use text_field as read-only
    # use states to create read only access
    # scroll to end of debug_text
    def write_to_Debug(self, message, tags):
        self.debug_text.config(state=NORMAL)
        self.debug_text.insert(END,message, tags)
        self.debug_text.config(state=DISABLED)
        self.debug_text.see("end")
        
    def add_button_command(self, *args):
        # Open File / Files      
        filetypes  = [('text/csv files', '*.csv;*.txt'), ('all files', '.*')]
        file_paths = tkFileDialog.askopenfilenames(initialdir=self.lastdirectory,filetypes = filetypes)
        
        if len(file_paths)>0:
            self.lastdirectory = os.path.split(file_paths[0])[0]
        
        # for each selected file do 
        for filepath in file_paths:
            data = None
            try:
                # differentiate if original spectroscopy txt or already processed csv
                # use file ending as criterion
                if os.path.splitext(filepath)[1].lower() == ".txt":              
                    data = ImportHelpers.convertTxtToPandaFrame(filepath)
                elif os.path.splitext(filepath)[1].lower() == ".csv":
                    data = ImportHelpers.convertCsvToPandaFrame(filepath)

                if data is None:
                    raise Exception("Import problem")
                
                # append to data array and UI list
                activeDataList.append(DataSet(data , os.path.split(filepath)[1]))
                self.item_list.insert(END,os.path.split(filepath)[1])
            except :
                self.write_to_Debug("[ERROR]: Processing of file: "+filepath+" failed\n", ("e"))

    def remove_button_command(self, *args):
        # check if there is something selected in listbox 
        if self.item_list.curselection():
            del activeDataList[self.item_list.curselection()[0]]
            self.item_list.delete(self.item_list.curselection()[0])
            if self.item_list.size()== 0:
                # clear the text boxes
                self.infobox_text.config(state=NORMAL)
                self.infobox_text.delete(1.0, END)
                self.infobox_text.config(state=DISABLED)
                self.createPreview()

            else:
                # update and set anchor
                self.item_list.select_set(0)
                # update textboxes
                self.updateTextBoxes()
                self.createPreview()
  
    # update parameter boxes and preview canvas
    def immediately(self,e):
        self.updateTextBoxes()
        self.createPreview()
    
    # update info box content
    def updateTextBoxes(self):
        if self.item_list.curselection():
            self.infobox_text.config(state=NORMAL)
            self.infobox_text.delete(1.0, END)
            self.infobox_text.insert(END,activeDataList[self.item_list.curselection()[0]].getDescription())
            self.infobox_text.config(state=DISABLED)

    # get the preview for the selected graph and put it into preview canvas
    def createPreview(self):
        global figu
        global canvas
        
        # initial creation of preview window
        if figu == None:
            figu = Figure(frameon=False,figsize=(1,1), dpi=100)
            
            canvas = FigureCanvasTkAgg(figu, self.middle_controls_frame)
            
            canvas.get_tk_widget().grid(
                in_    = self.middle_controls_frame,
                column = 1,
                row    = 15,
                columnspan = 2,
                ipadx = 0,
                ipady = 0,
                padx = 0,
                pady = 0,
                rowspan = 1,
                sticky = "news")

        # clear the preview and plot preview for current selected set
        figu.clf()
        a = figu.add_subplot(111)
        
        if self.item_list.curselection():
            activeDataList[self.item_list.curselection()[0]].showGraphOriginal(ax=a)
        canvas.show()    
        canvas.draw()
    
    ####
    #
    # EXPORT-FUNCTIONS
    #
    ####

    def export_csv_button_command(self, *args):
        if self.item_list.curselection():
            try:
                filetypes  = [('all files', '.*'), ('text files', '.txt'), ('csv files', '.csv')]
                filepath = tkFileDialog.asksaveasfilename(initialdir=self.lastdirectory, filetypes=filetypes,initialfile ="us"+activeDataList[self.item_list.curselection()[0]].filename.replace(".txt",".csv") )
                if filepath =="":
                    return
                
                if len(filepath)>0:
                    self.lastdirectory = os.path.split(filepath)[0]
                    
                # append parameter history to logfile
                with open("logfile.txt", "a") as logfile:
                    logfile.write(activeDataList[self.item_list.curselection()[0]].getLogEntry()+"\n")

                activeDataList[self.item_list.curselection()[0]].exportAsCSV(filepath)
                self.write_to_Debug("[INFO]: Unpsiked Data Set: "+self.item_list.get(self.item_list.curselection()[0]) +" exported as CSV to "+filepath+"\n",None)
            except:
                self.write_to_Debug("[ERROR]: There was an error exporting DataSet\n", ("e"))

    def export_mean_button_command(self, *args):
        if self.item_list.curselection():
            try:
                filetypes  = [('all files', '.*'), ('text files', '.txt'), ('csv files', '.csv')]
                filepath = tkFileDialog.asksaveasfilename(initialdir=self.lastdirectory, filetypes=filetypes,initialfile ="usmean"+activeDataList[self.item_list.curselection()[0]].filename.replace(".txt",".csv"))
                if filepath =="":
                    return
                if len(filepath)>0:
                    self.lastdirectory = os.path.split(filepath)[0]
                    
                # append parameter history to logfile
                with open("logfile.txt", "a") as logfile:
                    logfile.write(activeDataList[self.item_list.curselection()[0]].getLogEntry()+"\n")
                    
                activeDataList[self.item_list.curselection()[0]].exportMeanAsCSV(filepath)
                self.write_to_Debug("[INFO]: Unspiked Mean of Data Set: "+self.item_list.get(self.item_list.curselection()[0]) +" exported as CSV to "+filepath+"\n",None)
            except:
                self.write_to_Debug("[ERROR]: There was an error exporting DataSet\n", ("e"))

    ####
    #
    # DATASET-MANAGEMENT-FUNCTIONS
    #
    ####
    
    def reset_dataset_button_command(self, *args):
        if self.item_list.curselection():
            activeDataList[self.item_list.curselection()[0]].reset()
            self.updateTextBoxes()
    
    def revert_button_command(self, *args):
        if self.item_list.curselection():
            activeDataList[self.item_list.curselection()[0]].revertstep()
            self.updateTextBoxes()

    ####
    #
    # PLOTTING-FUNCTIONS
    #
    ####

    def plot_original_button_command(self, *args):
        if self.item_list.curselection():
            activeDataList[self.item_list.curselection()[0]].showGraphOriginal()
        
    def plot_unspiked_button_command(self, *args):
        if self.item_list.curselection():
            activeDataList[self.item_list.curselection()[0]].showGraphProcessed()
    
    def plot_mean_button_command(self, *args):
        if self.item_list.curselection():
            activeDataList[self.item_list.curselection()[0]].showGraphProcessedMean()
            
    ####
    #
    # UNSPIKE-FUNCTIONS
    #
    ####
    
    def dryrun_button_command(self, *args):
        # TODO: Unify this to fit a more abstract unspiking library / interface

        # check if nothing is selected, then do nothing
        if not self.item_list.curselection():
            return

        # get parameters
        trendlinedegree = self.trendlinedegree_entry.get()
        errorfactor = self.disterrfactor_entry.get()
        minmeanerror = self.mindistmean_entry.get()
        usetrendline = bool(self.useTrendlinevariable.get())
        
        # do type checks
        if not trendlinedegree.isdigit():
            self.write_to_Debug("[ERROR]: The trendline degree variable is not a valid number\n", ("e"))
            return

        if not errorfactor.isdigit():
            self.write_to_Debug("[ERROR]: The error factor variable is not a valid number\n", ("e"))
            return
        
        if not minmeanerror.isdigit():
            self.write_to_Debug("[ERROR]: The min dist mean variable is not a valid number\n", ("e"))
            return
        
        # do the dry run with debug set to True
        TrendlineUnspiking.unspike(activeDataList[self.item_list.curselection()[0]], usetrendline, trendlinedegree, errorfactor, minmeanerror, True)

    def manual_unspiker_button_command(self, *args):
        # check if nothing is selected, then do nothing
        if not self.item_list.curselection():
            return        
        # INFO: dirty workaround: pass self in order to update gui each time the manual unspiker deletes points
        # TODO: When the problem with the click event not fired for self contained manual unspiker class is solved
        # rework this 
        activeDataList[self.item_list.curselection()[0]].manualUnspike(self)

        return

    def run_unspike_button_command(self, *args):
        # TODO: Unify this to fit a more abstract unspiking library / interface
        
        # check if nothing is selected, then do nothing
        if not self.item_list.curselection():
            return
        
        # get parameters
        trendlinedegree = self.trendlinedegree_entry.get()
        errorfactor = self.disterrfactor_entry.get()
        minmeanerror = self.mindistmean_entry.get()
        usetrendline = bool(self.useTrendlinevariable.get())
        
        # do type checks
        if not trendlinedegree.isdigit():
            self.write_to_Debug("[ERROR]: The trendline degree variable is not a valid number\n", ("e"))
            return

        if not errorfactor.isdigit():
            self.write_to_Debug("[ERROR]: The error factor variable is not a valid number\n", ("e"))
            return
        
        if not minmeanerror.isdigit():
            self.write_to_Debug("[ERROR]: The min dist mean variable is not a valid number\n", ("e"))
            return

        TrendlineUnspiking.unspike(activeDataList[self.item_list.curselection()[0]], usetrendline, trendlinedegree, errorfactor, minmeanerror, False)
        self.updateTextBoxes()

root = None
def main():
    try: userinit()
    except NameError: pass
    global root
        
    root = Tix.Tk( )

    with SplashScreen( root, 'Pandas.gif', 3.0 ):
        ProgramInstances = Program(root)
        root.title('Unspike with Pandas')
        root.iconbitmap("Panda.ico")
        try: run()
        except NameError: pass
        root.protocol('WM_DELETE_WINDOW', root.destroy)
    
    root.mainloop( )
if __name__ == '__main__': main()
