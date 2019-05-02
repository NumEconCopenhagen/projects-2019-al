#cournot model

import numpy as np
import scipy as sp
import sympy as sm

sm.init_printing(use_unicode=True)
#defining all variables as symby symbols 
q1 = sm.symbols('q_1')
q2 = sm.symbols('q_2')
c1 = sm.symbols('c_1')
c2 = sm.symbols('c_2')
a = sm.symbols('a')
pi1 = sm.symbols('pi_1')
pi2 = sm.symbols('pi_2')
p = sm.symbols('p')

#Defining relations between symbols
p1 = (a-(q1+q2)*q1)
p2 = (a-(q1+q2)*q2)
pi1 =(p1*q1-c1*q1)
pi2 = (p2*q2-c2*q2)






