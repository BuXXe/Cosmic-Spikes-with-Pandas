'''
Created on 23.12.2015

@author: Christopher Skerra, Dennis Skerra
@contact: Skerra.Christopher@yahoo.de

Licensed under CC BY-NC-SA 4.0
https://creativecommons.org/licenses/by-nc-sa/4.0/

'''

from numpy import sqrt, nan
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
   
class DataSet(object):
    '''
    classdocs
    '''
    def __init__(self, originalData,filename):
        '''
        Constructor
        '''
        self.filename = filename
        
        # keep a copy of the original set always stored in originalData
        self.originalData = originalData.copy()
        
        # convention: history stores sets excluding processedData, which is the current set
        self.history = []
        self.processedData = originalData
        
        # applied parameter history as list of parameters 
        # (ex: [("Trendline",True,30,4,50),("DFThreshold",15,5)]
        self.parameterHistory=[]
        
        # this structure stores the marked points in manual unspiker mode
        # TODO: try to move this in a self contained manual unspiker class 
        # when the no click event with self contained unspiker problem is solved
        self.toDelete=[]
    
    # create a description string for the info box     
    def getDescription(self):
        title = "Original Filename: "+self.filename+"\n"
        framecount = "Frames in this Set: " + str(self.originalData.shape[1])+"\n"
        rowcount = "Sample Points in this Set: " + str(self.originalData.shape[0])+"\n"
        lowest = "Lowest Sample Point: "+ str(self.originalData.index[0])+"\n"
        highest = "Highest Sample Point: "+ str(self.originalData.index[len(self.originalData.index)-1])+"\n"
        description = title +"\n"+ framecount +"\n"+ rowcount +"\n"+ lowest +"\n"+ highest
        
        # append history of parameters
        OperatorHistory = ""
        if len(self.parameterHistory) == 0:
            OperatorHistory = "\nOperator-History:\nWe have not yet processed this set!"    
        else:
            OperatorHistory = "\nOperator-History:\n"
            # display parameters as string with their function (ex.: Trendline(True,30,4,50))
            for operation in self.parameterHistory:
                OperatorHistory +=str(operation)+ "\n"

        description += "\n"+OperatorHistory                
        return description
     
    def getOriginalData(self):
        return self.originalData 
    
    def exportAsCSV(self, filepath):
        self.processedData.to_csv(filepath, sep=';')
    
    def exportMeanAsCSV(self, filepath):
        self.processedData.interpolate().mean(axis=1).to_csv(filepath, sep=';')
    
    def showGraphOriginal(self,ax=None):
        if not ax == None:
            # we have a preview plot: do not show a title, legend and axes definitions
            self.originalData.plot(legend  = False,ax=ax,xticks=[],yticks=[])
        else:
            self.originalData.plot(title=self.filename,legend  = False)
    
    def showGraphProcessed(self):
        self.processedData.interpolate().plot(title=self.filename+" INTERPOLATED!",legend  = False)
    
    def showGraphProcessedMean(self):
        self.processedData.interpolate().mean(axis=1).plot(title=self.filename+" INTERPOLATED MEAN",legend  = False)    

    # open processed interpolated data and attach click and key events 
    def manualUnspike(self, ui):
        res = self.processedData.interpolate().plot(title="MANUAL UNSPIKER\nd: delete marked points , w: undo last marking\n"+self.filename,legend  = False,picker=2)
        res.figure.canvas.mpl_connect('pick_event', self.onpick)
        res.figure.canvas.mpl_connect('key_release_event', self.onkeyhand)
        # INFO: dirty workaround in order to update ui info boxes on delete 
        self.ui = ui

    # manual unspiker key events
    def onkeyhand(self,event):
            # undo button which deletes the circle and the entry in the toDelete set
            # the plot will be redrawn afterwards
            if event.key =="w":
                if len(self.toDelete) >0:
                    index = len(self.toDelete)-1
                    circ = self.toDelete[index][2]
                    del self.toDelete[index]
                    circ.remove()
                    plt.draw()
            # delete button to delete marked points out of the set
            if event.key =="d":
                if len(self.toDelete) > 0:
                    # first do history and parameter history updates
                    self.history.append(self.processedData.copy())
                    
                    
                    # create dictionary with each Frame as key and a list 
                    # for each x coord in this frame which has been deleted
                    # sort the x coord lists ascending to keep it readable
                    deleteset = {}
                    
                    for entry in self.toDelete:
                        if not entry[0] in deleteset:
                            deleteset[entry[0]] = []    
                        deleteset[entry[0]].append(self.processedData.index.values[entry[1]])
                    
                    for key in deleteset.keys():
                        deleteset[key].sort()
                        
                    self.parameterHistory.append(("Manual",deleteset))
                    
                    
                    # delete points out of processed data set
                    for item in self.toDelete:
                        self.processedData[item[0]][self.processedData.index.values[item[1]]] = nan
                    # clear toDelete set
                    self.toDelete=[]
                    # remember current zoomfactor and panning
                    axi =  plt.gca().axis()
                    # clear plot
                    plt.cla()
                    # plot updated processed set
                    self.processedData.interpolate().plot(title="MANUAL UNSPIKER\nd: delete marked points , w: undo last marking\n"+self.filename,ax=plt.gca(),legend  = False,picker=2)
                    # set zoomfactor and panning
                    plt.axis(axi)
                    # update infobox
                    self.ui.updateTextBoxes()

    # the pick event handler for the manual unspiker
    def onpick(self,event):
            # ensure there are no double entries
            for (frame,pos,circle) in self.toDelete:
                if frame == event.artist.get_label() and pos == event.ind[0]:
                    return
            
            # get clicked actor identity
            ind = event.ind
    
            # get the x and y values for the clicked actor
            yval = self.processedData[event.artist.get_label()].iloc[ind[0]]
            xval = self.processedData.index.values[ind[0]]
            
            # to avoid the distortion we use an ellipse with respect to aspect ratio
            height = self.processedData.max().max() - abs(self.processedData.min().min())
            width = self.processedData.index.values.max() - abs(self.processedData.index.values.min())
            aspect = height/width
            radius = 3.0
            circle1= Ellipse((xval,yval), radius/aspect,aspect*radius,color='r')
            
            # toDelete content: Frame, xpos, circle instance
            self.toDelete.append((event.artist.get_label(),ind[0],circle1))
            # add circle to the plot and update it
            event.artist.axes.add_artist(circle1)
            plt.draw()

    def revertstep(self):
        # TODO: ensure memory cleanup
        # set processed data to last in history (if it exists)
        # then remove history and parameter history entry
        if len(self.history) > 0:
            self.processedData = self.history.pop()
            self.parameterHistory.pop()
        return
    
    def reset(self):
        # TODO: ensure memory cleanup
        self.parameterHistory = []
        self.history = []
        self.processedData = self.originalData.copy()
        
        return

    # TODO: It seems that the garbage collector has a problem with our structure
    # the memory is never released even though we delete all structures
    def __del__(self):
        del self.originalData
        del self.processedData
