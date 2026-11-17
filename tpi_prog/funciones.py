import csv
import questionary
#
def mostrar_menu():
    opcion = questionary.select(
        "Seleccione una operación:",
        choices=[
            "1. Agregar un país (no se permiten campos vacíos)",
            "2. Actualizar población y superficie de un país",
            "3. Buscar un país por nombre (parcial o exacta)",
            "4. Filtrar países (continente / rango de población / rango de superficie)",
            "5. Ordenar países (nombre / población / superficie asc-desc)",
            "6. Mostrar estadísticas",
            "7. Salir"
        ]
    ).ask()
    return opcion

def cargar_paises(nombre_archivo):
    paises = []
    try:
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    pais = {
                        "nombre": fila["nombre"],
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"]
                    }
                    paises.append(pais)
                except ValueError:
                    print(f"Error en la fila: {fila}. Datos inválidos.")
    except FileNotFoundError:
        print(f"¡ERROR! No se encontró el archivo '{nombre_archivo}'.")
    return paises

def guardar_paises(nombre_archivo, paises):
    try:
        with open(nombre_archivo, mode="w", encoding="utf-8", newline="") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(paises)
    except Exception as e:
        print(f" Error al guardar: {e}")

def agregar_pais(paises):
    print("\n--- Agregar nuevo país ---")
    nombre = questionary.text("Nombre del país:").ask()
    if not nombre or not nombre.strip():
        print(" El nombre no puede estar vacío.")
        return
    for p in paises:
        if p["nombre"].lower() == nombre.strip().lower():
            print(f" El país '{nombre}' ya existe.")
            return
    poblacion = questionary.text(
        "Población:",
        validate=lambda x: x.isdigit() or "Ingresá un número válido"
    ).ask()
    if not poblacion:
        print(" La población no puede estar vacía.")
        return
    superficie = questionary.text(
        "Superficie (km²):",
        validate=lambda x: x.isdigit() or "Ingresá un número válido"
    ).ask()
    if not superficie:
        print(" La superficie no puede estar vacía.")
        return
    continente = questionary.select(
        "Continente:",
        choices=["América", "Europa", "Asia", "África", "Oceanía"]
    ).ask()
    if not continente:
        print(" El continente no puede estar vacío.")
        return
    nuevo = {
        "nombre": nombre.strip().title(), 
        "poblacion": int(poblacion),
        "superficie": int(superficie),
        "continente": continente
    }
    paises.append(nuevo)
    print(f" País '{nuevo['nombre']}' agregado correctamente.")
    
def actualizar_poblacion_superficie(paises):
    nombre_buscado = input("Nombre del país a actualizar: ").strip().title()

    for pais in paises:
        if pais["nombre"].lower() == nombre_buscado.lower():
            print(f"Población actual de {pais['nombre']}: {pais['poblacion']}, superficie: {pais['superficie']}")
            nuevapob = input("Nueva población: ").strip()
            nuevasup = input("Nueva superficie: ").strip()
            if nuevapob == "" or nuevasup == "":
                print(" No puedes dejar los campos vacíos.")
                return

            try:
                pais["poblacion"] = int(nuevapob)
                pais["superficie"] = int(nuevasup)
                print(f"Población de {pais['nombre']} actualizada a {pais['poblacion']}.")
                print(f"Superficie de {pais['nombre']} actualizada a {pais['superficie']}.")
            except ValueError:
                print(" La población/superficie debe ser un número.")
            return 

    print(f" No se encontró el país '{nombre_buscado}'.")

def buscar_pais(paises):
    nombre_buscado = input("Nombre del país a buscar: ").strip()
    

    while nombre_buscado == "" or not nombre_buscado.replace(" ", "").isalpha():
        print("El nombre a buscar no puede estar vacío ni contener números.")
        nombre_buscado = input("Nombre del país a buscar: ").strip()
        
    encontrado = False
    print("\n--- Resultados de la búsqueda ---")
    
    
    for pais in paises:
        if nombre_buscado.lower() in pais["nombre"].lower():
            print(f"País encontrado: {pais['nombre']} (Población: {pais['poblacion']}, Continente: {pais['continente']})")
            encontrado = True

    if not encontrado:
        print(f"No se encontraron países que coincidan con '{nombre_buscado}'.")

def filtrar_paises(paises):
    opcion = questionary.select(
        "Filtrar paises por:",
        choices=[
            "1. Continente",
            "2. Rango de Población",
            "3. Rango de Superficie"
        ]
    ).ask()
    if not opcion: 
        return
    if opcion.startswith("1"):
        continente_elegido = questionary.select(
            "Elige el continente:",
            choices=["América", "Europa", "Asia", "África", "Oceanía"]
        ).ask()
        if not continente_elegido:
            return
        encontrado = False
        print(f"\n--- Países en {continente_elegido} ---")
        for pais in paises:
            if pais["continente"].lower() == continente_elegido.lower():
                print(f"- {pais['nombre']} (Población: {pais['poblacion']})")
                encontrado = True
        if not encontrado:
            print(f"No se encontraron países en '{continente_elegido}'.")
    elif opcion.startswith("2"):
        min_str = questionary.text("Población MÍNIMA:", validate=lambda x: x.isdigit() or "Número inválido").ask()
        max_str = questionary.text("Población MÁXIMA:", validate=lambda x: x.isdigit() or "Número inválido").ask()
        if min_str is None or max_str is None:
            return
        min_pob = int(min_str)
        max_pob = int(max_str)
        encontrado = False
        print(f"\n--- Países con población entre {min_pob} y {max_pob} ---") 
        for pais in paises:
            if min_pob <= pais["poblacion"] <= max_pob:
                print(f"- {pais['nombre']} ({pais['poblacion']})")
                encontrado = True
        if not encontrado:
            print("No hay países en ese rango.")
    elif opcion.startswith("3"):
        min_str = questionary.text("Superficie MÍNIMA:", validate=lambda x: x.isdigit() or "Número inválido").ask()
        max_str = questionary.text("Superficie MÁXIMA:", validate=lambda x: x.isdigit() or "Número inválido").ask()

        if min_str is None or max_str is None:
            return

        min_sup = int(min_str)
        max_sup = int(max_str)

        encontrado = False
        print(f"\n--- Países con superficie entre {min_sup} y {max_sup} ---")
        for pais in paises:
            if min_sup <= pais["superficie"] <= max_sup:
                print(f"- {pais['nombre']} ({pais['superficie']} km²)")
                encontrado = True

        if not encontrado:
            print("No hay países en ese rango.")

def ordenar_paises(paises):
    opcion = questionary.select(
            "Ordenar paises por:",
            choices=[
                "1. Continente",
                "2. Población",
                "3. Superficie asc-desc",
            ]
        ).ask()
    if not opcion: 
        return
    if opcion.startswith("1"):
        paises_ordenados = sorted(paises, key=lambda p: p["continente"])

        for pais in paises_ordenados:
            print(f"{pais['continente']} - {pais['nombre']}")
    elif opcion.startswith("2"):
        orden = questionary.select(
            "¿En qué orden?",
            choices=[
                "1. Ascendente (menor a mayor)",
                "2. Descendente (mayor a menor)"
            ]
        ).ask()
        if not orden:
            return
        es_reversa = orden.startswith("2")
        paises_ordenados = sorted(paises, key=lambda p: p["poblacion"], reverse=es_reversa)

        print(f"\n--- Países ordenados por Población ({'Desc' if es_reversa else 'Asc'}) ---")
        for pais in paises_ordenados:
            print(f"- {pais['nombre']}: {pais['poblacion']} hab.")     
    elif opcion.startswith("3"):
        orden = questionary.select(
            "¿En qué orden?",
            choices=[
                "1. Ascendente (menor a mayor)",
                "2. Descendente (mayor a menor)"
            ]
        ).ask()
        if not orden:
            return
        es_reversa = orden.startswith("2")
        paises_ordenados = sorted(paises, key=lambda p: p["superficie"], reverse=es_reversa)

        print(f"\n--- Países ordenados por Superficie ({'Desc' if es_reversa else 'Asc'}) ---")
        for pais in paises_ordenados:
            print(f"- {pais['nombre']}: {pais['superficie']} km²")
            
def mostrar_estadisticas(paises):
    if not paises:
        print(" No hay países cargados para calcular estadísticas.")
        return
    print("\n--- 📊 ESTADÍSTICAS ---")
    pais_max = max(paises, key=lambda p: p["poblacion"])
    pais_min = min(paises, key=lambda p: p["poblacion"])
    
    print(f"👑 Mayor población: {pais_max['nombre']} ({pais_max['poblacion']} hab.)")
    print(f"🐜 Menor población: {pais_min['nombre']} ({pais_min['poblacion']} hab.)")

    cantidad_paises = len(paises)
    suma_poblacion = sum(p["poblacion"] for p in paises)
    suma_superficie = sum(p["superficie"] for p in paises)

    promedio_pob = suma_poblacion / cantidad_paises
    promedio_sup = suma_superficie / cantidad_paises
    print(f"📈 Promedio de población: {promedio_pob:.2f} hab.")
    print(f"📈 Promedio de superficie: {promedio_sup:.2f} km²")

    print("\n🌍 Cantidad de países por continente:")
    conteo_continentes = {}
    for pais in paises:
        cont = pais["continente"]
        conteo_continentes[cont] = conteo_continentes.get(cont, 0) + 1

    for continente, cantidad in conteo_continentes.items():
        print(f"- {continente}: {cantidad} país(es)")