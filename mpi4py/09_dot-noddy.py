#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n = int(sys.argv[1])

x = np.random.rand(n) if comm.rank == 0 else None
y = np.random.rand(n) if comm.rank == 0 else None

# initialize as numpy arrays
dot = np.zeros(1)
local_n = np.zeros(1, dtype=int)

if rank == 0:
  if n != y.size:
    print "vector length mismatch"
    comm.Abort()
  if n % size:
    print "the number of processors must divide n"
    comm.Abort()
  local_n = np.array([n/size])

comm.Bcast(local_n, root=0)

local_x = np.zeros(local_n[0])
local_y = np.zeros(local_n[0])

comm.Scatter(x, local_x, root=0)
comm.Scatter(y, local_y, root=0)

local_dot = np.array([ np.dot(local_x, local_y) ])

comm.Reduce(local_dot, dot, op = MPI.SUM)

if rank == 0:
  print "The dot product is {:f} computed in parallel and {:f} computed serially".format(dot[0], np.dot(x,y))
