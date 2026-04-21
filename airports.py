from tkinter import filedialog

class Airport:
    def __init__(self, code, latitude, longitude):
        self.code = code
        self.latitude = latitude
        self.longitude = longitude
        self.isSchengen = False

# Mira si l'aeroport es Schengen
def IsSchengenAirport(code):
    if not code or len(code)<2:
        return False
    schengen_prefixes=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH','BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES','LS']
    prefix=code[:2]
    if prefix in schengen_prefixes:
        return True
    else:
        return False

# Rep si es schengen o no i diu si es true o false
def SetSchengen(airport):
    result=IsSchengenAirport(airport.code)
    if result == True:
        airport.isSchengen=True
    else:
        airport.isSchengen=False

# Fica en la consola aeroport
def PrintAirport(airport):
    print("Datos del Aeropuerto:")
    print("Código ICAO:", airport.code)
    print("Latitude:", airport.latitude)
    print("Longitude:", airport.longitude)
    print("Schengen:", airport.isSchengen)


def LoadAirport(archivo_entrada):
    airports_list=[]
    try:
        F=open(archivo_entrada, "r")    #Obrir arxiu
        header=F.readline()
        linea=F.readline()
        while linea!="":
            elementos = linea.split()
            if len(elementos)>=3:
                # Codi aeroport
                code=elementos[0]
                letras=code.split()
                country=letras[0:1]

                #Convertir latitud
                lat=elementos[1]
                #Extraer los trozos
                lat_grados=float(lat[1:3])
                lat_min=float(lat[3:5])
                lat_seg=float(lat[5:7])

                lat_decimal=lat_grados+lat_min/60+lat_seg/3600
                if lat[0]=="S":           #Si es sud la latitud es negativa
                    lat_decimal=-lat_decimal

                #Convertir longitud
                lon=elementos[2]

                lon_grados=float(lon[1:4])
                lon_min=float(lon[4:6])
                lon_seg=float(lon[6:8])

                lon_decimal=lon_grados+lon_min/60+lon_seg/3600
                if lon[0]=="W":       #Si es oest (west) la longitud es negativa
                    lon_decimal=-lon_decimal

                    #Crear aeroport
            airport = Airport(code, lat_decimal, lon_decimal)

                    # Asignar Schengen
            SetSchengen(airport)

                    # Afegir a la llista
            airports_list.append(airport)

            linea = F.readline()

        F.close()

    except FileNotFoundError:
        print("Error: archivo no encontrado")


    return airports_list


# Guarde schengen en arxiugg
def SaveSchengenAirports(airports, archivo_salida):
    try:
        F=open(archivo_salida, "w")
        F.write('SHENGEN AIRPORTS (CODE LATITUDE LONGITUDE):\n')

        for airport in airports:
            if airport.isSchengen:
                F.write(f"{airport.code} {airport.latitude} {airport.longitude}\n")

        F.close()

    except:
        print("Error al guardar el archivo")


# Fa la grafica dels aeroports
def PlotAirports(airports):
    import matplotlib.pyplot as plt

    schengen_count = 0
    non_schengen_count = 0

    for airport in airports:
        if airport.isSchengen:
            schengen_count = schengen_count + 1
        else:
            non_schengen_count = non_schengen_count + 1

    plt.bar(0, schengen_count, color='blue', label='Schengen')
    plt.bar(0, non_schengen_count, bottom=schengen_count, color='red', label='No Schengen')

    plt.title("Schengen airports")
    plt.ylabel("Count")
    plt.xlabel("Airports")
    plt.xticks([])
    plt.legend()
    plt.show()

# Fa mapa d'aeroports
def MapAirports(airports):
    filepath = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("KML files", "*.kml"), ("All files", "*.*")],
        initialfile="Airp_map.kml",
        title="Desa el mapa d'aeroports"
    )

    # Si l'usuari tanca el diàleg sense escollir, filepath és ""
    if not filepath:
        return False

    F = open(filepath, 'w')

    # Escriu el format del kml per google earth
    F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    F.write('<kml xmlns="http://www.opengis.net/kml/2.2"\n>')
    F.write('<Document>')

    # Estil airp Schengen (Verd)
    F.write('<Style id="schengen">\n')
    F.write('  <IconStyle>\n')
    F.write('    <color>ff00ff00</color>\n')
    F.write('  </IconStyle>\n')
    F.write('</Style>\n')

    # Estil airp NO Schengen (vermell)
    F.write('<Style id="no_schengen">\n')
    F.write('  <IconStyle>\n')
    F.write('    <color>ff0000ff</color>\n')
    F.write('  </IconStyle>\n')
    F.write('</Style>\n')

    # Un punto por cada aeropuerto
    for airport in airports:
        F.write('<Placemark>\n')
        F.write('  <name>' + airport.code + '</name>\n')

        if airport.isSchengen:
            F.write('  <styleUrl>#schengen</styleUrl>\n')
        else:
            F.write('  <styleUrl>#no_schengen</styleUrl>\n')

        F.write('  <Point>\n')
        F.write('    <coordinates>\n')
        F.write('      ' + str(airport.longitude) + ',' + str(airport.latitude) + '\n')
        F.write('    </coordinates>\n')
        F.write('  </Point>\n')
        F.write('</Placemark>\n')

    # Cierre del archivo KML
    F.write('</Document>\n')
    F.write('</kml>\n')

    F.close()
    return True

def RemoveAirport(airports, code):
    for airport in airports:
        if airport.code == code:
            airports.remove(airport)
            print("Airport " + code + " removed.")
            return
    print("Error: airport " + code + " not found.")