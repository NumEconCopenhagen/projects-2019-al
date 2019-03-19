#This is the main file, here we do most things
#Always use git change before writing anything!

#to upload changes: 
#1) git commit 
#2) git sync

#importing packeges
import pip 
import pandas as pd
#if you don't have pandas_datareader installed write: "pip install pandas_datareader" without quotes in the terminal
import pandas_datareader as pdr
import numpy as np

#importing our other sheets
import Functions
import clean_sheet

