import sys

sys.setrecursionlimit(100000)

DIR_PRUEBAS = "Pruebas/"


def ganar_siempre(monedas):
    n = len(monedas)
    """
    Matriz de tamaño n x n, donde n es la cantidad de monedas. Almacena el valor máximo que Sophia 
    puede obtener si solo tuviera acceso a las monedas en el rango [i:j+1].

    """
    memo = [[-1] * n for _ in range(n)]

    elecciones = []

    """
    Las variables i, j representan los índices de las monedas que se están considerando en un turno
    de Sophia. 'i' representa el índice de la moneda en la parte izquierda y 'j' representa el
    índice de la moneda en la parte derecha.
    Ej: [4, 5, 9, 2] => i = 0 es la moneda de 4 y j = 3 es la de valor 2. 
    Los valores 'i' y 'j' cambian de acuerdo a la decisión que tome Sophia. Si Sophia elige la
    moneda izquierda, se suma 1 a 'i', si toma la moneda derecha, se resta 1 a 'j'.
    """

    def dp(i, j):
        if i > j:
            return 0

        if memo[i][j] != -1:
            # Ya fue calculado previamente, retorno el valor memorizado
            return memo[i][j]

        """Calculo la ganancia máxima que Sophia puede obtener si el arreglo fuera [i:j+1]"""
        # Sophia elige la moneda del extremo izquierdo (monedas[i]), entonces ahora Matheo va a
        # elegir de forma Greedy entre la moneda [i+1] y la [j].
        if monedas[i + 1] >= monedas[j]:
            # Mateo va a elegir la moneda izquierda que quedó [i+1] => la opcion1 va a ser:
            # lo que Sophia eligió ahora + la solución óptima del problema [i+2:j+1].
            # Esto es porque en esta opción, Sophia eligió la moneda i y Mateo agarró la moneda i+1
            opcion1 = monedas[i] + dp(i + 2, j)
        else:
            # La moneda derecha [j] es más grande, Mateo va a seleccionar esa
            opcion1 = monedas[i] + dp(i + 1, j - 1)

        # Sophia elige la moneda del extremo derecho (monedas[j]), entonces ahora Matheo va a
        # elegir de forma Greedy entre la moneda [i] y la [j-1].
        if monedas[i] >= monedas[j - 1]:
            # La moneda izquierda es más grande, Mateo va a elegir esa.
            opcion2 = monedas[j] + dp(i + 1, j - 1)
        else:
            # La moneda derecha es más grande, Mateo va a elegir esa.
            opcion2 = monedas[j] + dp(i, j - 2)

        # Guardar el resultado en la tabla memo
        memo[i][j] = max(opcion1, opcion2)
        return memo[i][j]

    def reconstruir_elecciones(i, j):
        """
        Inicialmente i = 0 y j = len(monedas) - 1. Se simula el juego usando la información
        almacenada en memo.
        """

        while i <= j:
            # Verifico qué opción escogió Sophia al comparar el valor en memo

            # Sofia elije la primer moneda [i].
            # Los ifs revisan que decisión va a tomar Mateo luego de esto.
            if monedas[i + 1] >= monedas[j]:
                # Mateo elije la moneda de la izquierda en el siguiente turno. El puntaje de Sophia
                # va a ser la moneda [i] seleccionada más la solución óptima encontrada para las
                # monedas restantes [i+2:j+1].
                # Si el memo se fue de rango, retorno 0.
                opcion1 = monedas[i] + (memo[i + 2][j] if i + 2 <= j else 0)
            else:
                # Ahora Mateo elige la moneda de la izquierda.
                opcion1 = monedas[i] + (memo[i + 1][j - 1] if i + 1 <= j - 1 else 0)

            # Sofia elije la última moneda [j].
            if monedas[i] >= monedas[j - 1]:
                # Mateo elige la moneda de la izquierda en el siguiente turno
                opcion2 = monedas[j] + (memo[i + 1][j - 1] if i + 1 <= j - 1 else 0)
            else:
                # Mateo elige la moneda de la derecha
                opcion2 = monedas[j] + (memo[i][j - 2] if i <= j - 2 else 0)

            # Nos quedamos con la mejor elección
            if opcion1 >= opcion2:
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[i]})")
                i += 1
            else:
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[j]})")
                j -= 1

            if i <= j:  # Siguen quedando monedas.
                # Mateo selecciona de forma greedy
                if monedas[i] >= monedas[j]:
                    elecciones.append(f"Mateo agarra la primera ({monedas[i]})")
                    i += 1
                else:
                    elecciones.append(f"Mateo agarra la ultima ({monedas[j]})")
                    j -= 1

    puntaje_sophia = dp(0, n - 1)
    puntaje_mateo = sum(monedas) - puntaje_sophia

    reconstruir_elecciones(0, n - 1)

    return puntaje_sophia, puntaje_mateo, "; ".join(elecciones)


def main():
    if len(sys.argv) > 1:
        nombre_archivo = sys.argv[1]
    else:
        nombre_archivo = input("Por favor ingrese el nombre de su set de datos: ")

    with open(DIR_PRUEBAS + nombre_archivo) as archivo:
        archivo.readline()
        monedas = [int(moneda) for moneda in archivo.readline().split(";")]
        puntaje_sophia, puntaje_mateo, elecciones = ganar_siempre(monedas)

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
