CARGAR = "Cargar"
ATACAR = "Atacar"
PRIMER_RENGLON = 2


#PRE: - .
#POST: Hace la lectura y el parseo del archivo para devolver los datos necesarios.
def carga(archivo):
    try:
        nombre_archivo = archivo + ".txt"
        with open(nombre_archivo) as archivo:
            lineas = archivo.readlines()
            mitad = (len(lineas) - PRIMER_RENGLON)/2
            ordas = []
            poder = []
            for linea in lineas[PRIMER_RENGLON:]: #O(n)
                if mitad > 0:
                    datos = linea.strip().split(",")
                    ordas.append(int(datos[0]))
                    mitad -= 1
                else:
                    datos = linea.strip().split(",")
                    poder.append(int(datos[0]))
        return ordas, poder
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


def main():
    archivo = input("ingrese nombre del archivo\n")
    ordas, poder = carga(archivo)
    estrategia, bajas_tot = batallas(ordas, poder) #O(n²)
    print("Cantidad de tropas eliminadas:", bajas_tot)
    print("Estrategia:", estrategia)

