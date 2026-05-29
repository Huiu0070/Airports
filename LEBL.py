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