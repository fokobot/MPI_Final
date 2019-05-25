from mpi4py import MPI
import time
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
received = []
if rank == 0:
	received.append(rank**2)
	for i in range(1,num_procs):
		comm.send(i, dest=i)
		received.append(comm.recv(source=i))
	print(received)	
else:
	data = comm.recv(source=0)
	print("estoy haciendo el proceso", rank, 'y su data es:', data)
	data = data**2
	comm.send(data, dest=0)
	