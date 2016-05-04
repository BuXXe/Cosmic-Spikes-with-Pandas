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
        self.originalData = originalData
        self.filename = filename
        self.processedData = None
        self.iterations = None
        self.threshold = None
        self.ARRPlot= None
        self.toDelete=[]
        
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
            res = self.originalData.plot(title=self.filename,legend  = False,picker=2)
             
            
            res.figure.canvas.mpl_connect('pick_event', self.onpick3)
            res.figure.canvas.mpl_connect('key_release_event', self.onkeyhand)


    def onkeyhand(self,event):
        if event.key =="k":
            if len(self.toDelete) >0:
                index = len(self.toDelete)-1
                circ = self.toDelete[index][2]
                del self.toDelete[index]
                circ.remove()
                plt.draw()
        if event.key =="d":
            for item in self.toDelete:
                self.originalData[item[0]][self.originalData.index.values[item[1]]] = nan
            self.toDelete=[]
            axi =  plt.gca().axis()
            plt.cla()
            self.originalData.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1)
            plt.axis(axi)
            
            
        if event.key == "t":
            axi =  plt.gca().axis()
            plt.cla()
            for framenr in xrange(1,len(self.originalData.columns)+1):
                print framenr 
                # compute trendline
                x = self.originalData.index.values
                y = self.originalData["Frame "+str(framenr)].as_matrix()

                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)

#                originalFrame.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1)

                orig = self.originalData["Frame "+str(framenr)]-p(x)
                
                orig.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1)
                
                #plt.plot(x,p(x),"r-")

            plt.axis(axi)
            

            
    def onpick3(self,event):
        ind = event.ind
        print event.ind
        print('onpick3 scatter:', ind)
        print event.artist.get_label()
        
        
        xval = self.originalData[event.artist.get_label()].iloc[ind[0]]
        yval = self.originalData.index.values[ind[0]]

            
        circle1=plt.Circle((yval,xval),5,color='r')
        
        self.toDelete.append((event.artist.get_label(),ind[0],circle1))
        
        event.artist.axes.add_artist(circle1)
        plt.draw()
        
    
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

    # sophisticated error correction
    # return True or False 
    # False: Set has not changed 
    def sophisticatedErrorCorrection(self,threshold):
        
        setHasChanged=False
        
        # get list of frames in the current set
        frames = self.processedData.columns.values
        
        # interpolate and differential quotient
        diff=self.processedData.interpolate().diff() 

        # calculate the mean of the differential quotient and append it to the dataset
        diffmeanset= diff.mean(axis=1)
        diffmeanset.name = "DiffMean"
        data = self.processedData.join(diffmeanset)

        # calculate the error of the differential quotient from the differential quotient mean
        for frame in frames:
            data["DiffError "+frame] = sqrt(((1.0-(diff[frame] / data["DiffMean"]))*100.0)**2)
        
        # get the column with the max error value
        maxerrors = data.filter(regex="DiffError ").idxmax(axis=1).replace("DiffError ","",regex=True)
        maxerrors.name="MaxErrorFrame"
     
        # compute range amplitude anomalies
        # we use a specific range (current xval +- range-width) 
        # in this range, we take the amplitudes and calculate the relation between these amplitudes
        # relation means: (Sum over all values in range with (value at xval - value at current xval)) / rangewidth*2
        # access rows: data[startrow(incl):endrow(excl)]
        # we circumvent the problem of heads and tails by allowing only positive values with endrow being at most length of dataframe
        # the sum division will keep track of this circumstance
        # ex: for the first entry and range of 2 we look at rows 0 1 2 
        # ex2: for another entry at pos 5 and range 2 we look at rows 3 4 5 6 7
        range = 5
        colss=[]
        for frame in frames:
            ARRframerows = []
            
            for walker in xrange (0,data.shape[0]):
                #if walker < 520 or walker > 600:
                #    ARRframerows.append( 0)
                #    continue
                
                startrow = walker-range
                endrow = walker+range+1
                if startrow <0:
                    startrow = 0
                if endrow > data.shape[0]:
                    endrow = data.shape[0]
                    
                valuecount = endrow - startrow
                # Amplitude Range Relation = ARR
                #TODO: What the hell happens here? it should not work at all because the slicing object is incorrectly applied
                # it needs to use the iloc in order to take the position. in this case we take the real value ranges
                #t1 = data[frame][startrow:endrow].sum()
                t1 = data[frame].iloc[startrow:endrow].sum()
                t2 = (valuecount * data[frame].iloc[walker])
                
#                 if  "Frame 1" in frame:
#                     if data.index.values[walker] == 891.558:
#                         print "XXXXXXXXXXXXX"
#                         print data[frame].iloc[startrow:endrow]
#                         print data["Frame 2"].iloc[startrow:endrow]
#                         print startrow
#                         print endrow
#                         
#                         for n in xrange(0,4):
#                             print data[frame].iloc[walker-2+n]
#                         for n in xrange(0,4):
#                             print data["Frame 2"].iloc[walker-2+n]
#                     print frame," xval: ",data.index.values[walker]
#                     print data[frame].iloc[walker], "\t| ",data["Frame 2"].iloc[walker]
#                     print t1 , "\t| ", data["Frame 2"].iloc[startrow:endrow].sum()
#                     print t2 , "\t| ", (valuecount * data["Frame 2"].iloc[walker])
#                     print "--------------------------"
                
                ARRframerows.append( (t1 - t2) / valuecount)
                
            colss.append("ARR "+frame)
            data["ARR "+frame] = ARRframerows
        #data[colss].plot()
        self.ARRPlot = data[colss]
        
        # Take distance to mean as criterion
        # find maximum distance to mean and give out x value for this potential spike
        
        
        mean = data[colss].mean(axis=1)
        maxframe = ""
        maxval = 0.0
        maxvalues = {}
        columnssss=[]
        for frame in frames:
            data["ARR Error " + frame]=(data["ARR "+frame] - mean).abs()
            columnssss.append("ARR Error "+frame) 
            maxvalues[frame] = (data["ARR Error " + frame].idxmax(),data["ARR Error " + frame].max())
            if data["ARR Error " + frame].max() > maxval:
                maxframe = frame
                maxval = data["ARR Error " + frame].max()
        
        #data[frames].diff().plot()
        
        data[columnssss].plot()
        print maxvalues
        print maxframe
        print maxvalues[maxframe]
        # get max of columns maxes
        # maxvalues has tuple of index and max value for each frame
        data[maxframe][maxvalues[maxframe][0]] = nan
        self.processedData = data[frames]
        # get the frame number and x value 
        
        #print data        
#         for x in xrange(0,len(maxerrors)):
#             if str(maxerrors.iloc[x]) != 'nan':
#                 if data["DiffError " + maxerrors.iloc[x]][maxerrors.index.values[x]] > threshold:
#                     setHasChanged =True
#                     data[maxerrors.iloc[x]][maxerrors.index.values[x]] = nan
#                      
#         # cleanup 
#         self.processedData= data[frames]
        setHasChanged=True
        return setHasChanged
     

    # TODO: It seems that the garbage collector has a problem with our structure
    # the memory is never release even though we delete all structures
    def __del__(self):
        del self.originalData
        del self.processedData
