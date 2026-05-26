from aircraft import *
from airport import *


# ─────────────────────────────────────────────
#  Classes
# ─────────────────────────────────────────────

class Gate:
    def __init__(self):
        self.name    = ""
        self.ocupado = False   # True = gate is occupied
        self.id      = ""      # aircraft id when occupied


class BoardingArea:
    def __init__(self):
        self.area     = ""     # letter, e.g. "A"
        self.schengen = False  # True = Schengen, False = non-Schengen
        self.gates    = []


class Terminal:
    def __init__(self):
        self.number        = ""   # e.g. "T1"
        self.BoardingAreas = []
        self.airlines      = []   # list of (airline_name, ICAO_code)


class BarcelonaAP:
    def __init__(self):
        self.CompleteName = ""
        self.Terminals    = []


# ─────────────────────────────────────────────
#  Functions
# ─────────────────────────────────────────────

def SetGates(area, init_gate, end_gate, prefix):
    """
    Fills area.gates with Gate objects named prefix+number.
    Returns -1 if end_gate <= init_gate (invalid range).
    """
    if end_gate <= init_gate:
        return -1
    area.gates = []
    i = init_gate
    while i <= end_gate:
        gate         = Gate()
        gate.name    = prefix + str(i)
        gate.ocupado = False
        gate.id      = ""
        area.gates.append(gate)
        i = i + 1


def LoadAirlines(terminal, t_name):
    """
    Reads {t_name}_Airlines.txt and fills terminal.airlines.
    Each line: "Airline Name<TAB>ICAO_code"
    Returns -1 if file does not exist.
    """
    filename = t_name + "_Airlines.txt"
    try:
        f = open(filename, "r")
    except OSError:
        return -1
    terminal.airlines = []
    for line in f:
        line = line.strip()
        if line == "":
            continue
        parts = line.split("\t")
        if len(parts) == 2:
            terminal.airlines.append((parts[0], parts[1]))
    f.close()


def LoadAirportStructure(filename):
    """
    Reads a LEBL.txt-style file and builds a BarcelonaAP object.
    Returns -1 if file does not exist.
    """
    try:
        f = open(filename, "r")
    except OSError:
        return -1

    lines = f.readlines()
    f.close()

    bcn = BarcelonaAP()
    i   = 0

    # First line: "LEBL 2 terminals"
    first = lines[i].split()
    bcn.CompleteName = first[0]
    i = i + 1

    while i < len(lines):
        line = lines[i].strip()
        if line == "":
            i = i + 1
            continue

        parts = line.split()
        if parts[0] == "Terminal":
            terminal        = Terminal()
            terminal.number = parts[1]
            num_areas       = int(parts[2])
            i = i + 1

            for _ in range(num_areas):
                area_line = lines[i].strip().split()
                i = i + 1

                ba          = BoardingArea()
                ba.area     = area_line[1]
                ba.schengen = (area_line[2].lower() == "schengen")

                init_gate = int(area_line[4])
                end_gate  = int(area_line[6])

                prefix = terminal.number + "BA" + ba.area + "G"
                SetGates(ba, init_gate, end_gate, prefix)

                terminal.BoardingAreas.append(ba)

            LoadAirlines(terminal, terminal.number)
            bcn.Terminals.append(terminal)
        else:
            i = i + 1

    return bcn


def GateOccupancy(bcn):
    """
    Returns a list of tuples (gate_name, occupied_bool, aircraft_id)
    for every gate in the airport.
    """
    result = []
    for terminal in bcn.Terminals:
        for ba in terminal.BoardingAreas:
            for gate in ba.gates:
                result.append((gate.name, gate.ocupado, gate.id))
    return result


def IsAirlineInTerminal(terminal, name):
    """
    Returns True if airline 'name' (name or ICAO) is in the terminal.
    Returns (False, -1) if name is empty.
    Returns False if list is empty or airline not found.
    """
    if name == "":
        return False, -1
    if len(terminal.airlines) == 0:
        return False
    for airline_name, icao in terminal.airlines:
        if airline_name == name or icao == name:
            return True
    return False


def SearchTerminal(bcn, name):
    """
    Returns the terminal name (e.g. "T1") where airline 'name' boards.
    Returns "" if not found.
    """
    for terminal in bcn.Terminals:
        if IsAirlineInTerminal(terminal, name) == True:
            return terminal.number
    return ""


def AssignGate(bcn, aircraft):
    """
    Assigns the first free gate in the correct terminal and
    Schengen/non-Schengen area to the aircraft. Updates bcn.

    Schengen is decided from the aircraft's origin airport ICAO code
    using IsSchengenAirport — the same function used for airports.
    Returns -1 if no free gate is available.
    """
    terminal_name = SearchTerminal(bcn, aircraft.company)
    is_schengen   = IsSchengenAirport(aircraft.origin)

    for terminal in bcn.Terminals:
        if terminal_name == "" or terminal.number == terminal_name:
            for ba in terminal.BoardingAreas:
                if ba.schengen == is_schengen:
                    for gate in ba.gates:
                        if not gate.ocupado:
                            gate.ocupado = True
                            gate.id      = aircraft.id
                            return
    return -1


# --- Funciones versión 4 ---
def AssignNightGates(bcn, aircraft):
    if len(aircraft) == 0:
        print('Error: la lista de aeronaves está vacía.')
        return []

    num = 0
    while num < len(aircraft):
        a=aircraft[num]
        if a.timelanding == '' and a.departure!= '':
            #Llamamos la función para asignarle puerta
           AssignGate(bcn, a)
        num = num + 1
    return []

def FreeGate(bcn, id):
    #Buscamos el avión
    t_idx = 0
    while t_idx < len(bcn.Terminals):
        terminal = bcn.Terminals[t_idx]

        ba_idx = 0
        while ba_idx < len(terminal.BoardingAreas):
            area = terminal.BoardingAreas[ba_idx]

            g_idx = 0
            while g_idx < len(area.gates):
                gate = area.gates[g_idx]

                #Liberamos la puerta ocupada por el avión
                if gate.ocupado and gate.id != id:
                    gate.ocupado = False
                    gate.id = ''
                    return 0 #Encontrado y liberado con éxito

                g_idx = g_idx + 1
            ba_idx = ba_idx + 1
        t_idx = t_idx + 1
    print('Error: El avión' + id + ' no se encontró en ninguna puerta.')
    return -1


def AssignGatesAtTime(bcn, aircrafts, time):
    partes_time = time.split(':')
    hora_simulacion = int(partes_time[0])

    contador_no_asignados = 0

    # 1. Liberar las puertas de los aviones cuya hora de salida coincida con esa hora
    t_idx = 0
    while t_idx < len(bcn.Terminals):
        terminal = bcn.Terminals[t_idx]

        ba_idx = 0
        while ba_idx < len(terminal.BoardingAreas):
            area = terminal.BoardingAreas[ba_idx]

            g_idx = 0
            while g_idx < len(area.gates):
                gate = area.gates[g_idx]

                if gate.ocupado:
                    #Buscamos cuando sale el avión
                    num_a = 0
                    encontrado = False
                    while num_a < len(aircrafts) and not encontrado:
                        a = aircrafts[num_a]

                        if a.id == gate.id and a.departure != '':
                            partes_dep = a.departure.split(':')
                            hora_salida = int(partes_dep[0])

                            #Si la hora de salida es la hora actual de la simulación, se va
                            if hora_salida == hora_simulacion:
                                gate.ocupado = False
                                gate.id = ''
                                encontrado = True
                        num_a = num_a + 1
                g_idx = g_idx + 1
            ba_idx = ba_idx + 1
        t_idx = t_idx + 1

    # 2. Sentar a los aviones que acaban de aterrizar en esta hora exacta
    num_a = 0
    while num_a < len(aircrafts):
        a = aircrafts[num_a]

        if a.timelanding != '':
            partes_arr = a.timelanding.split(':')
            hora_llegada = int(partes_arr[0])

            if hora_llegada == hora_simulacion:
                #Le asignamos una puerta
                resultado = AssignGate(bcn, a)
                if resultado == -1:
                    contador_no_asignados = contador_no_asignados + 1

        num_a = num_a + 1

    return contador_no_asignados

def PlotDayOccupancy(bcn, aircraft):
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    if  len(aircraft) == 0:
        print('Error: la lista de aeronaves está vacía.')
        return []

    #Listas vacías para guardar los datos de la gráfica
    horas_eje = []
    ocupacion_t1 = []
    ocupacion_t2 = []
    no_asignados = []

    #Bucle para simular las 24 horas del día
    h = 0
    while h < 24:

        #Fabricamos la cadena de texto de la hora
        if h < 10:
            time_str = '0' + str(h) + ':00'
        else:
            time_str = str(h) + ':00'

        horas_eje.append(time_str)

        # 1. Ejecutamos la simulación para esta hora exacta
        # Nos devuelve cuántos vuelos no han cabido en esta hora
        vuelos_sin_puerta = AssignGatesAtTime(bcn, aircraft, time_str)
        no_asignados.append(vuelos_sin_puerta)

        # 2. Contar cuántas puertas hay ocupadas en este instante en T1 y T2
        puertas_t1 = 0
        puertas_t2 = 0

        t_idx = 0
        while t_idx < len(bcn.Terminals):
            terminal = bcn.Terminals[t_idx]

            ba_idx = 0
            while ba_idx < len(terminal.BoardingAreas):
                area = terminal.BoardingAreas[ba_idx]

                g_idx = 0
                while g_idx < len(area.gates):
                    gate = area.gates[g_idx]

                    #Si la puerta está ocupada, miramos de qué terminal es
                    if gate.ocupado:
                        if terminal.number == 'T1':
                            puertas_t1 = puertas_t1 + 1
                        if terminal.number == 'T2':
                            puertas_t2 = puertas_t2 + 1

                    g_idx = g_idx + 1
                ba_idx = ba_idx + 1
            t_idx = t_idx + 1

        #Guardamos los totales de esta hora en sus respectivas listas
        ocupacion_t1.append(puertas_t1)
        ocupacion_t2.append(puertas_t2)

        h = h+1

    # 3. Dibujar la gráfica final
    #Pintamos las líneas de ocupación por terminal
    plt.figure(figsize=(10, 6))
    plt.plot(range(24), ocupacion_t1, color = 'blue', label='Ocupación T1')
    plt.plot(range(24), ocupacion_t2, color = 'green', label='Ocupación T2')

    #Pintamos las barras rojas para los vuelos que se quedaron sin puerta
    plt.bar(range(24), no_asignados, color = 'red', label='Vuelos no asignados')

    #Configuramos los textos de la gráfica
    plt.xticks(range(24), horas_eje, rotation=45)
    plt.xlabel('Hora de la simulación')
    plt.ylabel('Cantidad de puertas/aviones')
    plt.title('Evolución de la ocupación diaria en LEBL')
    plt.legend()
    plt.tight_layout()
    plt.show()



# ─────────────────────────────────────────────
#  Test section
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # 1. SetGates
    ba_test      = BoardingArea()
    ba_test.area = "A"
    result       = SetGates(ba_test, 1, 3, "T1BAAaG")
    print("SetGates – expected 3 gates, got:", len(ba_test.gates))
    print("  Names:", [g.name for g in ba_test.gates])
    print("  All free:", all(not g.ocupado for g in ba_test.gates))
    bad = SetGates(ba_test, 5, 3, "X")
    print("SetGates bad range – expected -1, got:", bad)

    # 2. LoadAirportStructure
    bcn = LoadAirportStructure("Terminals.txt")
    if bcn == -1:
        print("\nTerminals.txt not found – skipping remaining tests")
    else:
        print("\nLoadAirportStructure OK – terminals:", len(bcn.Terminals))
        for t in bcn.Terminals:
            print(f"  {t.number}: {len(t.BoardingAreas)} areas, {len(t.airlines)} airlines")

        # 3. GateOccupancy
        occ = GateOccupancy(bcn)
        print("\nGateOccupancy – total gates:", len(occ))
        print("  First 3:", occ[:3])

        # 4. IsAirlineInTerminal
        if bcn.Terminals and bcn.Terminals[0].airlines:
            first = bcn.Terminals[0].airlines[0][0]
            print(f"\nIsAirlineInTerminal – '{first}' in T1?",
                  IsAirlineInTerminal(bcn.Terminals[0], first))
        print("IsAirlineInTerminal – '' (empty)?",
              IsAirlineInTerminal(bcn.Terminals[0], ""))

        # 5. SearchTerminal
        if bcn.Terminals and bcn.Terminals[0].airlines:
            name = bcn.Terminals[0].airlines[0][0]
            print(f"\nSearchTerminal – '{name}':", SearchTerminal(bcn, name))
        print("SearchTerminal – 'UNKNOWN':", SearchTerminal(bcn, "UNKNOWN"))



# ─────────────────────────────────────────────
#  Sección de Pruebas - Versión 4
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- PROBANDO CARGA DE ESTRUCTURA ---")
    bcn = LoadAirportStructure("Terminals.txt")
    if bcn == -1:
        print("Error: No se encuentra Terminals.txt")
    else:
        print("Aeropuerto cargado:", bcn.CompleteName)

        from aircraft import LoadArrivals, LoadDepartures, MergeMovements, NightAircraft

        print("\n--- PROBANDO CARGA Y FUSIÓN DE VUELOS (V4) ---")
        arrivals = LoadArrivals("Arrivals.txt")
        departures = LoadDepartures("Departures.txt")

        vuelos_totales = MergeMovements(arrivals, departures)
        print("Llegadas reales leídas:", len(arrivals))
        print("Salidas reales leídas:", len(departures))
        print("Movimientos totales consolidados:", len(vuelos_totales))

        print("\n--- PROBANDO AVIONES DE PERNOCTA ---")
        aviones_noche = NightAircraft(vuelos_totales)
        print("Aviones detectados que pasaron la noche:", len(aviones_noche))

        print("\n--- PROBANDO ASIGNACIÓN DE PUERTAS NOCTURNAS ---")
        AssignNightGates(bcn, vuelos_totales)

        ocupacion_inicial = GateOccupancy(bcn)
        puertas_ocupadas = 0
        i = 0
        while i < len(ocupacion_inicial):
            if ocupacion_inicial[i][1] == True:
                puertas_ocupadas = puertas_ocupadas + 1
            i = i + 1
        print("Puertas ocupadas por aviones de pernocta antes de empezar el día:", puertas_ocupadas)

        print("\n--- PROBANDO LIBERACIÓN DE PUERTA (FreeGate) ---")
        if puertas_ocupadas > 0:
            id_avion_prueba = ""
            i = 0
            while i < len(ocupacion_inicial) and id_avion_prueba == "":
                if ocupacion_inicial[i][1] == True:
                    id_avion_prueba = ocupacion_inicial[i][2]
                i = i + 1

            print("Intentando liberar el avión de prueba:", id_avion_prueba)
            resultado_liberar = FreeGate(bcn, id_avion_prueba)
            print("Resultado de la liberación (debe ser 0):", resultado_liberar)
        else:
            print("No hay aviones asignados para probar FreeGate.")

        print("\n--- LANZANDO SIMULACIÓN COMPLETA Y GRÁFICA ---")
        print("Cerrando y relanzando para limpiar el aeropuerto...")
        bcn_simulacion = LoadAirportStructure("Terminals.txt")
        AssignNightGates(bcn_simulacion, vuelos_totales)

        PlotDayOccupancy(bcn_simulacion, vuelos_totales)
        print("Simulación terminada con éxito.")
