#This is the main file, here we do most things
#Always use git change before writing anything!

#to upload changes: 
#1) git commit 
#2) git sync

import pip 
import pandas as pd
#if you don't have pandas_datareader installed write: "pip install pandas_datareader" without quotes in the terminal
import pandas_datareader as pdr
import numpy as np


#import of data
#Here we import the CO2 database from OECD
df = pdr.DataReader("AIR_GHG","oecd")
type(df)
#something has gone wrong here. the data is here but it is a mess :(