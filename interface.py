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
sids_assigned = False
stars_assigned = False

# --- DATOS DE SIDs ---
SIDS_DATA = {
    "24L": {
        "AGENA7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("BL805", 40.995, 2.048),
            ("BL811", 40.861, 2.300),
            ("BL827", 41.130, 2.762),
            ("AGENA", 41.545, 3.489)
        ],
        "DALIN6Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("BL805", 40.995, 2.048),
            ("BL812", 40.936, 2.277),
            ("DALIN", 41.734, 3.358)
        ],
        "DIPES3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("BL805", 40.995, 2.048),
            ("BL811", 40.861, 2.300),
            ("BL813", 41.109, 3.008),
            ("DIPES", 41.063, 3.540)
        ],
        "DUNES7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL809", 40.934, 1.952),
            ("BL810", 40.770, 2.233),
            ("DUNES", 40.864, 3.158)
        ],
        "DUQQI3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706)
        ],
        "GRAUS7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("LRD", 41.553, 0.648),
            ("GRAUS", 41.979, 0.376)
        ],
        "LARPA7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL809", 40.934, 1.952),
            ("BL810", 40.770, 2.233),
            ("LARPA", 40.627, 2.349)
        ],
        "LOBAR8Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("LRD", 41.553, 0.648),
            ("LOBAR", 41.748, 0.318)
        ],
        "LOTOS7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL804", 41.053, 1.893),
            ("BL807", 40.955, 1.564),
            ("BL808", 40.847, 1.109),
            ("LOTOS", 40.550, 1.003)
        ],
        "MAMUK3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("BL815", 41.376, 1.680),
            ("MAMUK", 41.837, 2.072)
        ],
        "MOPAS6Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("MOPAS", 42.435, 1.034)
        ],
        "NATPI4Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VIBOK", 41.547, 1.502),
            ("NATPI", 42.724, 1.236)
        ],
        "OLOXO3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("BL815", 41.376, 1.680),
            ("BL816", 41.524, 1.657),
            ("OLOXO", 42.435, 1.513)
        ],
        "REBUL3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VLA", 41.343, 1.547),
            ("BL814", 41.511, 1.354),
            ("REBUL", 41.698, 1.113)
        ],
        "SENIA7Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("BL800", 41.176, 2.057),
            ("NITBA", 41.072, 1.986),
            ("BL804", 41.053, 1.893),
            ("BL806", 41.055, 1.524),
            ("BL836", 40.968, 1.152),
            ("SENIA", 40.869, 0.739)
        ],
        "VIBOK3Q": [
            ("LEBL 24L", 41.303, 2.098),
            ("PERAL", 41.188, 2.039),
            ("BL801", 41.134, 1.946),
            ("BL802", 41.112, 1.851),
            ("BL803", 41.140, 1.759),
            ("DUQQI", 41.211, 1.706),
            ("VIBOK", 41.547, 1.502)
        ]
    },
    "06R": {
        "AGENA4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL701", 41.248, 2.565),
            ("BL702", 41.311, 2.684),
            ("BL703", 41.411, 2.732),
            ("BL704", 41.511, 2.780),
            ("BL705", 41.504, 2.960),
            ("SALON", 41.494, 3.187),
            ("AGENA", 41.545, 3.489)
        ],
        "CLE1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL716", 41.523, 2.463),
            ("CLE", 41.640, 2.634)
        ],
        "DALIN4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL701", 41.248, 2.565),
            ("BL702", 41.311, 2.684),
            ("BL703", 41.411, 2.732),
            ("BL704", 41.511, 2.780),
            ("FEVIK", 41.679, 3.196),
            ("DALIN", 41.734, 3.358)
        ],
        "DIPES1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL701", 41.248, 2.565),
            ("BL702", 41.311, 2.684),
            ("BL703", 41.411, 2.732),
            ("BL704", 41.511, 2.780),
            ("BL705", 41.504, 2.960),
            ("BL706", 41.351, 3.163),
            ("DIPES", 41.063, 3.540)
        ],
        "DUNES4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("DUNES", 40.864, 3.158)
        ],
        "DUQQI1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL722", 41.292, 1.845),
            ("DUQQI", 41.211, 1.706)
        ],
        "GRAUS3R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("BL712", 41.769, 1.693),
            ("GRAUS", 41.979, 0.376)
        ],
        "LARPA4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("TASOS", 40.946, 2.650),
            ("LARPA", 40.627, 2.349)
        ],
        "LOBAR4R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL714", 41.687, 1.792),
            ("LOBAR", 41.748, 0.318)
        ],
        "LOTOS3R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("TASOS", 40.946, 2.650),
            ("BL721", 40.836, 2.180),
            ("LOTOS", 40.550, 1.003)
        ],
        "MAMUK1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("MAMUK", 41.837, 2.072)
        ],
        "MOPAS3R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("BL712", 41.769, 1.693),
            ("MOPAS", 42.435, 1.034)
        ],
        "NATPI2R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("BL712", 41.769, 1.693),
            ("NATPI", 42.724, 1.236)
        ],
        "OLOXO1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL709", 41.706, 2.395),
            ("BL710", 41.733, 2.096),
            ("BL711", 41.759, 1.805),
            ("OLOXO", 42.435, 1.513)
        ],
        "REBUL1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL715", 41.606, 1.728),
            ("REBUL", 41.698, 1.113)
        ],
        "SENIA5R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL720", 41.143, 2.671),
            ("TASOS", 40.946, 2.650),
            ("BL721", 40.836, 2.180),
            ("SENIA", 40.869, 0.739)
        ],
        "VIBOK1R": [
            ("LEBL 06R", 41.281, 2.074),
            ("BL700", 41.276, 2.308),
            ("BL707", 41.429, 2.328),
            ("BL708", 41.657, 2.383),
            ("BL713", 41.677, 2.006),
            ("BL715", 41.606, 1.728),
            ("VIBOK", 41.547, 1.502)
        ]
    }
}

# --- ASIGNACIÓN AUTOMÁTICA DE SIDs POR DESTINO ---
DESTINATION_SIDS = {
    "24L": {
        "BIKF": "NATPI4Q", "CYUL": "GRAUS7Q", "CYYZ": "GRAUS7Q", "DAAG": "LARPA7Q", "EBAW": "NATPI4Q",
        "EBBR": "OLOXO3Q", "EBOS": "NATPI4Q", "EDDB": "DALIN6Q", "EDDF": "DALIN6Q", "EDDH": "DALIN6Q",
        "EDDK": "DALIN6Q", "EDDL": "OLOXO3Q", "EDDM": "AGENA7Q", "EDDN": "DALIN6Q", "EDDP": "DALIN6Q",
        "EDDS": "DALIN6Q", "EDDT": "AGENA7Q", "EDDV": "DALIN6Q", "EETN": "DALIN6Q", "EFHK": "OLOXO3Q",
        "EGAA": "NATPI4Q", "EGBB": "NATPI4Q", "EGCC": "NATPI4Q", "EGFF": "NATPI4Q", "EGGD": "NATPI4Q",
        "EGGW": "NATPI4Q", "EGHI": "NATPI4Q", "EGKK": "NATPI4Q", "EGLL": "NATPI4Q", "EGMC": "NATPI4Q",
        "EGNM": "NATPI4Q", "EGNT": "NATPI4Q", "EGNX": "NATPI4Q", "EGPH": "NATPI4Q", "EGPK": "NATPI4Q",
        "EGSS": "NATPI4Q", "EHAM": "DALIN6Q", "EHEH": "DALIN6Q", "EHRD": "OLOXO3Q", "EIDW": "NATPI4Q",
        "EKBI": "OLOXO3Q", "EKCH": "OLOXO3Q", "ELLX": "OLOXO3Q", "ENBR": "OLOXO3Q", "ENGM": "OLOXO3Q",
        "EPKK": "AGENA7Q", "EPKT": "AGENA7Q", "EPWA": "AGENA7Q", "ESGG": "DALIN6Q", "ESKN": "DALIN6Q",
        "ESSA": "DALIN6Q", "ETNL": "OLOXO3Q", "EVRA": "AGENA7Q", "EYVI": "AGENA7Q", "GCFV": "LOTOS7Q",
        "GCLP": "LOTOS7Q", "GCRR": "LOTOS7Q", "GCXO": "LOTOS7Q", "GMFF": "LARPA7Q", "GMMN": "LOTOS7Q",
        "GMMX": "LOTOS7Q", "GMTT": "LOTOS7Q", "HECA": "DIPES3Q", "KATL": "GRAUS7Q", "KCLT": "NATPI4Q",
        "KEWR": "LOBAR8Q", "KJFK": "LOBAR8Q", "KMIA": "GRAUS7Q", "KPHL": "GRAUS7Q", "KUGN": "GRAUS7Q",
        "LBSF": "DIPES3Q", "LCLK": "DIPES3Q", "LDDU": "DIPES3Q", "LDSP": "DIPES3Q", "LDZA": "AGENA7Q",
        "LEAL": "LOTOS7Q", "LEAM": "LOTOS7Q", "LEAS": "GRAUS7Q", "LEBB": "GRAUS7Q", "LEBZ": "SENIA7Q",
        "LECO": "LOBAR8Q", "LEGE": "DALIN6Q", "LEGR": "LOTOS7Q", "LEIB": "LARPA7Q", "LEJR": "LOTOS7Q",
        "LELN": "LOBAR8Q", "LEMD": "SENIA7Q", "LEMG": "LOTOS7Q", "LEMH": "DUNES7Q", "LEPA": "LARPA7Q",
        "LESO": "GRAUS7Q", "LEST": "LOBAR8Q", "LEVC": "LOTOS7Q", "LEVD": "LOBAR8Q", "LEVX": "LOBAR8Q",
        "LEZL": "LOTOS7Q", "LFBD": "NATPI4Q", "LFLL": "DALIN6Q", "LFMD": "DALIN6Q", "LFML": "DALIN6Q",
        "LFMN": "DALIN6Q", "LFOB": "OLOXO3Q", "LFPG": "OLOXO3Q", "LFPO": "OLOXO3Q", "LFQQ": "OLOXO3Q",
        "LFRN": "NATPI4Q", "LFRS": "NATPI4Q", "LFSB": "DALIN6Q", "LGAV": "DIPES3Q", "LGIR": "DIPES3Q",
        "LGKR": "DIPES3Q", "LGMK": "DIPES3Q", "LHBP": "AGENA7Q", "LIBD": "DIPES3Q", "LICJ": "DIPES3Q",
        "LIEE": "DIPES3Q", "LIEO": "DIPES3Q", "LIMC": "AGENA7Q", "LIME": "AGENA7Q", "LIMF": "AGENA7Q",
        "LIML": "AGENA7Q", "LIPE": "AGENA7Q", "LIPH": "AGENA7Q", "LIPX": "AGENA7Q", "LIRF": "DIPES3Q",
        "LIRN": "DIPES3Q", "LIRP": "AGENA7Q", "LIRQ": "DIPES3Q", "LKPR": "AGENA7Q", "LLBG": "DIPES3Q",
        "LMML": "DIPES3Q", "LOWW": "AGENA7Q", "LPPR": "SENIA7Q", "LPPT": "SENIA7Q", "LRCL": "DALIN6Q",
        "LROP": "AGENA7Q", "LSGG": "DALIN6Q", "LSZH": "DALIN6Q", "LTBA": "DIPES3Q", "LTFJ": "DIPES3Q",
        "LWSK": "DIPES3Q", "LYTV": "DIPES3Q", "OLBA": "DIPES3Q", "OMAA": "LARPA7Q", "OMDB": "DIPES3Q",
        "OTHH": "DIPES3Q", "SAEZ": "GRAUS7Q", "SBGR": "LOTOS7Q", "SKBO": "SENIA7Q", "UKBB": "AGENA7Q",
        "UKKK": "DALIN6Q", "ULLI": "DALIN6Q", "UUDD": "DALIN6Q", "UUEE": "DALIN6Q", "WSSS": "DIPES3Q"
    },
    "06R": {
        "BIKF": "NATPI2R", "CYUL": "GRAUS3R", "CYYZ": "GRAUS3R", "DAAG": "LARPA4R", "EBAW": "NATPI2R",
        "EBBR": "OLOXO1R", "EBOS": "NATPI2R", "EDDB": "DALIN4R", "EDDF": "DALIN4R", "EDDH": "DALIN4R",
        "EDDK": "DALIN4R", "EDDL": "OLOXO1R", "EDDM": "AGENA4R", "EDDN": "DALIN4R", "EDDP": "DALIN4R",
        "EDDS": "DALIN4R", "EDDT": "AGENA4R", "EDDV": "DALIN4R", "EETN": "DALIN4R", "EFHK": "OLOXO1R",
        "EGAA": "NATPI2R", "EGBB": "NATPI2R", "EGCC": "NATPI2R", "EGFF": "NATPI2R", "EGGD": "NATPI2R",
        "EGGW": "NATPI2R", "EGHI": "NATPI2R", "EGKK": "NATPI2R", "EGLL": "NATPI2R", "EGMC": "NATPI2R",
        "EGNM": "NATPI2R", "EGNT": "NATPI2R", "EGNX": "NATPI2R", "EGPH": "NATPI2R", "EGPK": "NATPI2R",
        "EGSS": "NATPI2R", "EHAM": "DALIN4R", "EHEH": "DALIN4R", "EHRD": "OLOXO1R", "EIDW": "NATPI2R",
        "EKBI": "OLOXO1R", "EKCH": "OLOXO1R", "ELLX": "OLOXO1R", "ENBR": "OLOXO1R", "ENGM": "OLOXO1R",
        "EPKK": "AGENA4R", "EPKT": "AGENA4R", "EPWA": "AGENA4R", "ESGG": "DALIN4R", "ESKN": "DALIN4R",
        "ESSA": "DALIN4R", "ETNL": "OLOXO1R", "EVRA": "AGENA4R", "EYVI": "AGENA4R", "GCFV": "LOTOS3R",
        "GCLP": "LOTOS3R", "GCRR": "LOTOS3R", "GCXO": "LOTOS3R", "GMFF": "LARPA4R", "GMMN": "LOTOS3R",
        "GMMX": "LOTOS3R", "GMTT": "LOTOS3R", "HECA": "DIPES1R", "KATL": "GRAUS3R", "KCLT": "NATPI2R",
        "KEWR": "LOBAR4R", "KJFK": "LOBAR4R", "KMIA": "GRAUS3R", "KPHL": "GRAUS3R", "KUGN": "GRAUS3R",
        "LBSF": "DIPES1R", "LCLK": "DIPES1R", "LDDU": "DIPES1R", "LDSP": "DIPES1R", "LDZA": "AGENA4R",
        "LEAL": "LOTOS3R", "LEAM": "LOTOS3R", "LEAS": "GRAUS3R", "LEBB": "GRAUS3R", "LEBZ": "SENIA5R",
        "LECO": "LOBAR4R", "LEGE": "DALIN4R", "LEGR": "LOTOS3R", "LEIB": "LARPA4R", "LEJR": "LOTOS3R",
        "LELN": "LOBAR4R", "LEMD": "SENIA5R", "LEMG": "LOTOS3R", "LEMH": "DUNES4R", "LEPA": "LARPA4R",
        "LESO": "GRAUS3R", "LEST": "LOBAR4R", "LEVC": "LOTOS3R", "LEVD": "LOBAR4R", "LEVX": "LOBAR4R",
        "LEZL": "LOTOS3R", "LFBD": "NATPI2R", "LFLL": "DALIN4R", "LFMD": "DALIN4R", "LFML": "DALIN4R",
        "LFMN": "DALIN4R", "LFOB": "OLOXO1R", "LFPG": "OLOXO1R", "LFPO": "OLOXO1R", "LFQQ": "OLOXO1R",
        "LFRN": "NATPI2R", "LFRS": "NATPI2R", "LFSB": "DALIN4R", "LGAV": "DIPES1R", "LGIR": "DIPES1R",
        "LGKR": "DIPES1R", "LGMK": "DIPES1R", "LHBP": "AGENA4R", "LIBD": "DIPES1R", "LICJ": "DIPES1R",
        "LIEE": "DIPES1R", "LIEO": "DIPES1R", "LIMC": "AGENA4R", "LIME": "AGENA4R", "LIMF": "AGENA4R",
        "LIML": "AGENA4R", "LIPE": "AGENA4R", "LIPH": "AGENA4R", "LIPX": "AGENA4R", "LIRF": "DIPES1R",
        "LIRN": "DIPES1R", "LIRP": "AGENA4R", "LIRQ": "DIPES1R", "LKPR": "AGENA4R", "LLBG": "DIPES1R",
        "LMML": "DIPES1R", "LOWW": "AGENA4R", "LPPR": "SENIA5R", "LPPT": "SENIA5R", "LRCL": "DALIN4R",
        "LROP": "AGENA4R", "LSGG": "DALIN4R", "LSZH": "DALIN4R", "LTBA": "DIPES1R", "LTFJ": "DIPES1R",
        "LWSK": "DIPES1R", "LYTV": "DIPES1R", "OLBA": "DIPES1R", "OMAA": "LARPA4R", "OMDB": "DIPES1R",
        "OTHH": "DIPES1R", "SAEZ": "GRAUS3R", "SBGR": "LOTOS3R", "SKBO": "SENIA5R", "UKBB": "AGENA4R",
        "UKKK": "DALIN4R", "ULLI": "DALIN4R", "UUDD": "DALIN4R", "UUEE": "DALIN4R", "WSSS": "DIPES1R"
    }
}

# =========================================================
# --- DATOS DE STARs (LLEGADAS CON PUNTOS INTERMEDIOS) ---
# =========================================================
STARS_DATA = {
    "02": {
        "ALBER3N": [
            ("ALBER", 42.451, 2.832), ("CUTXE", 42.132, 2.754),
            ("UTHAN", 41.885, 2.379), ("ENJUC", 41.769, 2.204),
            ("SLL", 41.520, 2.110), ("BCN", 41.307, 2.108),
            ("BL645", 41.170, 2.185), ("VIBIM", 41.071, 2.206), ("LEBL 02", 41.282, 2.088)
        ],
        "BISBA5N": [
            ("BISBA", 42.086, 3.626), ("NEMUM", 42.009, 3.393),
            ("BGR", 41.948, 3.209), ("ENJUC", 41.769, 2.204),
            ("SLL", 41.520, 2.110), ("BCN", 41.307, 2.108),
            ("BL645", 41.170, 2.185), ("VIBIM", 41.071, 2.206), ("LEBL 02", 41.282, 2.088)
        ],
        "CASPE4N": [
            ("CASPE", 41.268, 0.199), ("BL678", 41.320, 1.106),
            ("BL670", 41.332, 1.327), ("VLA", 41.343, 1.548),
            ("ULKAL", 41.136, 1.588), ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "GRAUS3N": [
            ("GRAUS", 41.979, 0.376), ("LRD", 41.553, 0.648),
            ("VLA", 41.343, 1.548), ("ULKAL", 41.136, 1.588),
            ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "MARTA4N": [
            ("MARTA", 40.355, 1.280), ("PAPOS", 40.621, 1.449),
            ("TAQOH", 40.872, 1.631), ("ULKAL", 41.136, 1.588),
            ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "NEPAL4N": [
            ("NEPAL", 40.693, 1.925), ("TAQOH", 40.872, 1.631),
            ("ULKAL", 41.136, 1.588), ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ],
        "VERSO2N": [
            ("VERSO", 41.153, 3.757), ("OSTUR", 40.781, 2.894),
            ("ISWIQ", 41.014, 2.356), ("VIBIM", 41.071, 2.206), ("LEBL 02", 41.282, 2.088)
        ],
        "PUMAL5N": [
            ("PUMAL", 42.367, 2.008), ("BERGA", 42.172, 2.032),
            ("BOLQE", 41.734, 1.550), ("VIBOK", 41.547, 1.502),
            ("VLA", 41.343, 1.548), ("ULKAL", 41.136, 1.588),
            ("TOTKI", 41.134, 1.731), ("LEBL 02", 41.282, 2.088)
        ]
    },
    "06L": {
        "ALBER2E": [
            ("ALBER", 42.451, 2.832), ("CUTXE", 42.132, 2.754),
            ("UTHAN", 41.885, 2.379), ("ENJUC", 41.769, 2.204),
            ("BL573", 41.680, 2.170), ("SLL", 41.520, 2.110), ("LEBL 06L", 41.288, 2.083)
        ],
        "BISBA2E": [
            ("BISBA", 42.086, 3.626), ("NEMUM", 42.009, 3.393),
            ("BGR", 41.948, 3.209), ("ENJUC", 41.769, 2.204),
            ("BL573", 41.680, 2.170), ("SLL", 41.520, 2.110), ("LEBL 06L", 41.288, 2.083)
        ],
        "CASPE3E": [
            ("CASPE", 41.268, 0.199), ("INCAH", 41.219, 0.592),
            ("PIJUH", 40.982, 0.907), ("TAQOH", 40.872, 1.631),
            ("RUBOT", 40.974, 1.706), ("LEBL 06L", 41.288, 2.083)
        ],
        "GRAUS1E": [
            ("GRAUS", 41.979, 0.376), ("LRD", 41.553, 0.648),
            ("RES", 41.144, 1.162), ("TAQOH", 40.872, 1.631),
            ("RUBOT", 40.974, 1.706), ("LEBL 06L", 41.288, 2.083)
        ],
        "MARTA3E": [
            ("MARTA", 40.355, 1.280), ("EBROX", 40.709, 1.232),
            ("RES", 41.144, 1.162), ("BL561", 41.249, 1.365),
            ("VLA", 41.343, 1.548), ("LEBL 06L", 41.288, 2.083)
        ],
        "NEPAL3E": [
            ("NEPAL", 40.693, 1.925), ("TAQOH", 40.872, 1.631),
            ("RUBOT", 40.974, 1.706), ("LEBL 06L", 41.288, 2.083)
        ],
        "VERSO3E": [
            ("VERSO", 41.153, 3.757), ("OSTUR", 40.781, 2.894),
            ("ISWIQ", 41.014, 2.356), ("VIBIM", 41.071, 2.206), ("LEBL 06L", 41.288, 2.083)
        ],
        "PUMAL1E": [
            ("PUMAL", 42.367, 2.008), ("BERGA", 42.172, 2.032),
            ("BOLQE", 41.734, 1.550), ("VIBOK", 41.547, 1.502),
            ("VLA", 41.343, 1.548), ("LEBL 06L", 41.288, 2.083)
        ]
    },
    "24R": {
        "ALBER2W": [
            ("ALBER", 42.451, 2.832), ("CUTXE", 42.132, 2.754),
            ("BL469", 41.804, 2.674), ("CLE", 41.640, 2.635), ("LEBL 24R", 41.311, 2.115)
        ],
        "BISBA2W": [
            ("BISBA", 42.086, 3.626), ("USSOF", 41.654, 3.027),
            ("XAMUR", 41.403, 2.872), ("LESBA", 41.255, 2.663), ("LEBL 24R", 41.311, 2.115)
        ],
        "CASPE2W": [
            ("CASPE", 41.268, 0.199), ("MECUH", 41.457, 1.072),
            ("VIBOK", 41.547, 1.502), ("BL461", 41.550, 1.891),
            ("SLL", 41.520, 2.110), ("LEBL 24R", 41.311, 2.115)
        ],
        "GRAUS2W": [
            ("GRAUS", 41.979, 0.376), ("TIRGO", 41.784, 1.126),
            ("BL459", 41.577, 1.901), ("SLL", 41.520, 2.110), ("LEBL 24R", 41.311, 2.115)
        ],
        "MARTA2W": [
            ("MARTA", 40.355, 1.280), ("NEPAL", 40.693, 1.925),
            ("RAVAX", 40.921, 2.088), ("RULOS", 41.177, 2.281), ("LEBL 24R", 41.311, 2.115)
        ],
        "NEPAL2W": [
            ("NEPAL", 40.693, 1.925), ("RAVAX", 40.921, 2.088),
            ("RULOS", 41.177, 2.281), ("LEBL 24R", 41.311, 2.115)
        ],
        "VERSO2W": [
            ("VERSO", 41.153, 3.757), ("SADEM", 41.210, 3.174),
            ("BL468", 41.230, 2.948), ("LESBA", 41.255, 2.663), ("LEBL 24R", 41.311, 2.115)
        ],
        "PUMAL2W": [
            ("PUMAL", 42.367, 2.008), ("ELLIH", 42.131, 2.213),
            ("BL465", 41.781, 2.515), ("CLE", 41.640, 2.635), ("LEBL 24R", 41.311, 2.115)
        ]
    }
}

# --- ASIGNACIÓN AUTOMÁTICA DE STARs POR ORIGEN ---
ORIGIN_STARS = {
    "02": {
        "BIKF": "GRAUS3N", "CYUL": "GRAUS3N", "CYYZ": "GRAUS3N", "DAAG": "MARTA4N", "EBAW": "ALBER3N",
        "EBBR": "ALBER3N", "EBOS": "ALBER3N", "EDDB": "BISBA5N", "EDDF": "ALBER3N", "EDDH": "ALBER3N",
        "EDDK": "ALBER3N", "EDDL": "ALBER3N", "EDDM": "BISBA5N", "EDDN": "BISBA5N", "EDDP": "BISBA5N",
        "EDDS": "BISBA5N", "EDDT": "BISBA5N", "EDDV": "ALBER3N", "EETN": "BISBA5N", "EFHK": "ALBER3N",
        "EGAA": "PUMAL5N", "EGBB": "PUMAL5N", "EGCC": "PUMAL5N", "EGFF": "PUMAL5N", "EGGD": "PUMAL5N",
        "EGGW": "PUMAL5N", "EGHI": "PUMAL5N", "EGKK": "PUMAL5N", "EGLL": "PUMAL5N", "EGMC": "PUMAL5N",
        "EGNM": "PUMAL5N", "EGNT": "PUMAL5N", "EGNX": "PUMAL5N", "EGPH": "PUMAL5N", "EGPK": "PUMAL5N",
        "EGSS": "PUMAL5N", "EHAM": "ALBER3N", "EHEH": "ALBER3N", "EHRD": "ALBER3N", "EIDW": "PUMAL5N",
        "EKBI": "ALBER3N", "EKCH": "BISBA5N", "ELLX": "ALBER3N", "ENBR": "ALBER3N", "ENGM": "ALBER3N",
        "EPKK": "BISBA5N", "EPKT": "BISBA5N", "EPWA": "BISBA5N", "ESGG": "ALBER3N", "ESKN": "ALBER3N",
        "ESSA": "ALBER3N", "ETNL": "ALBER3N", "EVRA": "BISBA5N", "EYVI": "BISBA5N", "GCFV": "MARTA4N",
        "GCLP": "MARTA4N", "GCRR": "MARTA4N", "GCXO": "MARTA4N", "GMFF": "MARTA4N", "GMMN": "MARTA4N",
        "GMMX": "MARTA4N", "GMTT": "MARTA4N", "HECA": "VERSO2N", "KATL": "GRAUS3N", "KCLT": "GRAUS3N",
        "KEWR": "GRAUS3N", "KJFK": "GRAUS3N", "KMIA": "GRAUS3N", "KPHL": "GRAUS3N", "KUGN": "GRAUS3N",
        "LBSF": "VERSO2N", "LCLK": "VERSO2N", "LDDU": "VERSO2N", "LDSP": "VERSO2N", "LDZA": "VERSO2N",
        "LEAL": "MARTA4N", "LEAM": "MARTA4N", "LEAS": "GRAUS3N", "LEBB": "GRAUS3N", "LEBZ": "CASPE4N",
        "LECO": "GRAUS3N", "LEGE": "BISBA5N", "LEGR": "MARTA4N", "LEIB": "MARTA4N", "LEJR": "MARTA4N",
        "LELN": "GRAUS3N", "LEMD": "CASPE4N", "LEMG": "MARTA4N", "LEMH": "VERSO2N", "LEPA": "NEPAL4N",
        "LESO": "GRAUS3N", "LEST": "GRAUS3N", "LEVC": "MARTA4N", "LEVD": "GRAUS3N", "LEVX": "GRAUS3N",
        "LEZL": "MARTA4N", "LFBD": "PUMAL5N", "LFLL": "ALBER3N", "LFMD": "BISBA5N", "LFML": "BISBA5N",
        "LFMN": "BISBA5N", "LFOB": "ALBER3N", "LFPG": "ALBER3N", "LFPO": "ALBER3N", "LFQQ": "ALBER3N",
        "LFRN": "PUMAL5N", "LFRS": "PUMAL5N", "LFSB": "ALBER3N", "LGAV": "VERSO2N", "LGIR": "VERSO2N",
        "LGKR": "VERSO2N", "LGMK": "VERSO2N", "LHBP": "BISBA5N", "LIBD": "VERSO2N", "LICJ": "VERSO2N",
        "LIEE": "VERSO2N", "LIEO": "VERSO2N", "LIMC": "BISBA5N", "LIME": "BISBA5N", "LIMF": "BISBA5N",
        "LIML": "BISBA5N", "LIPE": "BISBA5N", "LIPH": "BISBA5N", "LIPX": "BISBA5N", "LIRF": "VERSO2N",
        "LIRN": "VERSO2N", "LIRP": "BISBA5N", "LIRQ": "BISBA5N", "LKPR": "BISBA5N", "LLBG": "VERSO2N",
        "LMML": "VERSO2N", "LOWW": "BISBA5N", "LPPR": "CASPE4N", "LPPT": "CASPE4N", "LRCL": "BISBA5N",
        "LROP": "VERSO2N", "LSGG": "ALBER3N", "LSZH": "ALBER3N", "LTBA": "VERSO2N", "LTFJ": "VERSO2N",
        "LWSK": "VERSO2N", "LYTV": "VERSO2N", "OLBA": "VERSO2N", "OMAA": "VERSO2N", "OMDB": "VERSO2N",
        "OTHH": "VERSO2N", "SAEZ": "MARTA4N", "SBGR": "MARTA4N", "SKBO": "CASPE4N", "UKBB": "BISBA5N",
        "UKKK": "BISBA5N", "ULLI": "BISBA5N", "UUDD": "BISBA5N", "UUEE": "BISBA5N", "WSSS": "VERSO2N"
    },
    "06L": {
        "BIKF": "GRAUS1E", "CYUL": "GRAUS1E", "CYYZ": "GRAUS1E", "DAAG": "MARTA3E", "EBAW": "ALBER2E",
        "EBBR": "ALBER2E", "EBOS": "ALBER2E", "EDDB": "BISBA2E", "EDDF": "ALBER2E", "EDDH": "ALBER2E",
        "EDDK": "ALBER2E", "EDDL": "ALBER2E", "EDDM": "BISBA2E", "EDDN": "BISBA2E", "EDDP": "BISBA2E",
        "EDDS": "BISBA2E", "EDDT": "BISBA2E", "EDDV": "ALBER2E", "EETN": "BISBA2E", "EFHK": "ALBER2E",
        "EGAA": "PUMAL1E", "EGBB": "PUMAL1E", "EGCC": "PUMAL1E", "EGFF": "PUMAL1E", "EGGD": "PUMAL1E",
        "EGGW": "PUMAL1E", "EGHI": "PUMAL1E", "EGKK": "PUMAL1E", "EGLL": "PUMAL1E", "EGMC": "PUMAL1E",
        "EGNM": "PUMAL1E", "EGNT": "PUMAL1E", "EGNX": "PUMAL1E", "EGPH": "PUMAL1E", "EGPK": "PUMAL1E",
        "EGSS": "PUMAL1E", "EHAM": "ALBER2E", "EHEH": "ALBER2E", "EHRD": "ALBER2E", "EIDW": "PUMAL1E",
        "EKBI": "ALBER2E", "EKCH": "BISBA2E", "ELLX": "ALBER2E", "ENBR": "ALBER2E", "ENGM": "ALBER2E",
        "EPKK": "BISBA2E", "EPKT": "BISBA2E", "EPWA": "BISBA2E", "ESGG": "ALBER2E", "ESKN": "ALBER2E",
        "ESSA": "ALBER2E", "ETNL": "ALBER2E", "EVRA": "BISBA2E", "EYVI": "BISBA2E", "GCFV": "MARTA3E",
        "GCLP": "MARTA3E", "GCRR": "MARTA3E", "GCXO": "MARTA3E", "GMFF": "MARTA3E", "GMMN": "MARTA3E",
        "GMMX": "MARTA3E", "GMTT": "MARTA3E", "HECA": "VERSO3E", "KATL": "GRAUS1E", "KCLT": "GRAUS1E",
        "KEWR": "GRAUS1E", "KJFK": "GRAUS1E", "KMIA": "GRAUS1E", "KPHL": "GRAUS1E", "KUGN": "GRAUS1E",
        "LBSF": "VERSO3E", "LCLK": "VERSO3E", "LDDU": "VERSO3E", "LDSP": "VERSO3E", "LDZA": "VERSO3E",
        "LEAL": "MARTA3E", "LEAM": "MARTA3E", "LEAS": "GRAUS1E", "LEBB": "GRAUS1E", "LEBZ": "CASPE3E",
        "LECO": "GRAUS1E", "LEGE": "BISBA2E", "LEGR": "MARTA3E", "LEIB": "MARTA3E", "LEJR": "MARTA3E",
        "LELN": "GRAUS1E", "LEMD": "CASPE3E", "LEMG": "MARTA3E", "LEMH": "VERSO3E", "LEPA": "NEPAL3E",
        "LESO": "GRAUS1E", "LEST": "GRAUS1E", "LEVC": "MARTA3E", "LEVD": "GRAUS1E", "LEVX": "GRAUS1E",
        "LEZL": "MARTA3E", "LFBD": "PUMAL1E", "LFLL": "ALBER2E", "LFMD": "BISBA2E", "LFML": "BISBA2E",
        "LFMN": "BISBA2E", "LFOB": "ALBER2E", "LFPG": "ALBER2E", "LFPO": "ALBER2E", "LFQQ": "ALBER2E",
        "LFRN": "PUMAL1E", "LFRS": "PUMAL1E", "LFSB": "ALBER2E", "LGAV": "VERSO3E", "LGIR": "VERSO3E",
        "LGKR": "VERSO3E", "LGMK": "VERSO3E", "LHBP": "BISBA2E", "LIBD": "VERSO3E", "LICJ": "VERSO3E",
        "LIEE": "VERSO3E", "LIEO": "VERSO3E", "LIMC": "BISBA2E", "LIME": "BISBA2E", "LIMF": "BISBA2E",
        "LIML": "BISBA2E", "LIPE": "BISBA2E", "LIPH": "BISBA2E", "LIPX": "BISBA2E", "LIRF": "VERSO3E",
        "LIRN": "VERSO3E", "LIRP": "BISBA2E", "LIRQ": "BISBA2E", "LKPR": "BISBA2E", "LLBG": "VERSO3E",
        "LMML": "VERSO3E", "LOWW": "BISBA2E", "LPPR": "CASPE3E", "LPPT": "CASPE3E", "LRCL": "BISBA2E",
        "LROP": "VERSO3E", "LSGG": "ALBER2E", "LSZH": "ALBER2E", "LTBA": "VERSO3E", "LTFJ": "VERSO3E",
        "LWSK": "VERSO3E", "LYTV": "VERSO3E", "OLBA": "VERSO3E", "OMAA": "VERSO3E", "OMDB": "VERSO3E",
        "OTHH": "VERSO3E", "SAEZ": "MARTA3E", "SBGR": "MARTA3E", "SKBO": "CASPE3E", "UKBB": "BISBA2E",
        "UKKK": "BISBA2E", "ULLI": "BISBA2E", "UUDD": "BISBA2E", "UUEE": "BISBA2E", "WSSS": "VERSO3E"
    },
    "24R": {
        "BIKF": "GRAUS2W", "CYUL": "GRAUS2W", "CYYZ": "GRAUS2W", "DAAG": "MARTA2W", "EBAW": "ALBER2W",
        "EBBR": "ALBER2W", "EBOS": "ALBER2W", "EDDB": "BISBA2W", "EDDF": "ALBER2W", "EDDH": "ALBER2W",
        "EDDK": "ALBER2W", "EDDL": "ALBER2W", "EDDM": "BISBA2W", "EDDN": "BISBA2W", "EDDP": "BISBA2W",
        "EDDS": "BISBA2W", "EDDT": "BISBA2W", "EDDV": "ALBER2W", "EETN": "BISBA2W", "EFHK": "ALBER2W",
        "EGAA": "PUMAL2W", "EGBB": "PUMAL2W", "EGCC": "PUMAL2W", "EGFF": "PUMAL2W", "EGGD": "PUMAL2W",
        "EGGW": "PUMAL2W", "EGHI": "PUMAL2W", "EGKK": "PUMAL2W", "EGLL": "PUMAL2W", "EGMC": "PUMAL2W",
        "EGNM": "PUMAL2W", "EGNT": "PUMAL2W", "EGNX": "PUMAL2W", "EGPH": "PUMAL2W", "EGPK": "PUMAL2W",
        "EGSS": "PUMAL2W", "EHAM": "ALBER2W", "EHEH": "ALBER2W", "EHRD": "ALBER2W", "EIDW": "PUMAL2W",
        "EKBI": "ALBER2W", "EKCH": "BISBA2W", "ELLX": "ALBER2W", "ENBR": "ALBER2W", "ENGM": "ALBER2W",
        "EPKK": "BISBA2W", "EPKT": "BISBA2W", "EPWA": "BISBA2W", "ESGG": "ALBER2W", "ESKN": "ALBER2W",
        "ESSA": "ALBER2W", "ETNL": "ALBER2W", "EVRA": "BISBA2W", "EYVI": "BISBA2W", "GCFV": "MARTA2W",
        "GCLP": "MARTA2W", "GCRR": "MARTA2W", "GCXO": "MARTA2W", "GMFF": "MARTA2W", "GMMN": "MARTA2W",
        "GMMX": "MARTA2W", "GMTT": "MARTA2W", "HECA": "VERSO2W", "KATL": "GRAUS2W", "KCLT": "GRAUS2W",
        "KEWR": "GRAUS2W", "KJFK": "GRAUS2W", "KMIA": "GRAUS2W", "KPHL": "GRAUS2W", "KUGN": "GRAUS2W",
        "LBSF": "VERSO2W", "LCLK": "VERSO2W", "LDDU": "VERSO2W", "LDSP": "VERSO2W", "LDZA": "VERSO2W",
        "LEAL": "MARTA2W", "LEAM": "MARTA2W", "LEAS": "GRAUS2W", "LEBB": "GRAUS2W", "LEBZ": "CASPE2W",
        "LECO": "GRAUS2W", "LEGE": "BISBA2W", "LEGR": "MARTA2W", "LEIB": "MARTA2W", "LEJR": "MARTA2W",
        "LELN": "GRAUS2W", "LEMD": "CASPE2W", "LEMG": "MARTA2W", "LEMH": "VERSO2W", "LEPA": "NEPAL2W",
        "LESO": "GRAUS2W", "LEST": "GRAUS2W", "LEVC": "MARTA2W", "LEVD": "GRAUS2W", "LEVX": "GRAUS2W",
        "LEZL": "MARTA2W", "LFBD": "PUMAL2W", "LFLL": "ALBER2W", "LFMD": "BISBA2W", "LFML": "BISBA2W",
        "LFMN": "BISBA2W", "LFOB": "ALBER2W", "LFPG": "ALBER2W", "LFPO": "ALBER2W", "LFQQ": "ALBER2W",
        "LFRN": "PUMAL2W", "LFRS": "PUMAL2W", "LFSB": "ALBER2W", "LGAV": "VERSO2W", "LGIR": "VERSO2W",
        "LGKR": "VERSO2W", "LGMK": "VERSO2W", "LHBP": "BISBA2W", "LIBD": "VERSO2W", "LICJ": "VERSO2W",
        "LIEE": "VERSO2W", "LIEO": "VERSO2W", "LIMC": "BISBA2W", "LIME": "BISBA2W", "LIMF": "BISBA2W",
        "LIML": "BISBA2W", "LIPE": "BISBA2W", "LIPH": "BISBA2W", "LIPX": "BISBA2W", "LIRF": "VERSO2W",
        "LIRN": "VERSO2W", "LIRP": "BISBA2W", "LIRQ": "BISBA2W", "LKPR": "BISBA2W", "LLBG": "VERSO2W",
        "LMML": "VERSO2W", "LOWW": "BISBA2W", "LPPR": "CASPE2W", "LPPT": "CASPE2W", "LRCL": "BISBA2W",
        "LROP": "VERSO2W", "LSGG": "ALBER2W", "LSZH": "ALBER2W", "LTBA": "VERSO2W", "LTFJ": "VERSO2W",
        "LWSK": "VERSO2W", "LYTV": "VERSO2W", "OLBA": "VERSO2W", "OMAA": "VERSO2W", "OMDB": "VERSO2W",
        "OTHH": "VERSO2W", "SAEZ": "MARTA2W", "SBGR": "MARTA2W", "SKBO": "CASPE2W", "UKBB": "BISBA2W",
        "UKKK": "BISBA2W", "ULLI": "BISBA2W", "UUDD": "BISBA2W", "UUEE": "BISBA2W", "WSSS": "VERSO2W"
    }
}


# =========================================================
# --- DATOS GLOBALES Y MOTOR DEL MAPA RADAR ---
# =========================================================
COLOR_MAR = "#08182B"
COLOR_TIERRA = "#172635"
COLOR_FRONTERA_INT = "#5D8AA8"
COLOR_FRONTERA_REG = "#3A5A78"

RADAR_MIN_LAT, RADAR_MAX_LAT = 40.0, 43.1
RADAR_MIN_LON, RADAR_MAX_LON = -1.0, 4.2


def get_radar_xy(lat, lon, w, h):
    x = (lon - RADAR_MIN_LON) / (RADAR_MAX_LON - RADAR_MIN_LON) * w
    y = h - ((lat - RADAR_MIN_LAT) / (RADAR_MAX_LAT - RADAR_MIN_LAT) * h)
    return x, y


LINEA_COSTA = [(40.00, 0.05), (40.20, 0.20), (40.40, 0.40), (40.52, 0.52), (40.61, 0.65), (40.71, 0.80), (40.74, 0.88),
               (40.78, 0.75), (40.85, 0.79), (40.95, 0.85), (41.05, 1.10), (41.11, 1.25), (41.15, 1.34), (41.19, 1.45),
               (41.21, 1.56), (41.23, 1.70), (41.24, 1.85), (41.27, 2.00), (41.29, 2.10), (41.35, 2.16), (41.40, 2.22),
               (41.45, 2.28), (41.50, 2.36), (41.55, 2.46), (41.60, 2.58), (41.65, 2.70), (41.68, 2.82), (41.73, 2.95),
               (41.80, 3.05), (41.85, 3.12), (41.95, 3.21), (42.02, 3.20), (42.12, 3.16), (42.20, 3.18), (42.27, 3.18),
               (42.32, 3.32), (42.40, 3.20), (42.44, 3.16), (42.50, 3.08), (42.60, 3.03), (42.70, 3.04), (42.80, 3.04),
               (43.00, 3.10), (43.10, 3.15)]
POLIGONO_TIERRA = LINEA_COSTA + [(43.10, -1.00), (40.00, -1.00), (40.00, 0.05)]
ANDORRA = [(42.54, 1.73), (42.43, 1.45), (42.56, 1.42), (42.65, 1.53), (42.54, 1.73)]
FRONTERA_FRA_ESP_ESTE = [(42.44, 3.16), (42.42, 2.95), (42.34, 2.86), (42.40, 2.44), (42.42, 2.15), (42.35, 1.95),
                         (42.54, 1.73)]
FRONTERA_FRA_ESP_OESTE = [(42.56, 1.42), (42.65, 1.25), (42.80, 0.85), (42.85, 0.73), (42.75, 0.00), (42.80, -0.40),
                          (42.90, -0.80), (43.00, -1.00)]
FRONTERA_CAT_ARA = [(42.85, 0.73), (42.75, 0.74), (42.60, 0.74), (42.45, 0.72), (42.30, 0.70), (42.15, 0.45),
                    (42.00, 0.35), (41.80, 0.32), (41.60, 0.30), (41.40, 0.30), (41.25, 0.20), (41.10, 0.15),
                    (40.90, 0.15), (40.70, 0.15)]
FRONTERA_CAT_VAL = [(40.70, 0.15), (40.65, 0.25), (40.60, 0.30), (40.52, 0.52)]
FRONTERA_ARA_VAL = [(40.70, 0.15), (40.60, -0.10), (40.40, -0.40), (40.20, -0.80), (40.10, -1.00)]
FRONTERA_ARA_NAV = [(42.90, -0.80), (42.75, -0.95), (42.60, -1.00)]
CIUDADES = [("BARCELONA", 41.38, 2.18), ("TARRAGONA", 41.11, 1.25), ("LLEIDA", 41.61, 0.62), ("GIRONA", 41.98, 2.82),
            ("ZARAGOZA", 41.65, -0.88), ("HUESCA", 42.14, -0.40)]


def draw_radar_base(canvas, w, h, pista_seleccionada=None):
    """Motor universal que dibuja el fondo del radar en cualquier canvas."""
    canvas.delete("radar")

    # 1. Tierra
    coords_tierra = []
    for lat, lon in POLIGONO_TIERRA:
        x, y = get_radar_xy(lat, lon, w, h)
        coords_tierra.extend([x, y])
    canvas.create_polygon(coords_tierra, fill=COLOR_TIERRA, outline="#2E75B6", width=3, tags="radar")

    # 2. Fronteras Internacionales
    for frontera in [ANDORRA, FRONTERA_FRA_ESP_ESTE, FRONTERA_FRA_ESP_OESTE]:
        for i in range(len(frontera) - 1):
            x1, y1 = get_radar_xy(frontera[i][0], frontera[i][1], w, h)
            x2, y2 = get_radar_xy(frontera[i + 1][0], frontera[i + 1][1], w, h)
            canvas.create_line(x1, y1, x2, y2, fill=COLOR_FRONTERA_INT, width=2, dash=(6, 4), tags="radar")

    # 3. Fronteras Autonómicas
    for frontera in [FRONTERA_CAT_ARA, FRONTERA_CAT_VAL, FRONTERA_ARA_VAL, FRONTERA_ARA_NAV]:
        for i in range(len(frontera) - 1):
            x1, y1 = get_radar_xy(frontera[i][0], frontera[i][1], w, h)
            x2, y2 = get_radar_xy(frontera[i + 1][0], frontera[i + 1][1], w, h)
            canvas.create_line(x1, y1, x2, y2, fill=COLOR_FRONTERA_REG, width=1, dash=(2, 4), tags="radar")

    # 4. Rutas Fantasma (Solo si se le pide)
    if pista_seleccionada and pista_seleccionada in SIDS_DATA:
        for sid_name, ruta in SIDS_DATA[pista_seleccionada].items():
            for i in range(len(ruta) - 1):
                x1, y1 = get_radar_xy(ruta[i][1], ruta[i][2], w, h)
                x2, y2 = get_radar_xy(ruta[i + 1][1], ruta[i + 1][2], w, h)
                canvas.create_line(x1, y1, x2, y2, fill="#203952", width=1, tags="radar")

    # 5. Anillos
    cx, cy = get_radar_xy(41.29, 2.07, w, h)
    for r in [50, 150, 250, 350, 450, 600]:
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#1B2F42", dash=(2, 6), tags="radar")

    # 6. Ciudades
    for nombre, lat, lon in CIUDADES:
        cx_city, cy_city = get_radar_xy(lat, lon, w, h)
        canvas.create_oval(cx_city - 2, cy_city - 2, cx_city + 2, cy_city + 2, fill="#7F8C8D", outline="", tags="radar")
        canvas.create_text(cx_city + 6, cy_city, text=nombre, fill="#7F8C8D", font=("Courier", 8, "bold"), anchor="w",
                           tags="radar")


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
    # Hacemos la ventana un poquito más alta (210) para que quepa todo holgado
    w, h = 320, 210
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

    # --- Contenedor invisible para guardar el espacio del error ---
    msg_frame = tk.Frame(dialog, bg="white", height=45)
    msg_frame.pack(fill="x")
    msg_frame.pack_propagate(False)

    error_lbl = tk.Label(msg_frame, text="", bg="white", font=("Helvetica", 9), fg="red")
    error_lbl.pack()

    def show_hint():
        messagebox.showinfo("Help", "ICAO Code Josep Tarradellas Barcelona – El Prat Airport", parent=dialog)

    help_btn = tk.Button(msg_frame, text="¿Forgot password?", command=show_hint,
                         bg="white", fg="royalblue", relief="flat",
                         font=("Helvetica", 8, "underline"), cursor="hand2")
    # ------------------------------------------------------------------------

    result = {"ok": False}

    def attempt():
        if entry.get() == PASSWORD:
            result["ok"] = True
            dialog.destroy()
        else:
            entry.delete(0, tk.END)
            # Cambiamos el texto vacío por el mensaje de error y mostramos la ayuda
            error_lbl.config(text="Incorrect password")
            help_btn.pack()

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
        title="Select airports file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not path:
        return

    airports = LoadAirports(path)

    # Comprovació d'error si és buit
    if len(airports) == 0:
        messagebox.showerror("Error",
                             "No airport could be loaded. Make sure that the file is the correct one.")
        return

    refresh_airport_list()

    lines = []
    for ap in airports:
        # Creem una línia maca amb el codi de l'aeroport i les seves coordenades
        schengen_txt = "Schengen" if ap.isSchengen else "No Schengen"
        lines.append(f"  {ap.code:<6} |  Lat: {ap.latitude:.4f}  |  Lon: {ap.longitude:.4f}  |  ({schengen_txt})")

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
        messagebox.showerror("Error", "Latitude and Longitude must be valid numbers.")
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
        title="Select arrivals file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not path:
        return

    aircrafts = LoadArrivals(path)

    # Si la lista está vacía (0 vuelos), lanzamos ERROR y paramos
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No flight could be loaded. Make sure that the file is the correct one.")
        return

    refresh_flights_list()
    lines = []
    for ac in aircrafts:
        lines.append(f"  {ac.timelanding:<10} {ac.origin:<8} {ac.company}")
    show_info_label(f"Flights loaded  ({len(aircrafts)})", lines)
    refresh_ticker()

    # Si llega hasta aquí es que ha ido bien, lanzamos INFO
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
        title="Select airport structure file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not path:
        return

    try:
        # Intentamos cargar la estructura
        bcn = LoadAirportStructure(path)

        # 1. Si devuelve un código de error o está vacío, lanzamos un fallo voluntario
        if bcn == -1 or bcn is None:
            raise Exception("Upload Error")

        # 2. Comprobamos de forma segura si tiene terminales (soporta 'terminals' y 'Terminals')
        num_terminales = 0
        if hasattr(bcn, "terminals"):
            num_terminales = len(bcn.terminals)
        elif hasattr(bcn, "Terminals"):
            num_terminales = len(bcn.Terminals)
        else:
            # Si el objeto no tiene ningún atributo de terminales, está mal creado
            raise Exception("Atribute not found")

        # 3. Si al final el recuento da 0 terminales, lanzamos el fallo
        if num_terminales == 0:
            raise Exception("0 terminals found")

        # Si pasa todos los filtros con éxito, muestra el mensaje de confirmación
        messagebox.showinfo("Done", "Airport structure loaded successfully.")

    except Exception:
        # Si pasa CUALQUIER cosa mala dentro del 'try', venimos directamente aquí:
        messagebox.showerror("Error", "No structure could not be loaded. Make sure that the file is the correct one.")
        bcn = None  # Reseteamos la variable para que no guarde dades corruptas
        return


def time_to_minutes(t_str):
    """Convierte una hora 'HH:MM' a minutos totales para poder comparar."""
    if not t_str or ":" not in t_str: return 0
    try:
        h, m = map(int, t_str.split(':'))
        return h * 60 + m
    except:
        return 0


def assign_dynamic_gates():
    if 'merged' not in globals() or len(merged) == 0:
        messagebox.showerror("Error", "Please run Merge Movements first.")
        return
    if 'bcn' not in globals() or bcn is None:
        messagebox.showerror("Error", "Airport structure not loaded.")
        return

    # 1. Limpiar todas las puertas y añadir el reloj de disponibilidad
    for t in bcn.Terminals:
        for a in t.BoardingAreas:
            for g in a.gates:
                g.id = None
                g.free_at = 0  # Minuto del día en el que se quedará libre

    # 2. Ordenar los vuelos por hora de LLEGADA (Cronológico)
    vuelos_ordenados = sorted(merged, key=lambda x: time_to_minutes(getattr(x, 'timelanding', '23:59')))

    asignados = 0
    sin_puerta = 0

    for ac in vuelos_ordenados:
        arr_mins = time_to_minutes(getattr(ac, 'timelanding', '00:00'))
        dep_mins = time_to_minutes(getattr(ac, 'timedeparture', '23:59'))

        # Ajustes si solo es llegada o solo salida
        if not getattr(ac, 'timelanding', ''): arr_mins = 0
        if not getattr(ac, 'timedeparture', ''): dep_mins = 24 * 60

        company = getattr(ac, 'company', '???')
        pref_t = "T2" if company in ["RYR", "EZY", "WZZ", "TRA", "NOR"] else "T1"

        asignado = False

        # 3. Intentar asignar en su terminal preferida
        for t in bcn.Terminals:
            if t.number != pref_t: continue
            for a in t.BoardingAreas:
                for g in a.gates:
                    # Comprobamos si está libre en el momento en que llega este avión
                    if getattr(g, 'free_at', 0) <= arr_mins:
                        g.id = ac.id
                        g.free_at = dep_mins + 15  # Se libera 15 mins tras el despegue
                        ac.gate = g.name  # Guardamos la puerta en el avión
                        ac.terminal = t.number
                        asignado = True
                        asignados += 1
                        break
                if asignado: break
            if asignado: break

        # 4. Si su terminal está llena, buscar en la otra (Overflow)
        if not asignado:
            for t in bcn.Terminals:
                if t.number == pref_t: continue
                for a in t.BoardingAreas:
                    for g in a.gates:
                        if getattr(g, 'free_at', 0) <= arr_mins:
                            g.id = ac.id
                            g.free_at = dep_mins + 15
                            ac.gate = g.name
                            ac.terminal = t.number
                            asignado = True
                            asignados += 1
                            break
                    if asignado: break
                if asignado: break

        if not asignado:
            sin_puerta += 1
            ac.gate = "---"
            ac.terminal = pref_t

    messagebox.showinfo("Gates Assigned",
                        f"Dynamic Gate Assignment Complete!\n\n✅ Flights parked: {asignados}\n⚠️ Kept in holding/No gate: {sin_puerta}")

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

    # Si la lista está vacía (0 vuelos), lanzamos ERROR y paramos
    if len(departures) == 0:
        messagebox.showerror("Error",
                             "No departure could be loaded. Make sure that the file is the correct one.")
        return

    lines = []
    for ac in departures:
        lines.append(f"  {ac.timedeparture:<10} {ac.destination:<8} {ac.company}  [{ac.id}]")
    show_info_label(f"Departures loaded  ({len(departures)})", lines)
    refresh_departures_list()
    refresh_ticker()

    # Si llega hasta aquí es que ha ido bien, lanzamos INFO
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

    # Rescatamos el STAR y el SID de las listas originales ya que la función MergeMovements genera objetos nuevos y los pierde.
    for ac in merged:
        # Buscar el STAR original en las llegadas
        for a in aircrafts:
            if a.id == ac.id and hasattr(a, 'star'):
                ac.star = a.star
                break
        # Buscar el SID original en las salidas
        for d in departures:
            if d.id == ac.id and hasattr(d, 'sid'):
                ac.sid = d.sid
                break

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


def show_interactive_diagram():
    import copy
    if bcn is None:
        messagebox.showerror("Error", "Load the airport structure first.")
        return
    if len(merged) == 0:
        messagebox.showerror("Error", "Merge movements first.")
        return

    # 1. Pre-calcular estados
    bcn_states = []
    current_bcn = copy.deepcopy(bcn)

    # Asignamos los vuelos nocturnos primero
    AssignNightGates(current_bcn, merged)

    # El paso 0 de nuestra lista será la foto PURA de los Night Gates
    bcn_states.append(copy.deepcopy(current_bcn))

    # Calculamos los 144 pasos del día (cada 10 min)
    for step in range(144):
        h = step // 6
        m = (step % 6) * 10

        if m == 0:
            AssignGatesAtTime(current_bcn, merged, f"{str(h).zfill(2)}:00")

        bcn_states.append(copy.deepcopy(current_bcn))

    # 2. Construir la interfaz en el panel derecho
    clear_info_panel()
    tk.Label(info_frame, text="Interactive Gate Diagram", bg="#F0F4F8",
             font=("Helvetica", 11, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 2))

    frame_slider = tk.Frame(info_frame, bg="#F0F4F8")
    frame_slider.pack(fill="x", padx=10, pady=5)

    lbl_hour = tk.Label(frame_slider, text="✈️  NIGHT GATES 00:00  ✈️", bg="#F0F4F8",
                        font=("Helvetica", 14, "bold"), fg="#2C3E50")
    lbl_hour.pack(side="top")

    # Función que se ejecuta al mover la barra
    def on_slider_move(val):
        step = int(val)

        # Si es el primer paso (el 0), mostramos el texto especial
        if step == 0:
            lbl_hour.config(text="✈️  NIGHT GATES 00:00  ✈️", fg="#2C3E50")
        else:
            # Como el paso 0 es night gates, restamos 1 para calcular la hora normal
            real_step = step - 1
            h = real_step // 6
            m = (real_step % 6) * 10
            lbl_hour.config(text=f"✈️  Time: {str(h).zfill(2)}:{str(m).zfill(2)}  ✈️", fg="#3A7FC1")

        _draw_airport_on_canvas(canvas, bcn_states[step])

    # Barra deslizadora de 0 a 144 (el 0 es Night Gates, 1-144 es el resto del día)
    slider = tk.Scale(frame_slider, from_=0, to=144, orient="horizontal",
                      bg="#F0F4F8", highlightthickness=0, command=on_slider_move,
                      showvalue=0, sliderlength=25, length=450, troughcolor="#b3d4ff")
    slider.pack(side="top", pady=5)

    frame_c = tk.Frame(info_frame, bg="#F0F4F8")
    frame_c.pack(fill="both", expand=True, padx=10, pady=(4, 4))

    h_scroll = tk.Scrollbar(frame_c, orient="horizontal")
    h_scroll.pack(side="bottom", fill="x")
    v_scroll = tk.Scrollbar(frame_c, orient="vertical")
    v_scroll.pack(side="right", fill="y")

    canvas = tk.Canvas(frame_c, bg="white", xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    h_scroll.config(command=canvas.xview)
    v_scroll.config(command=canvas.yview)

    tip_var = tk.StringVar(value="Hover over a gate to see its name.")
    tk.Label(info_frame, textvariable=tip_var, bg="#F0F4F8",
             font=("Courier", 9), fg="gray").pack(anchor="w", padx=10)

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

    # Dibujamos el estado inicial (que son los Night Gates)
    on_slider_move(0)


def check_active_runways(time_str=None):
    import datetime
    global CURRENT_WIND_DIR, CURRENT_WIND_SPEED

    if time_str is None:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")

    h, m, s = map(int, time_str.split(':'))

    # 1. Leer datos meteorológicos del sistema de forma directa
    wind_dir = CURRENT_WIND_DIR
    wind_speed = CURRENT_WIND_SPEED

    # 2. Evaluar si es de día o de noche (De las 23h a las 5:30h)
    is_night = False
    if h < 5 or (h == 5 and m <= 30) or h == 23:
        is_night = True

    # 3. Aplicar las reglas de El Prat
    explicacion = "Standard conditions. No exceptions applied."

    if is_night:
        # Excepción Nocturna: Viento entre 150 y 330 + velocidad > 18.5 km/h
        if 150 <= wind_dir <= 330 and wind_speed > 18.5:
            arr_rw = "02"
            dep_rw = "24L"
            mode = "Nighttime configuration (ATYPICAL) 🌙💨"
            explicacion = "⚠️ Configuration change: Strong crosswind/tailwind."
        else:
            arr_rw = "02"
            dep_rw = "06R"
            mode = "Standard nighttime configuration 🌙"
    else:
        # Excepción Diurna: Viento entre 330 y 150 (componente Norte/Este) + velocidad > 18.5
        if (wind_dir >= 330 or wind_dir <= 150) and wind_speed > 18.5:
            arr_rw = "06L"
            dep_rw = "06R"
            mode = "East daytime configuration (ATYPICAL) ☀️💨"
            explicacion = "⚠️ East configuration change: Strong wind coming from North/East."
        else:
            arr_rw = "24R"
            dep_rw = "24L"
            mode = "West daytime configuration (NORMAL) ☀️"

    # 4. Mostrar en pantalla
    lines = [
        f"  Time: {time_str}",
        f"  🧭 Local METAR: Wind {wind_dir}º at {wind_speed} km/h",
        f"  Operative mode: {mode}",
        f"  {explicacion}",
        "",
        f"  🛬 Landing Runway:  {arr_rw}",
        f"  🛫 Takeoff Runway:    {dep_rw}"
    ]

    show_info_label("Active Runways Configuration", lines)

def assign_sids_to_departures():
    if len(departures) == 0:
        messagebox.showerror("Error", "Please, upload the Departures file first.")
        return

    # Creamos una ventana limpia para elegir la configuración activa
    win = tk.Toplevel(root)
    win.title("Assign SID Routes")
    win.geometry("320x150")
    win.configure(bg="#F0F4F8")
    win.resizable(False, False)

    tk.Label(win, text="¿Which Runway Configuration is active now?",
             bg="#F0F4F8", font=("Helvetica", 10, "bold"), fg="#34495E").pack(pady=(20, 15))

    def aplicar_sids(pista):
        win.destroy()
        assigned_sid = 0
        assigned_dct = 0

        # 1. Asignamos a la lista de salidas normal
        for ac in departures:
            destino = ac.destination
            sid_asignada = DESTINATION_SIDS[pista].get(destino, "")

            if sid_asignada != "":
                ac.sid = sid_asignada
                assigned_sid += 1
            else:
                ac.sid = "DCT"
                assigned_dct += 1

        # 2. Asignamos también a la lista unificada (merged) si ya existe
        if 'merged' in globals() and len(merged) > 0:
            for ac in merged:
                if ac.destination:
                    sid_asignada = DESTINATION_SIDS[pista].get(ac.destination, "")
                    ac.sid = sid_asignada if sid_asignada != "" else "DCT"

        # Activamos la variable de control para que el validador sepa que están puestas
        global sids_assigned
        sids_assigned = True

        # Actualizamos la lista visual (Listbox) para que muestre las SIDs
        departures_listbox.delete(0, tk.END)
        for ac in departures:
            sid_text = getattr(ac, 'sid', 'DCT')
            departures_listbox.insert(tk.END,
                f"  {ac.timedeparture:<6} {ac.destination:<6} SID: {sid_text:<8} {ac.company}")

        update_status()
        messagebox.showinfo("Assignation Completed",
            f"Runway Configuration: {pista}\n\n✅ Flights with a Standard Instrumental Departure (SID): {assigned_sid}\n ✈️ Flights with a Direct Departure (DCT): {assigned_dct}")

    # Botones para elegir pista
    btn_frame = tk.Frame(win, bg="#F0F4F8")
    btn_frame.pack()
    tk.Button(btn_frame, text="WEST (24L)", command=lambda: aplicar_sids("24L"),
              bg="#3A7FC1", fg="white", relief="flat", width=12, font=("Helvetica", 9, "bold")).pack(side="left", padx=10)
    tk.Button(btn_frame, text="EAST (06R)", command=lambda: aplicar_sids("06R"),
              bg="#D9704A", fg="white", relief="flat", width=12, font=("Helvetica", 9, "bold")).pack(side="left", padx=10)


def view_aircraft_departure():
    if len(departures) == 0:
        messagebox.showerror("Error", "Please load departures first.")
        return

    # Preguntamos por el aeropuerto de destino
    apt_input = sd.askstring("View Departure", "Enter Destination Airport (ICAO, e.g. LEMD):")
    if not apt_input:
        return
    apt_input = apt_input.strip().upper()

    # Buscamos el primer avión que vaya a ese destino
    target_flight = None
    for ac in departures:
        dest = getattr(ac, 'destination', getattr(ac, 'dest', '')).strip().upper()
        if dest == apt_input:
            target_flight = ac
            break

    if not target_flight:
        messagebox.showerror("Not Found", f"No departure found heading to {apt_input}.")
        return

    # Extraemos datos
    sid = getattr(target_flight, 'sid', '---')
    if sid == '---':
        messagebox.showerror("No SID", f"Flight to {apt_input} has no SID assigned. Please run 'Assign SIDs' first.")
        return

    reg = getattr(target_flight, 'registration', getattr(target_flight, 'aircraft', 'FLIGHT'))
    aerolinea = getattr(target_flight, 'company', getattr(target_flight, 'airline', '???'))

    rwy = "24L"
    if sid != "DCT":
        for r, sids in SIDS_DATA.items():
            if sid in sids:
                rwy = r
                break

    clear_info_panel()

    tk.Label(info_frame, text=f"Departure Radar: {reg} ({aerolinea}) to {apt_input} | SID: {sid}",
             bg="#F0F4F8", font=("Helvetica", 11, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 2))

    canvas_frame = tk.Frame(info_frame, bg="#F0F4F8")
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    canvas = tk.Canvas(canvas_frame, bg=COLOR_MAR, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def init_and_draw():
        canvas.update_idletasks()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1: w, h = 800, 600

        draw_radar_base(canvas, w, h, pista_seleccionada=rwy if sid != "DCT" else None)
        start_animation(w, h)

    anim_job = None

    def start_animation(w, h):
        nonlocal anim_job
        dot_id = canvas.create_oval(-8, -8, -8, -8, fill="white", outline="#2980B9", width=2, tags="overlay")
        text_id = canvas.create_text(-20, -20, text=reg, fill="white", font=("Courier", 10, "bold"), anchor="w",
                                     tags="overlay")

        if sid == "DCT":
            cx, cy = get_radar_xy(41.29, 2.07, w, h)
            max_radius = max(w, h) * 1.5
            current_radius = 5

            canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#E74C3C", outline="white", tags="overlay")
            canvas.create_text(cx + 12, cy - 10, text="LEBL (DCT)", fill="white", font=("Courier", 10, "bold"),
                               anchor="w", tags="overlay")
            circle_id = canvas.create_oval(cx - current_radius, cy - current_radius, cx + current_radius,
                                           cy + current_radius, outline="#F1C40F", width=2, dash=(6, 4), tags="overlay")

            def animate_dct():
                nonlocal current_radius, anim_job
                if not canvas.winfo_exists(): return
                if current_radius < max_radius:
                    current_radius += 6
                    canvas.coords(circle_id, cx - current_radius, cy - current_radius, cx + current_radius,
                                  cy + current_radius)
                    canvas.coords(dot_id, cx + current_radius - 6, cy - 6, cx + current_radius + 6, cy + 6)
                    canvas.coords(text_id, cx + current_radius + 12, cy)
                    anim_job = root.after(30, animate_dct)
                else:
                    canvas.delete(circle_id)

            animate_dct()
            return

        ruta = SIDS_DATA[rwy][sid]
        puntos_pantalla = []
        for nombre, lat, lon in ruta:
            x, y = get_radar_xy(lat, lon, w, h)
            puntos_pantalla.append((x, y, nombre))

        for i in range(len(puntos_pantalla)):
            px, py, pnombre = puntos_pantalla[i]
            if i > 0:
                ax, ay, _ = puntos_pantalla[i - 1]
                canvas.create_line(ax, ay, px, py, fill="#F1C40F", width=2, tags="overlay")

            if i == 0:
                canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill="#E74C3C", outline="white", tags="overlay")
            else:
                canvas.create_polygon(px, py - 4, px - 4, py + 4, px + 4, py + 4, fill="#3498DB", outline="#2980B9",
                                      tags="overlay")
                canvas.create_text(px + 8, py, text=pnombre, fill="#BDC3C7", font=("Courier", 9), anchor="w",
                                   tags="overlay")

        anim_path = []
        pasos_por_tramo = 30
        for i in range(len(puntos_pantalla) - 1):
            x1, y1, _ = puntos_pantalla[i]
            x2, y2, _ = puntos_pantalla[i + 1]
            for step in range(pasos_por_tramo):
                nx = x1 + (x2 - x1) * (step / pasos_por_tramo)
                ny = y1 + (y2 - y1) * (step / pasos_por_tramo)
                anim_path.append((nx, ny))
        anim_path.append((puntos_pantalla[-1][0], puntos_pantalla[-1][1]))

        frame = 0

        def animate():
            nonlocal frame, anim_job
            if not canvas.winfo_exists(): return
            if frame < len(anim_path):
                cx, cy = anim_path[frame]
                canvas.coords(dot_id, cx - 6, cy - 6, cx + 6, cy + 6)
                canvas.coords(text_id, cx + 12, cy)
                frame += 1
                anim_job = root.after(40, animate)

        animate()

    root.after(50, init_and_draw)


import tkinter.simpledialog as sd
from tkinter import messagebox

def assign_stars_to_arrivals():
    if 'aircrafts' not in globals() or len(aircrafts) == 0:
        messagebox.showerror("Error", "Please load arrivals first.")
        return

    # Creamos ventana para elegir la pista activa de llegadas
    win = tk.Toplevel(root)
    win.title("Assign STARs")
    win.geometry("350x150")
    win.configure(bg="#F0F4F8")
    win.resizable(False, False)

    tk.Label(win, text="Select active Arrival Runway (LEBL):",
             bg="#F0F4F8", font=("Helvetica", 10, "bold"), fg="#34495E").pack(pady=(20, 15))

    def aplicar_stars(pista):
        win.destroy()
        assigned_star = 0
        assigned_dct = 0

        lines = []
        # 1. Asignamos a la lista original de llegadas
        for ac in aircrafts:
            origen = getattr(ac, 'origin', '')
            star_asignada = ORIGIN_STARS[pista].get(origen, "DCT")
            ac.star = star_asignada

            if star_asignada != "DCT":
                assigned_star += 1
            else:
                assigned_dct += 1

            timelanding = getattr(ac, 'timelanding', '00:00')
            company = getattr(ac, 'company', '')
            lines.append(f"  {timelanding:<6} {origen:<6} STAR: {star_asignada:<8} {company}")

        # 2. Asignamos también a la lista unificada (merged) si ya existe
        if 'merged' in globals() and len(merged) > 0:
            for ac in merged:
                if ac.origin:
                    ac.star = ORIGIN_STARS[pista].get(ac.origin, "DCT")

        # Activamos la variable de control para que el validador sepa que están puestas
        global stars_assigned
        stars_assigned = True

        # Actualizamos la interfaz principal
        show_info_label(f"Arrivals Config: {pista}", lines)

        messagebox.showinfo("Assignment Complete",
                            f"Runway {pista} Active\n\n✅ Flights with STAR: {assigned_star}\n✈️ Flights with Vectoring (DCT): {assigned_dct}")

    # Botones para elegir configuración de aterrizaje
    btn_frame = tk.Frame(win, bg="#F0F4F8")
    btn_frame.pack()
    tk.Button(btn_frame, text="24R (West)", command=lambda: aplicar_stars("24R"),
              bg="#8E44AD", fg="white", relief="flat", width=10, font=("Helvetica", 9, "bold")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="06L (East)", command=lambda: aplicar_stars("06L"),
              bg="#2980B9", fg="white", relief="flat", width=10, font=("Helvetica", 9, "bold")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="02 (North)", command=lambda: aplicar_stars("02"),
              bg="#27AE60", fg="white", relief="flat", width=10, font=("Helvetica", 9, "bold")).pack(side="left", padx=5)


import math
import tkinter.simpledialog as sd
from tkinter import messagebox

def view_aircraft_arrival():
    # 1. Comprobar que hay aviones cargados
    if 'aircrafts' not in globals() or len(aircrafts) == 0:
        messagebox.showerror("Error", "Please load arrivals first.")
        return

    # 2. Preguntar el origen
    apt_input = sd.askstring("View Arrival", "Enter Origin Airport (ICAO, e.g. LEMD):")
    if not apt_input:
        return
    apt_input = apt_input.strip().upper()

    # 3. Buscar el avión
    target_flight = None
    for ac in aircrafts:
        orig = getattr(ac, 'origin', '').strip().upper()
        if orig == apt_input:
            target_flight = ac
            break

    if not target_flight:
        messagebox.showerror("Not Found", f"No arrival found coming from {apt_input}.")
        return

    # Extraer atributos
    star = getattr(target_flight, 'star', 'DCT')
    aerolinea = getattr(target_flight, 'company', '???')
    reg = getattr(target_flight, 'id', 'FLIGHT')

    # Averiguar a qué pista corresponde la STAR
    rwy = "24R"
    if star != "DCT" and star != "":
        if 'STARS_DATA' in globals():
            for r, stars in STARS_DATA.items():
                if star in stars:
                    rwy = r
                    break

    # 4. Limpiar el panel derecho (info_frame)
    for widget in info_frame.winfo_children():
        widget.destroy()

    # Interfaz superior
    tk.Label(info_frame, text=f"Arrival Radar: {reg} ({aerolinea}) from {apt_input} | STAR: {star}",
             bg="#F0F4F8", font=("Helvetica", 11, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 2))

    canvas_frame = tk.Frame(info_frame, bg="#F0F4F8")
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    canvas = tk.Canvas(canvas_frame, bg="#08182B", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_and_animate():
        canvas.update_idletasks()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1: w, h = 800, 600

        # --- 1. DIBUJAR MAPA BASE ---
        if 'draw_radar_base' in globals():
            draw_radar_base(canvas, w, h)
            
        cx_dest, cy_dest = get_radar_xy(41.29, 2.07, w, h)

        # --- 1.1 DIBUJAR STARs EN SEGUNDO PLANO ---
        if 'STARS_DATA' in globals() and rwy in STARS_DATA:
            for star_name, ruta_bg in STARS_DATA[rwy].items():
                if star_name != star:
                    for i in range(len(ruta_bg) - 1):
                        x1, y1 = get_radar_xy(ruta_bg[i][1], ruta_bg[i][2], w, h)
                        x2, y2 = get_radar_xy(ruta_bg[i+1][1], ruta_bg[i+1][2], w, h)
                        # Línea fina en el mismo color que usas para fronteras (#5D8AA8)
                        canvas.create_line(x1, y1, x2, y2, fill="#5D8AA8", width=1, tags="overlay")

                    # Unir el último punto de la ruta en segundo plano con el aeropuerto
                    x_last, y_last = get_radar_xy(ruta_bg[-1][1], ruta_bg[-1][2], w, h)
                    canvas.create_line(x_last, y_last, cx_dest, cy_dest, fill="#5D8AA8", width=1, tags="overlay")

        # Dibujar LEBL fijo
        canvas.create_oval(cx_dest-5, cy_dest-5, cx_dest+5, cy_dest+5, fill="#E74C3C", outline="white", tags="overlay")
        canvas.create_text(cx_dest+12, cy_dest-10, text="LEBL", fill="white", font=("Courier", 10, "bold"), anchor="w", tags="overlay")

        # --- 2. LÓGICA VECTORES (8 RECTAS CONVERGENTES) ---
        if star == "DCT" or star == "":
            radius = max(w, h)
            puntos_animacion = []

            for i in range(8):
                angulo = math.radians(i * 45)
                ex = cx_dest + radius * math.cos(angulo)
                ey = cy_dest + radius * math.sin(angulo)

                canvas.create_line(cx_dest, cy_dest, ex, ey, fill="#E67E22", dash=(2, 4), width=1, tags="overlay")
                dot = canvas.create_oval(ex-5, ey-5, ex+5, ey+5, fill="white", outline="#E67E22", width=2, tags="overlay")
                puntos_animacion.append((dot, ex, ey))

            total_frames = 100
            frame = 0

            def animate_convergence():
                nonlocal frame
                if not canvas.winfo_exists(): return
                if frame <= total_frames:
                    progress = frame / total_frames
                    for dot, ex, ey in puntos_animacion:
                        current_x = ex + (cx_dest - ex) * progress
                        current_y = ey + (cy_dest - ey) * progress
                        canvas.coords(dot, current_x-4, current_y-4, current_x+4, current_y+4)

                    frame += 1
                    canvas.after(40, animate_convergence)
                else:
                    for dot, _, _ in puntos_animacion:
                        canvas.itemconfig(dot, fill="#E74C3C", outline="#E74C3C")

            animate_convergence()

        # --- 3. LÓGICA STAR NORMAL (RUTA FIJA) ---
        else:
            if 'STARS_DATA' in globals() and rwy in STARS_DATA and star in STARS_DATA[rwy]:
                ruta = STARS_DATA[rwy][star]
                path_points = []

                # Extraer puntos y dibujar la ruta
                for nombre, lat, lon in ruta:
                    px, py = get_radar_xy(lat, lon, w, h)
                    path_points.append((px, py))

                    if len(path_points) > 1:
                        ax, ay = path_points[-2]
                        canvas.create_line(ax, ay, px, py, fill="#E67E22", width=2, tags="overlay")

                    # Nombres de los waypoints (sin caja oscura)
                    if nombre != ruta[-1][0]:
                        canvas.create_polygon(px, py-4, px-4, py+4, px+4, py+4, fill="#D35400", outline="#E67E22", tags="overlay")
                        canvas.create_text(px+10, py, text=nombre, fill="#F39C12", font=("Courier", 9, "bold"), anchor="w", tags="overlay")

                # UNIR EL FINAL DE LA STAR CON EL CENTRO DEL AEROPUERTO
                ax, ay = path_points[-1]
                canvas.create_line(ax, ay, cx_dest, cy_dest, fill="#E67E22", width=2, tags="overlay")
                path_points.append((cx_dest, cy_dest))

                # Crear el avión, el RECTÁNGULO DE FONDO y la matrícula
                dot_id = canvas.create_oval(-8, -8, -8, -8, fill="white", outline="#E67E22", width=2, tags="overlay")
                bg_id = canvas.create_rectangle(-20, -20, -20, -20, fill="#08182B", outline="#E67E22", width=1, tags="overlay")
                text_id = canvas.create_text(-20, -20, text=reg, fill="white", font=("Courier", 10, "bold"), anchor="w", tags="overlay")

                # Preparar los saltos de la animación
                anim_path = []
                pasos_por_tramo = 30
                for i in range(len(path_points) - 1):
                    x1, y1 = path_points[i]
                    x2, y2 = path_points[i+1]
                    for step in range(pasos_por_tramo):
                        nx = x1 + (x2 - x1) * (step / pasos_por_tramo)
                        ny = y1 + (y2 - y1) * (step / pasos_por_tramo)
                        anim_path.append((nx, ny))
                anim_path.append(path_points[-1])

                frame = 0
                def animate_star():
                    nonlocal frame
                    if not canvas.winfo_exists(): return
                    if frame < len(anim_path):
                        cx, cy = anim_path[frame]

                        # Mover avión
                        canvas.coords(dot_id, cx-6, cy-6, cx+6, cy+6)

                        # Coordenadas base para el texto a la derecha
                        tx, ty = cx + 12, cy

                        # Mover fondo de la matrícula
                        canvas.coords(bg_id, tx-3, ty-8, tx+55, ty+8)
                        # Mover texto
                        canvas.coords(text_id, tx, ty)

                        frame += 1
                        canvas.after(40, animate_star)
                    else:
                        canvas.itemconfig(dot_id, fill="#E74C3C", outline="#E74C3C")
                        canvas.delete(bg_id)
                        canvas.itemconfig(text_id, fill="#E74C3C")

                animate_star()
            else:
                messagebox.showwarning("STAR Missing", f"Data for STAR {star} not found in STARS_DATA.")

    canvas.after(100, draw_and_animate)


def view_airport_map():
    # 1. Limpiar el panel derecho
    for widget in info_frame.winfo_children():
        widget.destroy()

    # 2. Título de la sección
    tk.Label(info_frame, text="LEBL - Barcelona El Prat | Schematic Map",
             bg="#F0F4F8", font=("Helvetica", 14, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 2))

    # 3. Marco y Canvas
    canvas_frame = tk.Frame(info_frame, bg="#F0F4F8")
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    # Usamos el mismo color de fondo del radar para mantener la cohesión visual
    canvas = tk.Canvas(canvas_frame, bg="#08182B", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_map():
        canvas.update_idletasks()
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 1: w, h = 800, 600

        color_rwy = "#5D6D7E"  # Gris asfalto
        color_line = "#FFFFFF"  # Blanco para marcas viales

        # --- COORDENADAS DE LAS PISTAS ---
        # 06L / 24R (Norte, más cerca de la T2)
        rwy1_y = h * 0.35
        rwy1_x1 = w * 0.30
        rwy1_x2 = w * 0.90

        # 06R / 24L (Sur, más cerca del mar)
        rwy2_y = h * 0.65
        rwy2_x1 = w * 0.20
        rwy2_x2 = w * 0.80

        # 02 / 20 (Diagonal, cruzando las horizontales)
        rwy3_x1 = w * 0.35
        rwy3_y1 = h * 0.85
        rwy3_x2 = w * 0.85
        rwy3_y2 = h * 0.15

        # --- DIBUJAR PISTAS (Fondo Gris Ancho) ---
        canvas.create_line(rwy1_x1, rwy1_y, rwy1_x2, rwy1_y, fill=color_rwy, width=35, capstyle=tk.ROUND)
        canvas.create_line(rwy2_x1, rwy2_y, rwy2_x2, rwy2_y, fill=color_rwy, width=35, capstyle=tk.ROUND)
        canvas.create_line(rwy3_x1, rwy3_y1, rwy3_x2, rwy3_y2, fill=color_rwy, width=35, capstyle=tk.ROUND)

        # --- DIBUJAR LÍNEAS CENTRALES (Punteadas) ---
        canvas.create_line(rwy1_x1, rwy1_y, rwy1_x2, rwy1_y, fill=color_line, width=2, dash=(12, 12))
        canvas.create_line(rwy2_x1, rwy2_y, rwy2_x2, rwy2_y, fill=color_line, width=2, dash=(12, 12))
        canvas.create_line(rwy3_x1, rwy3_y1, rwy3_x2, rwy3_y2, fill=color_line, width=2, dash=(12, 12))

        # --- TEXTOS DE CABECERAS (Identificadores) ---
        font_rwy = ("Helvetica", 11, "bold")
        canvas.create_text(rwy1_x1 - 35, rwy1_y, text="06L", fill="white", font=font_rwy)
        canvas.create_text(rwy1_x2 + 35, rwy1_y, text="24R", fill="white", font=font_rwy)

        canvas.create_text(rwy2_x1 - 35, rwy2_y, text="06R", fill="white", font=font_rwy)
        canvas.create_text(rwy2_x2 + 35, rwy2_y, text="24L", fill="white", font=font_rwy)

        canvas.create_text(rwy3_x1 - 20, rwy3_y1 + 25, text="02", fill="white", font=font_rwy)
        canvas.create_text(rwy3_x2 + 20, rwy3_y2 - 25, text="20", fill="white", font=font_rwy)

        # --- TERMINAL 1 (Izquierda) ---
        # Representación en forma de "Espada" característica de la T1
        cx_t1, cy_t1 = w * 0.15, h * 0.50
        canvas.create_polygon(
            cx_t1, cy_t1 - 70,  # Punta superior
                   cx_t1 + 40, cy_t1 - 10,  # Brazo derecho alto
                   cx_t1 + 10, cy_t1 + 70,  # Brazo derecho bajo
                   cx_t1 - 10, cy_t1 + 70,  # Brazo izquierdo bajo
                   cx_t1 - 40, cy_t1 - 10,  # Brazo izquierdo alto
            fill="#2980B9", outline="#5DADE2", width=2
        )
        # Texto rotado para encajar en la forma vertical
        canvas.create_text(cx_t1, cy_t1, text="TERMINAL 1", fill="white", font=("Helvetica", 11, "bold"), angle=90)

        # --- TERMINAL 2 (Arriba) ---
        # Representación rectangular clásica (Bloques A, B, C)
        cx_t2, cy_t2 = w * 0.65, h * 0.10
        canvas.create_rectangle(cx_t2 - 120, cy_t2 - 20, cx_t2 + 120, cy_t2 + 20, fill="#8E44AD", outline="#BB8FCE",
                                width=2)
        canvas.create_text(cx_t2, cy_t2, text="TERMINAL 2", fill="white", font=("Helvetica", 11, "bold"))

    # Dar tiempo a que el Canvas se dimensione antes de dibujar
    root.after(100, draw_map)


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


def view_ground_movements():
    # 1. Comprobar que hay aviones fusionados
    if 'merged' not in globals() or len(merged) == 0:
        messagebox.showerror("Error", "Please load arrivals/departures and run Merge Movements first.")
        return

    # 2. Pedir la matrícula
    reg_input = sd.askstring("Ground Radar", "Enter Aircraft ID for Taxiing (e.g. VLG123):")
    if not reg_input:
        return
    reg_input = reg_input.strip().upper()

    # 3. Buscar el avión
    target_flight = None
    for ac in merged:
        if ac.id.upper() == reg_input:
            target_flight = ac
            break

    if not target_flight:
        messagebox.showerror("Not Found", f"No merged flight found with ID {reg_input}.")
        return

    # 4. Determinar datos de rodaje
    company = getattr(target_flight, 'company', '???')
    orig = getattr(target_flight, 'origin', '')
    dest = getattr(target_flight, 'destination', '')

    # Averiguar Terminal
    terminal_dest = "T1"
    if company in ["RYR", "EZY", "WZZ", "TRA", "NOR"]:
        terminal_dest = "T2"

    # 5. Limpiar panel derecho
    for widget in info_frame.winfo_children():
        widget.destroy()

    tk.Label(info_frame, text=f"Ground Control: {target_flight.id} ({company}) | {terminal_dest}",
             bg="#F0F4F8", font=("Helvetica", 12, "bold"), fg="#1A1A1A").pack(anchor="w", padx=10, pady=(10, 2))

    canvas_frame = tk.Frame(info_frame, bg="#F0F4F8")
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    canvas = tk.Canvas(canvas_frame, bg="#08182B", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_and_animate():
        canvas.update_idletasks()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1: w, h = 800, 600

        # --- DIBUJAR MAPA BASE DEL AEROPUERTO (Limpio) ---
        color_rwy = "#5D6D7E"  # Gris pista
        color_line = "#FFFFFF"  # Blanco marcas

        # Coordenadas principales de Pistas
        r1_y = h * 0.35
        r1_start, r1_end = w * 0.90, w * 0.30  # 24R (Llegadas)

        r2_y = h * 0.65
        r2_start, r2_end = w * 0.80, w * 0.20  # 24L (Salidas)

        # Coordenadas lógicas invisibles para que el avión ruede en paralelo
        twy_n_y = h * 0.22  # Rodaje paralelo Norte (para ir a la T2)
        twy_c_y = h * 0.45  # Rodaje paralelo Central (para ir a la T1 desde llegadas)
        twy_s_y = h * 0.55  # Rodaje paralelo Sur (para ir a la 24L a despegar)

        # Coordenadas de Terminales
        cx_t1, cy_t1 = w * 0.15, h * 0.50
        cx_t2, cy_t2 = w * 0.65, h * 0.10

        # 1. Dibujar Pistas (Sin calles de rodaje)
        canvas.create_line(w * 0.35, h * 0.85, w * 0.55, h * 0.15, fill=color_rwy, width=35, capstyle=tk.ROUND)  # 02/20
        canvas.create_line(r1_start, r1_y, r1_end, r1_y, fill=color_rwy, width=35, capstyle=tk.ROUND)  # 24R
        canvas.create_line(r2_start, r2_y, r2_end, r2_y, fill=color_rwy, width=35, capstyle=tk.ROUND)  # 24L

        # Marcas Pistas
        canvas.create_line(r1_start, r1_y, r1_end, r1_y, fill=color_line, width=2, dash=(12, 12))
        canvas.create_line(r2_start, r2_y, r2_end, r2_y, fill=color_line, width=2, dash=(12, 12))

        # 2. Dibujar Terminales
        canvas.create_polygon(cx_t1, cy_t1 - 70, cx_t1 + 40, cy_t1 - 20, cx_t1 + 20, cy_t1 + 70, cx_t1 - 20, cy_t1 + 70,
                              cx_t1 - 40, cy_t1 - 20, fill="#2980B9", outline="#5DADE2", width=2)
        canvas.create_text(cx_t1, cy_t1, text="T1", fill="white", font=("Helvetica", 14, "bold"))

        canvas.create_rectangle(cx_t2 - 120, cy_t2 - 20, cx_t2 + 120, cy_t2 + 20, fill="#8E44AD", outline="#BB8FCE",
                                width=2)
        canvas.create_text(cx_t2, cy_t2, text="T2", fill="white", font=("Helvetica", 14, "bold"))

        # --- MOTOR DE ANIMACIÓN ---
        def add_segment(start_pt, end_pt, steps):
            return [(start_pt[0] + (end_pt[0] - start_pt[0]) * (i / steps),
                     start_pt[1] + (end_pt[1] - start_pt[1]) * (i / steps)) for i in range(steps)]

        anim_path = []

        # FASE 1: LLEGADA Y RODAJE
        if orig:
            # Aterrizaje en 24R
            anim_path += add_segment((r1_start, r1_y), (r1_end, r1_y), 40)

            if terminal_dest == "T1":
                # Salir de pista y rodar en paralelo por el centro
                anim_path += add_segment((r1_end, r1_y), (r1_end, twy_c_y), 15)
                anim_path += add_segment((r1_end, twy_c_y), (cx_t1, twy_c_y), 30)
                anim_path += add_segment((cx_t1, twy_c_y), (cx_t1, cy_t1), 15)
                anim_path += [(cx_t1, cy_t1)] * 40  # Escala
            else:  # T2
                # Salir de pista y rodar en paralelo por el norte
                anim_path += add_segment((r1_end, r1_y), (r1_end, twy_n_y), 15)
                anim_path += add_segment((r1_end, twy_n_y), (cx_t2, twy_n_y), 40)
                anim_path += add_segment((cx_t2, twy_n_y), (cx_t2, cy_t2), 15)
                anim_path += [(cx_t2, cy_t2)] * 40  # Escala

        # PAUSA INICIAL SI ES SOLO SALIDA
        if dest and not orig:
            if terminal_dest == "T1":
                anim_path += [(cx_t1, cy_t1)] * 20
            else:
                anim_path += [(cx_t2, cy_t2)] * 20

        # FASE 2: RODAJE Y DESPEGUE
        if dest:
            if terminal_dest == "T1":
                # Pushback y rodar en paralelo a la 24L por el sur
                anim_path += add_segment((cx_t1, cy_t1), (cx_t1, twy_s_y), 15)
                anim_path += add_segment((cx_t1, twy_s_y), (r2_start, twy_s_y), 50)
            else:
                # Pushback desde T2 y rodar en paralelo a la 24L por el sur
                anim_path += add_segment((cx_t2, cy_t2), (cx_t2, twy_s_y), 30)
                anim_path += add_segment((cx_t2, twy_s_y), (r2_start, twy_s_y), 30)

            # Entrar a Pista 24L
            anim_path += add_segment((r2_start, twy_s_y), (r2_start, r2_y), 10)
            anim_path += [(r2_start, r2_y)] * 15  # Holding point (esperar permiso)

            # Acelerar y Despegar
            anim_path += add_segment((r2_start, r2_y), (r2_end, r2_y), 40)

        # --- DIBUJAR AVIÓN ---
        dot_id = canvas.create_oval(-8, -8, -8, -8, fill="#F39C12", outline="white", width=2, tags="plane")
        text_id = canvas.create_text(-20, -20, text=target_flight.id, fill="#F39C12", font=("Courier", 10, "bold"),
                                     anchor="w", tags="plane")

        frame = 0

        def animate():
            nonlocal frame
            if not canvas.winfo_exists(): return
            if frame < len(anim_path):
                cx, cy = anim_path[frame]
                canvas.coords(dot_id, cx - 6, cy - 6, cx + 6, cy + 6)
                canvas.coords(text_id, cx + 10, cy)

                # Efecto visual: Naranja llegando, Amarillo saliendo
                if frame < (len(anim_path) // 2) and orig and dest:
                    canvas.itemconfig(dot_id, outline="#E67E22", fill="#D35400")
                elif dest:
                    canvas.itemconfig(dot_id, outline="#F1C40F", fill="#F39C12")

                frame += 1
                canvas.after(40, animate)
            else:
                canvas.itemconfig(dot_id, fill="#E74C3C", outline="#E74C3C")
                canvas.itemconfig(text_id, fill="#E74C3C")

        animate()

    root.after(100, draw_and_animate)


def view_merged_flight():
    # 1. Comprobar que hemos asignado SIDs y STARs
    if 'merged' not in globals() or len(merged) == 0:
        messagebox.showerror("Error", "Please load arrivals/departures and run Merge Movements first.")
        return

    # 2. Pedir la matrícula
    reg_input = sd.askstring("Merged Flight", "Enter Aircraft Registration (ID, e.g. VLG123):")
    if not reg_input:
        return
    reg_input = reg_input.strip().upper()

    # 3. Buscar el avión en la lista merged
    target_flight = None
    for ac in merged:
        if ac.id.upper() == reg_input:
            target_flight = ac
            break

    if not target_flight:
        messagebox.showerror("Not Found", f"No merged flight found with ID {reg_input}.")
        return

    # 4. Extraer datos del ciclo completo
    orig = getattr(target_flight, 'origin', '')
    dest = getattr(target_flight, 'destination', '')
    star = getattr(target_flight, 'star', 'DCT')
    sid = getattr(target_flight, 'sid', 'DCT')
    company = getattr(target_flight, 'company', '???')
    reg = target_flight.id

    if not orig and not dest:
        messagebox.showwarning("Incomplete Data", "This flight has neither origin nor destination.")
        return

    # 5. Averiguar Terminal y PUERTA ASIGNADA
    assigned_gate = getattr(target_flight, 'gate', '---')
    terminal_dest = "T1"

    if hasattr(target_flight, 'terminal'):
        terminal_dest = target_flight.terminal
    elif company in ["RYR", "EZY", "WZZ", "TRA", "NOR"]:
        terminal_dest = "T2"

    # Averiguar Pistas asignadas
    arr_rwy = "24R"
    if star != "DCT" and star != "" and 'STARS_DATA' in globals():
        for r, stars in STARS_DATA.items():
            if star in stars: arr_rwy = r

    dep_rwy = "24L"
    if sid != "DCT" and sid != "" and 'SIDS_DATA' in globals():
        for r, sids in SIDS_DATA.items():
            if sid in sids: dep_rwy = r

    # 6. Configurar panel derecho
    for widget in info_frame.winfo_children():
        widget.destroy()

    title_text = f"Full Flight Cycle: {reg} ({company}) | {orig} -> LEBL ({terminal_dest} - Gate {assigned_gate}) -> {dest}"
    tk.Label(info_frame, text=title_text, bg="#F0F4F8", font=("Helvetica", 10, "bold"), fg="#1A1A1A").pack(anchor="w",
                                                                                                           padx=10,
                                                                                                           pady=(10, 2))
    tk.Label(info_frame, text=f"STAR: {star} (Rwy {arr_rwy}) | SID: {sid} (Rwy {dep_rwy})", bg="#F0F4F8",
             font=("Helvetica", 9), fg="#34495E").pack(anchor="w", padx=10, pady=(0, 5))

    canvas_frame = tk.Frame(info_frame, bg="#F0F4F8")
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    canvas = tk.Canvas(canvas_frame, bg="#08182B", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_and_animate():
        canvas.update_idletasks()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1: w, h = 800, 600

        cx_dest, cy_dest = get_radar_xy(41.29, 2.07, w, h)

        # ==========================================
        # FASE 3: SALIDA RADAR (SID)
        # ==========================================
        def phase3_departure():
            if not dest: return
            canvas.delete("all")
            if 'draw_radar_base' in globals(): draw_radar_base(canvas, w, h)

            anim_path = []
            if sid == "DCT" or sid == "":
                end_x, end_y = w * 0.1, h * 0.1
                canvas.create_line(cx_dest, cy_dest, end_x, end_y, fill="#F1C40F", dash=(2, 4), width=2, tags="overlay")
                for step in range(50):
                    anim_path.append(
                        (cx_dest + (end_x - cx_dest) * (step / 50), cy_dest + (end_y - cy_dest) * (step / 50)))
            elif 'SIDS_DATA' in globals() and dep_rwy in SIDS_DATA and sid in SIDS_DATA[dep_rwy]:
                ruta = SIDS_DATA[dep_rwy][sid]
                path_points = [(cx_dest, cy_dest)] + [get_radar_xy(lat, lon, w, h) for _, lat, lon in ruta]

                for i in range(len(path_points) - 1):
                    canvas.create_line(path_points[i][0], path_points[i][1], path_points[i + 1][0],
                                       path_points[i + 1][1], fill="#F1C40F", width=2, tags="overlay")

                for i, (nombre, lat, lon) in enumerate(ruta):
                    if "LEBL" not in nombre:
                        px, py = path_points[i + 1]
                        canvas.create_text(px + 10, py, text=nombre, fill="#F1C40F", font=("Courier", 8, "bold"),
                                           anchor="w", tags="overlay")

                pasos = 25
                for i in range(len(path_points) - 1):
                    x1, y1 = path_points[i]
                    x2, y2 = path_points[i + 1]
                    for s in range(pasos): anim_path.append(
                        (x1 + (x2 - x1) * (s / pasos), y1 + (y2 - y1) * (s / pasos)))

            canvas.create_oval(cx_dest - 5, cy_dest - 5, cx_dest + 5, cy_dest + 5, fill="#E74C3C", outline="white",
                               tags="overlay")
            canvas.create_text(cx_dest + 12, cy_dest - 10, text="LEBL", fill="white", font=("Courier", 10, "bold"),
                               anchor="w", tags="overlay")

            dot_id = canvas.create_oval(-8, -8, -8, -8, fill="white", outline="#F1C40F", width=2, tags="overlay")
            bg_id = canvas.create_rectangle(-20, -20, -20, -20, fill="#08182B", outline="#F1C40F", width=1,
                                            tags="overlay")
            text_id = canvas.create_text(-20, -20, text=reg, fill="white", font=("Courier", 10, "bold"), anchor="w",
                                         tags="overlay")

            frame = 0

            def animate():
                nonlocal frame
                if not canvas.winfo_exists(): return
                if frame < len(anim_path):
                    cx, cy = anim_path[frame]
                    canvas.coords(dot_id, cx - 6, cy - 6, cx + 6, cy + 6)
                    canvas.coords(bg_id, cx + 9, cy - 8, cx + 67, cy + 8)
                    canvas.coords(text_id, cx + 12, cy)
                    frame += 1
                    canvas.after(40, animate)
                else:
                    canvas.itemconfig(dot_id, fill="#E74C3C", outline="#E74C3C")
                    canvas.delete(bg_id)
                    canvas.itemconfig(text_id, fill="#E74C3C")

            animate()

        # ==========================================
        # FASE 2: MOVIMIENTOS EN TIERRA (TAXI DINÁMICO)
        # ==========================================
        def phase2_ground():
            canvas.delete("all")

            # Coordenadas lógicas del aeropuerto
            color_rwy = "#5D6D7E";
            color_line = "#FFFFFF"
            twy_n_y = h * 0.22;
            twy_c_y = h * 0.45;
            twy_s_y = h * 0.55
            cx_t1, cy_t1 = w * 0.15, h * 0.50
            cx_t2, cy_t2 = w * 0.65, h * 0.10

            # Dibujar pistas
            canvas.create_line(w * 0.35, h * 0.85, w * 0.55, h * 0.15, fill=color_rwy, width=35,
                               capstyle=tk.ROUND)  # 02/20
            canvas.create_line(w * 0.90, h * 0.35, w * 0.30, h * 0.35, fill=color_rwy, width=35,
                               capstyle=tk.ROUND)  # 24R/06L
            canvas.create_line(w * 0.80, h * 0.65, w * 0.20, h * 0.65, fill=color_rwy, width=35,
                               capstyle=tk.ROUND)  # 24L/06R

            canvas.create_line(w * 0.90, h * 0.35, w * 0.30, h * 0.35, fill=color_line, width=2, dash=(12, 12))
            canvas.create_line(w * 0.80, h * 0.65, w * 0.20, h * 0.65, fill=color_line, width=2, dash=(12, 12))

            # Letreros de pistas
            canvas.create_text(w * 0.90 + 20, h * 0.35, text="24R", fill="#BDC3C7", font=("Helvetica", 9, "bold"))
            canvas.create_text(w * 0.30 - 20, h * 0.35, text="06L", fill="#BDC3C7", font=("Helvetica", 9, "bold"))
            canvas.create_text(w * 0.80 + 20, h * 0.65, text="24L", fill="#BDC3C7", font=("Helvetica", 9, "bold"))
            canvas.create_text(w * 0.20 - 20, h * 0.65, text="06R", fill="#BDC3C7", font=("Helvetica", 9, "bold"))
            canvas.create_text(w * 0.35 - 15, h * 0.85 + 15, text="02", fill="#BDC3C7", font=("Helvetica", 9, "bold"))
            canvas.create_text(w * 0.55 + 15, h * 0.15 - 15, text="20", fill="#BDC3C7", font=("Helvetica", 9, "bold"))

            # Indicador de Configuración Activa
            canvas.create_text(w * 0.50, h * 0.05, text=f"ACTIVE RUNWAYS -> ARR: {arr_rwy} | DEP: {dep_rwy}",
                               fill="#2ECC71", font=("Courier", 11, "bold"))

            # --- LÓGICA DINÁMICA DE COORDENADAS ---
            # Llegadas
            if arr_rwy == "06L":
                arr_start_pt = (w * 0.30, h * 0.35);
                arr_end_pt = (w * 0.90, h * 0.35)
            elif arr_rwy == "02":
                arr_start_pt = (w * 0.35, h * 0.85);
                arr_end_pt = (w * 0.55, h * 0.15)
            else:  # Default 24R
                arr_start_pt = (w * 0.90, h * 0.35);
                arr_end_pt = (w * 0.30, h * 0.35)

            # Salidas
            if dep_rwy == "06R":
                dep_start_pt = (w * 0.20, h * 0.65);
                dep_end_pt = (w * 0.80, h * 0.65)
            elif dep_rwy == "02":
                dep_start_pt = (w * 0.35, h * 0.85);
                dep_end_pt = (w * 0.55, h * 0.15)
            else:  # Default 24L
                dep_start_pt = (w * 0.80, h * 0.65);
                dep_end_pt = (w * 0.20, h * 0.65)

            # Terminal 1
            canvas.create_polygon(cx_t1, cy_t1 - 70, cx_t1 + 40, cy_t1 - 20, cx_t1 + 20, cy_t1 + 70, cx_t1 - 20,
                                  cy_t1 + 70, cx_t1 - 40, cy_t1 - 20, fill="#2980B9", outline="#5DADE2", width=2)
            canvas.create_text(cx_t1, cy_t1, text="T1", fill="white", font=("Helvetica", 14, "bold"))

            # Terminal 2
            canvas.create_rectangle(cx_t2 - 120, cy_t2 - 20, cx_t2 + 120, cy_t2 + 20, fill="#8E44AD", outline="#BB8FCE",
                                    width=2)
            canvas.create_text(cx_t2, cy_t2, text="T2", fill="white", font=("Helvetica", 14, "bold"))

            # Mostrar la puerta de embarque
            if terminal_dest == "T1":
                canvas.create_text(cx_t1, cy_t1 + 30, text=f"Gate: {assigned_gate}", fill="#F1C40F",
                                   font=("Helvetica", 10, "bold"))
            else:
                canvas.create_text(cx_t2, cy_t2 + 30, text=f"Gate: {assigned_gate}", fill="#F1C40F",
                                   font=("Helvetica", 10, "bold"))

            def add_segment(start_pt, end_pt, steps):
                return [(start_pt[0] + (end_pt[0] - start_pt[0]) * (i / steps),
                         start_pt[1] + (end_pt[1] - start_pt[1]) * (i / steps)) for i in range(steps)]

            anim_path = []

            # Llegada a terminal
            if orig:
                anim_path += add_segment(arr_start_pt, arr_end_pt, 40)
                if terminal_dest == "T1":
                    anim_path += add_segment(arr_end_pt, (arr_end_pt[0], twy_c_y), 15)
                    anim_path += add_segment((arr_end_pt[0], twy_c_y), (cx_t1, twy_c_y), 30)
                    anim_path += add_segment((cx_t1, twy_c_y), (cx_t1, cy_t1), 15)
                    anim_path += [(cx_t1, cy_t1)] * 40
                else:
                    anim_path += add_segment(arr_end_pt, (arr_end_pt[0], twy_n_y), 15)
                    anim_path += add_segment((arr_end_pt[0], twy_n_y), (cx_t2, twy_n_y), 40)
                    anim_path += add_segment((cx_t2, twy_n_y), (cx_t2, cy_t2), 15)
                    anim_path += [(cx_t2, cy_t2)] * 40

            if dest and not orig:
                if terminal_dest == "T1":
                    anim_path += [(cx_t1, cy_t1)] * 20
                else:
                    anim_path += [(cx_t2, cy_t2)] * 20

            # Salida desde terminal
            if dest:
                if terminal_dest == "T1":
                    anim_path += add_segment((cx_t1, cy_t1), (cx_t1, twy_s_y), 15)
                    anim_path += add_segment((cx_t1, twy_s_y), (dep_start_pt[0], twy_s_y), 50)
                else:
                    anim_path += add_segment((cx_t2, cy_t2), (cx_t2, twy_s_y), 30)
                    anim_path += add_segment((cx_t2, twy_s_y), (dep_start_pt[0], twy_s_y), 30)

                anim_path += add_segment((dep_start_pt[0], twy_s_y), dep_start_pt, 10)
                anim_path += [dep_start_pt] * 15
                anim_path += add_segment(dep_start_pt, dep_end_pt, 40)

            dot_id = canvas.create_oval(-8, -8, -8, -8, fill="#F39C12", outline="white", width=2, tags="plane")
            text_id = canvas.create_text(-20, -20, text=reg, fill="#F39C12", font=("Courier", 10, "bold"), anchor="w",
                                         tags="plane")

            frame = 0

            def animate():
                nonlocal frame
                if not canvas.winfo_exists(): return
                if frame < len(anim_path):
                    cx, cy = anim_path[frame]
                    canvas.coords(dot_id, cx - 6, cy - 6, cx + 6, cy + 6)
                    canvas.coords(text_id, cx + 10, cy)
                    if frame < (len(anim_path) // 2) and orig and dest:
                        canvas.itemconfig(dot_id, outline="#E67E22", fill="#D35400")
                    elif dest:
                        canvas.itemconfig(dot_id, outline="#F1C40F", fill="#F39C12")
                    frame += 1
                    canvas.after(40, animate)
                else:
                    phase3_departure()

            animate()

        # ==========================================
        # FASE 1: LLEGADA RADAR (STAR)
        # ==========================================
        def phase1_arrival():
            if not orig:
                phase2_ground()
                return

            canvas.delete("all")
            if 'draw_radar_base' in globals(): draw_radar_base(canvas, w, h)

            anim_path = []
            if star == "DCT" or star == "":
                start_x, start_y = w * 0.9, h * 0.1
                canvas.create_line(start_x, start_y, cx_dest, cy_dest, fill="#E67E22", dash=(2, 4), width=2,
                                   tags="overlay")
                for step in range(50): anim_path.append(
                    (start_x + (cx_dest - start_x) * (step / 50), start_y + (cy_dest - start_y) * (step / 50)))
            elif 'STARS_DATA' in globals() and arr_rwy in STARS_DATA and star in STARS_DATA[arr_rwy]:
                ruta = STARS_DATA[arr_rwy][star]
                path_points = [get_radar_xy(lat, lon, w, h) for _, lat, lon in ruta]

                for i in range(len(path_points) - 1):
                    canvas.create_line(path_points[i][0], path_points[i][1], path_points[i + 1][0],
                                       path_points[i + 1][1], fill="#E67E22", width=2, tags="overlay")
                    if i != len(path_points) - 2:
                        canvas.create_text(path_points[i][0] + 10, path_points[i][1], text=ruta[i][0], fill="#E67E22",
                                           font=("Courier", 8), anchor="w", tags="overlay")

                canvas.create_line(path_points[-1][0], path_points[-1][1], cx_dest, cy_dest, fill="#E67E22", width=2,
                                   tags="overlay")
                path_points.append((cx_dest, cy_dest))

                pasos = 25
                for i in range(len(path_points) - 1):
                    x1, y1 = path_points[i]
                    x2, y2 = path_points[i + 1]
                    for s in range(pasos): anim_path.append(
                        (x1 + (x2 - x1) * (s / pasos), y1 + (y2 - y1) * (s / pasos)))

            canvas.create_oval(cx_dest - 5, cy_dest - 5, cx_dest + 5, cy_dest + 5, fill="#E74C3C", outline="white",
                               tags="overlay")
            canvas.create_text(cx_dest + 12, cy_dest - 10, text="LEBL", fill="white", font=("Courier", 10, "bold"),
                               anchor="w", tags="overlay")

            dot_id = canvas.create_oval(-8, -8, -8, -8, fill="white", outline="#E67E22", width=2, tags="overlay")
            bg_id = canvas.create_rectangle(-20, -20, -20, -20, fill="#08182B", outline="#E67E22", width=1,
                                            tags="overlay")
            text_id = canvas.create_text(-20, -20, text=reg, fill="white", font=("Courier", 10, "bold"), anchor="w",
                                         tags="overlay")

            frame = 0

            def animate():
                nonlocal frame
                if not canvas.winfo_exists(): return
                if frame < len(anim_path):
                    cx, cy = anim_path[frame]
                    canvas.coords(dot_id, cx - 6, cy - 6, cx + 6, cy + 6)
                    canvas.coords(bg_id, cx + 9, cy - 8, cx + 67, cy + 8)
                    canvas.coords(text_id, cx + 12, cy)
                    frame += 1
                    canvas.after(40, animate)
                else:
                    phase2_ground()

            animate()

        # Iniciar la cadena
        phase1_arrival()

    canvas.after(100, draw_and_animate)

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

    # Obtenemos la hora local (LT) y la hora UTC
    now_lt = datetime.datetime.now()
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # Formateamos ambas horas para que queden bonitas
    lt_str = now_lt.strftime("%H:%M:%S")
    utc_str = now_utc.strftime("%H:%M:%S")

    # Actualizamos el texto del reloj en la interfaz
    clock_lbl.config(text=f"🕐 LT: {lt_str}  |  UTC: {utc_str}")

    current_hhmm = now_lt.strftime("%H:%M")
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

CURRENT_WIND_DIR = 0.0
CURRENT_WIND_SPEED = 0.0

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
        global CURRENT_WIND_DIR, CURRENT_WIND_SPEED
        try:
            import urllib.request, json
            url = ("https://api.open-meteo.com/v1/forecast"
                   "?latitude=41.2971&longitude=2.0785"
                   "&current=temperature_2m,wind_speed_10m,wind_direction_10m,weathercode"
                   "&wind_speed_unit=kmh&timezone=Europe/Madrid")
            with urllib.request.urlopen(url, timeout=5) as r:
                data = json.loads(r.read())

            cur = data["current"]
            temp = cur["temperature_2m"]
            wind = cur["wind_speed_10m"]
            wdir = cur["wind_direction_10m"]

            # ¡AQUÍ ESTÁ LA MAGIA! Guardamos el viento para todo el programa
            CURRENT_WIND_SPEED = float(wind)
            CURRENT_WIND_DIR = float(wdir)

            desc = _weather_code_to_text(cur["weathercode"])

            arrows = ['↓', '↙', '←', '↖', '↑', '↗', '→', '↘']
            idx = round(wdir / 45) % 8
            arrow = arrows[idx]

            text  = f"  BCN Weather: {desc}  |  {temp}°C  |  {arrow} {wind} km/h  "
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
    for item in buttons:
        if len(item) == 3:
            label, cmd, color = item
        else:
            label, cmd = item
            color = "royalblue"
        tk.Button(f, text=label, command=cmd,
                  bg=color, fg="white", relief="flat",
                  padx=6, pady=4, width=16, font=("Helvetica", 9),
                  activebackground="navy", activeforeground="white").pack(side="left", padx=3)


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

btn_row(left, [("Load Airports",   load_airports,   "#1A6B3C"),
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


# ── ARRIVALS ────────────────────────────────────────────────
section_label(left, "ARRIVALS")

btn_row(left, [("Load Arrivals",   load_arrivals,   "#1A6B3C"),
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

btn_row(left, [("Load Structure",  load_airport_structure, "#1A6B3C"),
               ("Assign Gates",    assign_dynamic_gates,   "#1A6B3C")])
btn_row(left, [("Gate Map", show_interactive_diagram,  "#1A6B3C"),
               ("Occupancy List",  show_gate_occupancy_list)])
btn_row(left, [("Night Gates",     assign_night_gates_v4),
               ("Day Occupancy",   plot_day_occupancy)])



# ── DEPARTURES ─────────────────────────────────────────────────
section_label(left, "DEPARTURES")

btn_row(left, [("Load Departures", load_departures,  "#1A6B3C"),
               ("Merge Movements", merge_movements,  "#1A6B3C")])
btn_row(left, [("Night Aircraft",  show_night_aircraft)])

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
    "   Version 4.0",
    "",
    "━" * 42,
    "",
    "   DEVELOPED BY",
    "",
    "      -  Guiu  -",
    "      -  Tejdeep  -",
    "      -  Xavi  -",
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
    "   :)"
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

# ── EXTRA FUNCTIONS ──────────────────────────────────────────────────
section_label(left, "EXTRA FUNCTIONS")

btn_row(left, [("Active Runways",     check_active_runways),
               ("Airport Map",        view_airport_map)])
btn_row(left, [("Assign STARs",       assign_stars_to_arrivals,),
               ("View Arrival",       view_aircraft_arrival,  "#1A6B3C")])
btn_row(left, [("Assign SIDs",        assign_sids_to_departures,),
               ("View Departure",     view_aircraft_departure,  "#1A6B3C")])
btn_row(left, [("Ground Taxiing",     view_ground_movements),
               ("View Merged Flight", view_merged_flight)])

# ── Footer label ──────────────────────────────────────────────────────
footer_lbl = tk.Label(left, text="Project by: Guiu  ·  Tejdeep  ·  Xavi",
                      bg="white", fg="royalblue", font=("Helvetica", 8),
                      cursor="hand2")
footer_lbl.pack(pady=(16, 8))
footer_lbl.bind("<Button-1>", _on_footer_click)


root.mainloop()
