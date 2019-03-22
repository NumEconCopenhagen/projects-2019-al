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
#Here we will clean all the data


#Here we import the CO2 database from OECD
df = pdr.DataReader("AIR_GHG","oecd")

#If we look at the data, we can se that it has the dimensions 7 rows X 8460 columns. This is clearly wrong. I have tried to transpose it, but it only fucks it up more
#The main problem is that i cannot access the "Coutry" - what i have done is to import a list of the countries manually from OECD, and used it to for-loop over
countries = ["Australia","Austria","Belgium","Canada","Chile","Czech Republic","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Iceland",	
    "Ireland","Israel","Italy","Japan","Korea","Latvia","Lithuania","Luxembourg","Mexico","Netherlands","New Zealand","Norway","Poland","Portugal","Slovak Republic",
    "Slovenia","Spain","Sweden","Switzerland","Turkey","United Kingdom","United States","OECD - Europe","OECD - Total","Argentina","Brazil","China (People's Republic of)",
    "Colombia","Costa Rica","India","Indonesia","Russia","South Africa"]

#I make a dataframe of with the country names, years and space for co2 emissions
data = []
for c in countries:
    for y in df.index.values:
        data.append({"country" : c,"year": y})

data = pd.DataFrame(data)
co2 = []
data = data.append({"co2_omission" : co2},ignore_index=True)
data.drop(data.tail(1).index,inplace=True)
data.set_index(data["year"])

#i want to add the co2 emissions, but it is rather hard for me. 
# they can be acessed via: df["Australia"]["Greenhouse gases"]["Total  emissions including LULUCF"].iloc[[0,1,2,3,4,5,6]]
####     NOT DONE!#####
# x = []
# for c in data["country"]:
#     for i in df[c]["Greenhouse gases"]["Total  emissions including LULUCF"].index.values:
#         x.append({"country" : c, "co2_emissions": df[c]["Greenhouse gases"]["Total  emissions including LULUCF"][i]})  

# x = pd.DataFrame(x)
# print(x)

#Here we import average income per capita data
data_wages= pd.read_csv("oecdwages.csv")
#drop column that we do not need
drop_these= ["INDICATOR","FREQUENCY","MEASURE","SUBJECT", "Flag Codes"]
copy = data_wages.drop(drop_these, axis=1, inplace=False)
copy.rename(columns = {'LOCATION':'Country', 'Value' : 'Average Wage', 'TIME' : 'Year'}, inplace=True)
copy.head(10)
copy.loc[copy.Country == 'AUS']
