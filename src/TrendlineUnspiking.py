'''
Created on 26.05.2016

@author: BuXXe
'''


# FUTURE manual picker 
#res.figure.canvas.mpl_connect('pick_event', self.onpick3)
#res.figure.canvas.mpl_connect('key_release_event', self.onkeyhand)


# EACH Library has do to this:
# deliver a debug function for dry runs
# deliver a function for unspiking given sets

# TODO: future perhaps use a params set instead of single  variables
#def unspike(params):
    



def unspike(useTrendline = True, trendlinedegree  = 90, errorfactor=3, minmeandist=100,debug=False):
    
    
    
    return    



import matplotlib.pyplot as plt    
    

    
    
    


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