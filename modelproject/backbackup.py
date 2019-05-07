#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'projects-2019-al\modelproject'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # The Cournot Model
#%% [markdown]
# ### Imports:

#%%
import numpy as np
import scipy as sp
import sympy as sm
import matplotlib.pyplot as plt
import ipywidgets as widgets
import pylab

#We initiate our printing as nice equations, using the sympy package 
sm.init_printing(use_unicode=True)

#%% [markdown]
# ## Model Description
#%% [markdown]
# In the model of Cournot Competition, two firms compete for the amount they produce, by simulataneously setting quantities. 
# 
# **We use the following parameters:**
# 
# 1. q1 is the quantity produced by firm 1
# 2. q2 is the quantity produced by firm 2
# 3. c is the cost, which is equal for both firms 
# 4. a,b are parameters of the price functions of the firms
# 5. pi1 and pi2 are profits of firms 1 and 2 
# 
# **Preliminaries of the model:**
# 
# 1. Both firms produce a homogenous product
# 2. There is no collusion between the firms
# 3. Both firms have identical costs and the same price functions 
# 4. The firms are economically rational
# 
# **Prices evolve according to:**
# 
# p1 = (a-b*(q1+q2))
# 
# p2 = (a-b*(q1+q2))
# 
# **Profits are derived through:**
# 
# pi1 =(p1*q1-c*q1)
# 
# pi2 = (p2*q2-c*q2)
# 
# 
#%% [markdown]
# ## Solving the model:
#%% [markdown]
# First we define all symbols:

#%%
q1 = sm.symbols('q_1')
q2 = sm.symbols('q_2')
c = sm.symbols('c')
a = sm.symbols('a')
b = sm.symbols("b")
pi1 = sm.symbols('pi_1')
pi2 = sm.symbols('pi_2')

#%% [markdown]
# We use the price and profit equations, to then derive the first order conditions wrt. the quantity produced by the respective firm:

#%%
p1 = (a-b*(q1+q2))

p2 = (a-b*(q1+q2))

pi1 =(p1*q1-c*q1)

pi2 = (p2*q2-c*q2)


#%%
foc1=sm.diff(pi1,q1)
foc1


#%%
foc2=sm.diff(pi2,q2)
foc2

#%% [markdown]
# Setting first order conditions to 0 and solving for the respective firms produced quantitiy (q1 and q2), give us the optimal qunatities the two firms should produce, given the other firms output (reaction functions).

#%%
sol1= sm.solve(sm.Eq(foc1,0),q1)[0]
sol1


#%%
sol2= sm.solve(sm.Eq(foc2,0),q2)[0]
sol2

#%% [markdown]
# The Cournot equlibrium is achieved, when substituting one firm's reaction function into the other firm's reaction function. This equlibrium constitutes the optimal quantity that both firms should produce, given that the other firm is rational and is aiming to produce the profit maximizing amount. 
# 
# We first substitute q2 in firm 1's fist order condition:

#%%
sol1_subs = foc1.subs(q2,sol2)
sol1_subs

#%% [markdown]
# We then solve the equation for q1, to get the Cournot equilibrium, which is dependent on a,b and c. 

#%%
sol1_subs_solve = sm.solve(sm.Eq(sol1_subs,0),q1)
sol1_subs_solve

#%% [markdown]
# ## Visualizations

#%%
#Needs commenting and docstrnigs
def reaction(q_other, a=100, b=1, cost=1,print_it=False):
    quantity = (a-b*q_other - cost)/2*b
    
    if print_it:
        print("Given the other firm produces",q_other,"The firm will produce", quantity, sep=" ")
        return
    else:
        return quantity


#%%
#Needs commenting and docstrnigs

def reaction_plot(q_other, a=100, b=1, cost=1,scatter=True):
    quantity = reaction(x ,a, b, cost)
    
    #ax = plt.subplot()
    if scatter == True :
        quantity = reaction(q_other,a, b, cost)
        plt.scatter(quantity,q_other,label = "Firm 1's reaction curve")
        plt.scatter(q_other,quantity,label = "Firm 2's reaction curve")
    else : 
        plt.plot(quantity,q_other,label = "Firm 1's reaction curve")
        plt.plot(q_other,quantity,label = "Firm 2's reaction curve")
        
    plt.xlabel("Firm 1 quantity")
    plt.ylabel("Firm 2 quantity")
    plt.legend()
    plt.xlim(0,100)
    plt.ylim(0,100)

    plt.show()
    return 


#%%
#Needs commenting and docstrnigs

def optimal(a, b, cost, r=False):
    equilibrium = (a-cost)/3*b
    equilibrium = round(equilibrium,0)
    if r:
        return equilibrium
    else:
        print("The Cournot equilibrium, given that","a =",a,", b =",b,"and that cost =",cost,",","is:",equilibrium)

#%% [markdown]
# Using the reaction function, we can now calculate the quatity that firm 1 produces, given firm 2's quantity 

#%%
qslider = widgets.IntSlider(min=0,max=100,step=1,value=50)

widgets.interact(reaction,q_other = qslider,a=widgets.fixed(100),b=widgets.fixed(1),cost=widgets.fixed(1),print_it=widgets.fixed(True))

#%% [markdown]
# While this is interesting, theory tells us that we will always end in the Cournout equilibrium, given fixed costs and prices.  

#%%
print("The equilibrium we derived earlier as:")

sm.pprint(sol1_subs_solve,use_unicode=True)

print("Which given a = 100, b= 1 and cost = 1, is:",optimal(100,1,1))


#%%
a_slider = widgets.IntSlider(min=10,max=150,step=1,value=50)
b_slider = widgets.IntSlider(min=1,max=10,step=1,value=1)
cost_slider = widgets.IntSlider(min=1,max=10,step=1,value=1)

widgets.interact(optimal,a=a_slider,b=b_slider,cost=cost_slider,r=widgets.fixed(False))

#%% [markdown]
# The relation between two firms output quantity decescion, can also be shown visually. In the below plot, one can observe two firms reaction curve, given a = 100, b= 1 and cost = 1. Later it will be posible to see how the relationship between the firms chang, when the parameters differ.

#%%
x = np.linspace(0, 100, 1000);
reaction_plot(q_other=x,scatter=False)


#%%

widgets.interact(reaction_plot, q_other = widgets.fixed(x), a = a_slider, b = b_slider, cost = cost_slider, scatter = widgets.fixed(False))



#%%
def f(n):
    plt.plot([0,1,2],[0,1,n])
    plt.show()

widgets.interact(f,n=(0,10))


#%%
[0,1,2]


#%%



#%%



