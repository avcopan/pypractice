#!/usr/bin/env python

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

r = np.zeros(1)

if rank == 1:
  r = np.random.random_sample(1)
  print("Process {:d} drew the number {:f}".format(rank, r[0]))
  comm.Send(r, dest=0)

if rank == 0:
  print("Process {:d} before receiving has the number {:f}".format(rank, r[0]))
  #comm.Recv(r, source=1)
  comm.Recv(r, source=MPI.ANY_SOURCE) # this also works
  print("Process {:d} has received the number {:f}".format(rank, r[0]))
