import time
k = int(input("Digite k: "))
start = time.time()
Cantidad_primos = 0
for i in range(2, k+1):
	Es_primo = True
	for j in range (2, int(i/2)+1):
		if(i%j == 0):
			Es_primo = False
			break
	if(Es_primo):
		Cantidad_primos += 1
print("La cantidad de primos en los ", k, "primeros números son: ", Cantidad_primos) 
end = time.time()
print("El tiempo de ejecucion fue:", end - start)