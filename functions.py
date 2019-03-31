def translate(code = True, countrycode = True) :
    """This function take one argument. By default it is the code of the country and return the name of the country. There is the possibility to precise if 
    the input is a code or country. It it's a country it will return the code."""
    i = 0
    if countrycode == True :
        return(data_all[data_all["countrycode"]==code]["country"][2010])
    elif countrycode == False :
        return(data_all[data_all["country"]==code]["countrycode"][2010])
    else : 
        return("check you'r spelling")


def information(a,b = 0,variable = True) :
    """ This function take three arguments, the country code, the year (optional the variable) and return the name of the country the average wage and the total emissions of GHG.
    The country code is the first column in our data base, three letters which represent the country. If the year is not define it will return for all years. If the variable is define
    it will return only this variable"""
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