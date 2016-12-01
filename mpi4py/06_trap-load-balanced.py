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
print local_n


# communication part - note that this works out because the number of trapezoids is n-1
recv_buffer = np.zeros(1)
integral = np.array([integrate(f, local_x0, local_x1, local_n)])
if rank == 0:  # root node receives results from all processes and sums them
  total = integral[0]
  for _ in range(size - 1):
    comm.Recv(recv_buffer, source=MPI.ANY_SOURCE)
    total += recv_buffer[0]
else:          # all other nodes send their results
  comm.Send(integral, dest=0)

# root note prints the final result
if rank == 0:
  print(total)
