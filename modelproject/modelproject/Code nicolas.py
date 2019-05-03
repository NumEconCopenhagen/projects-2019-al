import numpy as np
import scipy as sp
import sympy as sm

sm.init_printing(use_unicode=True)

q1 = sm.symbols('q_1')
q2 = sm.symbols('q_2')
c = sm.symbols('c')
a = sm.symbols('a')
b = sm.symbols('b')
pi1 = sm.symbols('pi_1')
pi2 = sm.symbols('pi_2')
p = sm.symbols('p')
p1 = (a-(q1+q2))
p2 = (a-(q1+q2))
pi1 =(p1*q1-c*q1)
pi2 = (p2*q2-c*q2)

#Take the derivative wrt. to q1 to get the optimal quantity of firm 1:

foc1=sm.diff(pi1,q1)
foc1

foc2=sm.diff(pi2,q2)
foc2

sol1= sm.solve(sm.Eq(foc1,0),q1)[0]
sol1

sol2= sm.solve(sm.Eq(foc2,0),q2)[0]
sol2

#sol1 and sol2 constitute the reaction functions of the two firms.
#Now we substitute for the optimal quantities:

sol1_subs = sol1.subs(q2,sol2)
sol1_subs

sol1_subs_solve = sm.solve(sm.Eq(sol1_subs,0),q1)
sol1_subs_solve

