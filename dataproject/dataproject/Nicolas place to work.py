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


#fooling around with some plots

plt.scatter(data_all["year"], data_all["total emissions of GHG"] , s=data_all["average wage"]/50 , alpha=0.6, edgecolors="white", linewidth=2)
plt.show()

### functions book :

#The translate function
def translate(code = True, country = True) :
    """This function take one argument. By default it is the code of the country and return the name of the country. There is the possibility to precise if 
    the input is a code or country. It it's a country it will return the code."""
    i = 0
    if country == True :
        for c in countrycode :
            if code != countrycode[i] and i < 34 :
                i = i + 1
            elif code == countrycode[i] :
                return countries[i]
            else :
                return "miss spelling of the code"
    else :
        for c in countries :
            if country != countries[i] and i < 34 :
                i = i + 1
            elif country == countries[i] :
                return countrycode[i]
            else :
                return "miss spelling of the country"

translate('USA')

#The information function
def information(a,b = 0,variable = True) :
    """ This function take two arguments, the country code and the year and return the name of the country the average wage and the total emissions of GHG.
    The country code is the first column in our data base, three letters which represent the country. If the year is not define it will return for all years."""
    x = data_all[data_all["countrycode"] == a]
#define year and co2
    if b != 0 and variable == 'co2':
        d= x[data_all["year"] == b]
        f = d.loc[:, ["year", "country", "total emissions of GHG"]]
        return f
#define year and wage
    elif b != 0 and variable == 'wage':
        d= x[data_all["year"] == b]
        g = d.loc[:, ["year", "country", "average wage"]]
        return g
 #define only co2
    elif b == 0 and variable == 'co2':
        d= x[data_all["year"] == b]
        return x.loc[:, ["year", "country", "total emissions of GHG"]]
#define only wage
    elif b == 0 and variable == 'wage':
        g = x.loc[:, ["year", "country", "average wage"]]
        return x.loc[:, ["year", "country", "average wage"]]
#define only the year
    elif b != 0 : 
        h = x[data_all["year"] == b]
        return h.loc[:, ["year", "country", "average wage", "total emissions of GHG"]]
#nothing define
    else :
        return x.loc[:, ["year", "country", "average wage", "total emissions of GHG"]]

information('FRA')
information('FRA', 2010)
information('AUS', 2010, 'co2')
information('AUS', 2010, 'wage')
information('AUS',variable = 'co2')
information('AUS', variable ='wage')
information (['AUS','FRA'], 2010)

#things to do : possibility to add several countries and several years and apply an error message