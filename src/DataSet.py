'''
Created on 23.12.2015

@author: BuXXe
'''
import pandas as pd
from numpy import sqrt, nan
from scipy.ndimage.morphology import iterate_structure
import numpy as np
import matplotlib.pyplot as plt
   
class DataSet(object):
    '''
    classdocs
    '''
    def __init__(self, originalData,filename):
        '''
        Constructor
        '''
        # TESTING: History with ALL entries
        # Circumvents problem of only one step back and then what to do with the ui button
        # convention:  history consists of all data sets without processed data (history is filled before changing a set)
        self.originalData = originalData
        self.history = []
        self.filename = filename
        self.processedData = None
        
        # applied parameter history as list of parameters (ex: [("Trendline",True,30,4),("DFThreshold",15,5)]
        self.paramterHistory=[]
        
        # parameters: TrendlineCorrection: T/F, Trendline Degree, Min Distance from mean, Distance Error Factor  
        #self.iterations = None
        #self.threshold = None
        #self.ARRPlot= None
        #self.toDelete=[]
        
    def getDescription(self):
        description = ""
        title = "Original Filename: "+self.filename+"\n"
        framecount = "Frames in this Set: " + str(self.originalData.shape[1])+"\n"
        rowcount = "Sample Points in this Set: " + str(self.originalData.shape[0])+"\n"
        lowest = "Lowest Sample Point: "+ str(self.originalData.index[0])+"\n"
        highest = "Highest Sample Point: "+ str(self.originalData.index[len(self.originalData.index)-1])+"\n"
        description = title +"\n"+ framecount +"\n"+ rowcount +"\n"+ lowest +"\n"+ highest
        
        # append history of parameters 
        
        OperatorHistory = ""
        if len(self.paramterHistory) == 0:
            OperatorHistory = "\nOperator-History:\nWe have not yet processed this set!"
            
        else:
            OperatorHistory = "\nOperator-History:\n"
            # display parameters as string with their function (ex.: Trendline(True,30,4))
            for operation in self.paramterHistory:
                # tuple resolution
                OperatorHistory +=str(operation)+ " "

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
            # we have a preview plot
            # dont show a title, legend and axis definitions
            self.originalData.plot(legend  = False,ax=ax,xticks=[],yticks=[])
        else:
            res = self.originalData.plot(title=self.filename,legend  = False)
    
    def showGraphProcessed(self):
        self.processedData.interpolate().plot(title=self.filename,legend  = False)
    
    def showGraphProcessedMean(self):
        self.processedData.interpolate().mean(axis=1).plot(title=self.filename,legend  = False)    

    def revertstep(self):
        # TODO: ensure memory cleanup
        # set processed data to last in history (if existing)
        # then remove history entry and parameter history entry
        if len(self.history) > 0:
            self.processedData = self.history.pop()
            self.paramterHistory.pop()
        
        return
    
    def reset(self):
        # TODO: ensure memory cleanup
        self.paramterHistory = []
        self.history = []
        self.processedData = self.originalData
        
        return

    # TODO: It seems that the garbage collector has a problem with our structure
    # the memory is never release even though we delete all structures
    def __del__(self):
        del self.originalData
        del self.processedData
