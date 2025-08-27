import time

VOL_MOCHILA = 4200
PESO_MOCHILA = 3000

LISTA1 = [[150, 20], [325, 40], [600, 50], [805, 36], [430, 25], [1200, 64], [770, 54], [60, 18], [930, 46], [353, 28]] # Volumen y Valor
LISTA2 = [[1800, 72], [600, 36], [1200, 60]] # Peso y Valor

# ------------------------------------------------------------------------------

# Menu principal
def menu_ppal():
    global ELEMENTOS
    global SELECCION
    while True:
        print("\n--- ¿Cuantos elementos tiene tu mochila? ---")
        print("1. 10 elementos (usando volumen)")
        print("2. 3 elementos (usando peso)")

        opcion = input("Elegí una opción (1 o 2): ")

        if opcion == "1":
            ELEMENTOS = 10
            break
        elif opcion == "2":
            ELEMENTOS = 3
            break
        else:
            print("Opción inválida. Probá de nuevo.\n")

    while True:
        print("\n--- Tipo de algoritmo disponibles ---")
        print("1. Búsqueda exhaustiva")
        print("2. Método Greedy")

        opcion = input("Elegí una opción (1 o 2): ")

        if opcion == "1":
            SELECCION = 'E'
            break
        elif opcion == "2":
            SELECCION = 'G'
            break
        else:
            print("Opción inválida. Probá de nuevo.\n")


def busqueda_exhaustiva(lista, capacidad, tamano):
    mejor_valor = 0
    mejor_comb = []

    for i in range(2**tamano):
        combinacion = []
        volumen_total = 0
        valor_total = 0

        # saber si el ítem j está incluido en la combinación i, donde i representa un número binario que codifica una combinación de ítems.
        for j in range(tamano):
            if ((i >> j) & 1) == 1:   
                # (i >> j) corre el numero i, j veces a la derecha (borrar los bits a la derecha de j). 
                # & 1, se queda con el bit de más a la derecha
                # == 1 pregunta si ese bit es 1
                volumen_total += lista[j][0]
                valor_total += lista[j][1]
                combinacion.append(j) 
            """
            Funcionamiento de la condición: ejemplo donde i itera 8 veces, j itera 3 veces

            La condición permite desplazar i hacia la derecha j bits. Por ejemplo:
            i = 0       # 000 en binario
            j = 0       --> i >> 0 = 000
                NO
            j = 1       --> i >> 1 = 00
                NO
            j = 2       --> i >> 2 = 0
                NO

            ----------------------------------------
            i = 1       # 001 en binario
            combinacion = [] 

            j = 0       --> i >> 0 = 001
                SI
                combinacion = [[1800, 72], ] 
                volumen_total = 1800
                valor_total = 72
            j = 1       --> i >> 1 = 00
                NO
                combinacion = [[1800, 72], ] 
            j = 2       --> i >> 2 = 0
                NO
                combinacion = [[1800, 72], ] 

            combinacion = [[1800, 72], ] 
            volumen_total = 1800
            valor_total = 72

            mejor_valor = valor_total
            mejor_comb = combinacion[:]
            --------------------------------------------------


            i = 2       # 010 en binario
            combinacion = [] 

            j = 0       --> i >> 0 = 010
                NO
            j = 1       --> i >> 1 = 001
                SI
            j = 2       --> i >> 2 = 000
                NO

            i = 3       # 011 en binario
            j = 0       --> i >> 0 = 011
                SI
            j = 1       --> i >> 1 = 01
                SI
            j = 2       --> i >> 2 = 0
                NO
            
            i = 4       # 100 en binario
            j = 0       --> i >> 0 = 100
                NO
            j = 1       --> i >> 1 = 010
                NO
            j = 2       --> i >> 2 = 001
                SI

            i = 5       # 101 en binario
            j = 0       --> i >> 0 = 101
                SI
            j = 1       --> i >> 1 = 10
                NO
            j = 2       --> i >> 2 = 1
                SI

            i = 6       # 110 en binario
            j = 0       --> i >> 0 = 110
                NO
            j = 1       --> i >> 1 = 011
                SI
            j = 2       --> i >> 2 = 001
                SI

            i = 7       # 111 en binario
            j = 0       --> i >> 0 = 111
                SI
            j = 1       --> i >> 1 = 011
                SI
            j = 2       --> i >> 2 = 001
                SI
            """

        # Actualizar mejor combinación válida
        if volumen_total <= capacidad and valor_total > mejor_valor:
            mejor_valor = valor_total
            mejor_comb = combinacion[:]
    
    return mejor_valor, mejor_comb


def algoritmo_greedy(lista, capacidad):
    # Agregar índice y ratio valor/volumen (o bien valor/peso)
    objetos_con_ratio = []
    for idx in range(len(lista)):
        volumen = lista[idx][0] # en el caso de 3 elementos, decimos peso en vez de volumen pero sirve igual
        valor = lista[idx][1]
        ratio = valor / volumen
        objetos_con_ratio.append((idx, volumen, valor, ratio))

    # Ordenar por mayor valor relativo (valor/volumen)
    objetos_ordenados = sorted(objetos_con_ratio, key=lambda x: x[3], reverse=True)

    mochila = []
    capacidad_actual = 0
    valor_total = 0

    for i, volumen, valor, ratio in objetos_ordenados:
        if capacidad_actual + volumen <= capacidad:
            mochila.append(i)
            capacidad_actual += volumen
            valor_total += valor

    return mochila, valor_total, capacidad_actual


# ------------------------------------------------------------------------------

def main():
    menu_ppal()
    if (ELEMENTOS == 10):
        n = len(LISTA1)
        lista = LISTA1
    else:
        n = len(LISTA2)
        lista = LISTA2
    
    if (SELECCION == 'E'):
        if (ELEMENTOS == 10):
            start_time = time.perf_counter()
            mejor_valor, mejor_comb = busqueda_exhaustiva(lista, VOL_MOCHILA, n)
            elapsed_time = time.perf_counter() - start_time
            
            print (f"Tiempo de ejecución: {elapsed_time:.6f} segundos | Ejecutadas {2**n} combinaciones en la Busqueda Exhaustiva" )
            print (f"La mejor combinación válida encontrada posee {len(mejor_comb)} objetos, existiendo {n} en el listado completo original")
            
            print("Elementos de la mejor combinación válida encontrada:")
            for idx in mejor_comb:
                print(f"Objeto N°{idx + 1} - Volumen: {lista[idx][0]}, Valor: ${lista[idx][1]}")
            print(f"Valor total: ${mejor_valor}")
            print(f"Volumen total: {sum([lista[i][0] for i in mejor_comb])} cm³")
        
        else: 
            start_time = time.perf_counter()
            mejor_valor, mejor_comb = busqueda_exhaustiva(lista, PESO_MOCHILA, n)
            elapsed_time = time.perf_counter() - start_time
            print (f"Tiempo de ejecución: {elapsed_time:.6f} segundos | Ejecutadas {2**n} combinaciones en la Busqueda Exhaustiva" )
            print (f"La mejor combinación válida encontrada posee {len(mejor_comb)} objetos, existiendo {n} en el listado completo original")
            
            print("Elementos de la mejor combinación válida encontrada:")
            for idx in mejor_comb:
                print(f"Objeto N°{idx + 1} - Peso: {lista[idx][0]}g, Valor: ${lista[idx][1]}")
            print(f"Valor total: ${mejor_valor}")
            print(f"Peso total: {sum([lista[i][0] for i in mejor_comb])} gramos")

    else:
        if (ELEMENTOS == 10):
            start_time = time.perf_counter()
            mochila, valor_total, volumen_total = algoritmo_greedy(lista, VOL_MOCHILA)
            elapsed_time = time.perf_counter() - start_time

            print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos | Algoritmo Greedy (valor/volumen)")

            for i in mochila:
                print(f"Objeto N°{i + 1} - Volumen: {lista[i][0]} cm³, Valor: ${lista[i][1]}")
            print(f"Valor total: ${valor_total}")
            print(f"Volumen total: {volumen_total} cm³")
            
        else:
            start_time = time.perf_counter()
            mochila, valor_total, peso_total = algoritmo_greedy(lista, PESO_MOCHILA)
            elapsed_time = time.perf_counter() - start_time

            print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos | Algoritmo Greedy (valor/peso)")

            for i in mochila:
                print(f"Objeto N°{i + 1} - Peso: {lista[i][0]} g, Valor: ${lista[i][1]}")
            print(f"Valor total: ${valor_total}")
            print(f"Peso total: {peso_total} g")

# Al utilizar 10 objetos: el algoritmo exhaustivo es un 3700% más lento (tarda 38 veces más) que el algoritmo greedy.
# Al utilizar 3 objetos: el algoritmo exhaustivo es un 4% más lento (apenas 1.04 veces más) que el algoritmo greedy.

if __name__ == "__main__":
    main()
