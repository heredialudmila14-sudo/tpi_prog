
from funciones import (
    mostrar_menu, cargar_paises, guardar_paises,
    agregar_pais, actualizar_poblacion_superficie, 
    buscar_pais, filtrar_paises, ordenar_paises, 
    mostrar_estadisticas
)

def main():

    paises = cargar_paises("paises.csv")

    while True:
        opcion = mostrar_menu()
 
        if not opcion: 
            break
 
        if opcion.startswith("1"):
            agregar_pais(paises)
            guardar_paises("paises.csv", paises)  
            
        elif opcion.startswith("2"):
            actualizar_poblacion_superficie(paises)
            guardar_paises("paises.csv", paises)  
            
        elif opcion.startswith("3"):
            buscar_pais(paises)  
            
        elif opcion.startswith("4"):
            filtrar_paises(paises)  
            
        elif opcion.startswith("5"):
            ordenar_paises(paises)  
            
        elif opcion.startswith("6"):
            mostrar_estadisticas(paises)  
        elif opcion.startswith("7"):
            print("👋 ¡Hasta luego!")
            break 

if __name__ == "__main__":
    main()