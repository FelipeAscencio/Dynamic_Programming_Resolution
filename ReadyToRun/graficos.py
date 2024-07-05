
import time
import math
import matplotlib.pyplot as plt

CARGAR = "Cargar"
ATACAR = "Atacar"
PRIMER_RENGLON = 2

def carga(archivo):
    try:
        nombre_archivo = archivo + ".txt"
        with open(nombre_archivo) as archivo:
            lineas = archivo.readlines()
            mitad = (len(lineas) -2 )//2
            minutos = lineas[1]
            ordas = []
            poder = []
            for linea in lineas[2:]: #O(n)
                if mitad > 0:
                    datos = linea.strip().split(",")
                    ordas.append(int(datos[0]))
                    mitad -= 1
                else:
                    datos = linea.strip().split(",")
                    poder.append(int(datos[0]))


        return ordas, poder, minutos
    except IOError:
        print("Error al abrir el archivo")
        return None

#PRE: Ordas y poder deben estar cargados correctamente.
#POST: Devuelve un arreglo con el numero de bajas optimo para cada ataque.
def batallas(ordas, poder): #O(n²)
    bajas_optimas = [0] * len(ordas)
    bajas_optimas[0] = (min(ordas[0], poder[0]))

    for i in range(1, len(ordas)): #O(n)
        bajas_optimas[i] = (min(ordas[i], poder[i]))
        for j in range(i): #O(n)
            bajas_optimas[i] = max(bajas_optimas[i], bajas_optimas[j] + min(ordas[i], poder[i -1-j]))
    estrategia = sacar_resultado(bajas_optimas, ordas, poder) #O(n²)
    return estrategia, bajas_optimas[len(bajas_optimas) - 1]


#PRE: bajas_optimas, ordas y poder deben estar cargados correctamente.
#POST: Devuelve un arreglo con la estrategia necesaria para llegar al optimo final.
def sacar_resultado(bajas_optimas, ordas, poder): #O(n²)
    estrategia = [CARGAR] * len(bajas_optimas)
    i = len(bajas_optimas) - 1

    while i > 0: #O(n)
        for j in range(i): #O(n)
            estrategia[i] = ATACAR
            bajas = bajas_optimas[i]
            if bajas == bajas_optimas[j] + min(ordas[i], poder[i - 1-j]):
                i = j
                break
        if i - 1 == j:
            break
        if i == 0:
            estrategia[i] = ATACAR
    return estrategia



archivo = input("ingrese nombre del archivo\n")
ordas, poder, minutos = carga(archivo)
# Realizar mediciones de tiempos
n = len(ordas)
tiempos = []
for i in range(1, n+1):
    inicio = time.time()
    cantidad,estrategia =  batallas(ordas[:i], poder[:i]) 
    fin = time.time()
    tiempos.append(fin - inicio)

#Graficar los tiempos de ejecución
escala = 10**7
tiempos_escalados = [t * escala for t in tiempos]
n_cuadrado = [2*(i**2) for i in range(1, n + 1)]


plt.figure(figsize=(12, 8))
plt.plot(range(1, n+1), tiempos_escalados, marker='o')
plt.plot(range(1, n + 1), n_cuadrado, linestyle='--', label='O(2*n^2)')
plt.xlabel('Número de ordas')
plt.ylabel('Tiempo de ejecución (s)')
plt.title('Tiempo de ejecución del algoritmo')
plt.grid(True)
plt.show()
