# route_data.py
# Benchmark route data for QuantumRoute India
# Distances, times, tolls, fuel prices and vehicle data are
# approximate/synthetic for the hackathon prototype.

CITIES = [
    "Bengaluru",
    "Pune",
    "Surat",
    "Jaipur"
]


# ============================================================
# ROUTE DATA
# ============================================================
# Each city pair has:
#   - NH48       -> faster, shorter, higher toll
#   - Alternative -> slower, longer, much lower toll
#
# The distances remain unchanged so the QAOA/TSP benchmark
# continues to use the same 4040 km classical optimum.
# ============================================================

ROUTES = {

    # --------------------------------------------------------
    # Bengaluru <-> Pune
    # --------------------------------------------------------

    ("Bengaluru", "Pune"): [
        {
            "route": "NH48",
            "distance_km": 840,
            "time_hours": 15.0,
            "toll": 1500
        },
        {
            "route": "Alternative",
            "distance_km": 875,
            "time_hours": 16.2,
            "toll": 300
        }
    ],

    ("Pune", "Bengaluru"): [
        {
            "route": "NH48",
            "distance_km": 840,
            "time_hours": 15.0,
            "toll": 1500
        },
        {
            "route": "Alternative",
            "distance_km": 875,
            "time_hours": 16.2,
            "toll": 300
        }
    ],


    # --------------------------------------------------------
    # Bengaluru <-> Surat
    # --------------------------------------------------------

    ("Bengaluru", "Surat"): [
        {
            "route": "NH48",
            "distance_km": 1290,
            "time_hours": 22.0,
            "toll": 2200
        },
        {
            "route": "Alternative",
            "distance_km": 1340,
            "time_hours": 23.5,
            "toll": 400
        }
    ],

    ("Surat", "Bengaluru"): [
        {
            "route": "NH48",
            "distance_km": 1290,
            "time_hours": 22.0,
            "toll": 2200
        },
        {
            "route": "Alternative",
            "distance_km": 1340,
            "time_hours": 23.5,
            "toll": 400
        }
    ],


    # --------------------------------------------------------
    # Bengaluru <-> Jaipur
    # --------------------------------------------------------

    ("Bengaluru", "Jaipur"): [
        {
            "route": "NH48",
            "distance_km": 1850,
            "time_hours": 30.0,
            "toll": 3000
        },
        {
            "route": "Alternative",
            "distance_km": 1930,
            "time_hours": 32.0,
            "toll": 500
        }
    ],

    ("Jaipur", "Bengaluru"): [
        {
            "route": "NH48",
            "distance_km": 1850,
            "time_hours": 30.0,
            "toll": 3000
        },
        {
            "route": "Alternative",
            "distance_km": 1930,
            "time_hours": 32.0,
            "toll": 500
        }
    ],


    # --------------------------------------------------------
    # Pune <-> Surat
    # --------------------------------------------------------

    ("Pune", "Surat"): [
        {
            "route": "NH48",
            "distance_km": 420,
            "time_hours": 8.0,
            "toll": 1200
        },
        {
            "route": "Alternative",
            "distance_km": 450,
            "time_hours": 8.5,
            "toll": 150
        }
    ],

    ("Surat", "Pune"): [
        {
            "route": "NH48",
            "distance_km": 420,
            "time_hours": 8.0,
            "toll": 1200
        },
        {
            "route": "Alternative",
            "distance_km": 450,
            "time_hours": 8.5,
            "toll": 150
        }
    ],


    # --------------------------------------------------------
    # Pune <-> Jaipur
    # --------------------------------------------------------

    ("Pune", "Jaipur"): [
        {
            "route": "NH48",
            "distance_km": 1050,
            "time_hours": 18.0,
            "toll": 1800
        },
        {
            "route": "Alternative",
            "distance_km": 1100,
            "time_hours": 19.0,
            "toll": 250
        }
    ],

    ("Jaipur", "Pune"): [
        {
            "route": "NH48",
            "distance_km": 1050,
            "time_hours": 18.0,
            "toll": 1800
        },
        {
            "route": "Alternative",
            "distance_km": 1100,
            "time_hours": 19.0,
            "toll": 250
        }
    ],


    # --------------------------------------------------------
    # Surat <-> Jaipur
    # --------------------------------------------------------

    ("Surat", "Jaipur"): [
        {
            "route": "NH48",
            "distance_km": 930,
            "time_hours": 16.0,
            "toll": 1600
        },
        {
            "route": "Alternative",
            "distance_km": 970,
            "time_hours": 17.0,
            "toll": 200
        }
    ],

    ("Jaipur", "Surat"): [
        {
            "route": "NH48",
            "distance_km": 930,
            "time_hours": 16.0,
            "toll": 1600
        },
        {
            "route": "Alternative",
            "distance_km": 970,
            "time_hours": 17.0,
            "toll": 200
        }
    ]
}


# ============================================================
# VEHICLES
# ============================================================

VEHICLES = {

    "Petrol Car": {
        "fuel_type": "Petrol",
        "mileage_kmpl": 15,
        "type": "car"
    },

    "Diesel Car": {
        "fuel_type": "Diesel",
        "mileage_kmpl": 20,
        "type": "car"
    },

    "Bike": {
        "fuel_type": "Petrol",
        "mileage_kmpl": 40,
        "type": "two_wheeler"
    },

    "Diesel Truck": {
        "fuel_type": "Diesel",
        "mileage_kmpl": 6,
        "type": "truck"
    },

    "Heavy Truck": {
        "fuel_type": "Diesel",
        "mileage_kmpl": 4,
        "type": "truck"
    }
}


# ============================================================
# FUEL PRICES
# ============================================================

FUEL_PRICES = {
    "Petrol": 110,
    "Diesel": 92
}