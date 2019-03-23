#This is the main file, here we do most things
#Always use git change before writing anything!

#to upload changes: 
#1) git commit 
#2) git sync

#importing packeges
import pip 
import pandas as pd
import pandas_datareader as pdr
import numpy as np

#importing our other sheets
#Here we will clean all the data


#Here we import the CO2 database from OECD
df = pdr.DataReader("AIR_GHG","oecd")

#the data is in "multi-index form", these codes turns it into a more common non-hieracical structure
df.reset_index()
dir(df.index)
df.columns = [' '.join(col).strip() for col in df.columns.values]

#The countries are not "availeble to grap" so i have manually made a list using excel
countries = ["Australia","Austria","Belgium","Canada","Chile","Czech Republic","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Iceland",	
    "Ireland","Israel","Italy","Japan","Korea","LatPvia","Lithuania","Luxembourg","Mexico","Netherlands","New Zealand","Norway","Poland","Portugal","Slovak Republic",
    "Slovenia","Spain","Sweden","Switzerland","Turkey","United Kingdom","United States","OECD - Europe","OECD - Total","Argentina","Brazil","China (People's Republic of)",
    "Colombia","Costa Rica","India","Indonesia","Russia","South Africa"]

# I initiate an empty list for the dataset and set the counter to 0
x = []
i = 0
for c in countries:
    for y in df.index.values : 
        x.append({"country" : c,"year": y,"Total emissions of GHG" : df[c+" "+"Greenhouse gases Total  emissions excluding LULUCF"][i]})
        i = i + 1 
        if i > 6 :
            i = 0

#In the for-loop i make a row for each country for each year, and insert a country, a year and the corrosponding of emissions of GHG (Green House Gases)
df_env = pd.DataFrame(x)
print(df_env)

#Here we import average income per capita data
data_wages= pd.read_csv("oecdwages.csv")
#drop column that we do not need
drop_these= ["INDICATOR","FREQUENCY","MEASURE","SUBJECT", "Flag Codes"]
copy = data_wages.drop(drop_these, axis=1, inplace=False)
copy.rename(columns = {'LOCATION':'Country', 'Value' : 'Average Wage', 'TIME' : 'Year'}, inplace=True)
copy.head(10)
copy.loc[copy.Country == 'AUS']
c = copy["Country"].unique()
print(c)
s= df_env["country"].unique()
print(s)
len(s)
len(c)
