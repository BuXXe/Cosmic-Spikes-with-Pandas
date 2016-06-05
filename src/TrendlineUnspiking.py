'''
Created on 23.12.2015

@author: Christopher Skerra, Dennis Skerra
@contact: Skerra.Christopher@yahoo.de

Licensed under CC BY-NC-SA 4.0
https://creativecommons.org/licenses/by-nc-sa/4.0/

'''

import matplotlib.pyplot as plt   
import pandas as pd
import numpy as np
from numpy import  nan

# TODO: future perhaps use a params set instead of single  variables
# def unspike(params):
    
# INFO: in the future, there should be some kind of interface driven system to define unspiking methods
# each method should provide a dryrun and a normal run functionality

# debug defines if we have a dryrun or a real run
def unspike(data, useTrendline = True, trendlinedegree  = 90, errorfactor=3, minmeandist=100,debug=False):

    # if not dryrun, update histories
    if not debug:
        data.history.append(data.processedData.copy())
        data.parameterHistory.append(("Trendline", useTrendline,trendlinedegree,errorfactor,minmeandist))

    # calculate the trendline and subtract it from the frame 
    if useTrendline:
        trendlinecalcs = []
        # TODO: take real frame numbers!!!! WARNING!!!
        for framenr in xrange(1,len(data.processedData.columns)+1):
            # compute trendline
            x = data.processedData.index.values
            y = data.processedData.interpolate()["Frame "+str(framenr)].as_matrix()
    
            z = np.polyfit(x, y, trendlinedegree)
            p = np.poly1d(z)
    
    #                originalFrame.plot(title=self.filename,ax=plt.gca(),legend  = False,picker=1)
    
            orig = data.processedData.interpolate()["Frame "+str(framenr)]-p(x)
            trendlinecalcs.append(orig)
            #orig.plot(title=data.filename,ax=plt.gca(),legend  = False,picker=1)
            
            #plt.plot(x,p(x),"r-")
        # get same zoomfactor as before 
        #plt.axis(axi)
        
        dataft = pd.concat(trendlinecalcs, axis=1)
    

    else: 
        dataft = data.processedData.copy()
    
    # ensure only positive values
    dataft = dataft + abs(dataft.min().min()) + 5.0

    
    #if not TRENDLINESUBSTRACTION:
    #    dataft=data
    
    #plt.cla()
    #dataft.plot(title=data.filename,ax=plt.gca(),legend  = False,picker=1)
    
    # TRENDLINE STUFF END
    
    #frames = dataft.columns.values
    circles = []
    
    # walk over each row 
    for x in xrange(0,len(dataft.index)):
        # series of frames
        # get row and sort values
        row = dataft.iloc[x].sort_values( ascending=False)
        
        # get mean distance (all points: distance a point to its next neighbour)
        meandist = []
        for ind,ent in enumerate(row[:-1]):
            # distance to next neighbour point
            meandist.append(ent-row[ind+1])   
        meandis = sum(meandist)/float(len(meandist))    
        
        
        # now we check only those points lying over the mean of all points
        try:
            distances = []  
            # filtered distances
            for ind,ent in enumerate(row[row > row.mean()]):
                distances.append(ent-row[ind+1])

            # get frame of the max value
            fram = row.index.values[distances.index(max(distances))]
            
#             if dataft.index[x] > 1150 and dataft.index[x] < 1152: 
#                 print dataft.index[x]," ",distances 
            
            if max(distances) > float(errorfactor)*meandis  and max(distances)>float(minmeandist):

                yval = data.processedData.interpolate()[fram][dataft.index.values[x]]
                xval = dataft.index.values[x]
                
                if debug:
                    circles.append((yval,xval))
                else:
                    data.processedData[fram][dataft.index.values[x]] = nan

        except:
            pass        
    
    # debug output with circles
    
    #plt.cla()
    if debug:
        data.processedData.interpolate().plot(title=data.filename,legend  = False) 
        for c in circles:    
            circle1=plt.Circle((c[1],c[0]),6,color='r')
            plt.gca().add_artist(circle1)
        plt.draw()
    
    return    



 
    

    
    
    


