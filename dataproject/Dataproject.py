import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets

## Data import and cleaning
# a. Import of enviromental data form the OECD statistics bank API
df = pdr.DataReader("AIR_GHG","oecd")
df.head()

# b. Import of locally placed OECD data on wages
df_wages= pd.read_csv("oecdwages.csv")
print("This is the first 5 rows of the wages dataset")
df_wages.head()

# a. The eviromental data is multi-indexed. Therefore we rearrange the index of the dataset
df.reset_index()
dir(df.index)
df.columns = [' '.join(col).strip() for col in df.columns.values]

# b. In this section, we define a dictionary with all the countries and the countrycodes for the OECD countries
countries = ["Australia","Austria","Belgium","Canada","Chile","Czech Republic","Denmark","Estonia","Finland","France",
             "Germany","Greece","Hungary","Iceland","Ireland","Israel","Italy","Japan","Korea","Latvia","Lithuania",
             "Luxembourg","Mexico","Netherlands","New Zealand","Norway","Poland","Portugal","Slovak Republic",
             "Slovenia","Spain","Sweden","Switzerland","United Kingdom","United States"]
countrycode = ["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU","GRC", "HUN", "ISL", 
               "IRL", "ISR", "ITA", "JPN", "KOR", "LVA", "LTU", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT",
               "SVK", "SVN", "SWE", "ESP", "CHE", "GBR", "USA"]

ccc = dict(zip(countries,countrycode))


# c. We make a tidy dataset, by making a row for each country in each year, and add the variable "Greenhouse gases..." 
    #to this new data set
    # c.i.  I initiate an empty list for the dataset and set a counter to 0
x = []
i = 0
    #c.ii. Iniate the for-loop that adds the rows to the dataset
for c in countries:
    for y in df.index.values : 
        x.append({"country" : c, "countrycode" : ccc[c],"emissions_GHG" : df[c+" "+"Greenhouse gases Total  emissions excluding LULUCF"][i]})
        i = i + 1 
        if i > 6 :
            i = 0
    # c.iii. Examening the new dataset  
df_env = pd.DataFrame(x)
df_env.head()

# a. We define the variables that we do not need in our analysis, and drop them
drop_these= ["INDICATOR","FREQUENCY","MEASURE","SUBJECT", "Flag Codes"]
df_wages = df_wages.drop(drop_these, axis=1, inplace=False)

# b. We change the name of some of the variables
df_wages.rename(columns = {'LOCATION':'countrycode', 'Value' : 'average wage', 'TIME' : 'year'}, inplace=True)


## Mergin data sets

# a. We defne the two datasets, and reset their index
left = df_wages.sort_values("countrycode")
left = left.reset_index()
rigth = df_env.sort_values("countrycode")
rigth = rigth.reset_index()

# b. We merge the two datasets with a left merge
data_all = left.merge(rigth,left_index=True,right_index=True)
data_all.head()

# a. This for-loop test whether or not the data has been merge correctly 
for i in data_all.index.values : 
    # a.i. This statement checks if all the rows have the same countrycode in the two countrycode variables
    if data_all["countrycode_x"][i]==data_all["countrycode_y"][i] :
        if i == data_all.index.values[-1] : 
            print("No mistakes in the mergin process")
    else :  
        print("mistake in "+data_all["country"][i])


# a. This section, drops the extra contrycode variable
drop_these= ["index_x","index_y","countrycode_y"]
data_all = data_all.drop(drop_these, axis=1, inplace=False)

data_all.rename(columns ={"countrycode_x":"countrycode"},inplace=True)

# b. Then we sort the dataset by countrycode and year, afterwards we reset the index
data_all = data_all.sort_values(by=["countrycode","year"])
data_all = data_all.reset_index(drop=True)
print(data_all.head())
print(data_all.tail())

## Creating new variables

# a. We use the apply method, and a discret function to make two new variables for percentage change
data_all['d_GHG'] = data_all.groupby('countrycode')['emissions_GHG'].apply(lambda x: x.pct_change())*100
data_all['d_aw'] = data_all.groupby('countrycode')['average wage'].apply(lambda x: x.pct_change())*100

# b. inspect the new data - it should contain a NaN value for each country in the year 2010
data_all.head()

# a. we create an insect both the mean an median of all of the OECD countries change in greenhouse gas emissions
GHG_change = data_all.groupby("year").d_GHG.mean()
print("The mean of change in greenhouse gas emission, in the OECD each",GHG_change)
print("The median change in greenhouse gas emissions in the OECD each", data_all.groupby("year").d_GHG.median())


# a. we create an insect both the mean an median of all of the OECD countries change in average wages
AW_change = data_all.groupby("year").d_aw.mean()
print("The mean of change in average wages, in the OECD each", AW_change)
print("The median of change in average wages, in the OECD each",data_all.groupby("year").d_aw.median())

## New functions

def information(a,b = 0,variable = True):
    """This function takes up to three arguments, the country code, the year (optional) and return the name of the country the average wage and the total emissions of GHG.
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

def translate(code = True, countrycode = True):
    """This function take one argument. By default it is the code of the country and return the name of the country. There is the possibility to precise if 
    the input is a code or country. It it's a country it will return the code.
    """
    i = 0
    if countrycode == True :
        c = str(data_all[data_all["countrycode"]==code]["country"].unique())
        c = c.replace("['","")
        c = c.replace("']","")
        return(c)
    elif countrycode == False :
        c = str(data_all[data_all["country"]==code]["countrycode"].unique())
        c = c.replace("['","")
        c = c.replace("']","")
        return(c)
    else : 
        return("check you'r spelling")

## Visual analysis
plt.plot(GHG_change,color="g")
plt.plot(AW_change,color="b")
plt.xlabel("Year")
plt.ylabel("Percentage change")
plt.legend(["Greenhouse gas emissions","Average wage"])
plt.axhline(y=0,color="r",linestyle="dashed")
plt.show()

plt.clf
av_w_c= data_all.groupby("countrycode")["average wage"].mean().sort_values()
av_w_c.plot.bar()
plt.xlabel("countrycode")
plt.ylabel("average wage in USD")
plt.show()


plt.clf
av_e_c= data_all.groupby("country")["emissions_GHG"].mean()
plt.ylabel("greenhouse gas emissions (thousands of metric tons)")
plt.xlabel("countrycode")
av_e_c.plot.bar()
plt.show()


plt.clf
#chart plot
united_state_d = information('USA', 2016)
country1 = float(united_state_d.loc[:,"emissions_GHG"])
japan_d = information('JPN', 2016)
country2 = float(japan_d.loc[:,"emissions_GHG"])
germany_d = information("DEU", 2016)
country3 = float(germany_d.loc[:,"emissions_GHG"])
others_d = data_all[(~data_all["countrycode"].isin(["USA","JAP","DEU"]))]
others_d = others_d[others_d['year'] == 2016]["emissions_GHG"]
others = float(np.nansum(others_d))

chart = [country1, country2, country3, others]
labels = 'United State', 'Japan', 'Germany', 'Others'
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
exp = [0.15 , 0, 0, 0]

fig1, chartg = plt.subplots()
chartg.pie(chart, explode=exp , labels=labels, colors=colors, autopct='%1.1f%%',  shadow=True, startangle=90)

chartg.axis('equal')
plt.show()


plt.clf
def get_con(Country = "Australia"):
    print("Country: "+ Country)
    print("Mean of Greenhouse gas emissions:" , round(information(translate(Country,countrycode=False))["emissions_GHG"].mean(),2))  
    print("Mean of average wages:" , round(information(translate(Country,countrycode=False))["average wage"].mean(),2))

    fig, ax = plt.subplots()
    fig.canvas.draw()
    plt.plot(data_all[data_all["country"]==Country]["d_GHG"],color="g")
    plt.plot(data_all[data_all["country"]==Country]["d_aw"],color="b")
    plt.xlabel("Year")
    plt.ylabel("Percentage change")
    labels= ["2010","2011","2012","2013","2014","2015","2016"]
    ax.set_xticklabels(labels) 
    plt.legend(["Greenhouse gas emissions","Average wage"])
    plt.axhline(y=0,color="r",linestyle="dashed")
    plt.show()

    return 

widgets.interact(get_con,Country=data_all["country"].unique())