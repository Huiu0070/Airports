import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from aircraft import *
from airports import *
from LEBL import *

airports   = []
aircrafts  = []
departures = []
merged     = []
bcn        = None


# ═══════════════════════════════════════════════════
#  Password
# ═══════════════════════════════════════════════════

PASSWORD = "LEBL"

def ask_password():
    """Shows a modal password dialog. Exits the program if cancelled or wrong."""
    dialog = tk.Tk()
    dialog.title("Airport Manager – Login")
    dialog.resizable(False, False)
    dialog.configure(bg="white")
    try:
        dialog.iconbitmap("icon.ico")
        dialog.wm_iconbitmap("icon.ico")
    except Exception:
        pass

    dialog.update_idletasks()
    w, h = 320, 160
    x = (dialog.winfo_screenwidth()  - w) // 2
    y = (dialog.winfo_screenheight() - h) // 2
    dialog.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(dialog, text="✈  Airport Manager", bg="white",
             font=("Helvetica", 13, "bold"), fg="black").pack(pady=(18, 2))
    tk.Label(dialog, text="Enter password to continue", bg="white",
             font=("Helvetica", 9), fg="#555555").pack()

    entry = tk.Entry(dialog, show="●", font=("Helvetica", 11),
                     relief="solid", bd=1, width=20, justify="center")
    entry.pack(pady=10)
    entry.focus_set()

    result = {"ok": False}

    def attempt():
        if entry.get() == PASSWORD:
            result["ok"] = True
            dialog.destroy()
        else:
            entry.delete(0, tk.END)
            tk.Label(dialog, text="Incorrect password", bg="white",
                     font=("Helvetica", 9), fg="red").place(relx=0.5, rely=0.88, anchor="center")

    def on_cancel():
        dialog.destroy()

    btn_frame = tk.Frame(dialog, bg="white")
    btn_frame.pack()
    tk.Button(btn_frame, text="Login", command=attempt,
              bg="royalblue", fg="white", relief="flat",
              padx=12, pady=4, font=("Helvetica", 9),
              activebackground="navy", activeforeground="white").pack(side="left", padx=6)
    tk.Button(btn_frame, text="Cancel", command=on_cancel,
              bg="#CCCCCC", fg="#333333", relief="flat",
              padx=12, pady=4, font=("Helvetica", 9)).pack(side="left", padx=6)

    dialog.bind("<Return>", lambda e: attempt())
    dialog.protocol("WM_DELETE_WINDOW", on_cancel)
    dialog.mainloop()

    if not result["ok"]:
        raise SystemExit

ask_password()


# ═══════════════════════════════════════════════════
#  Info panel helpers  (right column)
# ═══════════════════════════════════════════════════

def clear_info_panel():
    for widget in info_frame.winfo_children():
        widget.destroy()

def show_info_label(title, lines):
    clear_info_panel()
    tk.Label(info_frame, text=title, bg="#F0F4F8",
             font=("Helvetica", 11, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 4))

    frame_list = tk.Frame(info_frame, bg="#F0F4F8")
    frame_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    scroll = tk.Scrollbar(frame_list)
    scroll.pack(side="right", fill="y")

    lb = tk.Listbox(frame_list, font=("Courier", 9),
                    bg="white", fg="#1A1A1A",
                    selectbackground="royalblue",
                    relief="solid", bd=1,
                    yscrollcommand=scroll.set)
    lb.pack(side="left", fill="both", expand=True)
    scroll.config(command=lb.yview)

    for line in lines:
        lb.insert(tk.END, line)

def show_info_plot(fig):
    clear_info_panel()
    tk.Label(info_frame, text="Chart", bg="#F0F4F8",
             font=("Helvetica", 11, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 4))

    canvas_plot = FigureCanvasTkAgg(fig, master=info_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

def show_info_gate_diagram():
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first (Terminals.txt).")
        return

    clear_info_panel()
    tk.Label(info_frame, text="Gate Diagram – LEBL", bg="#F0F4F8",
             font=("Helvetica", 11, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 2))

    tip_var = tk.StringVar(value="Hover over a gate to see its name.")
    tk.Label(info_frame, textvariable=tip_var, bg="#F0F4F8",
             font=("Courier", 9), fg="gray").pack(anchor="w", padx=10)

    frame_c = tk.Frame(info_frame, bg="#F0F4F8")
    frame_c.pack(fill="both", expand=True, padx=10, pady=(4, 4))

    h_scroll = tk.Scrollbar(frame_c, orient="horizontal")
    h_scroll.pack(side="bottom", fill="x")
    v_scroll = tk.Scrollbar(frame_c, orient="vertical")
    v_scroll.pack(side="right", fill="y")

    canvas = tk.Canvas(frame_c, bg="white",
                       xscrollcommand=h_scroll.set,
                       yscrollcommand=v_scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    h_scroll.config(command=canvas.xview)
    v_scroll.config(command=canvas.yview)

    _draw_airport_on_canvas(canvas, bcn)

    def on_motion(event):
        cx = canvas.canvasx(event.x)
        cy = canvas.canvasy(event.y)
        items = canvas.find_overlapping(cx - 5, cy - 5, cx + 5, cy + 5)
        for item in items:
            tags = canvas.gettags(item)
            if "gate_hit" in tags:
                for t in tags:
                    if t != "gate_hit" and t != "current":
                        tip_var.set(t)
                        return
        tip_var.set("Hover over a gate to see its name.")

    canvas.bind("<Motion>", on_motion)

    tk.Button(info_frame, text="Refresh",
              command=lambda: _draw_airport_on_canvas(canvas, bcn),
              bg="royalblue", fg="white", relief="flat",
              padx=8, pady=3, font=("Helvetica", 9),
              activebackground="navy", activeforeground="white").pack(pady=(0, 6))


# ═══════════════════════════════════════════════════
#  Status bar
# ═══════════════════════════════════════════════════

def update_status():
    n_airp = len(airports)
    n_sch  = sum(1 for a in airports if a.isSchengen)
    n_nsch = n_airp - n_sch
    n_fl   = len(aircrafts)
    n_dep  = len(departures)
    n_mer  = len(merged)
    gate_txt = ""
    if bcn is not None:
        occ   = GateOccupancy(bcn)
        total = len(occ)
        used  = sum(1 for _, ocupado, _ in occ if ocupado)
        gate_txt = f"  |  Gates: {used}/{total} occupied"
    status_label.config(
        text=f"  ✈ Airports: {n_airp}  |  Schengen: {n_sch}  "
             f"Non-Schengen: {n_nsch}  |  Arrivals: {n_fl}  "
             f"Departures: {n_dep}  Merged: {n_mer}{gate_txt}"
    )


# ═══════════════════════════════════════════════════
#  Airport functions
# ═══════════════════════════════════════════════════

def refresh_airport_list():
    airport_listbox.delete(0, tk.END)
    for airport in airports:
        schengen = "✓ Sch" if airport.isSchengen else "✗ Non"
        airport_listbox.insert(tk.END,
            f"  {airport.code:<7} {str(round(airport.latitude,  2)):<9}"
            f" {str(round(airport.longitude, 2)):<10} {schengen}")
    update_status()

def load_airports():
    global airports
    path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not path:
        return
    airports = LoadAirport(path)
    for airport in airports:
        SetSchengen(airport)
    refresh_airport_list()
    lines = []
    for a in airports:
        sch = "Schengen" if a.isSchengen else "Non-Schengen"
        lines.append(f"  {a.code:<8}  lat {round(a.latitude,2):<9}  lon {round(a.longitude,2):<10}  {sch}")
    show_info_label(f"Airports loaded  ({len(airports)})", lines)
    messagebox.showinfo("Done", str(len(airports)) + " airports loaded.")

def add_airport():
    code = entry_code.get().strip().upper()
    if code == "":
        messagebox.showerror("Error", "Please enter an ICAO code.")
        return
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        new_airport = Airport(code, lat, lon)
        SetSchengen(new_airport)
        AddAirport(airports, new_airport)
        refresh_airport_list()
        messagebox.showinfo("Done", "Airport " + code + " added.")
    except ValueError:
        messagebox.showerror("Error", "Latitude and longitude must be valid numbers.")
    except TypeError:
        messagebox.showerror("Error", "Invalid type for latitude or longitude.")
    except AttributeError:
        messagebox.showerror("Error", "A widget or object is not correctly initialized.")

def delete_airport():
    code = entry_code.get().strip().upper()
    if code == "":
        messagebox.showerror("Error", "Please enter an ICAO code.")
        return
    found = any(airport.code == code for airport in airports)
    if not found:
        messagebox.showerror("Error", "Airport " + code + " not found.")
    else:
        RemoveAirport(airports, code)
        refresh_airport_list()
        messagebox.showinfo("Done", "Airport " + code + " deleted.")

def save_schengen():
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if path:
        SaveSchengenAirports(airports, path)
        messagebox.showinfo("Done", "Schengen airports saved.")

def update_schengen():
    for airport in airports:
        SetSchengen(airport)
    refresh_airport_list()
    messagebox.showinfo("Done", "Schengen updated for all airports.")

def show_airports():
    lines = []
    for a in airports:
        sch = "Schengen" if a.isSchengen else "Non-Schengen"
        lines.append(f"  {a.code:<8}  lat {round(a.latitude,2):<9}  lon {round(a.longitude,2):<10}  {sch}")
    show_info_label(f"All airports  ({len(airports)})", lines)

def plot_airports():
    if len(airports) == 0:
        messagebox.showerror("Error", "No airports loaded.")
        return
    n_sch  = sum(1 for a in airports if a.isSchengen)
    n_nsch = len(airports) - n_sch
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(["Schengen", "Non-Schengen"], [n_sch, n_nsch],
           color=["#3A7FC1", "#D9704A"])
    ax.set_title("Airports by type")
    ax.set_ylabel("Count")
    fig.tight_layout()
    show_info_plot(fig)

def map_airports():
    import os
    if len(airports) == 0:
        messagebox.showerror("Error", "No airports loaded.")
        return
    filepath = MapAirports(airports)
    if filepath:
        os.startfile(filepath)
        messagebox.showinfo("Done", "Map saved and opened in Google Earth.")


# ═══════════════════════════════════════════════════
#  Flights (arrivals) functions
# ═══════════════════════════════════════════════════

def refresh_flights_list():
    flights_listbox.delete(0, tk.END)
    for ac in aircrafts:
        flights_listbox.insert(tk.END,
            f"  {ac.timelanding:<10} {ac.origin:<8} {ac.company}")
    update_status()

def load_arrivals():
    global aircrafts
    path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not path:
        return
    aircrafts = LoadArrivals(path)
    refresh_flights_list()
    lines = []
    for ac in aircrafts:
        lines.append(f"  {ac.timelanding:<10} {ac.origin:<8} {ac.company}")
    show_info_label(f"Flights loaded  ({len(aircrafts)})", lines)
    refresh_ticker()
    messagebox.showinfo("Done", str(len(aircrafts)) + " flights loaded.")

def save_flights():
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if path:
        SaveFlights(aircrafts, path)
        messagebox.showinfo("Done", "Flights saved successfully.")

def plot_arrivals():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    hours = {}
    for ac in aircrafts:
        try:
            h = int(str(ac.timelanding)[:2])
        except (ValueError, TypeError):
            h = 0
        hours[h] = hours.get(h, 0) + 1
    sorted_hours = sorted(hours.keys())
    counts = [hours[h] for h in sorted_hours]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar([str(h).zfill(2) + "h" for h in sorted_hours], counts, color="#3A7FC1")
    ax.set_title("Arrivals by hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Flights")
    plt.xticks(rotation=45, ha="right", fontsize=7)
    fig.tight_layout()
    show_info_plot(fig)

def plot_airlines():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    airline_counts = {}
    for ac in aircrafts:
        airline_counts[ac.company] = airline_counts.get(ac.company, 0) + 1
    sorted_airlines = sorted(airline_counts.items(), key=lambda x: x[1], reverse=True)
    names  = [item[0] for item in sorted_airlines]
    counts = [item[1] for item in sorted_airlines]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(names, counts, color="#3A7FC1")
    ax.set_title("Flights by airline")
    ax.set_ylabel("Flights")
    plt.xticks(rotation=45, ha="right", fontsize=7)
    fig.tight_layout()
    show_info_plot(fig)

def plot_flights_type():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    n_sch  = sum(1 for ac in aircrafts if IsSchengenAirport(ac.origin))
    n_nsch = len(aircrafts) - n_sch
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(["Schengen", "Non-Schengen"], [n_sch, n_nsch],
           color=["#3A7FC1", "#D9704A"])
    ax.set_title("Flights by Schengen type")
    ax.set_ylabel("Flights")
    fig.tight_layout()
    show_info_plot(fig)

def map_flights():
    import os
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    filepath = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("KML files", "*.kml"), ("All files", "*.*")],
        initialfile="Flights_map.kml",
        title="Save flights KML map")
    if not filepath:
        return
    MapFlights(aircrafts, filepath)
    os.startfile(filepath)
    messagebox.showinfo("Done", "KML saved and opened in Google Earth.")

def long_distance():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    long = LongDistanceArrivals(aircrafts)
    lines = []
    for ac in long:
        lines.append(f"  {ac.timelanding:<10} {ac.origin:<8} {ac.company}")
    show_info_label(f"Long distance flights  ({len(long)})", lines)


# ═══════════════════════════════════════════════════
#  V3 – LEBL gate management functions
# ═══════════════════════════════════════════════════

def load_airport_structure():
    global bcn
    path = filedialog.askopenfilename(
        title="Select airport structure file (Terminals.txt)",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not path:
        return
    result = LoadAirportStructure(path)
    if result == -1:
        messagebox.showerror("Error", "Could not read the airport structure file.")
        return
    bcn = result
    total_gates = sum(len(ba.gates)
                      for t in bcn.Terminals
                      for ba in t.BoardingAreas)
    lines = []
    for t in bcn.Terminals:
        lines.append(f"  {t.number}  –  {len(t.BoardingAreas)} boarding areas")
        for ba in t.BoardingAreas:
            sch = "Schengen" if ba.schengen else "Non-Schengen"
            lines.append(f"      Area {ba.area}  {sch:<15}  {len(ba.gates)} gates")
    show_info_label(f"Structure: {bcn.CompleteName}  ({total_gates} gates total)", lines)
    update_status()
    messagebox.showinfo("Done",
        f"Airport '{bcn.CompleteName}' loaded.\n"
        f"{len(bcn.Terminals)} terminals, {total_gates} gates.")

def assign_gates_to_flights():
    global bcn
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first.")
        return
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    assigned   = 0
    unassigned = 0
    for ac in aircrafts:
        result = AssignGate(bcn, ac)
        if result == -1:
            unassigned = unassigned + 1
        else:
            assigned = assigned + 1
    update_status()
    show_gate_occupancy_list()
    messagebox.showinfo("Gate assignment",
        f"Assigned: {assigned}  |  Could not assign: {unassigned}")

def show_gate_diagram():
    show_info_gate_diagram()

def show_gate_occupancy_list():
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first.")
        return
    occ = GateOccupancy(bcn)
    lines = []
    for gate_name, ocupado, aircraft_id in occ:
        if ocupado:
            lines.append(f"  {gate_name:<22} OCCUPIED   {aircraft_id}")
        else:
            lines.append(f"  {gate_name:<22} free")
    show_info_label(f"Gate occupancy  ({len(occ)} gates)", lines)


# ═══════════════════════════════════════════════════
#  V4 – Departures and merged movements
# ═══════════════════════════════════════════════════

def refresh_departures_list():
    departures_listbox.delete(0, tk.END)
    for ac in departures:
        departures_listbox.insert(tk.END,
            f"  {ac.timedeparture:<10} {ac.destination:<8} {ac.company}  [{ac.id}]")
    update_status()

def load_departures():
    global departures
    path = filedialog.askopenfilename(
        title="Select departures file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not path:
        return
    departures = LoadDepartures(path)
    lines = []
    for ac in departures:
        lines.append(f"  {ac.timedeparture:<10} {ac.destination:<8} {ac.company}  [{ac.id}]")
    show_info_label(f"Departures loaded  ({len(departures)})", lines)
    refresh_departures_list()
    refresh_ticker()
    messagebox.showinfo("Done", str(len(departures)) + " departures loaded.")

def merge_movements():
    global merged
    if len(aircrafts) == 0 and len(departures) == 0:
        messagebox.showerror("Error", "Load arrivals and/or departures first.")
        return
    result = MergeMovements(aircrafts, departures)
    if result == -1:
        messagebox.showerror("Error", "Could not merge (both lists are empty).")
        return
    merged = result
    lines = []
    for ac in merged:
        arr = ac.timelanding   if ac.timelanding   else "---"
        dep = ac.timedeparture if ac.timedeparture else "---"
        lines.append(f"  {ac.id:<10} {ac.origin:<8} arr:{arr:<8} dep:{dep:<8} {ac.company}")
    show_info_label(f"Merged movements  ({len(merged)})", lines)
    update_status()
    messagebox.showinfo("Done", str(len(merged)) + " movements merged.")

def show_night_aircraft():
    if len(merged) == 0:
        messagebox.showerror("Error", "Merge movements first.")
        return
    result = NightAircraft(merged)
    if result == -1:
        messagebox.showerror("Error", "Merged list is empty.")
        return
    lines = []
    for ac in result:
        lines.append(f"  {ac.id:<10} {ac.destination:<8} dep:{ac.timedeparture}  {ac.company}")
    show_info_label(f"Night aircraft  ({len(result)})", lines)

def assign_night_gates_v4():
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first.")
        return
    if len(merged) == 0:
        messagebox.showerror("Error", "Merge movements first.")
        return
    night = NightAircraft(merged)
    if night == -1 or len(night) == 0:
        messagebox.showinfo("Info", "No night aircraft found.")
        return
    result = AssignNightGates(bcn, night)
    if result == -1:
        messagebox.showerror("Error", "Night aircraft list is empty.")
        return
    update_status()
    show_gate_occupancy_list()
    messagebox.showinfo("Done", f"Night gates assigned to {len(night)} aircraft.")

def free_gate_by_id():
    ac_id = entry_free_gate.get().strip().upper()
    if ac_id == "":
        messagebox.showerror("Error", "Enter an aircraft ID.")
        return
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first.")
        return
    result = FreeGate(bcn, ac_id)
    if result == -1:
        messagebox.showerror("Error", f"Aircraft '{ac_id}' not found in any gate.")
    else:
        update_status()
        show_gate_occupancy_list()
        messagebox.showinfo("Done", f"Gate freed for aircraft '{ac_id}'.")

def assign_gates_at_time():
    time_str = entry_time.get().strip()
    if time_str == "":
        messagebox.showerror("Error", "Enter a time (e.g. 08:00).")
        return
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first.")
        return
    if len(merged) == 0:
        messagebox.showerror("Error", "Merge movements first.")
        return
    unassigned = AssignGatesAtTime(bcn, merged, time_str)
    update_status()
    show_gate_occupancy_list()
    messagebox.showinfo("Gates at " + time_str,
        f"Gates updated for period starting {time_str}.\nUnassigned: {unassigned}")

def plot_day_occupancy():
    import copy
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first.")
        return
    if len(merged) == 0:
        messagebox.showerror("Error", "Merge movements first.")
        return
    fig = PlotDayOccupancy(copy.deepcopy(bcn), merged)
    show_info_plot(fig)


# ═══════════════════════════════════════════════════
#  Gate diagram drawing
# ═══════════════════════════════════════════════════

COL_FREE     = "#AAAAAA"
COL_OCCUPIED = "#2ECC71"
COL_SCHENGEN = "#3A7FC1"
COL_NONSCH   = "#D9704A"
COL_T1_BG    = "#D6EAF8"
COL_T2_BG    = "#E8DAEF"
COL_TEXT     = "#1A1A1A"

SPINE_W         = 18
GATE_LEN        = 36
AREA_SPACING    = 48
PAD             = 36
LABEL_H         = 22
SPINE_HEIGHT_PX = 520


def _draw_airport_on_canvas(canvas, bcn):
    canvas.delete("all")

    x_cursor = PAD
    y_top    = PAD

    for terminal in bcn.Terminals:
        num_areas = len(terminal.BoardingAreas)
        max_gates = max(len(ba.gates) for ba in terminal.BoardingAreas)

        gate_gap = max(4, SPINE_HEIGHT_PX // max_gates)
        finger_w = max(2, min(5, gate_gap - 1))

        t_width  = (num_areas * (SPINE_W + GATE_LEN + AREA_SPACING) + GATE_LEN + PAD)
        t_height = PAD + 20 + max_gates * gate_gap + LABEL_H + PAD

        t_color = COL_T1_BG if terminal.number == "T1" else COL_T2_BG
        canvas.create_rectangle(
            x_cursor, y_top, x_cursor + t_width, y_top + t_height,
            fill=t_color, outline="#7799AA", width=2)
        canvas.create_text(
            x_cursor + 10, y_top + 8, text=terminal.number,
            anchor="nw", font=("Helvetica", 12, "bold"), fill=COL_TEXT)

        x_spine     = x_cursor + PAD + GATE_LEN
        y_spine_top = y_top + PAD + 20

        for ba in terminal.BoardingAreas:
            num_gates    = len(ba.gates)
            spine_height = num_gates * gate_gap
            spine_color  = COL_SCHENGEN if ba.schengen else COL_NONSCH

            canvas.create_rectangle(
                x_spine, y_spine_top,
                x_spine + SPINE_W, y_spine_top + spine_height,
                fill=spine_color, outline=spine_color, width=0)
            canvas.create_text(
                x_spine + SPINE_W // 2, y_spine_top + spine_height + 6,
                text=ba.area, anchor="n",
                font=("Helvetica", 9, "bold"), fill=COL_TEXT)

            for j in range(num_gates):
                gate   = ba.gates[j]
                y_gate = y_spine_top + j * gate_gap + gate_gap // 2
                color  = COL_OCCUPIED if gate.ocupado else COL_FREE

                if j % 2 == 0:
                    x1 = x_spine + SPINE_W
                    x2 = x1 + GATE_LEN - 4
                else:
                    x1 = x_spine
                    x2 = x1 - GATE_LEN + 4

                canvas.create_line(x1, y_gate, x2, y_gate,
                                   fill=color, width=finger_w, capstyle=tk.ROUND)
                tag = gate.name + ("  [" + gate.id + "]" if gate.ocupado else "")
                canvas.create_line(x1, y_gate, x2, y_gate,
                                   fill="", width=10, tags=("gate_hit", tag))

            x_spine = x_spine + SPINE_W + GATE_LEN + AREA_SPACING

        x_cursor = x_cursor + t_width + 40

    max_gates_all = max(len(ba.gates) for t in bcn.Terminals for ba in t.BoardingAreas)
    gate_gap_all  = max(4, SPINE_HEIGHT_PX // max_gates_all)
    ly = y_top + PAD + 20 + max_gates_all * gate_gap_all + LABEL_H + PAD + 16
    lx = PAD

    canvas.create_line(lx, ly, lx + 22, ly,
                       fill=COL_OCCUPIED, width=5, capstyle=tk.ROUND)
    canvas.create_text(lx + 28, ly, text="occupied", anchor="w",
                       font=("Helvetica", 9), fill=COL_TEXT)
    canvas.create_line(lx + 120, ly, lx + 142, ly,
                       fill=COL_FREE, width=5, capstyle=tk.ROUND)
    canvas.create_text(lx + 148, ly, text="free", anchor="w",
                       font=("Helvetica", 9), fill=COL_TEXT)
    canvas.create_rectangle(lx + 210, ly - 7, lx + 224, ly + 7,
                             fill=COL_SCHENGEN, outline=COL_SCHENGEN)
    canvas.create_text(lx + 230, ly, text="Schengen", anchor="w",
                       font=("Helvetica", 9), fill=COL_TEXT)
    canvas.create_rectangle(lx + 330, ly - 7, lx + 344, ly + 7,
                             fill=COL_NONSCH, outline=COL_NONSCH)
    canvas.create_text(lx + 350, ly, text="non-Schengen", anchor="w",
                       font=("Helvetica", 9), fill=COL_TEXT)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


# ═══════════════════════════════════════════════════
#  Main window
# ═══════════════════════════════════════════════════

root = tk.Tk()
root.title("Airport Manager")
root.state("zoomed")
try:
    root.iconbitmap("icon.ico")
    root.wm_iconbitmap("icon.ico")
except Exception:
    pass
# Re-apply icon after zoom so Windows doesn't reset it
root.after(100, lambda: root.iconbitmap("icon.ico") if True else None)
root.configure(bg="white")

BTN = {"bg": "royalblue", "fg": "white", "relief": "flat",
       "padx": 6, "pady": 4, "width": 16, "font": ("Helvetica", 9),
       "activebackground": "navy", "activeforeground": "white"}

# ── Top title bar ────────────────────────────────────────────────────
title_bar = tk.Frame(root, bg="white")
title_bar.pack(fill="x")

title_lbl = tk.Label(title_bar, text="✈  Airport Manager", bg="white",
                     font=("Helvetica", 16, "bold"), fg="black")
title_lbl.pack(side="left", padx=20, pady=10)

# Clock label (right side of title bar)
clock_lbl = tk.Label(title_bar, text="", bg="white",
                     font=("Helvetica", 13, "bold"), fg="#3A7FC1")
clock_lbl.pack(side="right", padx=20, pady=10)

# Weather label (left of clock)
weather_lbl = tk.Label(title_bar, text="  BCN Weather: fetching...  ",
                       bg="white", font=("Helvetica", 9), fg="gray")
weather_lbl.pack(side="right", padx=(0, 10), pady=10)

sep1 = tk.Frame(root, bg="#CCCCCC", height=1)
sep1.pack(fill="x")

# ── Two-column body ──────────────────────────────────────────────────
body = tk.Frame(root, bg="white")
body.pack(fill="both", expand=True)

# LEFT column – scrollable
left_outer = tk.Frame(body, bg="white", width=370)
left_outer.pack(side="left", fill="y", padx=(10, 0), pady=8)
left_outer.pack_propagate(False)

left_canvas = tk.Canvas(left_outer, bg="white", highlightthickness=0)
left_scroll  = tk.Scrollbar(left_outer, orient="vertical", command=left_canvas.yview)
left_canvas.configure(yscrollcommand=left_scroll.set)
left_scroll.pack(side="right", fill="y")
left_canvas.pack(side="left", fill="both", expand=True)

left = tk.Frame(left_canvas, bg="white")
left_window = left_canvas.create_window((0, 0), window=left, anchor="nw")

def _on_left_configure(event):
    left_canvas.configure(scrollregion=left_canvas.bbox("all"))
    left_canvas.itemconfig(left_window, width=event.width)

left.bind("<Configure>", _on_left_configure)
left_canvas.bind("<Configure>",
    lambda e: left_canvas.itemconfig(left_window, width=e.width))

def _on_mousewheel(event):
    left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
left_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# RIGHT column
right = tk.Frame(body, bg="#F0F4F8")
right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

info_frame = tk.Frame(right, bg="#F0F4F8")
info_frame.pack(fill="both", expand=True)

tk.Label(info_frame,
         text="Select an action on the left\nto see results here.",
         bg="#F0F4F8", fg="#AAAAAA",
         font=("Helvetica", 13)).place(relx=0.5, rely=0.45, anchor="center")

# ── Announcements ticker bar ──────────────────────────────────────────
tk.Frame(root, bg="#CCCCCC", height=1).pack(fill="x")
ticker_bar = tk.Frame(root, bg="#F0F4F8")
ticker_bar.pack(fill="x")
ticker_lbl = tk.Label(ticker_bar, text="", bg="#F0F4F8", fg="#555555",
                      font=("Helvetica", 8), anchor="w", padx=8, width=60)
ticker_lbl.pack(side="right", pady=2, padx=(0, 10))

# ── Status bar (bottom) ──────────────────────────────────────────────
sep2 = tk.Frame(root, bg="#CCCCCC", height=1)
sep2.pack(fill="x")

status_label = tk.Label(root, bg="#F8F8F8", font=("Courier", 9), fg="gray",
                        anchor="w",
                        text="  ✈ Airports: 0  |  Schengen: 0  Non-Schengen: 0  |  Arrivals: 0  Departures: 0  Merged: 0")
status_label.pack(fill="x", pady=3)

# ── Clock tick ───────────────────────────────────────────────────────
_last_sound_minute = None

def _tick():
    import datetime
    global _last_sound_minute
    now        = datetime.datetime.now()
    clock_lbl.config(text=now.strftime("🕐  %H:%M:%S"))

    current_hhmm = now.strftime("%H:%M")
    if current_hhmm != _last_sound_minute:
        _last_sound_minute = current_hhmm
        _check_flight_events(current_hhmm)

    root.after(1000, _tick)

def _check_flight_events(hhmm):
    triggered = False
    for ac in merged if merged else aircrafts:
        if ac.timelanding == hhmm or ac.timedeparture == hhmm:
            triggered = True
            break
    if not triggered:
        for ac in departures:
            if ac.timedeparture == hhmm:
                triggered = True
                break
    if triggered:
        play_boarding_sound()

_tick()


# ═══════════════════════════════════════════════════
#  Weather overlay  (Open-Meteo, no API key needed)
# ═══════════════════════════════════════════════════

def _weather_code_to_text(code):
    table = {
        0: "☀ Clear", 1: "🌤 Mostly clear", 2: "⛅ Partly cloudy", 3: "☁ Overcast",
        45: "🌫 Foggy", 48: "🌫 Icy fog",
        51: "🌦 Light drizzle", 53: "🌦 Drizzle", 55: "🌧 Heavy drizzle",
        61: "🌧 Light rain", 63: "🌧 Rain", 65: "🌧 Heavy rain",
        71: "🌨 Light snow", 73: "🌨 Snow", 75: "❄ Heavy snow",
        80: "🌦 Light showers", 81: "🌧 Showers", 82: "⛈ Heavy showers",
        95: "⛈ Thunderstorm", 96: "⛈ Thunderstorm+hail", 99: "⛈ Thunderstorm+hail",
    }
    return table.get(code, "🌡 Unknown")

def fetch_weather():
    import threading
    def _fetch():
        try:
            import urllib.request, json
            url = ("https://api.open-meteo.com/v1/forecast"
                   "?latitude=41.2971&longitude=2.0785"
                   "&current=temperature_2m,wind_speed_10m,weathercode"
                   "&wind_speed_unit=kmh&timezone=Europe/Madrid")
            with urllib.request.urlopen(url, timeout=5) as r:
                data = json.loads(r.read())
            cur   = data["current"]
            temp  = cur["temperature_2m"]
            wind  = cur["wind_speed_10m"]
            desc  = _weather_code_to_text(cur["weathercode"])
            text  = f"  BCN Weather: {desc}  {temp}°C  💨 {wind} km/h  "
            weather_lbl.config(text=text, fg="#3A7FC1")
        except Exception:
            weather_lbl.config(text="  BCN Weather: unavailable  ", fg="gray")
    threading.Thread(target=_fetch, daemon=True).start()
    root.after(600_000, fetch_weather)


# ═══════════════════════════════════════════════════
#  Announcements ticker
# ═══════════════════════════════════════════════════

_announcement_queue = []
_ticker_pos         = 0
_ticker_text        = ""
_ticker_job         = None

GATE_PHRASES = [
    "now boarding at",
    "final call at",
    "gate change to",
    "delayed — new gate",
]
ARRIVAL_PHRASES = [
    "has landed. Welcome to Barcelona.",
    "arrived at gate",
    "on final approach to Barcelona El Prat.",
    "is taxiing to the terminal.",
]

def _build_announcements():
    import random
    msgs = []

    for ac in aircrafts:
        airline = ac.company
        origin  = ac.origin
        time    = ac.timelanding
        phrase  = random.choice(ARRIVAL_PHRASES)
        if "gate" in phrase and bcn is not None:
            occ = GateOccupancy(bcn)
            occupied_gates = [g for g, o, i in occ if o and i == ac.id]
            gate = occupied_gates[0] if occupied_gates else "TBA"
            msgs.append(f"✈  Flight {ac.id} ({airline}) from {origin} at {time} {phrase} {gate}.")
        else:
            msgs.append(f"✈  Flight {ac.id} ({airline}) from {origin} at {time} {phrase}")

    for ac in departures:
        airline = ac.company
        dest    = ac.destination
        time    = ac.timedeparture
        phrase  = random.choice(GATE_PHRASES)
        msgs.append(f"✈  {airline} flight {ac.id} to {dest} departing {time} — {phrase} TBA.  Please proceed.")

    if not msgs:
        msgs = [
            "✈  Welcome to Barcelona El Prat Airport — LEBL.",
            "✈  Please keep your boarding pass and ID ready at all times.",
            "✈  Unattended baggage will be removed by security.",
            "✈  Free Wi-Fi available throughout the terminal.",
            "✈  Load flights and departures to see live announcements.",
        ]

    random.shuffle(msgs)
    return ["          " + m + "                    " for m in msgs]

def _scroll_ticker():
    global _ticker_pos, _ticker_text, _ticker_job
    if not _ticker_text:
        return
    display = _ticker_text[_ticker_pos:] + "   " + _ticker_text[:_ticker_pos]
    ticker_lbl.config(text=display[:120])
    _ticker_pos = (_ticker_pos + 1) % len(_ticker_text)
    _ticker_job = root.after(200, _scroll_ticker)

def _start_ticker():
    global _ticker_text, _ticker_pos, _ticker_job
    msgs = _build_announcements()
    _ticker_text = "     ·     ".join(msgs)
    _ticker_pos  = 0
    if _ticker_job:
        root.after_cancel(_ticker_job)
    _scroll_ticker()

def refresh_ticker():
    _start_ticker()

fetch_weather()
_start_ticker()


# ════════════════════════════════════════════════════════════════════
#  LEFT PANEL CONTENTS
# ════════════════════════════════════════════════════════════════════

def section_label(parent, text):
    tk.Label(parent, text=text, bg="white",
             font=("Helvetica", 9, "bold"), fg="#555555").pack(anchor="w", pady=(10, 2))
    tk.Frame(parent, bg="#DDDDDD", height=1).pack(fill="x", pady=(0, 4))

def btn_row(parent, buttons):
    f = tk.Frame(parent, bg="white")
    f.pack(fill="x", pady=2)
    for label, cmd in buttons:
        tk.Button(f, text=label, command=cmd, **BTN).pack(side="left", padx=3)


# ── AIRPORTS ─────────────────────────────────────────────────────────
section_label(left, "AIRPORTS")

frame_inputs = tk.Frame(left, bg="white")
frame_inputs.pack(fill="x", pady=4)
tk.Label(frame_inputs, text="ICAO:", bg="white", font=("Helvetica", 9)).grid(row=0, column=0, padx=(0, 2))
entry_code = tk.Entry(frame_inputs, width=7, font=("Helvetica", 10), relief="solid", bd=1)
entry_code.grid(row=0, column=1, padx=(0, 6))
tk.Label(frame_inputs, text="Lat:", bg="white", font=("Helvetica", 9)).grid(row=0, column=2, padx=(0, 2))
entry_lat = tk.Entry(frame_inputs, width=7, font=("Helvetica", 10), relief="solid", bd=1)
entry_lat.grid(row=0, column=3, padx=(0, 6))
tk.Label(frame_inputs, text="Lon:", bg="white", font=("Helvetica", 9)).grid(row=0, column=4, padx=(0, 2))
entry_lon = tk.Entry(frame_inputs, width=7, font=("Helvetica", 10), relief="solid", bd=1)
entry_lon.grid(row=0, column=5)

btn_row(left, [("Load Airports",   load_airports),
               ("Add Airport",     add_airport)])
btn_row(left, [("Delete Airport",  delete_airport),
               ("Show List",       show_airports)])
btn_row(left, [("Save Schengen",   save_schengen),
               ("Update Schengen", update_schengen)])
btn_row(left, [("Plot Chart",      plot_airports),
               ("Export KML Map",  map_airports)])

tk.Label(left, text="Airports loaded:", bg="white",
         font=("Helvetica", 8, "bold"), fg="#444444").pack(anchor="w", pady=(6, 1))
frame_alist = tk.Frame(left, bg="white")
frame_alist.pack(fill="x")
a_scroll = tk.Scrollbar(frame_alist)
a_scroll.pack(side="right", fill="y")
airport_listbox = tk.Listbox(frame_alist, height=5, font=("Courier", 8),
                              bg="white", fg="black", selectbackground="royalblue",
                              relief="solid", bd=1, yscrollcommand=a_scroll.set)
airport_listbox.pack(side="left", fill="x", expand=True)
a_scroll.config(command=airport_listbox.yview)


# ── FLIGHTS (ARRIVALS) ────────────────────────────────────────────────
section_label(left, "FLIGHTS  (ARRIVALS)")

btn_row(left, [("Load Arrivals",   load_arrivals),
               ("Save Flights",    save_flights)])
btn_row(left, [("Plot by Hour",    plot_arrivals),
               ("Plot by Airline", plot_airlines)])
btn_row(left, [("Plot Schengen",   plot_flights_type),
               ("Flights KML Map", map_flights)])
btn_row(left, [("Long Distance",   long_distance)])

tk.Label(left, text="Arrivals loaded:", bg="white",
         font=("Helvetica", 8, "bold"), fg="#444444").pack(anchor="w", pady=(6, 1))
frame_flist = tk.Frame(left, bg="white")
frame_flist.pack(fill="x")
f_scroll = tk.Scrollbar(frame_flist)
f_scroll.pack(side="right", fill="y")
flights_listbox = tk.Listbox(frame_flist, height=5, font=("Courier", 8),
                              bg="white", fg="black", selectbackground="royalblue",
                              relief="solid", bd=1, yscrollcommand=f_scroll.set)
flights_listbox.pack(side="left", fill="x", expand=True)
f_scroll.config(command=flights_listbox.yview)


# ── GATE MANAGEMENT ──────────────────────────────────────────────────
section_label(left, "GATE MANAGEMENT")

btn_row(left, [("Load Structure",  load_airport_structure),
               ("Assign Gates",    assign_gates_to_flights)])
btn_row(left, [("Gate Diagram",    show_gate_diagram),
               ("Occupancy List",  show_gate_occupancy_list)])


# ── DEPARTURES  (V4) ─────────────────────────────────────────────────
section_label(left, "DEPARTURES  (V4)")

btn_row(left, [("Load Departures", load_departures),
               ("Merge Movements", merge_movements)])
btn_row(left, [("Night Aircraft",  show_night_aircraft),
               ("Night Gates",     assign_night_gates_v4)])
btn_row(left, [("Day Occupancy",   plot_day_occupancy)])

tk.Label(left, text="Departures loaded:", bg="white",
         font=("Helvetica", 8, "bold"), fg="#444444").pack(anchor="w", pady=(6, 1))
frame_dlist = tk.Frame(left, bg="white")
frame_dlist.pack(fill="x")
d_scroll = tk.Scrollbar(frame_dlist)
d_scroll.pack(side="right", fill="y")
departures_listbox = tk.Listbox(frame_dlist, height=5, font=("Courier", 8),
                                 bg="white", fg="black", selectbackground="royalblue",
                                 relief="solid", bd=1, yscrollcommand=d_scroll.set)
departures_listbox.pack(side="left", fill="x", expand=True)
d_scroll.config(command=departures_listbox.yview)

# Free gate by aircraft ID
tk.Label(left, text="Free gate – Aircraft ID:", bg="white",
         font=("Helvetica", 8, "bold"), fg="#444444").pack(anchor="w", pady=(8, 1))
frame_free = tk.Frame(left, bg="white")
frame_free.pack(fill="x", pady=2)
entry_free_gate = tk.Entry(frame_free, width=10, font=("Helvetica", 10),
                            relief="solid", bd=1)
entry_free_gate.pack(side="left", padx=(3, 4))
tk.Button(frame_free, text="Free Gate", command=free_gate_by_id, **BTN).pack(side="left", padx=3)

# Assign gates at a specific hour
tk.Label(left, text="Assign gates at hour (hh:mm):", bg="white",
         font=("Helvetica", 8, "bold"), fg="#444444").pack(anchor="w", pady=(8, 1))
frame_time = tk.Frame(left, bg="white")
frame_time.pack(fill="x", pady=2)
entry_time = tk.Entry(frame_time, width=7, font=("Helvetica", 10),
                      relief="solid", bd=1)
entry_time.pack(side="left", padx=(3, 4))
tk.Button(frame_time, text="Assign", command=assign_gates_at_time, **BTN).pack(side="left", padx=3)


# ── Boarding sound ────────────────────────────────────────────────────
def play_boarding_sound():
    import threading
    def _play():
        try:
            import winsound
            winsound.PlaySound("boarding_sound.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print("Sound error:", e)
    threading.Thread(target=_play, daemon=True).start()


# ── Developer credits screen ──────────────────────────────────────────
_credits_clicks    = 0
_credits_click_job = None

CREDITS_LINES = [
    "",
    "✈  AIRPORT MANAGER",
    "   Version 4.0  —  Final",
    "",
    "━" * 42,
    "",
    "   DEVELOPED BY",
    "",
    "      ★  Guiu  ★",
    "      ★  Tejdeep  ★",
    "      ★  Xavi  ★",
    "",
    "━" * 42,
    "",
    "   INFORMÀTICA 1",
    "   EETAC",
    "   Grau d'Enginyeria de Sistemes Aeroespacials",
    "   UPC",
    "",
    "━" * 42,
    "",
    "   Built with Python",
    "",
    "   Click anywhere to close",
    "",
]

def _on_footer_click(event):
    global _credits_clicks, _credits_click_job
    _credits_clicks += 1
    if _credits_click_job:
        root.after_cancel(_credits_click_job)
    if _credits_clicks >= 3:
        _credits_clicks = 0
        _show_credits()
    else:
        _credits_click_job = root.after(600, lambda: globals().update(_credits_clicks=0))

def _show_credits():
    win = tk.Toplevel(root)
    win.title("Credits")
    win.configure(bg="#0A0A1A")
    win.resizable(False, False)
    try:
        win.iconbitmap("icon.ico")
        win.wm_iconbitmap("icon.ico")
    except Exception:
        pass
    w, h = 420, 480
    x = (win.winfo_screenwidth()  - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

    canvas = tk.Canvas(win, bg="#0A0A1A", highlightthickness=0, width=w, height=h)
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", lambda e: win.destroy())

    text_ids = []
    y_start  = h + 20
    line_h   = 26
    for i, line in enumerate(CREDITS_LINES):
        color = "#3A7FC1" if line.startswith("✈") else \
                "#FFD700" if line.startswith("   ★") else \
                "#AAAACC" if line.startswith("━") else \
                "white"
        font  = ("Helvetica", 13, "bold") if line.startswith("✈") else \
                ("Helvetica", 11, "bold") if line.startswith("   ★") else \
                ("Helvetica", 9)
        tid = canvas.create_text(w // 2, y_start + i * line_h,
                                  text=line, fill=color, font=font)
        text_ids.append(tid)

    def _scroll():
        all_done = True
        for tid in text_ids:
            cx, cy = canvas.coords(tid)
            canvas.coords(tid, cx, cy - 1)
            if cy > -line_h:
                all_done = False
        if not all_done and win.winfo_exists():
            win.after(30, _scroll)
        elif win.winfo_exists():
            win.destroy()

    win.after(400, _scroll)

# ── Footer label ──────────────────────────────────────────────────────
footer_lbl = tk.Label(left, text="Project by: Guiu  ·  Tejdeep  ·  Xavi",
                      bg="white", fg="royalblue", font=("Helvetica", 8),
                      cursor="hand2")
footer_lbl.pack(pady=(16, 8))
footer_lbl.bind("<Button-1>", _on_footer_click)


root.mainloop()