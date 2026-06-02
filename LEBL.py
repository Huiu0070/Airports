from aircraft import *
from airports import *


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
    Reads a Terminals.txt-style file and builds a BarcelonaAP object.
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

    # First line: airport name
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
                            return 0
    return -1


# ─────────────────────────────────────────────
#  V4 functions
# ─────────────────────────────────────────────

def AssignNightGates(bcn, aircrafts):
    """
    Assigns a gate to each night aircraft (departure-only: no arrival time).
    Skips aircraft that have arrival data.
    Returns -1 if the list is empty.
    """
    if len(aircrafts) == 0:
        print("Error: aircraft list is empty.")
        return -1

    i = 0
    while i < len(aircrafts):
        a = aircrafts[i]
        if a.timelanding == '' and a.timedeparture != '':
            AssignGate(bcn, a)
        i = i + 1
    return 0


def FreeGate(bcn, id):
    """
    Finds the gate occupied by the aircraft with the given id
    and sets it to free. Returns -1 if not found.
    """
    t_idx = 0
    while t_idx < len(bcn.Terminals):
        terminal = bcn.Terminals[t_idx]

        ba_idx = 0
        while ba_idx < len(terminal.BoardingAreas):
            area = terminal.BoardingAreas[ba_idx]

            g_idx = 0
            while g_idx < len(area.gates):
                gate = area.gates[g_idx]

                if gate.ocupado and gate.id == id:
                    gate.ocupado = False
                    gate.id      = ''
                    return 0   # found and freed successfully

                g_idx = g_idx + 1
            ba_idx = ba_idx + 1
        t_idx = t_idx + 1

    print('Error: aircraft ' + id + ' not found in any gate.')
    return -1


def AssignGatesAtTime(bcn, aircrafts, time):
    """
    Updates bcn for the one-hour period starting at 'time' (format "hh:mm").
    1. Frees gates of aircraft that departed at this hour.
    2. Assigns gates to aircraft landing during this hour.
    Returns the number of arriving aircraft that could not be assigned a gate.
    """
    parts_time      = time.split(':')
    simulation_hour = int(parts_time[0])

    unassigned = 0

    # Step 1 – free gates of aircraft that departed at this hour
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
                    a_idx = 0
                    found = False
                    while a_idx < len(aircrafts) and not found:
                        a = aircrafts[a_idx]
                        if a.id == gate.id and a.timedeparture != '':
                            parts_dep   = a.timedeparture.split(':')
                            depart_hour = int(parts_dep[0])
                            if depart_hour == simulation_hour:
                                gate.ocupado = False
                                gate.id      = ''
                                found        = True
                        a_idx = a_idx + 1

                g_idx = g_idx + 1
            ba_idx = ba_idx + 1
        t_idx = t_idx + 1

    # Step 2 – assign gates to aircraft landing this hour
    a_idx = 0
    while a_idx < len(aircrafts):
        a = aircrafts[a_idx]
        if a.timelanding != '':
            parts_arr   = a.timelanding.split(':')
            landing_hour = int(parts_arr[0])
            if landing_hour == simulation_hour:
                result = AssignGate(bcn, a)
                if result == -1:
                    unassigned = unassigned + 1
        a_idx = a_idx + 1

    return unassigned


def PlotDayOccupancy(bcn, aircrafts):
    """
    Builds and RETURNS a matplotlib figure showing gate occupancy per terminal
    for each hour of the day, plus the number of unassigned aircraft per hour.
    The caller is responsible for displaying or embedding the figure.
    NOTE: bcn should be passed as a deepcopy so the live state is not mutated.
    """
    import matplotlib.pyplot as plt

    if len(aircrafts) == 0:
        print("Error: aircraft list is empty.")
        return None

    hours_axis   = []
    occupancy_t1 = []
    occupancy_t2 = []
    unassigned   = []

    h = 0
    while h < 24:
        time_str = str(h).zfill(2) + ':00'
        hours_axis.append(time_str)

        # Run simulation for this hour
        no_gate = AssignGatesAtTime(bcn, aircrafts, time_str)
        unassigned.append(no_gate)

        # Count occupied gates per terminal
        gates_t1 = 0
        gates_t2 = 0

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
                        if terminal.number == 'T1':
                            gates_t1 = gates_t1 + 1
                        if terminal.number == 'T2':
                            gates_t2 = gates_t2 + 1
                    g_idx = g_idx + 1
                ba_idx = ba_idx + 1
            t_idx = t_idx + 1

        occupancy_t1.append(gates_t1)
        occupancy_t2.append(gates_t2)

        h = h + 1

    # Build the figure and return it (do NOT call plt.show())
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(range(24), occupancy_t1, color='#3A7FC1', linewidth=2, marker='o', label='T1 occupied gates')
    ax1.plot(range(24), occupancy_t2, color='#2ECC71', linewidth=2, marker='s', label='T2 occupied gates')
    ax1.set_xlabel('Hour of day')
    ax1.set_ylabel('Gates occupied')
    ax1.set_title('Daily gate occupancy at LEBL')
    ax1.set_xticks(range(24))
    ax1.set_xticklabels(hours_axis, rotation=45, fontsize=7)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.bar(range(24), unassigned, color='#D9704A', alpha=0.5, label='Unassigned aircraft')
    ax2.set_ylabel('Unassigned aircraft', color='#D9704A')
    ax2.tick_params(axis='y', labelcolor='#D9704A')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    return fig   # returned so interface.py can embed it with show_info_plot()


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

        # 6. V4 – load, merge, assign night gates, plot
        from aircraft import LoadArrivals, LoadDepartures, MergeMovements, NightAircraft
        import copy

        arrivals   = LoadArrivals("Arrivals.txt")
        departures = LoadDepartures("Departures.txt")
        merged     = MergeMovements(arrivals, departures)
        night      = NightAircraft(merged)

        print("\nArrivals:", len(arrivals))
        print("Departures:", len(departures))
        print("Merged movements:", len(merged))
        print("Night aircraft:", len(night) if night != -1 else 0)

        AssignNightGates(bcn, merged)

        occ_initial = GateOccupancy(bcn)
        occupied    = sum(1 for _, occ, _ in occ_initial if occ)
        print("Gates occupied by night aircraft:", occupied)

        # FreeGate test
        if occupied > 0:
            test_id = next(ac_id for _, occ, ac_id in occ_initial if occ)
            print("Freeing aircraft:", test_id)
            print("FreeGate result (expected 0):", FreeGate(bcn, test_id))

        # PlotDayOccupancy – in test mode open the figure directly
        bcn_sim = LoadAirportStructure("Terminals.txt")
        AssignNightGates(bcn_sim, merged)
        fig = PlotDayOccupancy(copy.deepcopy(bcn_sim), merged)
        if fig is not None:
            import matplotlib.pyplot as plt
            plt.show()
        print("Simulation complete.")

# --- DATOS DE SIDs ---
SIDS_DATA = {
    "24L": {
        "AGENA7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("BL805", 40.995, 2.048),
            ("BL811", 40.861, 2.300),
            ("BL827", 41.130, 2.762),
            ("AGENA", 41.545, 3.489)
        ],
        "DALIN6Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("BL805", 40.995, 2.048),
            ("BL812", 40.936, 2.277),
            ("DALIN", 41.734, 3.358)
        ],
        "DIPES3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("BL805", 40.995, 2.048),
            ("BL811", 40.861, 2.300),
            ("BL813", 41.109, 3.008),
            ("DIPES", 41.063, 3.540)
        ],
        "DUNES7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL809", 40.934, 1.952),
            ("BL810", 40.770, 2.233),
            ("DUNES", 40.864, 3.158)
        ],
        "DUQQI3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706)
        ],
        "GRAUS7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("LRD", 41.553, 0.648),
            ("GRAUS", 41.979, 0.376)
        ],
        "LARPA7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL809", 40.934, 1.952),
            ("BL810", 40.770, 2.233),
            ("LARPA", 40.627, 2.349)
        ],
        "LOBAR8Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("LRD", 41.553, 0.648),
            ("LOBAR", 41.748, 0.318)
        ],
        "LOTOS7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL804", 41.053, 1.893),
            ("BL807", 40.955, 1.564),
            ("BL808", 40.847, 1.109),
            ("LOTOS", 40.550, 1.003)
        ],
        "MAMUK3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("BL815", 41.376, 1.680),
            ("MAMUK", 41.837, 2.072)
        ],
        "MOPAS6Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("MOPAS", 42.435, 1.034)
        ],
        "NATPI4Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VIBOK", 41.547, 1.502),
            ("NATPI", 42.724, 1.236)
        ],
        "OLOXO3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("BL815", 41.376, 1.680),
            ("BL816", 41.524, 1.657),
            ("OLOXO", 42.435, 1.513)
        ],
        "REBUL3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("REBUL", 41.698, 1.113)
        ],
        "SENIA7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL804", 41.053, 1.893),
            ("BL806", 41.055, 1.524),
            ("BL836", 40.968, 1.152),
            ("SENIA", 40.869, 0.739)
        ],
        "VIBOK3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VIBOK", 41.547, 1.502)
        ]
    },
    "06R": {
        "AGENA4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL701", 41.248, 2.565),
            ("BL702", 41.311, 2.684),
            ("BL703", 41.411, 2.732),
            ("BL704", 41.511, 2.780),
            ("BL705", 41.504, 2.960),
            ("SALON", 41.494, 3.187),
            ("AGENA", 41.545, 3.489)
        ],
        "CLE1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL716", 41.523, 2.463),
            ("CLE", 41.640, 2.634)
        ],
        "DALIN4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL701", 41.248, 2.565),
            ("BL702", 41.311, 2.684),
            ("BL703", 41.411, 2.732),
            ("BL704", 41.511, 2.780),
            ("FEVIK", 41.679, 3.196),
            ("DALIN", 41.734, 3.358)
        ],
        "DIPES1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL701", 41.248, 2.565),
            ("BL702", 41.311, 2.684),
            ("BL703", 41.411, 2.732),
            ("BL704", 41.511, 2.780),
            ("BL705", 41.504, 2.960),
            ("BL706", 41.351, 3.163),
            ("DIPES", 41.063, 3.540)
        ],
        "DUNES4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("DUNES", 40.864, 3.158)
        ],
        "DUQQI1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL722", 41.292, 1.845),
            ("DUQQI", 41.211, 1.706)
        ],
        "GRAUS3R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("BL712", 41.769, 1.693),
            ("GRAUS", 41.979, 0.376)
        ],
        "LARPA4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("TASOS", 40.946, 2.650),
            ("LARPA", 40.627, 2.349)
        ],
        "LOBAR4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL714", 41.687, 1.792),
            ("LOBAR", 41.748, 0.318)
        ],
        "LOTOS3R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("TASOS", 40.946, 2.650),
            ("BL721", 40.836, 2.180),
            ("LOTOS", 40.550, 1.003)
        ],
        "MAMUK1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("MAMUK", 41.837, 2.072)
        ],
        "MOPAS3R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("BL712", 41.769, 1.693),
            ("MOPAS", 42.435, 1.034)
        ],
        "NATPI2R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("BL712", 41.769, 1.693),
            ("NATPI", 42.724, 1.236)
        ],
        "OLOXO1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("OLOXO", 42.435, 1.513)
        ],
        "REBUL1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL715", 41.606, 1.728),
            ("REBUL", 41.698, 1.113)
        ],
        "SENIA5R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("TASOS", 40.946, 2.650),
            ("BL721", 40.836, 2.180),
            ("SENIA", 40.869, 0.739)
        ],
        "VIBOK1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL715", 41.606, 1.728),
            ("VIBOK", 41.547, 1.502)
        ]
    }
}

# --- ASIGNACIÓN AUTOMÁTICA DE SIDs POR DESTINO ---
DESTINATION_SIDS = {
    "24L": {
        "BIKF": "NATPI4Q", "CYUL": "GRAUS7Q", "CYYZ": "GRAUS7Q", "DAAG": "LARPA7Q", "EBAW": "NATPI4Q",
        "EBBR": "OLOXO3Q", "EBOS": "NATPI4Q", "EDDB": "DALIN6Q", "EDDF": "DALIN6Q", "EDDH": "DALIN6Q",
        "EDDK": "DALIN6Q", "EDDL": "OLOXO3Q", "EDDM": "AGENA7Q", "EDDN": "DALIN6Q", "EDDP": "DALIN6Q",
        "EDDS": "DALIN6Q", "EDDT": "AGENA7Q", "EDDV": "DALIN6Q", "EETN": "DALIN6Q", "EFHK": "OLOXO3Q",
        "EGAA": "NATPI4Q", "EGBB": "NATPI4Q", "EGCC": "NATPI4Q", "EGFF": "NATPI4Q", "EGGD": "NATPI4Q",
        "EGGW": "NATPI4Q", "EGHI": "NATPI4Q", "EGKK": "NATPI4Q", "EGLL": "NATPI4Q", "EGMC": "NATPI4Q",
        "EGNM": "NATPI4Q", "EGNT": "NATPI4Q", "EGNX": "NATPI4Q", "EGPH": "NATPI4Q", "EGPK": "NATPI4Q",
        "EGSS": "NATPI4Q", "EHAM": "DALIN6Q", "EHEH": "DALIN6Q", "EHRD": "OLOXO3Q", "EIDW": "NATPI4Q",
        "EKBI": "OLOXO3Q", "EKCH": "OLOXO3Q", "ELLX": "OLOXO3Q", "ENBR": "OLOXO3Q", "ENGM": "OLOXO3Q",
        "EPKK": "AGENA7Q", "EPKT": "AGENA7Q", "EPWA": "AGENA7Q", "ESGG": "DALIN6Q", "ESKN": "DALIN6Q",
        "ESSA": "DALIN6Q", "ETNL": "OLOXO3Q", "EVRA": "AGENA7Q", "EYVI": "AGENA7Q", "GCFV": "LOTOS7Q",
        "GCLP": "LOTOS7Q", "GCRR": "LOTOS7Q", "GCXO": "LOTOS7Q", "GMFF": "LARPA7Q", "GMMN": "LOTOS7Q",
        "GMMX": "LOTOS7Q", "GMTT": "LOTOS7Q", "HECA": "DIPES3Q", "KATL": "GRAUS7Q", "KCLT": "NATPI4Q",
        "KEWR": "LOBAR8Q", "KJFK": "LOBAR8Q", "KMIA": "GRAUS7Q", "KPHL": "GRAUS7Q", "KUGN": "GRAUS7Q",
        "LBSF": "DIPES3Q", "LCLK": "DIPES3Q", "LDDU": "DIPES3Q", "LDSP": "DIPES3Q", "LDZA": "AGENA7Q",
        "LEAL": "LOTOS7Q", "LEAM": "LOTOS7Q", "LEAS": "GRAUS7Q", "LEBB": "GRAUS7Q", "LEBZ": "SENIA7Q",
        "LECO": "LOBAR8Q", "LEGE": "DALIN6Q", "LEGR": "LOTOS7Q", "LEIB": "LARPA7Q", "LEJR": "LOTOS7Q",
        "LELN": "LOBAR8Q", "LEMD": "SENIA7Q", "LEMG": "LOTOS7Q", "LEMH": "DUNES7Q", "LEPA": "LARPA7Q",
        "LESO": "GRAUS7Q", "LEST": "LOBAR8Q", "LEVC": "LOTOS7Q", "LEVD": "LOBAR8Q", "LEVX": "LOBAR8Q",
        "LEZL": "LOTOS7Q", "LFBD": "NATPI4Q", "LFLL": "DALIN6Q", "LFMD": "DALIN6Q", "LFML": "DALIN6Q",
        "LFMN": "DALIN6Q", "LFOB": "OLOXO3Q", "LFPG": "OLOXO3Q", "LFPO": "OLOXO3Q", "LFQQ": "OLOXO3Q",
        "LFRN": "NATPI4Q", "LFRS": "NATPI4Q", "LFSB": "DALIN6Q", "LGAV": "DIPES3Q", "LGIR": "DIPES3Q",
        "LGKR": "DIPES3Q", "LGMK": "DIPES3Q", "LHBP": "AGENA7Q", "LIBD": "DIPES3Q", "LICJ": "DIPES3Q",
        "LIEE": "DIPES3Q", "LIEO": "DIPES3Q", "LIMC": "AGENA7Q", "LIME": "AGENA7Q", "LIMF": "AGENA7Q",
        "LIML": "AGENA7Q", "LIPE": "AGENA7Q", "LIPH": "AGENA7Q", "LIPX": "AGENA7Q", "LIRF": "DIPES3Q",
        "LIRN": "DIPES3Q", "LIRP": "AGENA7Q", "LIRQ": "DIPES3Q", "LKPR": "AGENA7Q", "LLBG": "DIPES3Q",
        "LMML": "DIPES3Q", "LOWW": "AGENA7Q", "LPPR": "SENIA7Q", "LPPT": "SENIA7Q", "LRCL": "DALIN6Q",
        "LROP": "AGENA7Q", "LSGG": "DALIN6Q", "LSZH": "DALIN6Q", "LTBA": "DIPES3Q", "LTFJ": "DIPES3Q",
        "LWSK": "DIPES3Q", "LYTV": "DIPES3Q", "OLBA": "DIPES3Q", "OMAA": "LARPA7Q", "OMDB": "DIPES3Q",
        "OTHH": "DIPES3Q", "SAEZ": "GRAUS7Q", "SBGR": "LOTOS7Q", "SKBO": "SENIA7Q", "UKBB": "AGENA7Q",
        "UKKK": "DALIN6Q", "ULLI": "DALIN6Q", "UUDD": "DALIN6Q", "UUEE": "DALIN6Q", "WSSS": "DIPES3Q"
    },
    "06R": {
        "BIKF": "NATPI2R", "CYUL": "GRAUS3R", "CYYZ": "GRAUS3R", "DAAG": "LARPA4R", "EBAW": "NATPI2R",
        "EBBR": "OLOXO1R", "EBOS": "NATPI2R", "EDDB": "DALIN4R", "EDDF": "DALIN4R", "EDDH": "DALIN4R",
        "EDDK": "DALIN4R", "EDDL": "OLOXO1R", "EDDM": "AGENA4R", "EDDN": "DALIN4R", "EDDP": "DALIN4R",
        "EDDS": "DALIN4R", "EDDT": "AGENA4R", "EDDV": "DALIN4R", "EETN": "DALIN4R", "EFHK": "OLOXO1R",
        "EGAA": "NATPI2R", "EGBB": "NATPI2R", "EGCC": "NATPI2R", "EGFF": "NATPI2R", "EGGD": "NATPI2R",
        "EGGW": "NATPI2R", "EGHI": "NATPI2R", "EGKK": "NATPI2R", "EGLL": "NATPI2R", "EGMC": "NATPI2R",
        "EGNM": "NATPI2R", "EGNT": "NATPI2R", "EGNX": "NATPI2R", "EGPH": "NATPI2R", "EGPK": "NATPI2R",
        "EGSS": "NATPI2R", "EHAM": "DALIN4R", "EHEH": "DALIN4R", "EHRD": "OLOXO1R", "EIDW": "NATPI2R",
        "EKBI": "OLOXO1R", "EKCH": "OLOXO1R", "ELLX": "OLOXO1R", "ENBR": "OLOXO1R", "ENGM": "OLOXO1R",
        "EPKK": "AGENA4R", "EPKT": "AGENA4R", "EPWA": "AGENA4R", "ESGG": "DALIN4R", "ESKN": "DALIN4R",
        "ESSA": "DALIN4R", "ETNL": "OLOXO1R", "EVRA": "AGENA4R", "EYVI": "AGENA4R", "GCFV": "LOTOS3R",
        "GCLP": "LOTOS3R", "GCRR": "LOTOS3R", "GCXO": "LOTOS3R", "GMFF": "LARPA4R", "GMMN": "LOTOS3R",
        "GMMX": "LOTOS3R", "GMTT": "LOTOS3R", "HECA": "DIPES1R", "KATL": "GRAUS3R", "KCLT": "NATPI2R",
        "KEWR": "LOBAR4R", "KJFK": "LOBAR4R", "KMIA": "GRAUS3R", "KPHL": "GRAUS3R", "KUGN": "GRAUS3R",
        "LBSF": "DIPES1R", "LCLK": "DIPES1R", "LDDU": "DIPES1R", "LDSP": "DIPES1R", "LDZA": "AGENA4R",
        "LEAL": "LOTOS3R", "LEAM": "LOTOS3R", "LEAS": "GRAUS3R", "LEBB": "GRAUS3R", "LEBZ": "SENIA5R",
        "LECO": "LOBAR4R", "LEGE": "DALIN4R", "LEGR": "LOTOS3R", "LEIB": "LARPA4R", "LEJR": "LOTOS3R",
        "LELN": "LOBAR4R", "LEMD": "SENIA5R", "LEMG": "LOTOS3R", "LEMH": "DUNES4R", "LEPA": "LARPA4R",
        "LESO": "GRAUS3R", "LEST": "LOBAR4R", "LEVC": "LOTOS3R", "LEVD": "LOBAR4R", "LEVX": "LOBAR4R",
        "LEZL": "LOTOS3R", "LFBD": "NATPI2R", "LFLL": "DALIN4R", "LFMD": "DALIN4R", "LFML": "DALIN4R",
        "LFMN": "DALIN4R", "LFOB": "OLOXO1R", "LFPG": "OLOXO1R", "LFPO": "OLOXO1R", "LFQQ": "OLOXO1R",
        "LFRN": "NATPI2R", "LFRS": "NATPI2R", "LFSB": "DALIN4R", "LGAV": "DIPES1R", "LGIR": "DIPES1R",
        "LGKR": "DIPES1R", "LGMK": "DIPES1R", "LHBP": "AGENA4R", "LIBD": "DIPES1R", "LICJ": "DIPES1R",
        "LIEE": "DIPES1R", "LIEO": "DIPES1R", "LIMC": "AGENA4R", "LIME": "AGENA4R", "LIMF": "AGENA4R",
        "LIML": "AGENA4R", "LIPE": "AGENA4R", "LIPH": "AGENA4R", "LIPX": "AGENA4R", "LIRF": "DIPES1R",
        "LIRN": "DIPES1R", "LIRP": "AGENA4R", "LIRQ": "DIPES1R", "LKPR": "AGENA4R", "LLBG": "DIPES1R",
        "LMML": "DIPES1R", "LOWW": "AGENA4R", "LPPR": "SENIA5R", "LPPT": "SENIA5R", "LRCL": "DALIN4R",
        "LROP": "AGENA4R", "LSGG": "DALIN4R", "LSZH": "DALIN4R", "LTBA": "DIPES1R", "LTFJ": "DIPES1R",
        "LWSK": "DIPES1R", "LYTV": "DIPES1R", "OLBA": "DIPES1R", "OMAA": "LARPA4R", "OMDB": "DIPES1R",
        "OTHH": "DIPES1R", "SAEZ": "GRAUS3R", "SBGR": "LOTOS3R", "SKBO": "SENIA5R", "UKBB": "AGENA4R",
        "UKKK": "DALIN4R", "ULLI": "DALIN4R", "UUDD": "DALIN4R", "UUEE": "DALIN4R", "WSSS": "DIPES1R"
    }
}

# =========================================================
# --- DATOS DE STARs (LLEGADAS CON PUNTOS INTERMEDIOS) ---
# =========================================================
STARS_DATA = {
    "02": {
        "ALBER3N": [
            ("ALBER", 42.451, 2.832), ("CUTXE", 42.132, 2.754),
            ("UTHAN", 41.885, 2.379), ("ENJUC", 41.769, 2.204),
            ("SLL", 41.520, 2.110), ("BCN", 41.307, 2.108),
            ("BL645", 41.170, 2.185), ("VIBIM", 41.071, 2.206), ("LEBL 02", 41.282, 2.088)
        ],
        "BISBA5N": [
            ("BISBA", 42.086, 3.626), ("NEMUM", 42.009, 3.393),
            ("BGR", 41.948, 3.209), ("ENJUC", 41.769, 2.204),
            ("SLL", 41.520, 2.110), ("BCN", 41.307, 2.108),
            ("BL645", 41.170, 2.185), ("VIBIM", 41.071, 2.206), ("LEBL 02", 41.282, 2.088)
        ],
        "CASPE4N": [
            ("CASPE", 41.268, 0.199), ("BL678", 41.320, 1.106),
            ("BL670", 41.332, 1.327), ("VLA", 41.343, 1.548),
            ("ULKAL", 41.136, 1.588), ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "GRAUS3N": [
            ("GRAUS", 41.979, 0.376), ("LRD", 41.553, 0.648),
            ("VLA", 41.343, 1.548), ("ULKAL", 41.136, 1.588),
            ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "MARTA4N": [
            ("MARTA", 40.355, 1.280), ("PAPOS", 40.621, 1.449),
            ("TAQOH", 40.872, 1.631), ("ULKAL", 41.136, 1.588),
            ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "NEPAL4N": [
            ("NEPAL", 40.693, 1.925), ("TAQOH", 40.872, 1.631),
            ("ULKAL", 41.136, 1.588), ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "VERSO2N": [
            ("VERSO", 41.153, 3.757), ("OSTUR", 40.781, 2.894),
            ("ISWIQ", 41.014, 2.356), ("VIBIM", 41.071, 2.206), ("LEBL 02", 41.282, 2.088)
        ],
        "PUMAL5N": [
            ("PUMAL", 42.367, 2.008), ("BERGA", 42.172, 2.032),
            ("BOLQE", 41.734, 1.550), ("VIBOK", 41.547, 1.502),
            ("VLA", 41.343, 1.548), ("ULKAL", 41.136, 1.588),
            ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ]
    },
    "06L": {
        "ALBER2E": [
            ("ALBER", 42.451, 2.832), ("CUTXE", 42.132, 2.754),
            ("UTHAN", 41.885, 2.379), ("ENJUC", 41.769, 2.204),
            ("BL573", 41.680, 2.170), ("SLL", 41.520, 2.110), ("LEBL 06L", 41.288, 2.083)
        ],
        "BISBA2E": [
            ("BISBA", 42.086, 3.626), ("NEMUM", 42.009, 3.393),
            ("BGR", 41.948, 3.209), ("ENJUC", 41.769, 2.204),
            ("BL573", 41.680, 2.170), ("SLL", 41.520, 2.110), ("LEBL 06L", 41.288, 2.083)
        ],
        "CASPE3E": [
            ("CASPE", 41.268, 0.199), ("INCAH", 41.219, 0.592),
            ("PIJUH", 40.982, 0.907), ("TAQOH", 40.872, 1.631),
            ("RUBOT", 40.974, 1.706), ("LEBL 06L", 41.288, 2.083)
        ],
        "GRAUS1E": [
            ("GRAUS", 41.979, 0.376), ("LRD", 41.553, 0.648),
            ("RES", 41.144, 1.162), ("TAQOH", 40.872, 1.631),
            ("RUBOT", 40.974, 1.706), ("LEBL 06L", 41.288, 2.083)
        ],
        "MARTA3E": [
            ("MARTA", 40.355, 1.280), ("EBROX", 40.709, 1.232),
            ("RES", 41.144, 1.162), ("BL561", 41.249, 1.365),
            ("VLA", 41.343, 1.548), ("LEBL 06L", 41.288, 2.083)
        ],
        "NEPAL3E": [
            ("NEPAL", 40.693, 1.925), ("TAQOH", 40.872, 1.631),
            ("RUBOT", 40.974, 1.706), ("LEBL 06L", 41.288, 2.083)
        ],
        "VERSO3E": [
            ("VERSO", 41.153, 3.757), ("OSTUR", 40.781, 2.894),
            ("ISWIQ", 41.014, 2.356), ("VIBIM", 41.071, 2.206), ("LEBL 06L", 41.288, 2.083)
        ],
        "PUMAL1E": [
            ("PUMAL", 42.367, 2.008), ("BERGA", 42.172, 2.032),
            ("BOLQE", 41.734, 1.550), ("VIBOK", 41.547, 1.502),
            ("VLA", 41.343, 1.548), ("LEBL 06L", 41.288, 2.083)
        ]
    },
    "24R": {
        "ALBER2W": [
            ("ALBER", 42.451, 2.832), ("CUTXE", 42.132, 2.754),
            ("BL469", 41.804, 2.674), ("CLE", 41.640, 2.635), ("LEBL 24R", 41.311, 2.115)
        ],
        "BISBA2W": [
            ("BISBA", 42.086, 3.626), ("USSOF", 41.654, 3.027),
            ("XAMUR", 41.403, 2.872), ("LESBA", 41.255, 2.663), ("LEBL 24R", 41.311, 2.115)
        ],
        "CASPE2W": [
            ("CASPE", 41.268, 0.199), ("MECUH", 41.457, 1.072),
            ("VIBOK", 41.547, 1.502), ("BL461", 41.550, 1.891),
            ("SLL", 41.520, 2.110), ("LEBL 24R", 41.311, 2.115)
        ],
        "GRAUS2W": [
            ("GRAUS", 41.979, 0.376), ("TIRGO", 41.784, 1.126),
            ("BL459", 41.577, 1.901), ("SLL", 41.520, 2.110), ("LEBL 24R", 41.311, 2.115)
        ],
        "MARTA2W": [
            ("MARTA", 40.355, 1.280), ("NEPAL", 40.693, 1.925),
            ("RAVAX", 40.921, 2.088), ("RULOS", 41.177, 2.281), ("LEBL 24R", 41.311, 2.115)
        ],
        "NEPAL2W": [
            ("NEPAL", 40.693, 1.925), ("RAVAX", 40.921, 2.088),
            ("RULOS", 41.177, 2.281), ("LEBL 24R", 41.311, 2.115)
        ],
        "VERSO2W": [
            ("VERSO", 41.153, 3.757), ("SADEM", 41.210, 3.174),
            ("BL468", 41.230, 2.948), ("LESBA", 41.255, 2.663), ("LEBL 24R", 41.311, 2.115)
        ],
        "PUMAL2W": [
            ("PUMAL", 42.367, 2.008), ("ELLIH", 42.131, 2.213),
            ("BL465", 41.781, 2.515), ("CLE", 41.640, 2.635), ("LEBL 24R", 41.311, 2.115)
        ]
    }
}

# --- ASIGNACIÓN AUTOMÁTICA DE STARs POR ORIGEN ---
ORIGIN_STARS = {
    "02": {
        "BIKF": "GRAUS3N", "CYUL": "GRAUS3N", "CYYZ": "GRAUS3N", "DAAG": "MARTA4N", "EBAW": "ALBER3N",
        "EBBR": "ALBER3N", "EBOS": "ALBER3N", "EDDB": "BISBA5N", "EDDF": "ALBER3N", "EDDH": "ALBER3N",
        "EDDK": "ALBER3N", "EDDL": "ALBER3N", "EDDM": "BISBA5N", "EDDN": "BISBA5N", "EDDP": "BISBA5N",
        "EDDS": "BISBA5N", "EDDT": "BISBA5N", "EDDV": "ALBER3N", "EETN": "BISBA5N", "EFHK": "ALBER3N",
        "EGAA": "PUMAL5N", "EGBB": "PUMAL5N", "EGCC": "PUMAL5N", "EGFF": "PUMAL5N", "EGGD": "PUMAL5N",
        "EGGW": "PUMAL5N", "EGHI": "PUMAL5N", "EGKK": "PUMAL5N", "EGLL": "PUMAL5N", "EGMC": "PUMAL5N",
        "EGNM": "PUMAL5N", "EGNT": "PUMAL5N", "EGNX": "PUMAL5N", "EGPH": "PUMAL5N", "EGPK": "PUMAL5N",
        "EGSS": "PUMAL5N", "EHAM": "ALBER3N", "EHEH": "ALBER3N", "EHRD": "ALBER3N", "EIDW": "PUMAL5N",
        "EKBI": "ALBER3N", "EKCH": "BISBA5N", "ELLX": "ALBER3N", "ENBR": "ALBER3N", "ENGM": "ALBER3N",
        "EPKK": "BISBA5N", "EPKT": "BISBA5N", "EPWA": "BISBA5N", "ESGG": "ALBER3N", "ESKN": "ALBER3N",
        "ESSA": "ALBER3N", "ETNL": "ALBER3N", "EVRA": "BISBA5N", "EYVI": "BISBA5N", "GCFV": "MARTA4N",
        "GCLP": "MARTA4N", "GCRR": "MARTA4N", "GCXO": "MARTA4N", "GMFF": "MARTA4N", "GMMN": "MARTA4N",
        "GMMX": "MARTA4N", "GMTT": "MARTA4N", "HECA": "VERSO2N", "KATL": "GRAUS3N", "KCLT": "GRAUS3N",
        "KEWR": "GRAUS3N", "KJFK": "GRAUS3N", "KMIA": "GRAUS3N", "KPHL": "GRAUS3N", "KUGN": "GRAUS3N",
        "LBSF": "VERSO2N", "LCLK": "VERSO2N", "LDDU": "VERSO2N", "LDSP": "VERSO2N", "LDZA": "VERSO2N",
        "LEAL": "MARTA4N", "LEAM": "MARTA4N", "LEAS": "GRAUS3N", "LEBB": "GRAUS3N", "LEBZ": "CASPE4N",
        "LECO": "GRAUS3N", "LEGE": "BISBA5N", "LEGR": "MARTA4N", "LEIB": "MARTA4N", "LEJR": "MARTA4N",
        "LELN": "GRAUS3N", "LEMD": "CASPE4N", "LEMG": "MARTA4N", "LEMH": "VERSO2N", "LEPA": "NEPAL4N",
        "LESO": "GRAUS3N", "LEST": "GRAUS3N", "LEVC": "MARTA4N", "LEVD": "GRAUS3N", "LEVX": "GRAUS3N",
        "LEZL": "MARTA4N", "LFBD": "PUMAL5N", "LFLL": "ALBER3N", "LFMD": "BISBA5N", "LFML": "BISBA5N",
        "LFMN": "BISBA5N", "LFOB": "ALBER3N", "LFPG": "ALBER3N", "LFPO": "ALBER3N", "LFQQ": "ALBER3N",
        "LFRN": "PUMAL5N", "LFRS": "PUMAL5N", "LFSB": "ALBER3N", "LGAV": "VERSO2N", "LGIR": "VERSO2N",
        "LGKR": "VERSO2N", "LGMK": "VERSO2N", "LHBP": "BISBA5N", "LIBD": "VERSO2N", "LICJ": "VERSO2N",
        "LIEE": "VERSO2N", "LIEO": "VERSO2N", "LIMC": "BISBA5N", "LIME": "BISBA5N", "LIMF": "BISBA5N",
        "LIML": "BISBA5N", "LIPE": "BISBA5N", "LIPH": "BISBA5N", "LIPX": "BISBA5N", "LIRF": "VERSO2N",
        "LIRN": "VERSO2N", "LIRP": "BISBA5N", "LIRQ": "BISBA5N", "LKPR": "BISBA5N", "LLBG": "VERSO2N",
        "LMML": "VERSO2N", "LOWW": "BISBA5N", "LPPR": "CASPE4N", "LPPT": "CASPE4N", "LRCL": "BISBA5N",
        "LROP": "VERSO2N", "LSGG": "ALBER3N", "LSZH": "ALBER3N", "LTBA": "VERSO2N", "LTFJ": "VERSO2N",
        "LWSK": "VERSO2N", "LYTV": "VERSO2N", "OLBA": "VERSO2N", "OMAA": "VERSO2N", "OMDB": "VERSO2N",
        "OTHH": "VERSO2N", "SAEZ": "MARTA4N", "SBGR": "MARTA4N", "SKBO": "CASPE4N", "UKBB": "BISBA5N",
        "UKKK": "BISBA5N", "ULLI": "BISBA5N", "UUDD": "BISBA5N", "UUEE": "BISBA5N", "WSSS": "VERSO2N"
    },
    "06L": {
        "BIKF": "GRAUS1E", "CYUL": "GRAUS1E", "CYYZ": "GRAUS1E", "DAAG": "MARTA3E", "EBAW": "ALBER2E",
        "EBBR": "ALBER2E", "EBOS": "ALBER2E", "EDDB": "BISBA2E", "EDDF": "ALBER2E", "EDDH": "ALBER2E",
        "EDDK": "ALBER2E", "EDDL": "ALBER2E", "EDDM": "BISBA2E", "EDDN": "BISBA2E", "EDDP": "BISBA2E",
        "EDDS": "BISBA2E", "EDDT": "BISBA2E", "EDDV": "ALBER2E", "EETN": "BISBA2E", "EFHK": "ALBER2E",
        "EGAA": "PUMAL1E", "EGBB": "PUMAL1E", "EGCC": "PUMAL1E", "EGFF": "PUMAL1E", "EGGD": "PUMAL1E",
        "EGGW": "PUMAL1E", "EGHI": "PUMAL1E", "EGKK": "PUMAL1E", "EGLL": "PUMAL1E", "EGMC": "PUMAL1E",
        "EGNM": "PUMAL1E", "EGNT": "PUMAL1E", "EGNX": "PUMAL1E", "EGPH": "PUMAL1E", "EGPK": "PUMAL1E",
        "EGSS": "PUMAL1E", "EHAM": "ALBER2E", "EHEH": "ALBER2E", "EHRD": "ALBER2E", "EIDW": "PUMAL1E",
        "EKBI": "ALBER2E", "EKCH": "BISBA2E", "ELLX": "ALBER2E", "ENBR": "ALBER2E", "ENGM": "ALBER2E",
        "EPKK": "BISBA2E", "EPKT": "BISBA2E", "EPWA": "BISBA2E", "ESGG": "ALBER2E", "ESKN": "ALBER2E",
        "ESSA": "ALBER2E", "ETNL": "ALBER2E", "EVRA": "BISBA2E", "EYVI": "BISBA2E", "GCFV": "MARTA3E",
        "GCLP": "MARTA3E", "GCRR": "MARTA3E", "GCXO": "MARTA3E", "GMFF": "MARTA3E", "GMMN": "MARTA3E",
        "GMMX": "MARTA3E", "GMTT": "MARTA3E", "HECA": "VERSO3E", "KATL": "GRAUS1E", "KCLT": "GRAUS1E",
        "KEWR": "GRAUS1E", "KJFK": "GRAUS1E", "KMIA": "GRAUS1E", "KPHL": "GRAUS1E", "KUGN": "GRAUS1E",
        "LBSF": "VERSO3E", "LCLK": "VERSO3E", "LDDU": "VERSO3E", "LDSP": "VERSO3E", "LDZA": "VERSO3E",
        "LEAL": "MARTA3E", "LEAM": "MARTA3E", "LEAS": "GRAUS1E", "LEBB": "GRAUS1E", "LEBZ": "CASPE3E",
        "LECO": "GRAUS1E", "LEGE": "BISBA2E", "LEGR": "MARTA3E", "LEIB": "MARTA3E", "LEJR": "MARTA3E",
        "LELN": "GRAUS1E", "LEMD": "CASPE3E", "LEMG": "MARTA3E", "LEMH": "VERSO3E", "LEPA": "NEPAL3E",
        "LESO": "GRAUS1E", "LEST": "GRAUS1E", "LEVC": "MARTA3E", "LEVD": "GRAUS1E", "LEVX": "GRAUS1E",
        "LEZL": "MARTA3E", "LFBD": "PUMAL1E", "LFLL": "ALBER2E", "LFMD": "BISBA2E", "LFML": "BISBA2E",
        "LFMN": "BISBA2E", "LFOB": "ALBER2E", "LFPG": "ALBER2E", "LFPO": "ALBER2E", "LFQQ": "ALBER2E",
        "LFRN": "PUMAL1E", "LFRS": "PUMAL1E", "LFSB": "ALBER2E", "LGAV": "VERSO3E", "LGIR": "VERSO3E",
        "LGKR": "VERSO3E", "LGMK": "VERSO3E", "LHBP": "BISBA2E", "LIBD": "VERSO3E", "LICJ": "VERSO3E",
        "LIEE": "VERSO3E", "LIEO": "VERSO3E", "LIMC": "BISBA2E", "LIME": "BISBA2E", "LIMF": "BISBA2E",
        "LIML": "BISBA2E", "LIPE": "BISBA2E", "LIPH": "BISBA2E", "LIPX": "BISBA2E", "LIRF": "VERSO3E",
        "LIRN": "VERSO3E", "LIRP": "BISBA2E", "LIRQ": "BISBA2E", "LKPR": "BISBA2E", "LLBG": "VERSO3E",
        "LMML": "VERSO3E", "LOWW": "BISBA2E", "LPPR": "CASPE3E", "LPPT": "CASPE3E", "LRCL": "BISBA2E",
        "LROP": "VERSO3E", "LSGG": "ALBER2E", "LSZH": "ALBER2E", "LTBA": "VERSO3E", "LTFJ": "VERSO3E",
        "LWSK": "VERSO3E", "LYTV": "VERSO3E", "OLBA": "VERSO3E", "OMAA": "VERSO3E", "OMDB": "VERSO3E",
        "OTHH": "VERSO3E", "SAEZ": "MARTA3E", "SBGR": "MARTA3E", "SKBO": "CASPE3E", "UKBB": "BISBA2E",
        "UKKK": "BISBA2E", "ULLI": "BISBA2E", "UUDD": "BISBA2E", "UUEE": "BISBA2E", "WSSS": "VERSO3E"
    },
    "24R": {
        "BIKF": "GRAUS2W", "CYUL": "GRAUS2W", "CYYZ": "GRAUS2W", "DAAG": "MARTA2W", "EBAW": "ALBER2W",
        "EBBR": "ALBER2W", "EBOS": "ALBER2W", "EDDB": "BISBA2W", "EDDF": "ALBER2W", "EDDH": "ALBER2W",
        "EDDK": "ALBER2W", "EDDL": "ALBER2W", "EDDM": "BISBA2W", "EDDN": "BISBA2W", "EDDP": "BISBA2W",
        "EDDS": "BISBA2W", "EDDT": "BISBA2W", "EDDV": "ALBER2W", "EETN": "BISBA2W", "EFHK": "ALBER2W",
        "EGAA": "PUMAL2W", "EGBB": "PUMAL2W", "EGCC": "PUMAL2W", "EGFF": "PUMAL2W", "EGGD": "PUMAL2W",
        "EGGW": "PUMAL2W", "EGHI": "PUMAL2W", "EGKK": "PUMAL2W", "EGLL": "PUMAL2W", "EGMC": "PUMAL2W",
        "EGNM": "PUMAL2W", "EGNT": "PUMAL2W", "EGNX": "PUMAL2W", "EGPH": "PUMAL2W", "EGPK": "PUMAL2W",
        "EGSS": "PUMAL2W", "EHAM": "ALBER2W", "EHEH": "ALBER2W", "EHRD": "ALBER2W", "EIDW": "PUMAL2W",
        "EKBI": "ALBER2W", "EKCH": "BISBA2W", "ELLX": "ALBER2W", "ENBR": "ALBER2W", "ENGM": "ALBER2W",
        "EPKK": "BISBA2W", "EPKT": "BISBA2W", "EPWA": "BISBA2W", "ESGG": "ALBER2W", "ESKN": "ALBER2W",
        "ESSA": "ALBER2W", "ETNL": "ALBER2W", "EVRA": "BISBA2W", "EYVI": "BISBA2W", "GCFV": "MARTA2W",
        "GCLP": "MARTA2W", "GCRR": "MARTA2W", "GCXO": "MARTA2W", "GMFF": "MARTA2W", "GMMN": "MARTA2W",
        "GMMX": "MARTA2W", "GMTT": "MARTA2W", "HECA": "VERSO2W", "KATL": "GRAUS2W", "KCLT": "GRAUS2W",
        "KEWR": "GRAUS2W", "KJFK": "GRAUS2W", "KMIA": "GRAUS2W", "KPHL": "GRAUS2W", "KUGN": "GRAUS2W",
        "LBSF": "VERSO2W", "LCLK": "VERSO2W", "LDDU": "VERSO2W", "LDSP": "VERSO2W", "LDZA": "VERSO2W",
        "LEAL": "MARTA2W", "LEAM": "MARTA2W", "LEAS": "GRAUS2W", "LEBB": "GRAUS2W", "LEBZ": "CASPE2W",
        "LECO": "GRAUS2W", "LEGE": "BISBA2W", "LEGR": "MARTA2W", "LEIB": "MARTA2W", "LEJR": "MARTA2W",
        "LELN": "GRAUS2W", "LEMD": "CASPE2W", "LEMG": "MARTA2W", "LEMH": "VERSO2W", "LEPA": "NEPAL2W",
        "LESO": "GRAUS2W", "LEST": "GRAUS2W", "LEVC": "MARTA2W", "LEVD": "GRAUS2W", "LEVX": "GRAUS2W",
        "LEZL": "MARTA2W", "LFBD": "PUMAL2W", "LFLL": "ALBER2W", "LFMD": "BISBA2W", "LFML": "BISBA2W",
        "LFMN": "BISBA2W", "LFOB": "ALBER2W", "LFPG": "ALBER2W", "LFPO": "ALBER2W", "LFQQ": "ALBER2W",
        "LFRN": "PUMAL2W", "LFRS": "PUMAL2W", "LFSB": "ALBER2W", "LGAV": "VERSO2W", "LGIR": "VERSO2W",
        "LGKR": "VERSO2W", "LGMK": "VERSO2W", "LHBP": "BISBA2W", "LIBD": "VERSO2W", "LICJ": "VERSO2W",
        "LIEE": "VERSO2W", "LIEO": "VERSO2W", "LIMC": "BISBA2W", "LIME": "BISBA2W", "LIMF": "BISBA2W",
        "LIML": "BISBA2W", "LIPE": "BISBA2W", "LIPH": "BISBA2W", "LIPX": "BISBA2W", "LIRF": "VERSO2W",
        "LIRN": "VERSO2W", "LIRP": "BISBA2W", "LIRQ": "BISBA2W", "LKPR": "BISBA2W", "LLBG": "VERSO2W",
        "LMML": "VERSO2W", "LOWW": "BISBA2W", "LPPR": "CASPE2W", "LPPT": "CASPE2W", "LRCL": "BISBA2W",
        "LROP": "VERSO2W", "LSGG": "ALBER2W", "LSZH": "ALBER2W", "LTBA": "VERSO2W", "LTFJ": "VERSO2W",
        "LWSK": "VERSO2W", "LYTV": "VERSO2W", "OLBA": "VERSO2W", "OMAA": "VERSO2W", "OMDB": "VERSO2W",
        "OTHH": "VERSO2W", "SAEZ": "MARTA2W", "SBGR": "MARTA2W", "SKBO": "CASPE2W", "UKBB": "BISBA2W",
        "UKKK": "BISBA2W", "ULLI": "BISBA2W", "UUDD": "BISBA2W", "UUEE": "BISBA2W", "WSSS": "VERSO2W"
    }
}

# =========================================================
# --- DATOS GLOBALES Y MOTOR DEL MAPA RADAR ---
# =========================================================
COLOR_MAR = "#08182B"
COLOR_TIERRA = "#172635"
COLOR_FRONTERA_INT = "#5D8AA8"
COLOR_FRONTERA_REG = "#3A5A78"

RADAR_MIN_LAT, RADAR_MAX_LAT = 40.0, 43.1
RADAR_MIN_LON, RADAR_MAX_LON = -1.0, 4.2


def get_radar_xy(lat, lon, w, h):
    x = (lon - RADAR_MIN_LON) / (RADAR_MAX_LON - RADAR_MIN_LON) * w
    y = h - ((lat - RADAR_MIN_LAT) / (RADAR_MAX_LAT - RADAR_MIN_LAT) * h)
    return x, y


LINEA_COSTA = [(40.00, 0.05), (40.20, 0.20), (40.40, 0.40), (40.52, 0.52), (40.61, 0.65), (40.71, 0.80), (40.74, 0.88),
               (40.78, 0.75), (40.85, 0.79), (40.95, 0.85), (41.05, 1.10), (41.11, 1.25), (41.15, 1.34), (41.19, 1.45),
               (41.21, 1.56), (41.23, 1.70), (41.24, 1.85), (41.27, 2.00), (41.29, 2.10), (41.35, 2.16), (41.40, 2.22),
               (41.45, 2.28), (41.50, 2.36), (41.55, 2.46), (41.60, 2.58), (41.65, 2.70), (41.68, 2.82), (41.73, 2.95),
               (41.80, 3.05), (41.85, 3.12), (41.95, 3.21), (42.02, 3.20), (42.12, 3.16), (42.20, 3.18), (42.27, 3.18),
               (42.32, 3.32), (42.40, 3.20), (42.44, 3.16), (42.50, 3.08), (42.60, 3.03), (42.70, 3.04), (42.80, 3.04),
               (43.00, 3.10), (43.10, 3.15)]
POLIGONO_TIERRA = LINEA_COSTA + [(43.10, -1.00), (40.00, -1.00), (40.00, 0.05)]
ANDORRA = [(42.54, 1.73), (42.43, 1.45), (42.56, 1.42), (42.65, 1.53), (42.54, 1.73)]
FRONTERA_FRA_ESP_ESTE = [(42.44, 3.16), (42.42, 2.95), (42.34, 2.86), (42.40, 2.44), (42.42, 2.15), (42.35, 1.95),
                         (42.54, 1.73)]
FRONTERA_FRA_ESP_OESTE = [(42.56, 1.42), (42.65, 1.25), (42.80, 0.85), (42.85, 0.73), (42.75, 0.00), (42.80, -0.40),
                          (42.90, -0.80), (43.00, -1.00)]
FRONTERA_CAT_ARA = [(42.85, 0.73), (42.75, 0.74), (42.60, 0.74), (42.45, 0.72), (42.30, 0.70), (42.15, 0.45),
                    (42.00, 0.35), (41.80, 0.32), (41.60, 0.30), (41.40, 0.30), (41.25, 0.20), (41.10, 0.15),
                    (40.90, 0.15), (40.70, 0.15)]
FRONTERA_CAT_VAL = [(40.70, 0.15), (40.65, 0.25), (40.60, 0.30), (40.52, 0.52)]
FRONTERA_ARA_VAL = [(40.70, 0.15), (40.60, -0.10), (40.40, -0.40), (40.20, -0.80), (40.10, -1.00)]
FRONTERA_ARA_NAV = [(42.90, -0.80), (42.75, -0.95), (42.60, -1.00)]
CIUDADES = [("BARCELONA", 41.38, 2.18), ("TARRAGONA", 41.11, 1.25), ("LLEIDA", 41.61, 0.62), ("GIRONA", 41.98, 2.82),
            ("ZARAGOZA", 41.65, -0.88), ("HUESCA", 42.14, -0.40)]

# ─────────────────────────────────────────────
#  Meteorological rules for Barcelona (LEBL)
# ─────────────────────────────────────────────
def GetLEBLRunwayConfig(wind_dir, wind_speed, is_night):
    """
    Devuelve (Pista_Aterrizaje, Pista_Despegue, Modo_Operativo, Explicacion)
    basado en las normativas reales del aeropuerto de El Prat.
    """
    if is_night:
        # Excepción Nocturna: Viento fuerte de cola/cruzado
        if 150 <= wind_dir <= 330 and wind_speed > 18.5:
            return "02", "24L", "Nighttime configuration (ATYPICAL) 🌙💨", "⚠️ Configuration change: Strong crosswind/tailwind."
        else:
            return "02", "06R", "Standard nighttime configuration 🌙", "Standard conditions. No exceptions applied."
    else:
        # Excepción Diurna: Viento componente Norte/Este
        if (wind_dir >= 330 or wind_dir <= 150) and wind_speed > 18.5:
            return "06L", "06R", "East daytime configuration (ATYPICAL) ☀️💨", "⚠️ East configuration change: Strong wind coming from North/East."
        else:
            return "24R", "24L", "West daytime configuration (NORMAL) ☀️", "Standard conditions. No exceptions applied."