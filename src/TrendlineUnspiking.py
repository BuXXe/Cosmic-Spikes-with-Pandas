'''
Created on 23.12.2015

@author: Christopher Skerra, Dennis Skerra
@contact: Skerra.Christopher@yahoo.de - https://github.com/BuXXe/Cosmic-Spikes-with-Pandas
@license: Licensed under CC BY-NC-SA 4.0 - https://creativecommons.org/licenses/by-nc-sa/4.0/ 

'''

import matplotlib.pyplot as plt   
import pandas as pd
import numpy as np
from numpy import  nan
from _sqlite3 import Row

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
         
        for frame in data.processedData.columns.values:
            # compute trendline
            x = data.processedData.index.values
            y = data.processedData.interpolate()[frame].as_matrix()
    
            z = np.polyfit(x, y, trendlinedegree)
            p = np.poly1d(z)
    
            orig = data.processedData.interpolate()[frame]-p(x)
            trendlinecalcs.append(orig)
        
        dataft = pd.concat(trendlinecalcs, axis=1)
    else: 
        dataft = data.processedData.copy().interpolate()
    
    # ensure only positive values
    dataft = dataft + abs(dataft.min().min()) + 5.0

    circles = []
    
    # walk over each row 
    for x in xrange(0,len(dataft.index)):

        row = dataft.iloc[x].sort_values( ascending=False)
        
        # get mean distance (all points: distance a point to its next neighbour)
        meandist = []
        # ignore the first (maximum) entry and create mean only with the rest
        # this helps improving the sensitivity of the error factor 
        for ind,ent in enumerate(row[:-1]):
            if ind == 0:
                continue
            # distance to next neighbour point
            meandist.append(ent-row[ind+1])
               
        meandis = sum(meandist)/float(len(meandist)-1)    

        # now we check only those points lying over the mean of all points
        try:
            distances = []  
            # filtered distances
            for ind,ent in enumerate(row[row > row.mean()]):
                distances.append(ent-row[ind+1])

            
            # check if this frame has a valid entry in the non interpolated set
            # otherwise use next distance entry or, if no more distance value, continue with next x value
            
            # get frame of the max value
            for dis in distances:
                fram = row.index.values[distances.index(max(distances))]
                
                if pd.isnull(data.processedData[fram][dataft.index.values[x]]):
                    # blacklist this entry
                    distances[distances.index(max(distances))] = 0
                else:
                    # break out of for loop if we found a valid entry
                    break
           
            if max(distances) > float(errorfactor)*meandis  and max(distances)>float(minmeandist):
                yval = data.processedData.interpolate()[fram][dataft.index.values[x]]
                xval = dataft.index.values[x]
                
                if debug:
                    circles.append((yval,xval))
                else:
                    data.processedData[fram][dataft.index.values[x]] = nan
        except:
            print "ERROR during Trendline Distances calcs"
            pass
                
    # if dryrun, plot processed set with points to be removed marked as circles
    if debug:
        data.processedData.interpolate().plot(title=data.filename,legend  = False) 
        for c in circles:    
            circle1=plt.Circle((c[1],c[0]),6,color='r')
            plt.gca().add_artist(circle1)
        plt.draw()
    return    
