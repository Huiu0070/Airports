import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from aircraft import *

airports = []
aircrafts = []


#Funcions auxiliars UI

def update_status():
    n_airp = len(airports)
    n_sch  = sum(1 for a in airports if a.isSchengen)
    n_nsch = n_airp - n_sch
    n_fl   = len(aircrafts)
    airlines = len(set(getattr(ac, "airline", "") for ac in aircrafts)) if aircrafts else 0
    status_label.config(
        text=f"  ✈ Airports: {n_airp}  |  Schengen: {n_sch}  Non-Schengen: {n_nsch}"
             f"  |  Flights: {n_fl}"
    )


#Funcions Aeroports

def refresh_airport_list():
    airport_listbox.delete(0, tk.END)
    for airport in airports:
        schengen = "✓ Schengen" if airport.isSchengen else "✗ Non-Schengen"
        airport_listbox.insert(tk.END,
            f"  {airport.code:<8} {str(round(airport.latitude, 2)):<10} {str(round(airport.longitude, 2)):<12} {schengen}")
    update_status()

def load_airports():
    global airports
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if path:
        airports = LoadAirport(path)
        for airport in airports:
            SetSchengen(airport)
        refresh_airport_list()
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
    else:
        found = any(airport.code == code for airport in airports)
        if not found:
            messagebox.showerror("Error", "Airport " + code + " not found.")
        else:
            RemoveAirport(airports, code)
            refresh_airport_list()
            messagebox.showinfo("Done", "Airport " + code + " deleted.")

def save_schengen():
    path = filedialog.asksaveasfilename(defaultextension=".txt",
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
    for airport in airports:
        PrintAirport(airport)
    messagebox.showinfo("Done", "Airports printed to console.")

def plot_airports():
    if len(airports) == 0:
        messagebox.showerror("Error", "No airports loaded.")
        return
    PlotAirports(airports)

def map_airports():
    if len(airports) == 0:
        messagebox.showerror("Error", "No airports loaded.")
        return
    saved = MapAirports(airports)
    if saved:
        messagebox.showinfo("Done", "Map saved successfully.")


#Funcions Vols

def refresh_flights_list():
    flights_listbox.delete(0, tk.END)
    for ac in aircrafts:
        flights_listbox.insert(tk.END,
            f"  {ac.timelanding:<10} {ac.origin:<10} {ac.company}")
    update_status()

def load_arrivals():
    global aircrafts
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if path:
        aircrafts = LoadArrivals(path)
        refresh_flights_list()
        messagebox.showinfo("Done", str(len(aircrafts)) + " flights loaded.")

def save_flights():
    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if path:
        SaveFlights(aircrafts, path)
        messagebox.showinfo("Done", "Flights saved successfully.")

def plot_arrivals():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    PlotArrivals(aircrafts)

def plot_airlines():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    PlotAirlines(aircrafts)

def plot_flights_type():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    PlotFlightsType(aircrafts)

def map_flights():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    filepath = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("KML files", "*.kml"), ("All files", "*.*")],
        initialfile="Flights_map.kml",
        title="Save flights KML map"
    )
    if not filepath:
        return
    # Cridem MapFlights: si accepta filepath com a segon argument, ho passem
    import inspect
    try:
        sig = inspect.signature(MapFlights)
        if len(sig.parameters) >= 2:
            MapFlights(aircrafts, filepath)
        else:
            MapFlights(aircrafts)
    except Exception:
        MapFlights(aircrafts)
    messagebox.showinfo("Done", "KML flight map saved.")

def long_distance():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flights loaded.")
        return
    long = LongDistanceArrivals(aircrafts)
    messagebox.showinfo("Done", "Long distance flights: " + str(len(long)))
    MapFlights(long)


#Finestra principal

root = tk.Tk()
root.title("Airport Manager")
root.geometry("640x1000")
root.configure(bg="white")
root.resizable(False, True)

#Estil botons
BTN = {"bg": "blue", "fg": "white", "relief": "flat",
       "padx": 6, "pady": 5, "width": 17, "font": ("Helvetica", 9),
       "activebackground": "navy", "activeforeground": "white"}

#Títol
tk.Label(root, text="✈  Airport Manager", bg="white",
         font=("Helvetica", 18, "bold"), fg="black").pack(pady=(14, 4))

tk.Frame(root, bg="gray", height=1).pack(fill="x", padx=20)

#Secció AIRPORTS
tk.Label(root, text="AIRPORTS", bg="white",
         font=("Helvetica", 10, "bold"), fg="gray").pack(anchor="w", padx=22, pady=(10, 2))

# Inputs
frame_inputs = tk.Frame(root, bg="white")
frame_inputs.pack(fill="x", padx=20, pady=4)

tk.Label(frame_inputs, text="ICAO:", bg="white", font=("Helvetica", 9)).grid(row=0, column=0, padx=(0, 2))
entry_code = tk.Entry(frame_inputs, width=7, font=("Helvetica", 10), relief="solid", bd=1)
entry_code.grid(row=0, column=1, padx=(0, 10))

tk.Label(frame_inputs, text="Lat:", bg="white", font=("Helvetica", 9)).grid(row=0, column=2, padx=(0, 2))
entry_lat = tk.Entry(frame_inputs, width=9, font=("Helvetica", 10), relief="solid", bd=1)
entry_lat.grid(row=0, column=3, padx=(0, 10))

tk.Label(frame_inputs, text="Lon:", bg="white", font=("Helvetica", 9)).grid(row=0, column=4, padx=(0, 2))
entry_lon = tk.Entry(frame_inputs, width=9, font=("Helvetica", 10), relief="solid", bd=1)
entry_lon.grid(row=0, column=5)

# Botons aeroports — fila 1
frame_btn1 = tk.Frame(root, bg="white")
frame_btn1.pack(pady=3)
tk.Button(frame_btn1, text="Load Airports",   command=load_airports,   **BTN).grid(row=0, column=0, padx=4)
tk.Button(frame_btn1, text="Add Airport",     command=add_airport,     **BTN).grid(row=0, column=1, padx=4)
tk.Button(frame_btn1, text="Delete Airport",  command=delete_airport,  **BTN).grid(row=0, column=2, padx=4)

# Botons aeroports — fila 2
frame_btn2 = tk.Frame(root, bg="white")
frame_btn2.pack(pady=3)
tk.Button(frame_btn2, text="Show in Console", command=show_airports,   **BTN).grid(row=0, column=0, padx=4)
tk.Button(frame_btn2, text="Save Schengen",   command=save_schengen,   **BTN).grid(row=0, column=1, padx=4)
tk.Button(frame_btn2, text="Update Schengen", command=update_schengen, **BTN).grid(row=0, column=2, padx=4)

# Botons aeroports — fila 3
frame_btn3 = tk.Frame(root, bg="white")
frame_btn3.pack(pady=3)
tk.Button(frame_btn3, text="Plot Chart",      command=plot_airports,   **BTN).grid(row=0, column=0, padx=4)
tk.Button(frame_btn3, text="Export KML Map",  command=map_airports,    **BTN).grid(row=0, column=1, padx=4)

# Llista aeroports
tk.Label(root, text="Airports loaded:",
         font=("Helvetica", 9, "bold"), fg="black", bg="white").pack(anchor="w", padx=22, pady=(8, 2))

frame_alist = tk.Frame(root, bg="white", padx=20)
frame_alist.pack(fill="x")

a_scroll = tk.Scrollbar(frame_alist)
a_scroll.pack(side="right", fill="y")

airport_listbox = tk.Listbox(frame_alist, width=68, height=9, font=("Courier", 9),
                              bg="white", fg="black", selectbackground="blue",
                              relief="solid", bd=1, yscrollcommand=a_scroll.set)
airport_listbox.pack(side="left")
a_scroll.config(command=airport_listbox.yview)

#Separador
tk.Frame(root, bg="gray", height=1).pack(fill="x", padx=20, pady=(12, 0))

# Secció FLIGHTS
tk.Label(root, text="FLIGHTS", bg="white",
         font=("Helvetica", 10, "bold"), fg="gray").pack(anchor="w", padx=22, pady=(8, 4))

# Botons vols — fila 1
frame_f1 = tk.Frame(root, bg="white")
frame_f1.pack(pady=3)
tk.Button(frame_f1, text="Load Flights",      command=load_arrivals,    **BTN).grid(row=0, column=0, padx=4)
tk.Button(frame_f1, text="Save Flights",      command=save_flights,     **BTN).grid(row=0, column=1, padx=4)
tk.Button(frame_f1, text="Plot by Hour",      command=plot_arrivals,    **BTN).grid(row=0, column=2, padx=4)

# Botons vols — fila 2
frame_f2 = tk.Frame(root, bg="white")
frame_f2.pack(pady=3)
tk.Button(frame_f2, text="Plot by Airline",   command=plot_airlines,    **BTN).grid(row=0, column=0, padx=4)
tk.Button(frame_f2, text="Plot Schengen",     command=plot_flights_type,**BTN).grid(row=0, column=1, padx=4)
tk.Button(frame_f2, text="Flights KML Map",   command=map_flights,      **BTN).grid(row=0, column=2, padx=4)

# Botons vols — fila 3
frame_f3 = tk.Frame(root, bg="white")
frame_f3.pack(pady=3)
tk.Button(frame_f3, text="Long Distance",     command=long_distance,    **BTN).grid(row=0, column=0, padx=4)

# Llista vols
tk.Label(root, text="Flights loaded:",
         font=("Helvetica", 9, "bold"), fg="black", bg="white").pack(anchor="w", padx=22, pady=(8, 2))

frame_flist = tk.Frame(root, bg="white", padx=20)
frame_flist.pack(fill="x")

f_scroll = tk.Scrollbar(frame_flist)
f_scroll.pack(side="right", fill="y")

flights_listbox = tk.Listbox(frame_flist, width=68, height=9, font=("Courier", 9),
                              bg="white", fg="black", selectbackground="blue",
                              relief="solid", bd=1, yscrollcommand=f_scroll.set)
flights_listbox.pack(side="left")
f_scroll.config(command=flights_listbox.yview)

# Barra d'estat
tk.Frame(root, bg="gray", height=1).pack(fill="x", padx=20, pady=(12, 0))

status_label = tk.Label(root, bg="white", font=("Courier", 9), fg="gray", anchor="w",
                         text="  ✈ Airports: 0  |  Schengen: 0  Non-Schengen: 0  |  Flights: 0")
status_label.pack(fill="x", padx=0, pady=6)

#Credits
tk.Frame(root, bg="gray", height=1).pack(fill="x", padx=20, pady=(12, 0))

status_label = tk.Label(root, bg="white", fg="gray", anchor="w",
                         text="       Project by: Tejdeep, Xavi, Guiu")
status_label.pack(fill="x", padx=0, pady=6)

root.mainloop()