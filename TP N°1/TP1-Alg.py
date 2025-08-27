import random
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd

COEF = 2**30 - 1
LONG_CROM = 30
LONG_POBLACION = 10
PC = 0.75
PM = 0.05
 

# ------------------------------------------------------------------------------

# Menu principal
def menu_ppal():
    global GENERACIONES
    global SELECCION
    while True:
        print("\n--- Cantidad de Generaciones ---")
        print("1. 20 generaciones")
        print("2. 100 generaciones")
        print("3. 200 generaciones")

        opcion = input("Elegí una opción (1, 2 o 3): ")

        if opcion == "1":
            GENERACIONES = 20
            break
        elif opcion == "2":
            GENERACIONES = 100
            break
        elif opcion == "3":
            GENERACIONES = 200
            break
        else:
            print("Opción inválida. Probá de nuevo.\n")

    while True:
        print("\n--- Tipo de selecciones disponibles ---")
        print("1. Ruleta")
        print("2. Torneo")
        print("3. Elitismo (aplicado a ruleta)")

        opcion = input("Elegí una opción (1, 2 o 3): ")

        if opcion == "1":
            SELECCION = 'R'
            break
        elif opcion == "2":
            SELECCION = 'T'
            break
        elif opcion == "3":
            SELECCION = 'E'
            break
        else:
            print("Opción inválida. Probá de nuevo.\n")



# Generación de población
def individuo():
    return [1 if random.random() > 0.5 else 0 for _ in range(LONG_CROM)]    # Genera una lista de 30 bits con 1s y 0s al azar

def pob_ini():
    return [individuo() for _ in range(LONG_POBLACION)]


# Evaluación y conversión
def pasaje(ind):
    cadena = ''.join(str(bit) for bit in ind)   # Convierte una lista de bits en una cadena unica tipo string
    valor = int(cadena, 2)  # Convierte la cadena binaria a número entero, sabiendo que están en base 2 (binario)
    return valor

def func_obj(x):
    return (x / COEF) ** 2

def calculaFitness(poblacion):
    # Calcula el fitness relativo de cada individuo
    decimales = [pasaje(ind) for ind in poblacion]  # Para cada individuo de la poblacion hacemos el pasaje y lo guardamos en el array decimales
    objetivos = [func_obj(x) for x in decimales]    # Para cada individuo de la poblacion (ya en decimal) calculamos su funcion objetivo y lo guardamos en el array objetivos
    suma_total = sum(objetivos)
    if suma_total == 0:
        # Si todo es cero (muy raro, pero hay que contemplarlo ya que la division por cero no esta definida), repartimos el fitness de forma pareja
        fitness = [1 / LONG_POBLACION for _ in objetivos]
    else:
        # Si no, cada uno recibe su parte proporcional (peso que tiene cada uno dentro de la poblacion)
        fitness = [obj / suma_total for obj in objetivos]
    return fitness


# Selección por ruleta
def seleccionRuleta(poblacion, fitness):
    """
    Se basa en el peso relativo de cada individuo como probabilidad de salir elegido (puede ser elegido incluso más de una vez)
    """
    acumulado = []  # Acá vamos a ir guardando la suma acumulada de los fitness
    suma = 0
    for f in fitness:
        suma += f
        acumulado.append(suma)  # Ya tenemos el array acumulado completado
    
    seleccion = []  # Acá vamos a guardar los padres que generarán la siguiente generación
    for _ in range(LONG_POBLACION): # Vamos a seleccionar tantos individuos como el tamaño de la población
        r = random.random() # Número aleatorio entre 0 y 1
        for (idx, valorAcum) in enumerate(acumulado):    # Enumerate() devuelve tanto el id como el valor en cada posición que recorre del array
            if r <= valorAcum:  # Si el numero aleatorio generado es menor o igual al valor acumulado entonces 
                seleccion.append(poblacion[idx].copy())   # Copiamos al individuo seleccionado en la posicion coincidente. Usamos copy() para crear un clon del individuo, no una referencia al array original
                break
    return seleccion
    """
    Ejemplo: 
    Array fitness: [0.15, 0.12, 0.10, 0.08, 0.05, 0.20, 0.07, 0.03, 0.10, 0.10]
    Array acumulado: [0.15, 0.27, 0.37, 0.45, 0.50, 0.70, 0.77, 0.80, 0.90, 1.00]
    Numero aleatorio: 0.49
    Enumerate(acumulado): [(0, 0.15),(1, 0.27),(2, 0.37),(3, 0.45),(4, 0.50),(5, 0.70),...,(9, 1.00)]
    0.49 <= 0.15? ---> NO
    ...
    0.49 <= 0.5 ---> Sí: selecionar ese individuo en la id donde estaba 0.50 (4). Ese individuo será un padre. Romper el ciclo FOR interno.
    Este proceso de seleccion se cumplió bien ya que el individuo seleccionado tenía 5% de chances, y el acumulado que posibilitaba estaba un numero entre 0.45 y 0.5 (0.05)
    """


def seleccionTorneo(poblacion):
    """
    Elige al mejor entre el 40% de la población al azar, y esto se repite tantas veces como el tamaño de la población.
    
    (VIEJO):
    Algo a tener en cuenta es que si incluimos prints en los individuos que van subiendo al ring podría parecer que se está subiendo dos veces el mismo individuo.
    Esto no es técnicamente así, lo que ocurre es que en nuestra población seguramente tenemos dos individuos que son genéticamente idénticos (el mismo número), entonces da esa sensación.
    
    Podemos verificar cuántos individuos genéticamente únicos hay en la población haciendo:
    # individuos_unicos = {tuple(individuo) for individuo in poblacion} 
    # print(f'Individuos genéticamente únicos: {len(individuos_unicos)} / {len(poblacion)}')
    ¿Como funciona el tuple() en este caso?
    numeros = [(1, 2, 3), (1, 2, 4), (1, 2, 3)]
    print(numeros)  # Devuelve: [(1, 2, 3), (1, 2, 4), (1, 2, 3)]
    numUnicos = {tuple(n) for n in numeros} 
    print(numUnicos)    # Devuelve: {(1, 2, 3), (1, 2, 4)}
    """
    seleccion = []
    cantidadGrupo = int(len(poblacion) * 0.4)

    for _ in range(LONG_POBLACION):  # Hace un for iterando tantas veces como la longitud de la poblacion
        ring = []

        while len(ring) < cantidadGrupo: # Bucle que se asegura que sean siempre 40% de individuos dentro de "ring"
            idx = random.randint(0, LONG_POBLACION - 1)
            ring.append(poblacion[idx].copy())
        
        fitnessRing = calculaFitness(ring) # Calcula el fitness de cada uno de los individuos dentro del "ring"
        mejor_idx = fitnessRing.index(max(fitnessRing)) # Encuentra cuál es el índice del individuo que tiene el mayor fitness en el ring.
        seleccion.append(ring[mejor_idx].copy()) # Toma al individuo ganador(el que tiene mejor fitness) y lo agrega a la lista "seleccion"
    return seleccion


def seleccionElitismo(poblacion, fitness, cantidad_elite):
    """
    El 20% mejor de la poblacion pasará directamente a la siguiente generación, entre el resto aplicamos el método de Ruleta para su selección
    """

    # Seleccionamos los 20% mejores individuos de la poblacion
    fitness_y_poblacion = list(zip(fitness, poblacion))   # Vincular cada fitness calculado a su correspondiente individuo, y lo hacemos lista para poder manejarlo como un array de elementos (x, y)
    fitness_y_poblacion.sort(reverse=True)  # ordena por el primer elemento de cada tupla automáticamente (fitness)
    pob = [individuo for _, individuo in fitness_y_poblacion]  # Ahora volvemos a obtener el array de poblacion, pero ya ordenado de mayor a menor fitness
    fitness_pob = [fit for fit, _ in fitness_y_poblacion]
    elite = [ind.copy() for ind in pob[:cantidad_elite]]    # Agarramos solo los dos mejores

    # Calcular fitness acumulado (para ruleta)
    acumulado = []
    suma = 0
    for f in fitness_pob:
        suma += f
        acumulado.append(suma)  # Ya tenemos el array acumulado completado

    # Selección por ruleta para completar el resto
    seleccion = elite.copy()
    while len(seleccion) < LONG_POBLACION:
        r = random.random() # Número aleatorio entre 0 y 1
        for (idx, valorAcum) in enumerate(acumulado):
            if r <= valorAcum:
                seleccion.append(pob[idx].copy())
                break
    return seleccion


# Cruce y mutación
def crossover(poblacionSeleccionada, longitud_poblacion):
    prox_gen = []
    for i in range(0, longitud_poblacion, 2):   # Voy agarrando los padres de a pares
        padre1 = poblacionSeleccionada[i] 
        padre2 = poblacionSeleccionada[(i + 1) % longitud_poblacion]    # Esto se asegura que siempre haya una pareja: si i es el último índice (9), el siguiente será 0. Operador modulo: 10 % 3 = 1 --> 10 dividido 3 da cociente 3 y resto 1.
        if random.random() <= PC:
            punto = random.randint(1, LONG_CROM - 1)    # Punto aleatorio donde se va a cortar el cruce
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]
        else:
            hijo1, hijo2 = padre1.copy(), padre2.copy() # Si no cruzamos, los hijos son iguales a los padres
        
        # Añadimos los 2 hijos generados al array prox_gen
        prox_gen.append(hijo1)
        prox_gen.append(hijo2)
    return prox_gen   # Devuelve los hijos

def mutacion(nuevaPoblacion):
    for ind in nuevaPoblacion:
        if random.random() <= PM:
            punto = random.randint(0, LONG_CROM - 1)     # Elegimos una posición aleatoria entre 0 y la longitud del cromosoma
            ind[punto] = 1 - ind[punto]  # Invierte solo ese bit


# ------------------------------------------------------------------------------


def main():
    menu_ppal()

    # Defino variables para despues el grafico final
    historico_mejor_x = []
    historico_mejor_f = []
    historico_peor_f = []
    historico_promedio_f = []
    registro_generaciones = []

    poblacion = pob_ini()

    for gen in range(GENERACIONES):
        poblacionDecimal = [pasaje(crom) for crom in poblacion]

        mejor_x = max(poblacionDecimal)
        historico_mejor_x.append(mejor_x)
        peor_x = min(poblacionDecimal)
        promedio_x = sum(poblacionDecimal) / len(poblacionDecimal)

        mejor_f = func_obj(mejor_x)
        historico_mejor_f.append(mejor_f)
        peor_f = func_obj(peor_x)
        historico_peor_f.append(peor_f)
        promedio_f = func_obj(promedio_x)
        historico_promedio_f.append(promedio_f)

        print(f"Generación {gen+1:03d}: -> Mejor x: {mejor_x:<{12}}  /    {bin(mejor_x)[2:]}    ///    Peor x: {peor_x:<{12}}  /    ///    Promedio x: {promedio_x:<{12}.2f}")

        registro_generaciones.append({
            "Generación": gen + 1,
            "Mejor x": mejor_x,
            "Mejor x (Bin)": bin(mejor_x)[2:],
            "Peor x": peor_x,
            "Promedio x": promedio_x,
            "f(Mejor x)": mejor_f
        })

        fitnessPob = calculaFitness(poblacion) # Aca tengo los pesos relativos de cada individuo
        if gen < GENERACIONES - 1:
            # Ahora obtengo los que serán padres
            if SELECCION == 'R':
                seleccionados = seleccionRuleta(poblacion, fitnessPob) 
            
            elif SELECCION == 'T':
                seleccionados = seleccionTorneo(poblacion)
            else:
                cantidad_elite = int(LONG_POBLACION*0.2)
                seleccionados = seleccionElitismo(poblacion, fitnessPob, cantidad_elite)
            # En caso de Elitismo, los dos mejores (que están primeros) pasan directo a la nueva generación sin crossover ni mutacion
            if SELECCION == 'E':
                elites = seleccionados[:cantidad_elite]  # Los primeros 20% son los elites
                restantes_crossover = seleccionados[cantidad_elite:]  # Los 80% restantes sí se cruzan y mutan
                hijos = crossover(restantes_crossover, (LONG_POBLACION - cantidad_elite)) # Solo vamos a cruzar el 80%, ya que el 20% restante pasó directamente por elitismo
                mutacion(hijos)    # Muto solo los hijos surgidos del crossover
                poblacion = elites + hijos  # Nueva generación: elites + hijos ya mutados
            else: 
                nuevaPoblacion = crossover(seleccionados, LONG_POBLACION)   # Cruzamos toda la poblacion
                mutacion(nuevaPoblacion)  # Muto los hijos (mi nueva poblacion)
                poblacion = nuevaPoblacion    # Ya tengo mi nueva población (hijos) para la siguiente generacion

    # Para el resumen final (fuera del bucle)
    mejor_x_total = max(historico_mejor_x)
    
    print(f"--------------------------------------------------------------------------------------------")
    print(f"------------------------------------  RESULTADO FINAL  -------------------------------------")
    print(f"--------------------------------------------------------------------------------------------")
    print(f"Máximo x logrado: {mejor_x_total} ({bin(mejor_x_total)[2:]}), que evaluado en f da como resultado: {func_obj(mejor_x_total):.6f}")

    # Guardar resultados en un archivo Excel
    df_resultados = pd.DataFrame(registro_generaciones)
    df_resultados.to_excel("resultados_generaciones.xlsx", index=False)
    print("Los resultados por generación fueron guardados en 'resultados_generaciones.xlsx'")

    # GRAFICAR evolución de f(x) y x
    generaciones = list(range(1, GENERACIONES + 1))

    lienzo, eje = plt.subplots(figsize=(12, 10)) 

    lineamejor = eje.plot(generaciones, historico_mejor_f, label='f(Mejor_x)')[0]
    lineapeor = eje.plot(generaciones, historico_promedio_f, label='f(Promedio_x)')[0]
    lineaprom = eje.plot(generaciones, historico_peor_f, label='f(Peor_x)')[0]
    eje.set_title('Evolución de f(x) por Generación')
    eje.set_xlabel('Generación')
    eje.set_ylabel('Valor de f(x)')
    
    if GENERACIONES == 20:
        eje.set_xticks(range(0, GENERACIONES + 1, 1))
    elif GENERACIONES == 100:
        eje.set_xticks(range(0, GENERACIONES + 1, 10))
    else:
        eje.set_xticks(range(0, GENERACIONES + 1, 20))
    
    eje.legend()
    eje.grid(True)

    plt.tight_layout()

    # Esto permite que al pasar el mouse por los puntos del gráfico te diga el valor exacto
    mplcursors.cursor([lineamejor, lineapeor, lineaprom], hover=True)
    plt.show()


if __name__ == "__main__":
    main()
