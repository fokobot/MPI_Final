from mpi4py import MPI
import numpy as np
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
window_data = np.zeros(2,dtype=np.int)
my_number = np.empty(1,dtype=np.int)
src = 0; tgt = num_procs-1
if rank==src:
    my_number[0] = 37
else:
    my_number[0] = 1


intsize = np.dtype('int').itemsize
win = MPI.Win.Create(window_data,intsize,comm=comm)


win.Fence()
if rank==src:
    # put data in the second element of the window
    win.Put(my_number,tgt,target=1)
win.Fence()
