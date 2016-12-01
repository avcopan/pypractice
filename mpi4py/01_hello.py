#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print("Hello world! From process {:d} out of {:d}".format(rank+1, size))
