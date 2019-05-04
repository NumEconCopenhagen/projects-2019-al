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
pi1 = (p1*q1-c*q1)
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

sol1_subs = foc1.subs(q2,sol2)
sol1_subs

sol2_subs = foc2.subs(q1,sol1)
sol2_subs



sol1_subs_solve = sm.solve(sm.Eq(sol1_subs,0),q1)
sol1_subs_solve


# Calculate equilibrium prices and profits:

n1 = sm.diff(pi1,q2)
n2 = sm.diff(pi2,q1)
sm.Matrix([foc1,n1])
f11 = sm.diff(pi1,q1,q1)
f12 = sm.diff(pi1,q1,q2)
f21 = sm.diff(pi1,q2,q1)
f22 = sm.diff(pi1,q2,q2)
sm.Matrix([[f11,f12],[f21,f22]])

from scipy import linalg
from scipy import optimize
from scipy import interpolate

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

bf = sm.lambdify((q1,q2),pi1)

# a. grids
x1_vec = np.linspace(-2,2,500)
x2_vec = np.linspace(-2,2,500)
x1_grid,x2_grid = np.meshgrid(x1_vec,x2_vec,indexing='ij')
f_grid = bf(x1_grid,x2_grid)

# b. main
fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')
cs = ax.plot_surface(x1_grid,x2_grid,f_grid,cmap=cm.jet)

# c. add labels
ax.set_xlabel('$q_1$')
ax.set_ylabel('$q_2$')
ax.set_zlabel('$pi$')

# d. invert xaxis
ax.invert_xaxis()

# e. remove background
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# f. add colorbar
fig.colorbar(cs);