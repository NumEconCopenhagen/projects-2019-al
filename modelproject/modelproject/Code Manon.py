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
p1 = (a-b*(q1+q2))
p2 = (a-b*(q1+q2))
pi1 =(p1*q1-c*q1)
pi2 = (p2*q2-c*q2)

"take the derivative wrt. to q1 to get the optimal quantity of firm 1:"

foc=sm.diff(pi1,q1)
foc

