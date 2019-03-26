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
import matplotlib.pyplot as plt

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
    "Ireland","Israel","Italy","Japan","Korea","Latvia","Lithuania","Luxembourg","Mexico","Netherlands","New Zealand","Norway","Poland","Portugal","Slovak Republic",
    "Slovenia","Spain","Sweden","Switzerland","United Kingdom","United States"]	
countrycode = ["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU","GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", 
    "KOR", "LVA", "LTU", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN", "SWE", "ESP", "CHE", "GBR", "USA"]
ccc = dict(zip(countries,countrycode))
# I initiate an empty list for the dataset and set the counter to 0
x = []
i = 0
for c in countries:
    for y in df.index.values : 
        x.append({"country" : c, "countrycode" : ccc[c],"total emissions of GHG" : df[c+" "+"Greenhouse gases Total  emissions excluding LULUCF"][i]})
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
copy.rename(columns = {'LOCATION':'countrycode', 'Value' : 'average wage', 'TIME' : 'year'}, inplace=True)
c = copy["countrycode"].unique()


#here i reset the index of the two variables, and sort by the common variable (countrycode). Then i merge by index position 
left = copy.sort_values("countrycode")
left = left.reset_index()
rigth = df_env.sort_values("countrycode")
rigth = rigth.reset_index()
data_all = left.merge(rigth,left_index=True,right_index=True)

#this for loop test if all the values of the countrycodes are the same in the same row
for i in data_all.index.values : 
    if data_all["countrycode_x"][i]==data_all["countrycode_y"][i] :
        if i == data_all.index.values[-1] : 
            print("Done")
    else :  
        print("mistake in "+data_all["country"][i])

#I then drop a few columns that are not needed
drops = ["index_x","index_y","countrycode_y"]
data_all.drop(drops,axis=1,inplace=True)
data_all.rename(columns ={"countrycode_x":"countrycode"},inplace=True)
#data_all.set_index("year",inplace=True)


#i make to lagged variables and take the log of them (this is almost like use percentage change in GHG and average wage)
data_all["d_GHG"] = data_all.groupby("countrycode")["total emissions of GHG"].diff(periods=1)
data_all["d_aw"] = data_all.groupby("countrycode")["average wage"].diff(periods=1)
data_all["ld_GHG"] = np.log(data_all.groupby("countrycode")["total emissions of GHG"]).diff(periods=1)






#fooling around with some plots

plt.scatter(data_all["year"], data_all["total emissions of GHG"] , s=data_all["average wage"]/50 , alpha=0.6, edgecolors="white", linewidth=2)
plt.show()
