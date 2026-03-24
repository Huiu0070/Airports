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
print('Prueba:')
PrintAirport (airport)

print()

# Carrega aeroports de Airports.txt
airports = LoadAirport("Airports.txt")
print(f"Aeropuertos cargados: {len(airports)}")

# Crea nou fitxer amb els aeroports schengen
SaveSchengenAirports(airports, "schengen_output.txt")
print("Archivo 'schengen_output.txt' guardado.")

# Crea la grafica
PlotAirports(airports)
print('Grafica creada')

# Crea fitxer per google earth
MapAirports(airports)
print("Archivo 'airports.kml' creado. Ábrelo con Google Earth.")