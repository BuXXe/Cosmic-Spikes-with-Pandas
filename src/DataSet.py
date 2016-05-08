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
        self.history = originalData
        self.filename = filename
        self.processedData = None
        
        # applied parameter history as list of parameters
        self.paramterHistory=[]
        
        # parameters: TrendlineCorrection: T/F, Trendline Degree, Min Distance from mean, Distance Error Factor  
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
            TRENDLINESUBSTRACTION= True
            axi =  plt.gca().axis()
            plt.cla()
            trendlinecalcs = []
            for framenr in xrange(1,len(self.originalData.columns)+1):
                print framenr 
                # compute trendline
                x = self.originalData.index.values
                y = self.originalData["Frame "+str(framenr)].as_matrix()

                z = np.polyfit(x, y, 90)
                p = np.poly1d(z)

#                originalFrame.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1)

                orig = self.originalData["Frame "+str(framenr)]-p(x)
                trendlinecalcs.append(orig)
                orig.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1)
                
                #plt.plot(x,p(x),"r-")
            
            plt.axis(axi)
            
            dataft= pd.concat(trendlinecalcs, axis=1)
            
            dataft = dataft + abs(dataft.min().min()) + 5.0
            
            if not TRENDLINESUBSTRACTION:
                dataft=self.originalData
            
            plt.cla()
            dataft.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1)
            
            
            frames = dataft.columns.values
            circles = []
            
            for x in xrange(0,len(dataft.index)):
                # series of frames
                row = dataft.iloc[x].sort_values( ascending=False)
                
                # get mean distance
                meandist = []
                for ind,ent in enumerate(row[:-1]):
                    # distance to each point
                    meandist.append(ent-row[ind+1])
                    
                meandis = sum(meandist)/float(len(meandist))    
                
                try:
                    distances = []  
                    # filtered distances
                    for ind,ent in enumerate(row[row > row.mean()]):
                        distances.append(ent-row[ind+1])

                    # get frame of the max value
                    fram = row.index.values[distances.index(max(distances))]
                    
                    if max(distances) > 3*meandis  and max(distances)>100.0:

                        xval = self.originalData[fram][dataft.index.values[x]]
                        yval = dataft.index.values[x]
                        
                        circles.append((xval,yval))
                        #self.originalData[fram][dataft.index.values[x]] = nan

                except:
                    pass        
            plt.cla()
            self.originalData.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1) 
            for c in circles:
                
                circle1=plt.Circle((c[1],c[0]),15,color='r')
                        
                plt.gca().add_artist(circle1)
            plt.draw()    
   
    def onpick3(self,event):
        ind = event.ind

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
    


    # TODO: It seems that the garbage collector has a problem with our structure
    # the memory is never release even though we delete all structures
    def __del__(self):
        del self.originalData
        del self.processedData
