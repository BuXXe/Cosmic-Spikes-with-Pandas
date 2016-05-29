'''
Created on 26.05.2016

@author: BuXXe
'''

# FUTURE manual picker 
#res.figure.canvas.mpl_connect('pick_event', self.onpick3)
#res.figure.canvas.mpl_connect('key_release_event', self.onkeyhand)

import matplotlib.pyplot as plt   
import pandas as pd
import numpy as np
from numpy import  nan
class manualUnspiker(object):
    

        
        

    def onkeyhand(self,event):
            
            print "test"
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

                    
       
    def onpick3(self,event):
            print event.ind
            print "test"
            ind = event.ind
    
            xval = self.originalData[event.artist.get_label()].iloc[ind[0]]
            yval = self.originalData.index.values[ind[0]]
    
            circle1=plt.Circle((yval,xval),5,color='r')
            
            self.toDelete.append((event.artist.get_label(),ind[0],circle1))
            
            event.artist.axes.add_artist(circle1)
            plt.draw()
            
            
    def __init__(self, data):
        self.toDelete=[]
        # history and parameter history stuff
        

        self.res = data.processedData.plot(title="MANUAL UNSPIKER\n"+data.filename,legend  = False,picker=2)
        self.res.figure.canvas.mpl_connect('pick_event', self.onpick3)
        self.res.figure.canvas.mpl_connect('key_release_event', self.onkeyhand)
        
        print self.res
        print self.res.figure
        print self.res.figure.canvas