from mpi4py import MPI
import time
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
print(num_procs)
if rank == 0:
	data = range(0,num_procs)
else:
	data = None
enviado = comm.scatter(data, root=0)
print ('rank',rank,'has data:',enviado)
comm.Barrier()
data = comm.gather(enviado**2, root=0)
if rank == 0:
	print('received', data)