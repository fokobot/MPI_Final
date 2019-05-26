from mpi4py import MPI
import time
import random
import numpy as np
from prettytable import PrettyTable
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
# Función para tomar tenedores
def Tomar_Tenedor(tenedor, proceso, Tenedores):
    if(Tenedores[tenedor] == 0):
        Tenedores[tenedor] = proceso
        return Tenedores, True;
    else:
        return Tenedores, False;
# Creación del vector global de la informacipon de los tenedores
itemsize = MPI.INT.Get_size()
if rank == 0:
    nbytes = (num_procs-1) * itemsize
else:
    nbytes = 0
win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
buf, itemsize = win.Shared_query(0)
assert itemsize == MPI.INT.Get_size()
Tenedores = np.ndarray(buffer=buf, dtype=int, shape=(num_procs-1,))
# Asignamos el número del tenedor de la derecha y del tenedor de la izquierda a cada proceso
if(rank < num_procs-1 and rank!=0):
    right = rank
    left = rank-1
elif(num_procs-1 == rank):
    right = 0
    left = rank-1
if rank == 0:
    names = []
    Array_Tenedores = []
    for i in range(1, num_procs):
        names.append("Filosofo "+ str(i))
    Filosofos = PrettyTable(names)
    while(True):
        Filosofos.clear_rows()
        Array_Tenedores = []
        for t in range(1, num_procs):
            if(t < num_procs-1):
                Array_Tenedores.append(str(Tenedores[t-1])+" | "+str(Tenedores[t]))
            else:
                Array_Tenedores.append(str(Tenedores[t-1])+" | "+str(Tenedores[0]))
        Filosofos.add_row(Array_Tenedores)
        print(Filosofos)
        time.sleep(1)
else:
    # Tipo 1 = Amistoso
    # Tipo 0 = Ambicioso
    Tipo = 1
    Comido = True
    if(Tipo == 1):
        # Codigo Filosofo Amigable
        while Comido:
            tpensando = random.randrange(7, 11)
            time.sleep(tpensando)
            Tenedores, Lo_Tomo = Tomar_Tenedor(left, rank, Tenedores)
            print("Proceso",rank,"tomo el de la izquierda",Lo_Tomo)
            if Lo_Tomo:
                Tenedores, Lo_Tomo = Tomar_Tenedor(right, rank, Tenedores)
                print("Proceso",rank,"tomo el de la derecha",Lo_Tomo)
                if(Lo_Tomo == False):
                    tespera = random.randrange(5, 16)
                    time.sleep(tespera)
                    Tenedores, Lo_Tomo = Tomar_Tenedor(right, rank, Tenedores)
                    print("Proceso",rank,"tomo el de la derecha",Lo_Tomo)
                    if(Lo_Tomo==False):
                        Tenedores[left] = 0
                    else:
                        tcomiendo = random.randrange(2, 6)
                        time.sleep(tcomiendo)
                        Comido = False
                        Tenedores[left] = 0
                        Tenedores[right] = 0
                        print("Filosofo", rank, "ya comió")
                        tpensando = random.randrange(7, 11)
                        time.sleep(tpensando)
                else:
                    tcomiendo = random.randrange(2, 6)
                    time.sleep(tcomiendo)
                    Comido = False
                    Tenedores[left] = 0
                    Tenedores[right] = 0
                    print("Filosofo", rank, "ya comió")
                    tpensando = random.randrange(7, 11)
                    time.sleep(tpensando)
    else:
        # Codigo Filosofo Ambicioso
        while Comido:
            tpensando = random.randrange(7, 11)
            time.sleep(tpensando)
            Tenedores, Lo_Tomo = Tomar_Tenedor(left, rank, Tenedores)
            if Lo_Tomo:
                Obtener_Derecha = False
                while Obtener_Derecha == False:
                    Tenedores, Obtener_Derecha = Tomar_Tenedor(right, rank, Tenedores)
                tcomiendo = random.randrange(2, 6)
                time.sleep(tcomiendo)
                Comido = False
                Tenedores[left] = 0
                Tenedores[right] = 0
                print("Filosofo", rank, "ya comió")
                tpensando = random.randrange(7, 11)
                time.sleep(tpensando)
# if rank == 0:
#     win_mem = np.empty(num_procs-1,dtype=int)
#     win_mem.fill(1)
#     win = MPI.Win.Create( win_mem,comm=comm )
# else:
#     win = MPI.Win.Create(None,comm=comm )
# win.Fence()
# if(rank == 1):
#     x = np.empty(num_procs-1,dtype=int)
#     print(x)
#     x = win.Get(x,0,target=0)
#     print(x)
# win.Fence()
