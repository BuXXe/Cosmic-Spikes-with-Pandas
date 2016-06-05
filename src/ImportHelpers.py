'''
Created on 23.12.2015

@author: Christopher Skerra, Dennis Skerra
@contact: Skerra.Christopher@yahoo.de - https://github.com/BuXXe/Cosmic-Spikes-with-Pandas
@license: Licensed under CC BY-NC-SA 4.0 - https://creativecommons.org/licenses/by-nc-sa/4.0/

'''

import pandas as pd

# We want to import an already processed set
# we have to ensure that it has the same Dataframe format as the Txt importer
# meaning: columns may only be x, Frame1, Frame2.....
def convertCsvToPandaFrame(inputf):
    df = pd.read_csv(inputf,sep=";")
    for entry in df.columns.values:
        if entry is not "x" and "Frame" not in entry:
            df.drop(entry, axis=1,inplace=True)
    
    df.sort_values("x",inplace=True)
    df.set_index("x", inplace=True)
    return df
    
# Transforms spectroscopy format: FrameX\n64.624;305.000...\n\nFrameX+1 to Pandas DataFrame
# ASSUMPTION: we always have the same x entries for all Frames!
def convertTxtToPandaFrame(inputf):
    with open(inputf) as f:
        content = f.readlines()
    
    parsedObject = {}    
    columns = ["x"]
    wholesetlistings = {}  
    
    # each line can be:
    # x;y pair
    # FrameX
    # empty line  
    # Create a datastructure with:
    # all columns (Frame1,Frame2...) in columns
    # a dictionary of format key = x value = list of y in wholesetlistings
    for line2 in content:
        line = line2.replace("\n","")
        # check if valid format
        if not "Frame" in line and not ";" in line and len(line)>1:
            raise Exception("Format problem")
        if "Frame" in line:
            columns.append(line)
            continue
        if ";" in line:
            # check if valid format
            if len(line.split(";")) != 2:
                raise Exception("wrong format")
            # create a new key and list entry in wholesetlistings
            if line.split(";")[0] not in wholesetlistings:
                wholesetlistings[line.split(";")[0]]=[]
            # append y value for a given x value    
            wholesetlistings[line.split(";")[0]].append(float(line.split(";")[1]))
    
    # check if we dont have only x column
    if len(columns) <2:
        raise Exception("No Frames in set found")
    
    # create columns
    for col in columns:
        parsedObject[col]=[]     
    
    # go through each x value
    for entry in wholesetlistings:
        parsedObject["x"].append(float(entry))
        # append each y val for the given x val
        for g,i in enumerate(columns[1:]):
            parsedObject[i].append(float(wholesetlistings[entry][g]))
        
    df = pd.DataFrame(parsedObject)
    df.sort_values("x",inplace=True)
    df.set_index("x", inplace=True)

    return df


