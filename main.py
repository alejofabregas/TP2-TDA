import sys

DIR_PRUEBAS = "Pruebas/"


def maximizar_ganancia(monedas):
    n = len(monedas)
    """
    Matriz de tamaño n x n, donde n es la cantidad de monedas. Almacena el valor máximo que Sophia 
    puede obtener si solo tuviera acceso a las monedas en el rango [i:j] (subproblema de tamaño menor).
    """
    mem = [[-1] * n for _ in range(n)]
    elecciones = []

    """
    Las variables i, j representan los índices de las monedas que se están considerando en un turno
    de Sophia. 'i' representa el índice de la moneda en la parte izquierda y 'j' representa el
    índice de la moneda en la parte derecha.
    Ej: [4, 5, 9, 2] => i = 0 es la moneda de 4 y j = 3 es la de valor 2. 
    Los valores 'i' y 'j' cambian de acuerdo a la decisión que tome Sophia. Si Sophia elige la
    moneda izquierda, se suma 1 a 'i', si toma la moneda derecha, se resta 1 a 'j'.
    """
    # Llenar la tabla mem de forma iterativa (bottom-up)
    for largo_subarreglo in range(1, n + 1):  # largo_subarreglo es el tamaño del subarreglo que estamos evaluando
        for i in range(n - largo_subarreglo + 1): # i es el inicio del subarreglo
            j = i + largo_subarreglo - 1  # j es el final del subarreglo

            # Caso base: una sola moneda.
            # Como Sophia elige primero, la toma y gana siempre.
            if i == j:
                mem[i][j] = monedas[i]  # Solo una moneda, Sophia la toma
            # Caso base: dos monedas
            # Como Sophia elige primero, toma la mayor y gana siempre.
            elif i + 1 == j:
                mem[i][j] = max(monedas[i], monedas[j]) # Dos monedas, Sophia toma la mayor
            else:
                """Calculo la ganancia máxima que Sophia puede obtener si el arreglo fuera [i:j]"""
                # Sophia elige la moneda del extremo izquierdo (monedas[i]), entonces ahora Mateo va a
                # elegir de forma Greedy entre la moneda izquierda [i+1] y la derecha [j].
                # Por eso, Sophia se queda con la mínima entre ambas.
                opcion_izq_izq = monedas[i] + mem[i+2][j] if monedas[i+1] >= monedas[j] and i+2 <= j else 0
                opcion_izq_der = monedas[i] + mem[i+1][j-1] if monedas[i+1] < monedas[j] and i+1 <= j-1 else 0
                opcion_izq = max(opcion_izq_izq, opcion_izq_der)
                
                # Sophia elige la moneda del extremo derecho (monedas[j]), entonces ahora Matheo va a
                # elegir de forma Greedy entre la moneda izquierda [i] y la derecha [j-1].
                # Por eso, Sophia se queda con la mínima entre ambas.
                opcion_der_der = monedas[j] + mem[i][j-2] if monedas[i] < monedas[j-1] and i <= j-2 else 0
                opcion_der_izq = monedas[j] + mem[i+1][j-1] if monedas[i] >= monedas[j-1] and i+1 <= j-1 else 0
                opcion_der = max(opcion_der_der, opcion_der_izq)
                
                mem[i][j] = max(opcion_izq, opcion_der)

    # Reconstrucción de las decisiones de Sophia y Mateo
    def reconstruir_elecciones(i, j):
        while i <= j:
            # Verifico qué moneda eligió Sophia al comparar el valor en memo
            # Calculamos las opciones igual que antes y vemos cuál se utilizó en memo
            opcion_izq_izq = monedas[i] + mem[i+2][j] if monedas[i+1] >= monedas[j] and i+2 <= j else 0
            opcion_izq_der = monedas[i] + mem[i+1][j-1] if monedas[i+1] < monedas[j] and i+1 <= j-1 else 0
            opcion_izq = max(opcion_izq_izq, opcion_izq_der)
            
            opcion_der_der = monedas[j] + mem[i][j-2] if monedas[i] < monedas[j-1] and i <= j-2 else 0
            opcion_der_izq = monedas[j] + mem[i+1][j-1] if monedas[i] >= monedas[j-1] and i+1 <= j-1 else 0
            opcion_der = max(opcion_der_der, opcion_der_izq)

            if mem[i][j] == opcion_der:
                # Se eligió la moneda del lado derecho
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[j]})")
                j -= 1
            else:
                # Se eligió la moneda del lado izquierdo
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[i]})")
                i += 1
            
            if i <= j: # Siguen quedando monedas.
                # Mateo selecciona de forma greedy
                if monedas[i] >= monedas[j]:
                    elecciones.append(f"Mateo agarra la primera ({monedas[i]})")
                    i += 1
                else:
                    elecciones.append(f"Mateo agarra la ultima ({monedas[j]})")
                    j -= 1

    puntaje_sophia = mem[0][n-1]
    puntaje_mateo = sum(monedas) - puntaje_sophia

    # Reconstruir la secuencia de decisiones
    reconstruir_elecciones(0, n-1)

    return puntaje_sophia, puntaje_mateo, "; ".join(elecciones)


def main():
    if len(sys.argv) > 1:
        nombre_archivo = sys.argv[1]
    else:
        nombre_archivo = input("Por favor ingrese el nombre de su set de datos: ")

    with open(DIR_PRUEBAS + nombre_archivo) as archivo:
        archivo.readline()
        monedas = [int(moneda) for moneda in archivo.readline().split(";")]
        puntaje_sophia, puntaje_mateo, elecciones = maximizar_ganancia(monedas)

        print(f"\n--- {nombre_archivo} ---")
        print(elecciones)
        print(f"Total monedas: {sum(monedas)}")
        print(f"Puntaje Sophia: {puntaje_sophia} - Puntaje Mateo: {puntaje_mateo}")

        # Comparar ganancia de Sophia
        total_monedas = sum(monedas)
        assert (
            puntaje_sophia + puntaje_mateo == total_monedas
        ), f"Error en {nombre_archivo}: la suma de puntajes ({puntaje_sophia + puntaje_mateo}) no coincide con el total de las monedas ({total_monedas})."

        assert (
            puntaje_sophia >= puntaje_mateo
        ), f"Error en {nombre_archivo}: Puntaje de Sophia ({puntaje_sophia}) es menor que el de Mateo ({puntaje_mateo})."

        print(f"Prueba {nombre_archivo} exitosa.")


if __name__ == "__main__":
    main()
