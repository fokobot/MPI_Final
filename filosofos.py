from mpi4py import MPI
import time
import random
import numpy as np
from prettytable import PrettyTable
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
names = []
Tenedores_Obtenidos = []
Tenedores_Disponibles = []
if rank == 0:
	for i in range (1, num_procs):
		names.append("Filosofo " + str(i))
		Tenedores_Obtenidos.append(" O | O ")
		Tenedores_Disponibles.append(" X | X ")
	Filosofos = PrettyTable(names)
	while(True):
		
		Filosofos.add_row(Tenedores_Obtenidos)
		Filosofos.add_row(Tenedores_Disponibles)
		print(Filosofos)
		time.sleep(1)
	
else:
def Filosofo_Amigable():
	tespera = random.randrange(7, 11)
	time.sleep(tespera)
	Lo_Tomo = Tomar_Tenedor_Izquierda()
	if(Lo_Tomo):
		Segundo = Tomar_Tenedor_Derecha()
		if(Segundo):
			tespera = random.randrange(7, 11)
			time.sleep(tespera)
		else:
			tespera = random.randrange(5, 16)
			time.sleep(tespera)
	return 0
	
def Filosofo_Ambicioso():
	return 0
	
def Tomar_Tenedor_Izquierda():
	return 0
	
def Tomar_Tenedor_Derecha():
	return 0