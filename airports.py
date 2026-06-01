from tkinter import filedialog

class Airport:
    def __init__(self, code, latitude, longitude):
        self.code = code
        self.latitude = latitude
        self.longitude = longitude
        self.isSchengen = False

# Checks if the airport is within the Schengen Area
def IsSchengenAirport(code):
    if not code or len(code)<2:
        return False
    schengen_prefixes=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH','BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES','LS']
    prefix=code[:2]
    if prefix in schengen_prefixes:
        return True
    else:
        return False

# Receives the Schengen status and updates the boolean to True or False
def SetSchengen(airport):
    result=IsSchengenAirport(airport.code)
    if result == True:
        airport.isSchengen=True
    else:
        airport.isSchengen=False

# Prints the airport details to the console
def PrintAirport(airport):
    print("Airport data:")
    print("ICAO code:", airport.code)
    print("Latitude:", airport.latitude)
    print("Longitude:", airport.longitude)
    print("Schengen:", airport.isSchengen)


def LoadAirports(filename):
    airports_list = []
    try:
        F = open(filename, "r")
        header = F.readline()  #Reads the first line to skip it

        line = F.readline()
        while line != '':
            items = line.split()

            #Chech that the line has 3 items (CODE, LAT, LON)
            if len(items) == 3:
                #Airport code
                code = items[0]
                letters = code.split()
                country = letters[0:1]

                #Convert latitude
                lat = items[1]
                #Extract the pieces
                lat_deg = float(lat[1:3])
                lat_min = float(lat[3:5])
                lat_seg = float(lat[5:7])

                lat_decimal = lat_deg + lat_min/60 + lat_seg/3600
                if lat[0] == "S":           #If it south, the latitude is negative
                    lat_decimal = -lat_decimal

                #Convert longitude
                lon = items[2]

                lon_deg = float(lon[1:4])
                lon_min = float(lon[4:6])
                lon_seg = float(lon[6:8])

                lon_decimal = lon_deg + lon_min/60 + lon_seg/3600
                if lon[0] == "W":       #If it's west, the longitude si negative
                    lon_decimal = -lon_decimal

                #Create airport
                airport = Airport(code, lat_decimal, lon_decimal)

                # Assign Schengen
                SetSchengen(airport)

                # Add to the list
                airports_list.append(airport)
                # -----------------------------------------------

            line = F.readline()

        F.close()


    except FileNotFoundError:

        print("Error: file not found.")

    return airports_list


#Saves Schengen in file
def SaveSchengenAirports(airports, output_file):
    try:
        F=open(output_file, "w")
        F.write('SCHENGEN AIRPORTS (CODE LATITUDE LONGITUDE):\n')

        for airport in airports:
            if airport.isSchengen:
                F.write(f"{airport.code} {airport.latitude} {airport.longitude}\n")

        F.close()

    except:
        print("Error saving file.")


#Airports graphic
def PlotAirports(airports):
    import matplotlib.pyplot as plt

    schengen_count = 0
    non_schengen_count = 0

    for airport in airports:
        if airport.isSchengen:
            schengen_count = schengen_count + 1
        else:
            non_schengen_count = non_schengen_count + 1

    plt.bar(0, schengen_count, color='blue', label='Schengen')
    plt.bar(0, non_schengen_count, bottom=schengen_count, color='red', label='No Schengen')

    plt.title("Schengen airports")
    plt.ylabel("Count")
    plt.xlabel("Airports")
    plt.xticks([])
    plt.legend()
    plt.show()

#Airports map
def MapAirports(airports):
    filepath = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("KML files", "*.kml"), ("All files", "*.*")],
        initialfile="Airp_map.kml",
        title="Desa el mapa d'aeroports"
    )

    #If the user closes the dialog without making a choice, filepath is ""
    if not filepath:
        return None

    F = open(filepath, 'w')

    #Write the KML format for Google Earth
    F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    F.write('<kml xmlns="http://www.opengis.net/kml/2.2"\n>')
    F.write('<Document>')

    #Schengen airport style (green)
    F.write('<Style id="schengen">\n')
    F.write('  <IconStyle>\n')
    F.write('    <color>ff00ff00</color>\n')
    F.write('  </IconStyle>\n')
    F.write('</Style>\n')

    #Non Schengen airport style (red)
    F.write('<Style id="no_schengen">\n')
    F.write('  <IconStyle>\n')
    F.write('    <color>ff0000ff</color>\n')
    F.write('  </IconStyle>\n')
    F.write('</Style>\n')

    #One placemark point each airport
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

    # Tanca arxiu KML
    F.write('</Document>\n')
    F.write('</kml>\n')

    F.close()
    return filepath

#Adds an airport to the list if the code isn't previously there
def AddAirport(airports_list, code, latitude, longitude):

    #Check if the airport already exists in the list to avoid duplicating it
    for ap in airports_list:
        if ap.code == code:
            print('The airport',code, 'already exists.')
            return -1  #If it already exists

    #Create the new airport instance
    new_airport = Airport(code, latitude, longitude)

    #Assign or not Schengen Area
    SetSchengen(new_airport)

    #Add it to the general list
    airports_list.append(new_airport)
    print('The airport',code,'has been added successfully.')
    return 0

#Removes an airport from the list based on its ICAO code
def RemoveAirport(airports, code):
    #Look for the airport with the matching ICAO code
    for airport in airports:
        if airport.code == code:
            #Remove the airport after finding it
            airports.remove(airport)
            print('Airport ', code, 'removed.')
            return
    print("Error: airport " , code , " not found.")