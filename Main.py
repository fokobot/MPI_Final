from mpi4py import MPI
import time
import random
import numpy as np
from prettytable import PrettyTable
import sys
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
K=int(sys.argv[1])
# Función para tomar tenedores
def Tomar_Tenedor(tenedor, proceso, Tenedores):
    MPI.Win.Lock(win, proceso, MPI.LOCK_EXCLUSIVE)
    if(Tenedores[tenedor] == 0):
        Tenedores[tenedor] = proceso
        MPI.Win.Unlock(win, proceso)
        return Tenedores, True;
    else:
        MPI.Win.Unlock(win, proceso)
        return Tenedores, False;
# Designación del Tipo de Filosofo a ser
if rank == 0:
    AmbiciososRestantes = 2
    Tipo = [0]
    for i in range(0, num_procs-1):
        if(num_procs-1-i<=AmbiciososRestantes):
            Tipo.append(0)
            AmbiciososRestantes -= 1
        elif(AmbiciososRestantes == 0):
            Tipo.append(1)
        else:
            Tipo.append(random.randrange(0, 2))
            if(Tipo[i+1] == 0):
                AmbiciososRestantes -= 1
    TipoFil = Tipo
else:
    Tipo = None
Tipo = comm.scatter(Tipo, root=0)
# Creación del vector global de la informacipon de los tenedores
itemsize = MPI.INT.Get_size()
if rank == 0:
    nbytes = (num_procs) * itemsize
else:
    nbytes = 0
win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
buf, itemsize = win.Shared_query(0)
assert itemsize == MPI.INT.Get_size()
Tenedores = np.ndarray(buffer=buf, dtype=int, shape=(num_procs,))
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
        if(TipoFil[i] == 1):
            fil = " (Amigable)"
        else:
            fil = " (Ambicioso)"
        names.append("Filosofo " + str(i) + fil)
    Filosofos = PrettyTable(names)
    while(Tenedores[num_procs-1]<num_procs-1):
        Filosofos.clear_rows()
        Array_Tenedores = []
        Array_Disponibles = []
        for t in range(1, num_procs):
            if(t == Tenedores[t-1]):
                first = 'X'
            else:
                first = 'O'
            if(t < num_procs-1):
                if(t == Tenedores[t]):
                    second = 'X'
                else:
                    second = 'O'
                Array_Tenedores.append(first+" | "+second)
            else:
                if(t == Tenedores[0]):
                    second = 'X'
                else:
                    second = 'O'
                Array_Tenedores.append(first+" | "+second)
            if(Tenedores[t-1] == 0):
                Array_Disponibles.append('X')
            else:
                Array_Disponibles.append('O')
        Filosofos.add_row(Array_Tenedores)
        Filosofos.add_row(Array_Disponibles)
        print(Filosofos)
        sys.stdout.flush()
        time.sleep(1)
else:
    # Tipo 1 = Amistoso
    # Tipo 0 = Ambicioso
    Comido = 0
    if(Tipo == 1):
        # Codigo Filosofo Amigable
        while Comido < K:
            tpensando = random.randrange(7, 11)
            time.sleep(tpensando)
            Tenedores, Lo_Tomo = Tomar_Tenedor(left, rank, Tenedores)
            if Lo_Tomo:
                Tenedores, Lo_Tomo = Tomar_Tenedor(right, rank, Tenedores)
                if(Lo_Tomo == False):
                    tespera = random.randrange(5, 16)
                    time.sleep(tespera)
                    Tenedores, Lo_Tomo = Tomar_Tenedor(right, rank, Tenedores)
                    if(Lo_Tomo==False):
                        MPI.Win.Lock(win, rank, MPI.LOCK_EXCLUSIVE)
                        Tenedores[left] = 0
                        MPI.Win.Unlock(win, rank)
                    else:
                        tcomiendo = random.randrange(2, 6)
                        time.sleep(tcomiendo)
                        Comido += 1
                        MPI.Win.Lock(win, rank, MPI.LOCK_EXCLUSIVE)
                        Tenedores[left] = 0
                        Tenedores[right] = 0
                        MPI.Win.Unlock(win, rank)
                        tpensando = random.randrange(7, 11)
                        time.sleep(tpensando)
                else:
                    tcomiendo = random.randrange(2, 6)
                    time.sleep(tcomiendo)
                    Comido += 1
                    MPI.Win.Lock(win, rank, MPI.LOCK_EXCLUSIVE)
                    Tenedores[left] = 0
                    Tenedores[right] = 0
                    MPI.Win.Unlock(win, rank)
                    tpensando = random.randrange(7, 11)
                    time.sleep(tpensando)
    else:
        # Codigo Filosofo Ambicioso
        while Comido < K:
            tpensando = random.randrange(7, 11)
            time.sleep(tpensando)
            Tenedores, Lo_Tomo = Tomar_Tenedor(left, rank, Tenedores)
            if Lo_Tomo:
                Obtener_Derecha = False
                while Obtener_Derecha == False:
                    Tenedores, Obtener_Derecha = Tomar_Tenedor(right, rank, Tenedores)
                tcomiendo = random.randrange(2, 6)
                time.sleep(tcomiendo)
                Comido += 1
                MPI.Win.Lock(win, rank, MPI.LOCK_EXCLUSIVE)
                Tenedores[left] = 0
                Tenedores[right] = 0
                MPI.Win.Unlock(win, rank)
                tpensando = random.randrange(7, 11)
                time.sleep(tpensando)
    MPI.Win.Lock(win, rank, MPI.LOCK_EXCLUSIVE)
    Tenedores[num_procs-1] += 1
    MPI.Win.Unlock(win, rank)
