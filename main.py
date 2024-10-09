import sys

DIR_PRUEBAS = "Pruebas/"


# Además de los puntajes, debería devolver qué monedas va agarrando cada uno.
def ganar_siempre(monedas):
    
    return 0, 0


def main():
    if len(sys.argv) > 1:
        nombre_archivo = sys.argv[1]
    else:
        nombre_archivo = input("Por favor ingrese el nombre de su set de datos: ")

    with open(DIR_PRUEBAS + nombre_archivo) as archivo:
        archivo.readline()
        monedas = [int(moneda) for moneda in archivo.readline().split(";")]
        puntaje_sophia, puntaje_mateo = ganar_siempre(monedas)

        print(f"\n--- {nombre_archivo} ---")
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
