import sys

DIR_PRUEBAS = "Pruebas/"


def maximizar_ganancia(monedas):
    n = len(monedas)
    mem = [[-1] * n for _ in range(n)]
    elecciones = []

    # Llenar la tabla mem de forma iterativa (bottom-up)
    for largo_subarreglo in range(1, n + 1):  # largo_subarreglo es el tamaño del subarreglo que estamos evaluando
        for i in range(n - largo_subarreglo + 1): # i es el inicio del subarreglo
            j = i + largo_subarreglo - 1  # j es el final del subarreglo

            if i == j: # Caso base: una moneda
                mem[i][j] = monedas[i]  # Solo una moneda, Sophia la toma
            else:
                # Si Sophia toma la moneda en la posición i
                opcion_izq = monedas[i] + min(mem[i+2][j] if i+2 <= j else 0, mem[i+1][j-1] if i+1 <= j-1 else 0)
                # Si Sophia toma la moneda en la posición j
                opcion_der = monedas[j] + min(mem[i][j-2] if i <= j-2 else 0, mem[i+1][j-1] if i+1 <= j-1 else 0)
                mem[i][j] = max(opcion_izq, opcion_der)

    # Reconstrucción de las decisiones de Sophia y Mateo
    def reconstruir_elecciones(i, j):
        while i <= j:
            # Revisar si Sophia eligió la primera o la última moneda
            # Comparamos las opciones basándonos en lo que calculamos en mem
            opcion_izq = monedas[i] + min(mem[i+2][j] if i+2 <= j else 0, mem[i+1][j-1] if i+1 <= j-1 else 0)
            opcion_der = monedas[j] + min(mem[i][j-2] if i <= j-2 else 0, mem[i+1][j-1] if i+1 <= j-1 else 0)

            if mem[i][j] == opcion_izq:
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[i]})")
                i += 1
            else:
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[j]})")
                j -= 1
            
            # Ahora es el turno de Mateo
            if i <= j:
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
