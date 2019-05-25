from mpi4py import MPI
#import numpy as np
#from time import sleep
import sys

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
	data = range(0,size)
	#print ('we will be scattering:',data)
else:
	data = None

data = comm.scatter(data, root=0)
print ('rank',rank,'has data:',data)


sys.stdout.flush()
comm.Barrier()
#sleep(1)

data = comm.gather(data**2, root=0)
if rank == 0:
	print('rank ',rank,' data ',data)