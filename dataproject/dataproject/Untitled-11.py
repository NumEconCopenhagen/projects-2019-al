#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'dataproject'))
	print(os.getcwd())
except:
	pass

#%%
import pip 
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets


#%%



#%%
df = pdr.DataReader("AIR_GHG","oecd")
data_wages= pd.read_csv("oecdwages.csv")
df.head()
data_wages.head()


#%%

df.reset_index()
dir(df.index)
df.columns = [' '.join(col).strip() for col in df.columns.values]


#%%
countries = ["Australia","Austria","Belgium","Canada","Chile","Czech Republic","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Iceland",	
    "Ireland","Israel","Italy","Japan","Korea","Latvia","Lithuania","Luxembourg","Mexico","Netherlands","New Zealand","Norway","Poland","Portugal","Slovak Republic",
    "Slovenia","Spain","Sweden","Switzerland","United Kingdom","United States"]	
countrycode = ["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU","GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", 
    "KOR", "LVA", "LTU", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN", "SWE", "ESP", "CHE", "GBR", "USA"]
ccc = dict(zip(countries,countrycode))
# I initiate an empty list for the dataset and set the counter to 0


#%%
x = []
i = 0
for c in countries:
    for y in df.index.values : 
        x.append({"country" : c, "countrycode" : ccc[c],"emissions_GHG" : df[c+" "+"Greenhouse gases Total  emissions excluding LULUCF"][i]})
        i = i + 1 
        if i > 6 :
            i = 0

#In the for-loop i make a row for each country for each year, and insert a country, a year and the corrosponding of emissions of GHG (Green House Gases)
df_env = pd.DataFrame(x)
df_env.head()


#%%
drop_these= ["INDICATOR","FREQUENCY","MEASURE","SUBJECT", "Flag Codes"]
copy = data_wages.drop(drop_these, axis=1, inplace=False)
copy.rename(columns = {'LOCATION':'countrycode', 'Value' : 'average wage', 'TIME' : 'year'}, inplace=True)
c = copy["countrycode"].unique()


#%%
left = copy.sort_values("countrycode")
left = left.reset_index()
rigth = df_env.sort_values("countrycode")
rigth = rigth.reset_index()
data_all = left.merge(rigth,left_index=True,right_index=True)


#%%
for i in data_all.index.values : 
    if data_all["countrycode_x"][i]==data_all["countrycode_y"][i] :
        if i == data_all.index.values[-1] : 
            print("Done")
    else :  
        print("mistake in "+data_all["country"][i])


#%%
data_all.rename(columns ={"countrycode_x":"countrycode"},inplace=True)
data_all = data_all.sort_values(by=["countrycode","year"])
data_all = data_all.reset_index(drop=True)
data_all.head()


#%%
data_all['d_GHG'] = data_all.groupby('countrycode')['emissions_GHG'].apply(lambda x: x.pct_change())*100
data_all['d_aw'] = data_all.groupby('countrycode')['average wage'].apply(lambda x: x.pct_change())*100

GHG_change = data_all.groupby("year").d_GHG.mean()
print(GHG_change)
AW_change = data_all.groupby("year").d_aw.mean()
print(AW_change)
data_all.head()


#%%
def information(a,b = 0,variable = True):
    """This function take three arguments, the country code, the year (optional the variable) and return the name of the country the average wage and the total emissions of GHG.
    The country code is the first column in our data base, three letters which represent the country. If the year is not define it will return for all years. If the variable is define
    it will return only this variable
    """
    x = data_all[data_all["countrycode"] == a]
#define year and co2
    if b != 0 and variable == 'co2':
        d= x[data_all["year"] == b]
        f = d.loc[:, ["year", "country", "emissions_GHG"]]
        return f
#define year and wage
    elif b != 0 and variable == 'wage':
        d= x[data_all["year"] == b]
        g = d.loc[:, ["year", "country", "average wage"]]
        return g
 #define only co2
    elif b == 0 and variable == 'co2':
        d= x[data_all["year"] == b]
        return x.loc[:, ["year", "country", "emissions_GHG"]]
#define only wage
    elif b == 0 and variable == 'wage':
        g = x.loc[:, ["year", "country", "average wage"]]
        return x.loc[:, ["year", "country", "average wage"]]
#define only the year
    elif b != 0 : 
        h = x[data_all["year"] == b]
        return h.loc[:, ["year", "country", "average wage", "emissions_GHG"]]
#nothing define
    else :
        return x.loc[:, ["year", "country", "average wage", "emissions_GHG"]]


#%%
def translate(code = True, countrycode = True):
    """This function take one argument. By default it is the code of the country and return the name of the country. There is the possibility to precise if 
    the input is a code or country. It it's a country it will return the code.
    """
    i = 0
    if countrycode == True :
        return(data_all[data_all["countrycode"]==code]["country"][2010])
    elif countrycode == False :
        return(data_all[data_all["country"]==code]["countrycode"][2010])
    else : 
        return("check you'r spelling")


#%%
#plot 1 - percentage change in co2 and wages over time 
plt.plot(GHG_change,color="g")
plt.plot(AW_change,color="b")
plt.xlabel("Year")
plt.ylabel("Percentage change")
plt.legend(["Greenhouse gas emissions","Average wage"])
plt.axhline(y=0,color="r",linestyle="dashed")
plt.show()


#%%
av_w_c= data_all.groupby("countrycode")["average wage"].mean().sort_values()
av_w_c.plot.bar()
plt.xlabel("countrycode")
plt.ylabel("average wage in USD")
plt.show()


#%%
av_e_c= data_all.groupby("country")["emissions_GHG"].mean()
plt.ylabel("greenhouse gas emissions (thousands of metric tons)")
plt.xlabel("countrycode")
av_e_c.plot.bar()
plt.show()


#%%
def get_con(x="Australia"):
    print("Country: "+x)
    print("Mean of Greenhouse gas emissions:" , round(information(translate(x,countrycode=False))["emissions_GHG"].mean(),2))  
    print("Mean of average wages:" , round(information(translate(x,countrycode=False))["average wage"].mean(),2))

    plt.plot(data_all[data_all["country"]==x]["d_GHG"],color="g")
    plt.plot(data_all[data_all["country"]==x]["d_aw"],color="b")
    plt.xlabel("Year")
    plt.ylabel("Percentage change")
    plt.legend(["Greenhouse gas emissions","Average wage"])
    plt.axhline(y=0,color="r",linestyle="dashed")
    plt.show()

    return 

widgets.interact(get_con,x=data_all["country"].unique())


#%%



#%%



#%%



