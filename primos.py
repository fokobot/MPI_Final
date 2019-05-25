from mpi4py import MPI
import time
import numpy as np
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
destino = 1
Cantidad_Primos = 0
k = 0
received = 0
Validados = np.ones(num_procs-1)
sw = True

def Primos(num):
	Es_primo = True
	for j in range (2, int(num/2)+1):
		if(num%j == 0):
			Es_primo = False
			break
	return Es_primo

if rank == 0:
	k = int(input("Digite k: "))
	start = time.time()
	for i in range(1, num_procs):
		if(k>=i+1):
			comm.send(i+1, dest= i)
else:
	Primo_a_verificar = comm.recv(source = 0)
	comm.send([Primos(Primo_a_verificar), rank], dest = 0)
k = comm.bcast(k, root=0)

if rank == 0:
	for i in range(num_procs+1, k+1):
		if(destino == num_procs):
			destino = 1
		comm.send(i, dest=destino)
		destino += 1
		Informacion = comm.recv()
		received += 1
		if(Informacion[0]):
			Cantidad_Primos += 1
else:
	while(sw):
		Primo_a_verificar = comm.recv(source=0)
		comm.send([Primos(Primo_a_verificar), rank], dest=0)
		Validados[rank-1] += 1 
		if(k-Primo_a_verificar<num_procs-1):
			sw = False
	print("Los validados por el proceso", rank, "fueron:", Validados[rank-1])
		
if rank == 0:
	while(received < k-1):
		Informacion = comm.recv()
		received += 1
		if(Informacion[0]):
			Cantidad_Primos += 1
	print("La cantidad de primos es: ",Cantidad_Primos)
	end = time.time()
	print("El tiempo de ejecucion fue:", end - start)