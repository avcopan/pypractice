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


################
# parallel part#
################
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

dx = (x1 - x0) / n
# this load balances the algorithm, so that size need not divide n
local_n = n // size + (rank < (n % size))
local_x0 = x0 + dx * sum(n // size + (r < (n % size)) for r in range(rank))
local_x1 = local_x0  + dx * local_n

# communication part
# use collective rather than point-to-point communication to sum results
total = np.zeros(1)
integral = np.array([integrate(f, local_x0, local_x1, local_n)])
comm.Reduce(integral, total, op=MPI.SUM, root=0)
# gotcha: the values stored in total on processes other than the root (here, 0) are not guaranteed
#         to be anything in particular -- I tested it, and it looks like they get set to zero in this case

# root note prints the final result
if rank == 0:
  print(total[0])
