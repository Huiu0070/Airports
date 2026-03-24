# interface.py
# Graphical interface for Airport Management - Version 1
# Built with tkinter

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from airports import *

# ─── Color palette ───────────────────────────────────────────
BG        = "#0f1923"   # dark navy background
PANEL     = "#1a2635"   # slightly lighter panel
ACCENT    = "#00c9a7"   # teal accent
ACCENT2   = "#e74c3c"   # red for non-Schengen
TEXT      = "#e8edf2"   # light text
SUBTEXT   = "#7f8c9a"   # muted text
BTN_BG    = "#1e3a4a"   # button background
BTN_HOV   = "#00c9a7"   # button hover
ENTRY_BG  = "#0d1e2c"   # entry background
ROW_A     = "#16232f"   # table row A
ROW_B     = "#1a2a38"   # table row B

airports = []  # global list of airports


# ─── Helper: styled button ───────────────────────────────────
def make_button(parent, text, command, color=BTN_BG, width=22):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=TEXT, font=("Courier New", 10, "bold"),
        relief="flat", bd=0, padx=10, pady=7,
        activebackground=ACCENT, activeforeground=BG,
        cursor="hand2", width=width
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT, fg=BG))
    btn.bind("<Leave>", lambda e: btn.config(bg=color, fg=TEXT))
    return btn


# ─── Refresh the airport table ───────────────────────────────
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for i in range(len(airports)):
        airport = airports[i]
        schengen_str = "✔ Yes" if airport.isSchengen else "✘ No"
        tag = "schengen" if airport.isSchengen else "nonschengen"
        tree.insert("", "end",
                    values=(airport.code,
                            f"{airport.latitude:.4f}",
                            f"{airport.longitude:.4f}",
                            schengen_str),
                    tags=(tag,))
    lbl_count.config(
        text=f"Total: {len(airports)}  |  "
             f"Schengen: {sum(1 for a in airports if a.isSchengen)}  |  "
             f"Non-Schengen: {sum(1 for a in airports if not a.isSchengen)}"
    )


# ─── Operations ──────────────────────────────────────────────
def load_airports():
    global airports
    path = filedialog.askopenfilename(
        title="Select airports file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if path:
        airports = LoadAirport(path)
        for airport in airports:
            SetSchengen(airport)
        refresh_table()
        messagebox.showinfo("Loaded", f"{len(airports)} airports loaded successfully.")


def add_airport():
    win = tk.Toplevel(root)
    win.title("Add Airport")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.geometry("320x220")

    tk.Label(win, text="Add New Airport", bg=BG, fg=ACCENT,
             font=("Courier New", 13, "bold")).pack(pady=(18, 10))

    frame = tk.Frame(win, bg=BG)
    frame.pack(padx=20)

    fields = [("ICAO Code", ""), ("Latitude", ""), ("Longitude", "")]
    entries = []
    for label, default in fields:
        row = tk.Frame(frame, bg=BG)
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, bg=BG, fg=SUBTEXT,
                 font=("Courier New", 9), width=12, anchor="w").pack(side="left")
        entry = tk.Entry(row, bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT,
                         font=("Courier New", 10), relief="flat", width=16)
        entry.pack(side="left", ipady=4)
        entries.append(entry)

    def confirm():
        code = entries[0].get().strip().upper()
        try:
            lat = float(entries[1].get().strip())
            lon = float(entries[2].get().strip())
        except ValueError:
            messagebox.showerror("Error", "Latitude and longitude must be numbers.")
            return
        if len(code) != 4:
            messagebox.showerror("Error", "ICAO code must be 4 characters.")
            return
        new_airport = Airport(code, lat, lon)
        SetSchengen(new_airport)
        AddAirport(airports, new_airport)
        refresh_table()
        win.destroy()

    make_button(win, "Add Airport", confirm, width=18).pack(pady=12)


def delete_airport():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an airport to delete.")
        return
    code = tree.item(selected[0])["values"][0]
    if messagebox.askyesno("Confirm", f"Delete airport {code}?"):
        RemoveAirport(airports, code)
        refresh_table()


def set_schengen_all():
    for airport in airports:
        SetSchengen(airport)
    refresh_table()
    messagebox.showinfo("Done", "Schengen attribute updated for all airports.")


def show_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an airport.")
        return
    code = tree.item(selected[0])["values"][0]
    for airport in airports:
        if airport.code == code:
            schengen_str = "Yes" if airport.isSchengen else "No"
            messagebox.showinfo(
                f"Airport {code}",
                f"ICAO Code:  {airport.code}\n"
                f"Latitude:   {airport.latitude:.6f}\n"
                f"Longitude:  {airport.longitude:.6f}\n"
                f"Schengen:   {schengen_str}"
            )
            return


def save_schengen():
    if not airports:
        messagebox.showwarning("Warning", "No airports loaded.")
        return
    path = filedialog.asksaveasfilename(
        title="Save Schengen airports",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if path:
        result = SaveSchengenAirports(airports, path)
        if result != -1:
            messagebox.showinfo("Saved", f"Schengen airports saved to:\n{path}")
        else:
            messagebox.showerror("Error", "Could not save file.")


def plot_airports():
    if not airports:
        messagebox.showwarning("Warning", "No airports loaded.")
        return
    PlotAirports(airports)


def map_airports():
    if not airports:
        messagebox.showwarning("Warning", "No airports loaded.")
        return
    path = filedialog.asksaveasfilename(
        title="Save KML file",
        defaultextension=".kml",
        filetypes=[("KML files", "*.kml")]
    )
    if path:
        # temporarily override default filename in MapAirports
        MapAirports_to_file(airports, path)
        messagebox.showinfo("Saved", f"KML file saved to:\n{path}\n\nOpen it with Google Earth.")


def MapAirports_to_file(airports, filename):
    F = open(filename, "w")
    F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    F.write('<Document>\n')
    F.write('<Style id="schengen">\n')
    F.write('  <IconStyle><color>ff00ff00</color></IconStyle>\n')
    F.write('</Style>\n')
    F.write('<Style id="no_schengen">\n')
    F.write('  <IconStyle><color>ff0000ff</color></IconStyle>\n')
    F.write('</Style>\n')
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
    F.write('</Document>\n')
    F.write('</kml>\n')
    F.close()


# ─── Main window ─────────────────────────────────────────────
root = tk.Tk()
root.title("✈  Airport Management")
root.configure(bg=BG)
root.geometry("900x620")
root.minsize(800, 550)

# ── Title bar ─────────────────────────────────────────────────
title_bar = tk.Frame(root, bg=PANEL, height=60)
title_bar.pack(fill="x")
title_bar.pack_propagate(False)

tk.Label(title_bar, text="✈  AIRPORT MANAGEMENT",
         bg=PANEL, fg=ACCENT,
         font=("Courier New", 17, "bold")).pack(side="left", padx=24, pady=10)
tk.Label(title_bar, text="Version 1  |  Informàtica 1",
         bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 9)).pack(side="right", padx=24)

# ── Main layout ───────────────────────────────────────────────
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=0, pady=0)

# Left panel (buttons)
left = tk.Frame(main, bg=PANEL, width=210)
left.pack(side="left", fill="y")
left.pack_propagate(False)

tk.Label(left, text="OPERATIONS", bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 8, "bold")).pack(pady=(20, 6), padx=16, anchor="w")

separator = tk.Frame(left, bg=ACCENT, height=2)
separator.pack(fill="x", padx=16, pady=(0, 14))

buttons = [
    ("📂  Load Airports",       load_airports),
    ("➕  Add Airport",          add_airport),
    ("🗑  Delete Airport",       delete_airport),
    ("🔍  Show Selected",        show_selected),
    ("🌍  Set Schengen (All)",   set_schengen_all),
    ("💾  Save Schengen File",   save_schengen),
    ("📊  Plot Bar Chart",       plot_airports),
    ("🗺  Export to Google Earth", map_airports),
]

for label, cmd in buttons:
    make_button(left, label, cmd, width=24).pack(pady=4, padx=14)

# Right panel (table)
right = tk.Frame(main, bg=BG)
right.pack(side="left", fill="both", expand=True, padx=16, pady=16)

tk.Label(right, text="AIRPORT LIST", bg=BG, fg=ACCENT,
         font=("Courier New", 11, "bold")).pack(anchor="w", pady=(0, 6))

# Table
cols = ("ICAO Code", "Latitude", "Longitude", "Schengen")
style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.Treeview",
                background=ROW_A, foreground=TEXT,
                fieldbackground=ROW_A, rowheight=26,
                font=("Courier New", 10))
style.configure("Custom.Treeview.Heading",
                background=PANEL, foreground=ACCENT,
                font=("Courier New", 10, "bold"), relief="flat")
style.map("Custom.Treeview",
          background=[("selected", ACCENT)],
          foreground=[("selected", BG)])

tree_frame = tk.Frame(right, bg=BG)
tree_frame.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                    style="Custom.Treeview",
                    yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

for col in cols:
    tree.heading(col, text=col)
tree.column("ICAO Code",  width=110, anchor="center")
tree.column("Latitude",   width=120, anchor="center")
tree.column("Longitude",  width=120, anchor="center")
tree.column("Schengen",   width=100, anchor="center")

tree.tag_configure("schengen",    background="#0d2e1f", foreground="#2ecc71")
tree.tag_configure("nonschengen", background="#2e0d0d", foreground="#e74c3c")

tree.pack(fill="both", expand=True)

# Status bar
status_bar = tk.Frame(root, bg=PANEL, height=30)
status_bar.pack(fill="x", side="bottom")
status_bar.pack_propagate(False)

lbl_count = tk.Label(status_bar,
                     text="Total: 0  |  Schengen: 0  |  Non-Schengen: 0",
                     bg=PANEL, fg=SUBTEXT, font=("Courier New", 9))
lbl_count.pack(side="left", padx=16, pady=5)

root.mainloop()