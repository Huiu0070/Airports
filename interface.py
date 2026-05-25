import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from aircraft import *
from airports import *
from LEBL import *

airports  = []
aircrafts = []
bcn       = None    # BarcelonaAP object, loaded in V3 section


# ═══════════════════════════════════════════════════
#  Info panel helpers  (right column)
# ═══════════════════════════════════════════════════

def clear_info_panel():
    """Remove everything currently shown in the right panel."""
    for widget in info_frame.winfo_children():
        widget.destroy()

def show_info_label(title, lines):
    """
    Show a scrollable text list in the info panel.
    title  – string shown as header
    lines  – list of strings, one per row
    """
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
    """
    Embed a matplotlib figure in the info panel instead of
    opening a separate window.
    """
    clear_info_panel()
    tk.Label(info_frame, text="Chart", bg="#F0F4F8",
             font=("Helvetica", 11, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 4))

    canvas_plot = FigureCanvasTkAgg(fig, master=info_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

def show_info_gate_diagram():
    """
    Draw the gate diagram directly inside the info panel (scrollable canvas).
    """
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
    n_airp   = len(airports)
    n_sch    = sum(1 for a in airports if a.isSchengen)
    n_nsch   = n_airp - n_sch
    n_fl     = len(aircrafts)
    gate_txt = ""
    if bcn is not None:
        occ   = GateOccupancy(bcn)
        total = len(occ)
        used  = sum(1 for _, ocupado, _ in occ if ocupado)
        gate_txt = f"  |  Gates: {used}/{total} occupied"
    status_label.config(
        text=f"  ✈ Airports: {n_airp}  |  Schengen: {n_sch}  "
             f"Non-Schengen: {n_nsch}  |  Flights: {n_fl}{gate_txt}"
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
    # Show the loaded list in the info panel
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
    # Build the figure and embed it in the info panel
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
#  Flights functions
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
    # Count arrivals per hour
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
    # Show summary in info panel
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
    # Show occupancy list in info panel after assigning
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

    # Legend
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
#  Main window – fullscreen two-column layout
# ═══════════════════════════════════════════════════

root = tk.Tk()
root.title("Airport Manager")
root.state("zoomed")
try:
    root.iconbitmap("icon.ico")
except Exception:
    pass   # icon not found – app still opens normally          # start maximised
root.configure(bg="white")

BTN = {"bg": "royalblue", "fg": "white", "relief": "flat",
       "padx": 6, "pady": 4, "width": 16, "font": ("Helvetica", 9),
       "activebackground": "navy", "activeforeground": "white"}

# ── Top title bar ────────────────────────────────────────────────────
title_bar = tk.Frame(root, bg="white")
title_bar.pack(fill="x")
tk.Label(title_bar, text="✈  Airport Manager", bg="white",
         font=("Helvetica", 16, "bold"), fg="black").pack(side="left", padx=20, pady=10)
tk.Frame(root, bg="#CCCCCC", height=1).pack(fill="x")

# ── Two-column body ──────────────────────────────────────────────────
body = tk.Frame(root, bg="white")
body.pack(fill="both", expand=True)

# LEFT column – controls
left = tk.Frame(body, bg="white", width=360)
left.pack(side="left", fill="y", padx=(10, 0), pady=8)
left.pack_propagate(False)          # keep fixed width

# RIGHT column – info / charts / diagram
right = tk.Frame(body, bg="#F0F4F8")
right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

info_frame = tk.Frame(right, bg="#F0F4F8")
info_frame.pack(fill="both", expand=True)

# Placeholder text shown before anything is displayed
tk.Label(info_frame,
         text="Select an action on the left\nto see results here.",
         bg="#F0F4F8", fg="#AAAAAA",
         font=("Helvetica", 13)).place(relx=0.5, rely=0.45, anchor="center")

# ── Status bar (bottom) ──────────────────────────────────────────────
tk.Frame(root, bg="#CCCCCC", height=1).pack(fill="x")
status_label = tk.Label(root, bg="#F8F8F8", font=("Courier", 9), fg="gray",
                         anchor="w",
                         text="  ✈ Airports: 0  |  Schengen: 0  Non-Schengen: 0  |  Flights: 0")
status_label.pack(fill="x", pady=3)

# ────────────────────────────────────────────────────────────────────
#  LEFT PANEL CONTENTS
# ────────────────────────────────────────────────────────────────────

def section_label(parent, text):
    tk.Label(parent, text=text, bg="white",
             font=("Helvetica", 9, "bold"), fg="#555555").pack(anchor="w", pady=(10, 2))
    tk.Frame(parent, bg="#DDDDDD", height=1).pack(fill="x", pady=(0, 4))

def btn_row(parent, buttons):
    """buttons = list of (label, command)  — max 2 per row"""
    f = tk.Frame(parent, bg="white")
    f.pack(fill="x", pady=2)
    for label, cmd in buttons:
        tk.Button(f, text=label, command=cmd, **BTN).pack(side="left", padx=3)

# ── ICAO / lat / lon inputs ──────────────────────────────────────────
section_label(left, "AIRPORTS")

frame_inputs = tk.Frame(left, bg="white")
frame_inputs.pack(fill="x", pady=4)
tk.Label(frame_inputs, text="ICAO:", bg="white", font=("Helvetica", 9)).grid(row=0, column=0, padx=(0,2))
entry_code = tk.Entry(frame_inputs, width=7, font=("Helvetica", 10), relief="solid", bd=1)
entry_code.grid(row=0, column=1, padx=(0,8))
tk.Label(frame_inputs, text="Lat:", bg="white", font=("Helvetica", 9)).grid(row=0, column=2, padx=(0,2))
entry_lat = tk.Entry(frame_inputs, width=8, font=("Helvetica", 10), relief="solid", bd=1)
entry_lat.grid(row=0, column=3, padx=(0,8))
tk.Label(frame_inputs, text="Lon:", bg="white", font=("Helvetica", 9)).grid(row=0, column=4, padx=(0,2))
entry_lon = tk.Entry(frame_inputs, width=8, font=("Helvetica", 10), relief="solid", bd=1)
entry_lon.grid(row=0, column=5)

btn_row(left, [("Load Airports",   load_airports),
               ("Add Airport",     add_airport)])
btn_row(left, [("Delete Airport",  delete_airport),
               ("Show List",       show_airports)])
btn_row(left, [("Save Schengen",   save_schengen),
               ("Update Schengen", update_schengen)])
btn_row(left, [("Plot Chart",      plot_airports),
               ("Export KML Map",  map_airports)])

# Airports mini-list (compact, just for reference)
tk.Label(left, text="Airports loaded:", bg="white",
         font=("Helvetica", 8, "bold"), fg="#444444").pack(anchor="w", pady=(6,1))
frame_alist = tk.Frame(left, bg="white")
frame_alist.pack(fill="x")
a_scroll = tk.Scrollbar(frame_alist)
a_scroll.pack(side="right", fill="y")
airport_listbox = tk.Listbox(frame_alist, height=6, font=("Courier", 8),
                              bg="white", fg="black", selectbackground="royalblue",
                              relief="solid", bd=1, yscrollcommand=a_scroll.set)
airport_listbox.pack(side="left", fill="x", expand=True)
a_scroll.config(command=airport_listbox.yview)

# ── FLIGHTS ──────────────────────────────────────────────────────────
section_label(left, "FLIGHTS")

btn_row(left, [("Load Flights",    load_arrivals),
               ("Save Flights",    save_flights)])
btn_row(left, [("Plot by Hour",    plot_arrivals),
               ("Plot by Airline", plot_airlines)])
btn_row(left, [("Plot Schengen",   plot_flights_type),
               ("Flights KML Map", map_flights)])
btn_row(left, [("Long Distance",   long_distance)])

tk.Label(left, text="Flights loaded:", bg="white",
         font=("Helvetica", 8, "bold"), fg="#444444").pack(anchor="w", pady=(6,1))
frame_flist = tk.Frame(left, bg="white")
frame_flist.pack(fill="x")
f_scroll = tk.Scrollbar(frame_flist)
f_scroll.pack(side="right", fill="y")
flights_listbox = tk.Listbox(frame_flist, height=6, font=("Courier", 8),
                              bg="white", fg="black", selectbackground="royalblue",
                              relief="solid", bd=1, yscrollcommand=f_scroll.set)
flights_listbox.pack(side="left", fill="x", expand=True)
f_scroll.config(command=flights_listbox.yview)

# ── GATE MANAGEMENT ─────────────────────────────────────────────
section_label(left, "GATE MANAGEMENT")

btn_row(left, [("Load Structure",  load_airport_structure),
               ("Assign Gates",    assign_gates_to_flights)])
btn_row(left, [("Gate Diagram",    show_gate_diagram),
               ("Occupancy List",  show_gate_occupancy_list)])

# ── Footer ───────────────────────────────────────────────────────────
tk.Label(left, text="Project by: Guiu  ·  Tejdeep  ·  Xavi",
         bg="white", fg="royalblue", font=("Helvetica", 8)).pack(side="bottom", pady=8)

root.mainloop()