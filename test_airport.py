'''
import airports
airport = airports.Airport ("LEBL", 41.297445, 2.0832941)
airports.SetSchengen(airport)
airports.PrintAirport (airport)
'''

from airports import *

# Mira que tot funcioni bé
airport = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
print('Proba:')
PrintAirport (airport)

print()

# Carrega aeroports de Airports.txt
airports = LoadAirport("Airports.txt")
print(f"Aeroports carregats: {len(airports)}")

# Crea nou fitxer amb els aeroports schengen
SaveSchengenAirports(airports, "schengen_output.txt")
print("Arxiu 'schengen_output.txt' guardat.")

# Crea la grafica
PlotAirports(airports)
print('Gràfica creada')

# Crea fitxer per google earth
MapAirports(airports)
print("Arxiu 'airports.kml' creat.. Obre amb  Google Earth.")