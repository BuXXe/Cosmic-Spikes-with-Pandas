'''
Created on 23.12.2015

@author: BuXXe
'''
import pandas as pd
from numpy import sqrt, nan
from scipy.ndimage.morphology import iterate_structure

class DataSet(object):
    '''
    classdocs
    '''

    
    def __init__(self, originalData,filename):
        '''
        Constructor
        '''
        self.originalData = originalData
        self.filename = filename
        self.processedData = None
        self.iterations = None
        self.threshold = None
        
    def getDescriptionOriginalData(self):
        description = ""
        title = "Original Filename: "+self.filename+"\n"
        framecount = "Frames in this Set: " + str(self.originalData.shape[1])+"\n"
        rowcount = "Sample Points in this Set: " + str(self.originalData.shape[0])+"\n"
        lowest = "Lowest Sample Point: "+ str(self.originalData.index[0])+"\n"
        highest = "Highest Sample Point: "+ str(self.originalData.index[len(self.originalData.index)-1])+"\n"
        description = title +"\n"+ framecount +"\n"+ rowcount +"\n"+ lowest +"\n"+ highest
        return description
    
    def getDescriptionProcessedData(self):
        description = ""
        #if self.processedData=None:
        # Workaround to check if processed data is there
        if self.iterations == None or self.threshold == None:
            description = "\n\nWe have not yet processed this set!"
            
        else:
            description = "The processed data was computed with the following parameters:\n"
            description += "Threshold: "+str(self.threshold)+"\nIterations: "+str(self.iterations)
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
            self.originalData.plot(title=self.filename,legend  = False)
    
    def showGraphProcessed(self):
        self.processedData.interpolate().plot(title=self.filename,legend  = False)
    
    def showGraphProcessedMean(self):
        self.processedData.interpolate().mean(axis=1).plot(title=self.filename,legend  = False)    
    
            
    def initProcessedDataWithOriginal(self):
        self.processedData = self.originalData.copy()
        
    def setProcessingParameters(self,iterat,thresh):
        self.iterations = iterat
        self.threshold = thresh
    
    

            
    # do one iteration differential error correction
    def errorcorrectdiff(self,threshold,inplace):
        # if inplace = False we copy the original data and start a new iteration 
        if inplace == False:
            self.processedData = self.originalData.copy()
            
        # if inplace is True we do another iteration on the current processed Data
        setHasChanged=False
        frames = self.processedData.columns.values
         
        # TODO: idea: interpolate here to fill nan gaps 
        # but not give an interpolated result
        # need to interpolate for the diff quot
        # use with caution!?
        diff=self.processedData.interpolate().diff() 

        diffmeanset= diff.mean(axis=1)
        diffmeanset.name = "DiffMean"
        data = self.processedData.join(diffmeanset)
          
        for frame in frames:
            data["DiffError "+frame] = sqrt(((1.0-(diff[frame] / data["DiffMean"]))*100.0)**2)
        # get the column with the max error value
        maxerrors = data.filter(regex="DiffError ").idxmax(axis=1).replace("DiffError ","",regex=True)
        maxerrors.name="MaxErrorFrame"
        #diffs = data.filter(regex="DiffError ").max(axis=1).sort_values(ascending=False)
     
        for x in xrange(0,len(maxerrors)):
            if str(maxerrors.iloc[x]) != 'nan':
                if data["DiffError " + maxerrors.iloc[x]][maxerrors.index.values[x]] > threshold:
                    setHasChanged =True
                    newmean = data[frames].drop(maxerrors.iloc[x], axis=1).mean(axis=1)   
                    data[maxerrors.iloc[x]][maxerrors.index.values[x]] = nan
                     
        # cleanup 
        self.processedData= data[frames]
        print "step"
        return setHasChanged#,diffs
    

    # TODO: It seems that the garbage collector has a problem with our structure
    # the memory is never release even though we delete all structures
    def __del__(self):
        del self.originalData
        del self.processedData
