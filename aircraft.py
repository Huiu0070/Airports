from airports import *

class Aircraft:
    def __init__(self, id, company, origin, timelanding):
        self.id            = id
        self.company       = company
        self.origin        = origin
        self.timelanding   = timelanding    # arrival time, e.g. "08:30"  ('' if no arrival)
        self.destination   = ''             # departure destination ICAO   ('' if no departure)
        self.timedeparture = ''             # departure time, e.g. "14:50" ('' if no departure)


# ═══════════════════════════════════════════════════
#  V1 / V2 functions
# ═══════════════════════════════════════════════════

def LoadArrivals(filename):
    arrivals_list = []
    try:
        f = open(filename, "r")
        header = f.readline()
        linea = f.readline()
        while linea != '':
            elementos = linea.split()
            if len(elementos) == 4:
                id          = elementos[0]
                company     = elementos[3]
                origin      = elementos[1]
                timelanding = elementos[2]
                aircraft = Aircraft(id, company, origin, timelanding)
                arrivals_list.append(aircraft)
            linea = f.readline()
        f.close()
    except FileNotFoundError:
        print('Error: archivo no encontrado.')
    return arrivals_list


def PlotArrivals(aircrafts):
    import matplotlib.pyplot as plt

    if len(aircrafts) == 0:
        print('Error: lista vacía.')
        return

    horas = [0] * 24
    i = 0
    while i < len(aircrafts):
        tiempo = aircrafts[i].timelanding
        partes = tiempo.split(':')
        hora = int(partes[0])
        horas[hora] = horas[hora] + 1
        i = i + 1

    plt.bar(range(24), horas)
    plt.xlabel('Hora')
    plt.ylabel('Vols')
    plt.title('Arribades per hora')
    plt.show()


def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        print('Error: llista buida.')
        return

    f = open(filename, "w")
    f.write('AIRCRAFT ORIGIN ARRIVAL AIRLINE\n')
    num = 0
    while num < len(aircrafts):
        a = aircrafts[num]
        f.write(a.id + ' ' + a.origin + ' ' + a.timelanding + ' ' + a.company + '\n')
        num = num + 1
    f.close()


def PlotAirlines(aircrafts):
    import matplotlib.pyplot as plt

    if len(aircrafts) == 0:
        print('Error: llista buida.')
        return

    companies = []
    counts    = []
    num = 0
    while num < len(aircrafts):
        a       = aircrafts[num]
        company = a.company
        encontrado = False
        i = 0
        while i < len(companies) and not encontrado:
            if companies[i] == company:
                counts[i] = counts[i] + 1
                encontrado = True
            i = i + 1
        if not encontrado:
            companies.append(company)
            counts.append(1)
        num = num + 1

    paired = sorted(zip(counts, companies), reverse=True)
    counts, companies = zip(*paired)

    fig, ax = plt.subplots(figsize=(max(10, len(companies) * 0.7), 6))
    bars = ax.bar(range(len(companies)), counts, color='steelblue', edgecolor='white', width=0.6)
    ax.set_xticks(range(len(companies)))
    ax.set_xticklabels(companies, rotation=45, ha='right', fontsize=8)
    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.2,
                str(val), ha='center', va='bottom', fontsize=7)
    ax.set_xlabel('Aerolínea')
    ax.set_ylabel('Vols')
    ax.set_title('Vols per aerolínea')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    fig.tight_layout()
    plt.show()


def PlotFlightsType(aircrafts):
    import matplotlib.pyplot as plt

    if len(aircrafts) == 0:
        print('Error: llista buida.')
        return

    Schengen   = 0
    NoSchengen = 0
    num = 0
    while num < len(aircrafts):
        a = aircrafts[num]
        if IsSchengenAirport(a.origin):
            Schengen = Schengen + 1
        else:
            NoSchengen = NoSchengen + 1
        num = num + 1

    plt.bar(0, Schengen,   color='blue', label='Schengen')
    plt.bar(0, NoSchengen, bottom=Schengen, color='red', label='No Schengen')
    plt.title('Vols Schengen vs No Schengen')
    plt.ylabel('Vols')
    plt.xticks([])
    plt.legend()
    plt.show()


def MapFlights(aircrafts, filepath='Flight_map.kml'):
    f = open(filepath, 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('<Style id="Schengen">\n')
    f.write('  <LineStyle><color>ff00ff00</color></LineStyle>\n')
    f.write('</Style>\n')
    f.write('<Style id="NoSchengen">\n')
    f.write('  <LineStyle><color>ff0000ff</color></LineStyle>\n')
    f.write('</Style>\n')

    lebl_lon  = 2.07833
    lebl_lat  = 41.29694
    airports  = LoadAirport('Airports.txt')

    num = 0
    while num < len(aircrafts):
        a = aircrafts[num]
        origin_lat = 0.0
        origin_lon = 0.0
        i = 0
        Found = False
        while i < len(airports) and not Found:
            if airports[i].code == a.origin:
                origin_lat = airports[i].latitude
                origin_lon = airports[i].longitude
                Found = True
            i = i + 1
        f.write('<Placemark>\n')
        f.write('  <name>' + a.id + '</name>\n')
        if IsSchengenAirport(a.origin):
            f.write('  <styleUrl>#Schengen</styleUrl>\n')
        else:
            f.write('  <styleUrl>#NoSchengen</styleUrl>\n')
        f.write('  <LineString>\n')
        f.write('    <coordinates>\n')
        f.write('      ' + str(origin_lon) + ',' + str(origin_lat) + '\n')
        f.write('      ' + str(lebl_lon)   + ',' + str(lebl_lat)   + '\n')
        f.write('    </coordinates>\n')
        f.write('  </LineString>\n')
        f.write('</Placemark>\n')
        num = num + 1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    return filepath


def Haversine(lat1, lon1, lat2, lon2):
    import math
    r    = 6371
    lat1 = lat1 * math.pi / 180
    lon1 = lon1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    lon2 = lon2 * math.pi / 180
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def LongDistanceArrivals(aircrafts):
    lebl_lat  = 41.29694
    lebl_lon  = 2.07833
    airports  = LoadAirport('Airports.txt')
    long_distance = []
    num = 0
    while num < len(aircrafts):
        a = aircrafts[num]
        i = 0
        while i < len(airports):
            if airports[i].code == a.origin:
                origin_lat = airports[i].latitude
                origin_lon = airports[i].longitude
                distancia  = Haversine(origin_lat, origin_lon, lebl_lat, lebl_lon)
                if distancia > 2000:
                    long_distance.append(a)
            i = i + 1
        num = num + 1
    return long_distance


# ═══════════════════════════════════════════════════
#  V4 functions
# ═══════════════════════════════════════════════════

def LoadDepartures(filename):
    '''
    Opens the departures file and returns a list of Aircraft with only
    the departure fields filled in (destination, timedeparture, company, id).
    Format:  AIRCRAFT  DESTINATION  DEPARTURE  AIRLINE
    Returns an empty list if the file does not exist.
    '''
    departures_list = []
    try:
        f = open(filename, "r")
        header = f.readline()
        linea  = f.readline()
        while linea != '':
            elementos = linea.split()
            if len(elementos) == 4:
                ac = Aircraft(elementos[0], elementos[3], '', '')
                ac.destination   = elementos[1]
                ac.timedeparture = elementos[2]
                departures_list.append(ac)
            linea = f.readline()
        f.close()
    except FileNotFoundError:
        print('Error: archivo de salidas no encontrado.')
    return departures_list


def _time_to_minutes(t):
    '''Helper: converts "hh:mm" or "h:mm" to total minutes. Returns -1 on error.'''
    try:
        parts = t.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    except (ValueError, IndexError, AttributeError):
        return -1


def MergeMovements(arrivals, departures):
    '''
    Receives two lists (arrivals and departures) and returns a merged list.
    - Aircraft that appear in both lists with compatible times
      (arrival before departure, same id) are merged into one Aircraft.
    - Aircraft only in arrivals are kept as-is.
    - Aircraft only in departures (night aircraft) are kept as-is.
    Returns -1 if both lists are empty.
    '''
    if len(arrivals) == 0 and len(departures) == 0:
        return -1

    merged = []

    # Copy all arrivals into the merged list first
    i = 0
    while i < len(arrivals):
        a = arrivals[i]
        ac = Aircraft(a.id, a.company, a.origin, a.timelanding)
        ac.destination   = a.destination
        ac.timedeparture = a.timedeparture
        merged.append(ac)
        i = i + 1

    # Go through every departure and try to match it with an arrival
    d = 0
    while d < len(departures):
        dep = departures[d]
        matched = False

        m = 0
        while m < len(merged):
            ac = merged[m]
            # Same aircraft id, has an arrival time, arrival is before departure
            if ac.id == dep.id and ac.timelanding != '':
                arr_min = _time_to_minutes(ac.timelanding)
                dep_min = _time_to_minutes(dep.timedeparture)
                if arr_min != -1 and dep_min != -1 and arr_min < dep_min:
                    # Only merge if this slot has no departure yet
                    if ac.timedeparture == '':
                        ac.destination   = dep.destination
                        ac.timedeparture = dep.timedeparture
                        matched = True
                        break
            m = m + 1

        # No matching arrival found → night aircraft, add as departure-only
        if not matched:
            ac = Aircraft(dep.id, dep.company, '', '')
            ac.destination   = dep.destination
            ac.timedeparture = dep.timedeparture
            merged.append(ac)

        d = d + 1

    return merged


def NightAircraft(aircrafts):
    '''
    Returns a list of aircraft that have NO arrival (timelanding == '')
    but DO have a departure. These are aircraft that spent the night at LEBL.
    Returns -1 if the input list is empty.
    '''
    if len(aircrafts) == 0:
        return -1

    night = []
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.timelanding == '' and ac.timedeparture != '':
            night.append(ac)
        i = i + 1
    return night


def AssignNightGates(bcn, aircrafts):
    '''
    Assigns a gate to each night aircraft (departure-only).
    Skips any aircraft that has arrival data.
    Returns -1 if the list is empty.
    '''
    if len(aircrafts) == 0:
        return -1

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.timelanding == '':        # confirm it is a night aircraft
            AssignGate(bcn, ac)
        i = i + 1
    return 0


def FreeGate(bcn, id):
    '''
    Finds the gate occupied by the aircraft with the given id
    and sets it to free. Returns -1 if not found.
    '''
    t = 0
    while t < len(bcn.Terminals):
        terminal = bcn.Terminals[t]
        b = 0
        while b < len(terminal.BoardingAreas):
            ba = terminal.BoardingAreas[b]
            g = 0
            while g < len(ba.gates):
                gate = ba.gates[g]
                if gate.ocupado and gate.id == id:
                    gate.ocupado = False
                    gate.id      = ''
                    return 0
                g = g + 1
            b = b + 1
        t = t + 1
    return -1


def AssignGatesAtTime(bcn, aircrafts, time):
    '''
    Updates bcn for the one-hour period starting at 'time' (format "hh:mm").
    1. Frees gates of aircraft that have already departed before 'time'.
    2. Assigns gates to aircraft landing during [time, time+1h).
    Returns the number of arriving aircraft that could not be assigned a gate.
    '''
    start_min = _time_to_minutes(time)
    end_min   = start_min + 60

    # Step 1 – free gates of aircraft that departed before start_min
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.timedeparture != '':
            dep_min = _time_to_minutes(ac.timedeparture)
            if dep_min != -1 and dep_min <= start_min:
                FreeGate(bcn, ac.id)
        i = i + 1

    # Step 2 – assign gates to aircraft landing in [start_min, end_min)
    unassigned = 0
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.timelanding != '':
            land_min = _time_to_minutes(ac.timelanding)
            if land_min != -1 and start_min <= land_min < end_min:
                result = AssignGate(bcn, ac)
                if result == -1:
                    unassigned = unassigned + 1
        i = i + 1

    return unassigned


def PlotDayOccupancy(bcn, aircrafts):
    '''
    Returns a matplotlib figure with the number of occupied gates per terminal
    for each hour of the day, plus the number of unassigned aircraft per hour.
    NOTE: bcn should be passed as a deepcopy so the live state is not mutated.
    '''
    import matplotlib.pyplot as plt
    import copy

    # Count terminal names
    terminal_names = []
    t = 0
    while t < len(bcn.Terminals):
        terminal_names.append(bcn.Terminals[t].number)
        t = t + 1

    hours        = list(range(24))
    occupied     = []
    unassigned_h = []

    h = 0
    while h < 24:
        time_str = str(h).zfill(2) + ':00'
        # Deep copy per hour so each hour starts from the same state
        bcn_copy = copy.deepcopy(bcn)
        unasgn   = AssignGatesAtTime(bcn_copy, aircrafts, time_str)
        unassigned_h.append(unasgn)

        counts = []
        t = 0
        while t < len(bcn_copy.Terminals):
            terminal = bcn_copy.Terminals[t]
            used = 0
            b = 0
            while b < len(terminal.BoardingAreas):
                g = 0
                while g < len(terminal.BoardingAreas[b].gates):
                    if terminal.BoardingAreas[b].gates[g].ocupado:
                        used = used + 1
                    g = g + 1
                b = b + 1
            counts.append(used)
            t = t + 1

        occupied.append(counts)
        h = h + 1

    # Build stacked bar chart
    fig, ax1 = plt.subplots(figsize=(14, 6))

    colors = ['#3A7FC1', '#D9704A', '#2ECC71', '#9B59B6']
    bottom = [0] * 24

    t = 0
    while t < len(terminal_names):
        values = []
        h = 0
        while h < 24:
            values.append(occupied[h][t])
            h = h + 1
        color = colors[t % len(colors)]
        ax1.bar(hours, values, bottom=bottom, label=terminal_names[t], color=color, alpha=0.8)
        new_bottom = []
        i = 0
        while i < 24:
            new_bottom.append(bottom[i] + values[i])
            i = i + 1
        bottom = new_bottom
        t = t + 1

    ax2 = ax1.twinx()
    ax2.plot(hours, unassigned_h, color='red', marker='o', linewidth=2, label='Unassigned')
    ax2.set_ylabel('Unassigned aircraft', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax1.set_xlabel('Hour of day')
    ax1.set_ylabel('Gates occupied')
    ax1.set_title('Gate occupancy by terminal throughout the day')
    ax1.set_xticks(hours)
    ax1.set_xticklabels([str(h).zfill(2) + 'h' for h in hours], rotation=45, fontsize=8)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    return fig          # ← returned so the GUI can embed it in the panel


# ═══════════════════════════════════════════════════
#  TEST
# ═══════════════════════════════════════════════════

if __name__ == '__main__':
    arrivals = LoadArrivals('Arrivals.txt')
    print('Arrivals loaded:', len(arrivals))

    departures = LoadDepartures('Departures.txt')
    print('Departures loaded:', len(departures))

    merged = MergeMovements(arrivals, departures)
    print('Merged movements:', len(merged))

    night = NightAircraft(merged)
    if night != -1:
        print('Night aircraft:', len(night))
    else:
        print('Night aircraft: none or empty list')