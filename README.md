Welcome to our Airports project, by Xavi, Tejdeep and Guiu

-----------------------------------------------------------

Video Demo V1: https://youtu.be/irLzpuAMCo4 \
Video Demo V2: https://youtu.be/O8eSWfXMhNE \
Video Demo V3: https://youtu.be/JGOBCdmfzOs 
Video Demo V4: https://youtu.be/SLlC3pC_XZc


🗂️ **Files in this project**

🛬 *airport.py* — the main file from version 1, has the Airport class and all the functions to load, save and manage airports

🛩️ *aircraft.py* — added in version 2, has the Aircraft class and everything to do with flights arriving to Barcelona

🏗️ *LEBL.py* — added in version 3, handles all the gate stuff: terminals, boarding areas and assigning planes to gates

🖥️ *interface.py* — the graphical interface where the user can do everything without touching the code

🧪 *test_airport.py* —  a file we used to test that our functions were working correctly


📦 **Versions**

*Version 1 — Airports*
Our first version, here we learned how to work with classes, files and basic graphics.

What it does:
- Load a list of airports from a file
- Add or remove airports
- Check if an airport is in the Schengen zone
- Show a bar chart with Schengen vs non-Schengen airports
- Export airport locations to Google Earth


*Version 2 — Flights*
We added flights and now the app can load the planes arriving to Barcelona and show different graphs.

What it does:
- Load arriving flights from a file
- Show how many planes land each hour
- Show flights grouped by airline
- Show Schengen vs non-Schengen flights
- Draw flight routes in Google Earth
- Find flights coming from more than 2000 km away


*Version 3 — Gates*
We added the gate structure of LEBL (terminals, boarding areas and gates) and the app can now assign a gate to each arriving flight.

What it does:
- Load the airport structure from a file
- Know which airline goes to which terminal
- Assign a gate to each flight automatically
- Show which gates are free and which are occupied


*Version 4 — Departures and full day*
The last version! Now planes can also depart, freeing up their gates for new arrivals. The app manages the whole day hour by hour.

What it does:
- Load departures and combine them with arrivals
- Handle planes that stayed overnight at the airport
- Assign and free gates dynamically throughout the day
- Show a plot of gate occupancy for the whole day

**And our extra features**:
- 🔐 *Password — previous step before acceding to the interface*
- 🕐 *Local and UTC Time — see real time*
- 💨 *Wind Intensity and Direction — see from where and how fast the wind is coming*
- 🛫 **Active Runways** — checks which runways are active at LEBL in real time
- 🗺️ **Assign SIDs** — assigns a real SID departure route to each outgoing flight and shows it on a map
- 🛬 **Assign STARs** — assigns a real STAR arrival route to each incoming flight and shows it on a map
- 🔍 **View Aircraft Departure / Arrival** — look up any plane by ID and see its full route on a map
- 🏗️ **View Airport Map** — shows a visual diagram of the full LEBL terminal and gate layout
- 🚜 **View Ground Taxiing** — shows the taxiing path a plane would follow on the ground at LEBL
- ✈️ **View Merged Flight** — shows the complete journey of a plane: arrival route, gate, and departure route all together
- 🎬 **Hidden credits screen** — triple click the footer to see a surprise 😄


 **How to run it**

1. Install Python and the `matplotlib` library
2. Put the data files (`airports.txt`, `arrivals.txt`, etc.) in the same folder as the code
3. Run the interface:

```
python interface.py
```

To run the tests:

```
python test_airport.py
python aircraft.py
```
