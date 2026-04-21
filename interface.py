import tkinter as tk
from tkinter import filedialog, messagebox
from airports import *

airports = []

def refresh_list():
    listbox.delete(0, tk.END)
    for airport in airports:
        schengen = "Schengen" if airport.isSchengen else "Non-Schengen"
        listbox.insert(tk.END, "  " + airport.code + "   " + str(round(airport.latitude, 2)) + "   " + str(round(airport.longitude, 2)) + "   " + schengen)

def load_airports():
    global airports
    path = filedialog.askopenfilename()
    airports = LoadAirport(path)
    for airport in airports:
        SetSchengen(airport)
    refresh_list()
    messagebox.showinfo("Done", str(len(airports)) + " airports loaded.")

def add_airport():
    code = entry_code.get().strip().upper()
    if code == "":
        messagebox.showerror("Error", "Please enter an ICAO code.")
    else:
        try:
            lat = float(entry_lat.get())
            lon = float(entry_lon.get())
            new_airport = Airport(code, lat, lon)
            SetSchengen(new_airport)
            AddAirport(airports, new_airport)
            refresh_list()
            messagebox.showinfo("Done", "Airport " + code + " added.")
        except ValueError:
            messagebox.showerror("Error", "Airport " + code + " not valid.")


def delete_airport():
    code = entry_code.get().strip().upper()
    if code == "":
        messagebox.showerror("Error", "Please enter an ICAO code.")
    else:
        found = False
        for airport in airports:
            if airport.code == code:
                found = True
        if found == False:
            messagebox.showerror("Error", "Airport " + code + " not found.")
        else:
            RemoveAirport(airports, code)
            refresh_list()
            messagebox.showinfo("Done", "Airport " + code + " deleted.")

def save_schengen():
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    SaveSchengenAirports(airports, path)
    messagebox.showinfo("Done", "Schengen airports saved.")

def plot():
    PlotAirports(airports)

def map_airports():
    saved = MapAirports(airports)
    if saved:
        messagebox.showinfo("Done", "Map saved successfully.")

# ── Ventana ──────────────────────────────────────────────────
root = tk.Tk()
root.title("Airport Management")
root.geometry("520x580")
root.configure(bg="white")

tk.Label(root, text="✈ Airport Management", bg="white",
         font=("Helvetica", 16, "bold"), fg="black").pack(pady=10)

# ── Inputs ────────────────────────────────────────────
frame_inputs = tk.Frame(root, bg="white")
frame_inputs.pack(pady=5)

tk.Label(frame_inputs, text="ICAO Code:", bg="white", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
entry_code = tk.Entry(frame_inputs, width=8, font=("Helvetica", 10))
entry_code.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="Latitude:", bg="white", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)
entry_lat = tk.Entry(frame_inputs, width=10, font=("Helvetica", 10))
entry_lat.grid(row=0, column=3, padx=5)

tk.Label(frame_inputs, text="Longitude:", bg="white", font=("Helvetica", 10)).grid(row=0, column=4, padx=5)
entry_lon = tk.Entry(frame_inputs, width=10, font=("Helvetica", 10))
entry_lon.grid(row=0, column=5, padx=5)

# ── Botones ─────────────────────────────────────────────────
frame_buttons = tk.Frame(root, bg="white")
frame_buttons.pack(pady=10)

btn_style = {"bg": "blue", "fg": "white",
             "relief": "flat", "padx": 8, "pady": 5, "width": 16}

tk.Button(frame_buttons, text="Load Airports",       command=load_airports, **btn_style).grid(row=0, column=0, padx=4, pady=3)
tk.Button(frame_buttons, text="Add Airport",         command=add_airport,   **btn_style).grid(row=0, column=1, padx=4, pady=3)
tk.Button(frame_buttons, text="Delete Airport",      command=delete_airport,**btn_style).grid(row=0, column=2, padx=4, pady=3)
tk.Button(frame_buttons, text="Save Schengen",       command=save_schengen, **btn_style).grid(row=1, column=0, padx=4, pady=3)
tk.Button(frame_buttons, text="Plot Chart",          command=plot,          **btn_style).grid(row=1, column=1, padx=4, pady=3)
tk.Button(frame_buttons, text="Export Google Earth", command=map_airports,  **btn_style).grid(row=1, column=2, padx=4, pady=3)

# ── Lista Aeropuertos ────────────────────────────────────────────
tk.Label(root, text="Airports loaded:",
         font=("Helvetica", 10, "bold"), fg="black").pack(anchor="w", padx=20)

listbox = tk.Listbox(root, width=65, height=16, font=("Courier", 10),
                     bg="white", fg="black", selectbackground="blue")
listbox.pack(padx=20, pady=5)

root.mainloop()