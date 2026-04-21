from airports import *
class Aircraft:
    def __init__(self, id, company, origin, timelanding):
        self.id = id
        self.company = company
        self.origin = origin
        self.timelanding = timelanding


def LoadArrivals(filename):
    arrivals_list=[]
    try:
        f = open(filename, "r")
        header=f.readline()
        linea = f.readline()
        while linea!='':
            elementos=linea.split()
            if len(elementos)==4:
                id=elementos[0]
                company=elementos[3]
                origin=elementos[1]
                timelanding=elementos[2]

                aircraft=Aircraft(id, company, origin, timelanding)
                arrivals_list.append(aircraft)
            linea=f.readline()
        f.close()

    except FileNotFoundError:
        print('Error: archivo no encontrado.')

    return arrivals_list


def PlotArrivals(aircrafts):
    import matplotlib.pyplot as plt

    if len(aircrafts)==0:
        print('Error:lista vacía.')
        return

    horas = [0]*24

    i = 0
    while i < len(aircrafts):
        tiempo = aircrafts[i].timelanding
        partes = tiempo.split(':')
        hora = int(partes[0])
        horas[hora] = horas[hora]+1
        i = i+1

    plt.bar(range(24),horas)
    plt.xlabel('Hora')
    plt.ylabel('Vuelos')
    plt.title('Llegadas por hora')
    plt.show()


def SaveFlights(aircrafts, filename):
    if len(aircrafts)==0:
        print('Error: lista vacía.')
        return

    f = open(filename, "w")
    f.write('AIRCRAFT ORIGIN ARRIVAL AIRLINE\n')

    num=0
    while num < len(aircrafts):
        a = aircrafts[num]
        f.write(a.id + ' ' + a.origin + ' ' + a.timelanding + ' ' + a.company + '\n')
        num = num+1
    f.close()

def PlotAirlines(aircrafts):
    import matplotlib.pyplot as plt

    if len(aircrafts)==0:
        print('Error: lista vacía.')
        return

    companies = []
    counts = []

    num=0
    while num < len(aircrafts):
        a = aircrafts[num]
        company = a.company

        encontrado = False
        i=0
        while i < len(companies) and not encontrado:
            if companies[i] == company:
                counts[i] = counts[i]+1
                encontrado = True
            i = i+1

        if not encontrado:
            companies.append(company)
            counts.append(1)

        num = num+1

    # Ordenar de major a menor
    paired = sorted(zip(counts, companies), reverse=True)
    counts, companies = zip(*paired)

    fig, ax = plt.subplots(figsize=(max(10, len(companies) * 0.7), 6))
    bars = ax.bar(range(len(companies)), counts, color='steelblue', edgecolor='white', width=0.6)

    # Etiquetes inclinades 45° per evitar col·lisions
    ax.set_xticks(range(len(companies)))
    ax.set_xticklabels(companies, rotation=45, ha='right', fontsize=8)

    # Valor numèric sobre cada barra
    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.2,
                str(val), ha='center', va='bottom', fontsize=7)

    ax.set_xlabel('Aerolinea')
    ax.set_ylabel('Vols')
    ax.set_title('Vols per aerolinea')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    fig.tight_layout()
    plt.show()


def PlotFlightsType(aircrafts):
    import matplotlib.pyplot as plt

    if len(aircrafts)==0:
        print('Error: lista vacía.')
        return

    Schengen = 0
    NoSchengen = 0

    num=0
    while num < len(aircrafts):
        a = aircrafts[num]
        if IsSchengenAirport(a.origin):
            Schengen = Schengen+1
        else:
            NoSchengen = NoSchengen+1
        num = num+1

    plt.bar(0, Schengen, color='blue', label='Schengen')
    plt.bar(0, NoSchengen, bottom=Schengen, color='red', label='No Schengen')
    plt.title('Vuelos Schengen vs No Schengen')
    plt.ylabel('Vuelos')
    plt.xticks([])
    plt.legend()
    plt.show()


def MapFlights(aircrafts):
    f = open('Flight_map.kml', 'w')

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    #Vuelos Schengen (verde)
    f.write('<Style id="Schengen">\n')
    f.write('  <LineStyle>\n')
    f.write('    <color>ff00ff00</color>\n')
    f.write('  </LineStyle>\n')
    f.write('</Style>\n')

    #Vuelos NoSchengen (rojo)
    f.write('<Style id="NoSchengen">\n')
    f.write('  <LineStyle>\n')
    f.write('    <color>ff0000ff</color>\n')
    f.write('  </LineStyle>\n')
    f.write('</Style>\n')

    #Coordenadas LEBL
    lebl_lon = 2.07833
    lelb_lat = 41.29694

    #Buscar el aeropuerto origen en la lista de aeropuertos
    airports = LoadAirport('Airports.txt')

    num=0
    while num < len(aircrafts):
        a = aircrafts[num]

        #Buscar las coordenadas del aeropuerto origen
        origin_lat = 0.0
        origin_lon = 0.0
        i = 0
        Found = False
        while i < len(airports) and not Found:
            if airports[i].code == a.origin:
                origin_lat = airports[i].latitude
                origin_lon = airports[i].longitude
                Found = True
            i = i+1

        #Dibujar la línea
        f.write('<Placemark>\n')
        f.write('  <name>' + a.id + '</name>\n')
        if IsSchengenAirport(a.origin):
            f.write('  <styleUrl>#Schengen</styleUrl>\n')
        else:
            f.write('  <styleUrl>#NoSchengen</styleUrl>\n')
        f.write('  <LineString>\n')
        f.write('    <coordinates>\n')
        f.write('      ' + str(origin_lon) + ',' + str(origin_lat) + '\n')
        f.write('      ' + str(lebl_lon) + ',' + str(lelb_lat) + '\n')
        f.write('      </coordinates>\n')
        f.write('  </LineString>\n')
        f.write('</Placemark>\n')

        num = num+1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()


def Haversine(lat1, lon1, lat2, lon2):
    import math

    r = 6371 #Radio Tierra en km

    #Convertir a radianes
    lat1 = lat1*math.pi/180
    lon1 = lon1*math.pi/180
    lat2 = lat2*math.pi/180
    lon2 = lon2*math.pi/180

    dlat = lat2-lat1
    dlon = lon2-lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r * c

def LongDistanceArrivals(aircrafts):
    #Coordenadas LEBL
    lebl_lat = 41.29694
    lebl_lon = 2.07833

    airports = LoadAirport('Airports.txt')
    long_distance = []

    num=0
    while num < len(aircrafts):
        a = aircrafts[num]

        #Buscar coordenadas del aeropuerto origen
        i=0
        while i < len(airports):
            if airports[i].code == a.origin:
                origin_lat = airports[i].latitude
                origin_lon = airports[i].longitude
                distancia = Haversine(origin_lat, origin_lon, lebl_lat, lebl_lon)
                if distancia > 2000:
                    long_distance.append(a)
            i = i+1
        num = num+1
    return long_distance



#TEST SECTION
if __name__ == '__main__':
    aircrafts = LoadArrivals('Arrivals.txt')
    print('Vuelos cargados:', len(aircrafts))

    print('TEST PLOT ARRIVALS')
    PlotArrivals(aircrafts)

    print('TEST SAVE FLIGHTS')
    SaveFlights(aircrafts, 'arrivals_output.txt')
    print('Fichero guardado correctamente.')

    print('TEST PLOT AIRLINES')
    PlotAirlines(aircrafts)

    print('TEST PLOT FLIGHTS TYPE')
    PlotFlightsType(aircrafts)

    print('TEST MAP FLIGHTS')
    MapFlights(aircrafts)
    print('Fichero KML generado correctamente.')

    print('LONG DISTANCE ARRIVALS')
    long = LongDistanceArrivals(aircrafts)
    print('Vuelos de larga distancia:', len(long))