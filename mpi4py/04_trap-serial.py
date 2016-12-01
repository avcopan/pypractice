#!/usr/bin/env python
import numpy as np
import sys

def integrate(f, x0, x1, n):
  '''
  Numerically integrate function f from x0 to x1 using n trapezoids
  '''
  integral = 0
  for i, x in enumerate(np.linspace(x0, x1, n+1)):
    integral += 2 * f(x) if not i in [0, n] else f(x)
  integral *= (x1 - x0) / (2. * n)
  return integral
  

x0 = float(sys.argv[1])
x1 = float(sys.argv[2])
n  = int  (sys.argv[3])

def f(x): return x*x

print integrate(f, x0, x1, n)
