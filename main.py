import sys

sys.setrecursionlimit(100000)

DIR_PRUEBAS = "Pruebas/"


def ganar_siempre(monedas):
    n = len(monedas)
    memo = [[-1] * n for _ in range(n)]
    
    elecciones = []
    
    def dp(i, j):
        if i > j:
            return 0
        if memo[i][j] != -1:
            return memo[i][j]
        
        # Si Sophia elige monedas[i]
        if monedas[i+1] >= monedas[j]:
            opcion1 = monedas[i] + dp(i+2, j)
        else:
            opcion1 = monedas[i] + dp(i+1, j-1)
        
        # Si Sophia elige monedas[j]
        if monedas[i] >= monedas[j-1]:
            opcion2 = monedas[j] + dp(i+1, j-1)
        else:
            opcion2 = monedas[j] + dp(i, j-2)
        
        # Guardar el resultado en la tabla memo
        memo[i][j] = max(opcion1, opcion2)
        return memo[i][j]

    def reconstruir_elecciones(i, j):
        while i <= j:
            # Verificar qué opción escogió Sophia al comparar el valor en memo
            if monedas[i+1] >= monedas[j]:
                opcion1 = monedas[i] + (memo[i+2][j] if i+2 <= j else 0)
            else:
                opcion1 = monedas[i] + (memo[i+1][j-1] if i+1 <= j-1 else 0)
            
            if monedas[i] >= monedas[j-1]:
                opcion2 = monedas[j] + (memo[i+1][j-1] if i+1 <= j-1 else 0)
            else:
                opcion2 = monedas[j] + (memo[i][j-2] if i <= j-2 else 0)

            # Sophia elige la mejor opción
            if opcion1 >= opcion2:
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
    
    puntaje_sophia = dp(0, n-1)
    puntaje_mateo = sum(monedas) - puntaje_sophia

    reconstruir_elecciones(0, n-1)

    return puntaje_sophia, puntaje_mateo,  "; ".join(elecciones)


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
