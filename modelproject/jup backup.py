#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'projects-2019-al\modelproject'))
	print(os.getcwd())
except:
	pass

#%%
import numpy as np
import scipy as sp
import sympy as sm
import matplotlib.pyplot as plt
import ipywidgets as widgets
import pylab

#We initiate our printing as nice equations, using the sympy package 
sm.init_printing(use_unicode=True)


#%%
#defining all variables as symby symbols 
q1 = sm.symbols('q_1')
q2 = sm.symbols('q_2')
c = sm.symbols('c')
a = sm.symbols('a')
b = sm.symbols("b")
pi1 = sm.symbols('pi_1')
pi2 = sm.symbols('pi_2')

#Now we define the equations describing the relationship between the two firms 
#prices (p), costs(c), someting(a), revenue(pi) and quantity(q).
p1 = (a-b*(q1+q2))
p2 = (a-b*(q1+q2))
pi1 =(p1*q1-c*q1)
pi2 = (p2*q2-c*q2)


#%%
#Take the derivative wrt. to q1 and q2 respecticly
#to get the optimal quantity of firm 1 and firm 2:

foc1=sm.diff(pi1,q1)
foc1

foc2=sm.diff(pi2,q2)
foc2


#%%
# We solve the first firms equation equal to 0
sol1= sm.solve(sm.Eq(foc1,0),q1)[0]
sol1


#%%
# We solve the second firms equation equal to 0
sol2= sm.solve(sm.Eq(foc2,0),q2)[0]
sol2


#%%
#We then substitute the q2 in equation 1
sol1_subs = foc1.subs(q2,sol2)
sol1_subs


#%%
#then we solve the first equation for the quantity
sol1_subs_solve = sm.solve(sm.Eq(sol1_subs,0),q1)
sol1_subs_solve


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
    quantity = reaction(q_other,a, b, cost)
    
    #ax = plt.subplot()
    if scatter == True :
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
        print("The Cournot equilibrium, given that","a =",a,", b =","and that cost =",cost,",","is:",equilibrium)


#%%
qslider = widgets.IntSlider(min=0,max=100,step=1,value=50)

widgets.interact(reaction,q_other = qslider,a=widgets.fixed(100),b=widgets.fixed(1),cost=widgets.fixed(1),print_it=widgets.fixed(True))


#%%
print("The equilibrium we derived earlier as:")

sm.pprint(sol1_subs_solve,use_unicode=True)

print("Which given a = 100, b= 1 and cost = 1, is:",optimal(100,1,1))


#%%
a_slider = widgets.IntSlider(min=10,max=150,step=1,value=50)
b_slider = widgets.IntSlider(min=1,max=10,step=1,value=1)
cost_slider = widgets.IntSlider(min=1,max=10,step=1,value=1)

widgets.interact(optimal,a=a_slider,b=b_slider,cost=cost_slider,r=widgets.fixed(False))


#%%
x = np.linspace(0, 100, 1000);
reaction_plot(q_other=x,scatter=False)


#%%
widgets.interact(reaction_plot,q_other=widgets.IntSlider(min=0,max=100,step=5,value=50))



#%%



#%%
def f(n):
    plt.plot([0,1,2],[0,1,n])
    plt.show()

    widgets.interact(f,n=(0,10))


#%%
f


#%%



