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