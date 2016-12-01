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
local_ns = tuple(n // size + (r < n % size) for r in range(size))
offsets  = tuple(sum(local_ns[:r]) for r in range(size))
local_n = local_ns[rank]
print local_n

local_x = np.zeros(local_n)
local_y = np.zeros(local_n)

comm.Scatterv([x, local_ns, offsets, MPI.DOUBLE], local_x)
comm.Scatterv([y, local_ns, offsets, MPI.DOUBLE], local_y)

local_dot = np.array([np.dot(local_x, local_y)])

comm.Reduce(local_dot, dot, op = MPI.SUM)

if rank == 0:
  print "The dot product is {:f} computed in parallel and {:f} computed serially".format(dot[0], np.dot(x,y))
