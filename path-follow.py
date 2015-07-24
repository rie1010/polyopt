#!/usr/bin/python3

#from numpy import *
from sympy import *
from utils import Utils

# min c_0*x_0 + c_1*x_1
# s.t. I_3 + A_0*x_0 + A_1*x_1 >= 0

# initialization of the problem
c = Matrix([[3], [-2]])
#A0 = Matrix([[3, 5, 13], [5, 8, 7], [13, 7, 9]])
#A1 = Matrix([[11, 2, 3], [2, 3, 4], [3, 4, 5]])
A0 = Matrix([[1, 1, 0],
             [1, 1, 0],
             [0, 0, 0]])
A1 = Matrix([[1, 1, 1],
             [1, 0, 0],
             [1, 0, 1]])

# symbolic variables
x0 = Symbol('x0')
x1 = Symbol('x1')

# self-concordant barrier
X = simplify(eye(3) + A0*x0 + A1*x1)
print('X = ' + str(X))
F = -log(X.det())
print('F = ' + str(F))
nu = 3

# first symbolic derivation
Fdx0 = diff(F, x0)
Fdx1 = diff(F, x1)
Fd = Matrix([[Fdx0], [Fdx1]])
print('Fd = ' + str(simplify(Fd)))

# symbolic hessian
Fddx0x0 = diff(Fdx0, x0)
Fddx1x1 = diff(Fdx1, x1)
Fddx0x1 = diff(Fdx0, x1)
Fdd = Matrix([[Fddx0x0, Fddx0x1], [Fddx0x1, Fddx1x1]])
print('Fdd = ' + str(simplify(Fdd)))

# some constants
beta = 1/9
gamma = 5/36

# Auxiliary path-following scheme [Nesterov, p. 205]
t = 1
k = 0
# starting point
y = Matrix([[0], [0]])

FdS0 = Fd.subs([(x0, y[0, 0]), (x1, y[1, 0])])
print('\n\nFdS0 = ' + str(FdS0))

print('AUXILIARY PATH-FOLLOWING')
FdS = Fd.subs([(x0, y[0, 0]), (x1, y[1, 0])])
FddS = Fdd.subs([(x0, y[0, 0]), (x1, y[1, 0])])
while True:
  k += 1
  print('\nk = ' + str(k))
  print('FdS = ' + str(FdS))
  print('FddS = ' + str(FddS))

  t = t - gamma/Utils.LocalNormA(FdS0, FddS)
  y = y - FddS.inv()*(t*FdS0 + FdS)
  print('t = ' + str(t))
  print('y = ' + str(y))

  FdS = Fd.subs([(x0, y[0, 0]), (x1, y[1, 0])])
  FddS = Fdd.subs([(x0, y[0, 0]), (x1, y[1, 0])])
  print('Breaking condition = ' + str(Utils.LocalNorm(FdS, FddS)))
  if Utils.LocalNorm(FdS, FddS) <= sqrt(beta)/(1 + sqrt(beta)):
    break

# prepare x
x = y - FddS.inv()*FdS

# Main path-following scheme [Nesterov, p. 202]
print('\nMAIN PATH-FOLLOWING')

# initialization of the iteration process
t = 0
eps = 10**(-3)
k = 0

print('Input condition = ' + str(Utils.LocalNormA(Fd.subs([(x0, x[0, 0]), (x1, x[1, 0])]), Fdd.subs([(x0, x[0, 0]), (x1, x[1, 0])]))))

print('\nPress enter to continue')
input()

while True:
  k += 1
  print('\nk = ' + str(k))
  FdS = Fd.subs([(x0, x[0, 0]), (x1, x[1, 0])])
  FddS = Fdd.subs([(x0, x[0, 0]), (x1, x[1, 0])])
  t = t + gamma/Utils.LocalNormA(c, FddS)
  x = x - FddS.inv()*(t*c+FdS)
  print('t = ' + str(t))
  print('x = ' + str(x))
  print('Breaking condition = ' + str(eps*t))
  if eps*t >= nu + (beta + sqrt(nu))*beta/(1 - beta):
    break

