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
objective = q1*(p*(q1+q2)-c1)
objective

more = sm.Eq(q1*(p*(q1+q2)-c1),pi1)
more

lala = sm.solve(more,q2)
lala

objective_subs = objective.subs(q2,lala[0])
objective_subs

foc = sm.diff(objective_subs,q1)
foc


x = sm.Eq(foc,0)
sm.solve(x,q1)
solution = sm.solve(x,q1)
solution


firm_diff_q1 = sm.diff(objective,q1)
firm_diff_q1




