from airport import *
class Aircraft:
    def __init__(self, id, company, origin, timelanding, destination, departure):
        self.id = id
        self.company = company
        self.origin = origin
        self.timelanding = timelanding
        self.destination = destination
        self.departure = departure


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

                aircraft=Aircraft(id, company, origin, timelanding, '', '')
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

    #Buscar todas las compañías y contar sus vuelos
    companies = []
    counts = []

    num=0
    while num < len(aircrafts):
        a = aircrafts[num]
        company = a.company

        #Buscar si la companía ya está en la lista
        encontrado = False
        i=0
        while i < len(companies) and not encontrado:
            if companies[i] == company:
                counts[i] = counts[i]+1
                encontrado = True

            i = i+1

        #Añadirla si no estaba
        if not encontrado:
            companies.append(company)
            counts.append(1)

        num = num+1

    plt.bar(range(len(companies)), counts)
    plt.xticks(range(len(companies)), companies)
    plt.xlabel('Compañía')
    plt.ylabel('Vuelos')
    plt.title('Vuelos por compañía')
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
        encontrado = False
        while i < len(airports) and not encontrado:
            if airports[i].code == a.origin:
                origin_lat = airports[i].latitude
                origin_lon = airports[i].longitude
                encontrado = True
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

# --- FUNCIONES VERSIÓN 4 ---

def LoadDepartures(filename):
    departures_list=[]
    try:
        f = open(filename, "r")
        header=f.readline()
        linea=f.readline()
        while linea!='':
            elementos=linea.split()
            if len(elementos)==4:
                id=elementos[0]
                company=elementos[3]
                destination=elementos[1]
                departure=elementos[2]

                aircraft=Aircraft(id, company, '', '', destination, departure)
                departures_list.append(aircraft)
            linea=f.readline()
        f.close()

    except FileNotFoundError:
        print('Error: archivo no encontrado.')

    return departures_list


def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 or len(departures) == 0:
        print('Error: alguna lista está vacía.')
        return[]
    merged_list = []

    #Lista vacía donde guardaremos las posiciones de las salidas que ya usamos
    posiciones_salidas_usadas = []

    # 1. Buscar correspondencias para cada llegada
    num_arr = 0
    while num_arr < len(arrivals):
        a_arr = arrivals[num_arr]
        encontrado = False
        num_dep = 0
        while num_dep < len(departures) and not encontrado:
            a_dep = departures[num_dep]

            #Miramos si ya hemos usado esta posición de salida
            ya_usada = False
            k = 0
            while k < len(posiciones_salidas_usadas):
                if posiciones_salidas_usadas[k] == num_dep:
                    ya_usada = True
                k = k+1

            #Si tienen el mismo ID y la salida NO ha sido usada
            if a_arr.id == a_dep.id and not ya_usada:

                #Comprobar que la hora de llegada sea anterior o igual a la de salida
                partes_arr = a_arr.timelanding.split(':')
                partes_dep = a_dep.departure.split(':')

                h_arr = int(partes_arr[0])
                m_arr = int(partes_arr[1])
                h_dep = int(partes_dep[0])
                m_dep = int(partes_dep[1])

                if (h_arr < h_dep) or (h_arr == h_dep and m_arr <= m_dep):
                    a_arr.destination = a_dep.destination
                    a_arr.departure = a_dep.departure

                    merged_list.append(a_arr)

                    #Guardamos la posición para no volver a usarla
                    posiciones_salidas_usadas.append(num_dep)
                    encontrado = True

            num_dep = num_dep+1

        #Si recorremos todas las salidas y ninguna coincide, se añade solo como llegada
        if not encontrado:
            merged_list.append(a_arr)

        num_arr =  num_arr+1

    # 2. Añadir las salidas de aviones que ya estaban en el aeropuerto
    num_dep = 0
    while num_dep < len(departures):

        #Comprobamos si esta posición fue usada en el bloque anterior
        fue_usada = False
        k = 0
        while k < len(posiciones_salidas_usadas):
            if posiciones_salidas_usadas[k] == num_dep:
                fue_usada = True
            k = k+1

        #Si no se ha usado significa que el avión pernocta
        if not fue_usada:
            merged_list.append(departures[num_dep])

        num_dep = num_dep+1

    return merged_list


def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        print('Error: la lista de aeronaves está vacía.')
        return[]  #Devolvemos lista vacía

    night_list = []

    num = 0
    while num < len(aircrafts):
        a = aircrafts[num]
        if a.timelanding == '' and a.departure != '':
            night_list.append(a)

        num = num+1

    return night_list


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
