from prettytable import PrettyTable
n = int(input("Digite n: "))
names = []
for i in range (1, n+1):
	names.append("Filosofo " + str(i))
Filosofos = PrettyTable(names)
Array_Tenedores = (["X | O","O | X","O | O"])
Array_Tenedores2 = (["  O  ","  X  ", "  O  "])
Filosofos.add_row(Array_Tenedores)
Filosofos.add_row(Array_Tenedores2)
Filosofos.clear_rows()
print(Filosofos)
https://github.com/bezidejni/drinking_philosophers_mpi
http://monismith.info/cs599/examples.html
https://gist.github.com/markusos/7472879
-------------------------------------------------------------------
https://www.google.com/search?client=ubuntu&hs=Dkg&channel=fs&ei=eXToXIPNFa_H5gLmporYBg&q=omp+set+lock++descripcion&oq=omp+set+lock++descripcion&gs_l=psy-ab.3..33i21.160056.162774..163010...0.0..0.347.2741.2-10j1......0....1..gws-wiz.......0i71j0i22i30j0i22i10i30j33i22i29i30j33i160.8bSkjrSq0GE
http://code.kiutz.com/paral/docu.pdf
http://pages.tacc.utexas.edu/~eijkhout/pcse/html/mpiexamples.html
https://www.mpich.org/static/docs/latest/
https://www.mpich.org/static/docs/latest/www3/MPI_Win_create.html
https://mpi4py.readthedocs.io/en/stable/overview.html
https://mpi4py.readthedocs.io/en/stable/
----------------------------------------------------------------------
http://www.cas.mcmaster.ca/~nedialk/COURSES/mpi/Lectures/lec2_1.pdf
https://pyformat.info/
https://bitbucket.org/VictorEijkhout/parallel-computing-book/src/default/
