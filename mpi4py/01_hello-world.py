#!/usr/bin/env python

from mpi4py import MPI

comm = MPI.COMM_WORLD
print("Hello! I'm rank {:d} from {:d} running in total...".format(comm.rank, comm.size))
comm.Barrier()
