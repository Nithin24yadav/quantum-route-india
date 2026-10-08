# QuantumRoute India

## Fastest vs Cheapest Route Optimization using Qiskit

QuantumRoute India is a hackathon prototype that compares the fastest and most cost-effective routes between Indian cities while considering:

- Distance
- Travel time
- Fuel consumption
- Fuel price
- Toll charges
- Vehicle type

The project also demonstrates a **Quantum Approximate Optimization Algorithm (QAOA)** approach to the Travelling Salesman Problem (TSP), compared against a classical brute-force solution.

---

## Problem

Logistics companies need to decide between routes that may be:

- Faster but more expensive
- Slower but cheaper

The cost of a journey depends not only on distance, but also on vehicle mileage, fuel price and toll charges.

QuantumRoute India provides two types of route optimization:

1. **Fastest Route**
2. **Cheapest Route**

It also includes a quantum TSP demonstration for optimizing a multi-city journey.

---

## Features

### 1. Fastest Route

Finds the route with the lowest travel time.

### 2. Cheapest Route

Calculates total journey cost using:

```text
Fuel Cost + Toll Cost
Fuel cost:
Distance / Vehicle Mileage × Fuel Price

Supported Vehicles
- Petrol Car
- Diesel Car
- Bike
- Diesel Truck
- Heavy Truck
Custom Routes
Users can create their own route with any number of stops.
A city can appear multiple times, but the same city cannot be selected consecutively.
Example:
Bengaluru -> Jaipur -> Pune -> Jaipur -> Bengaluru

Quantum TSP
The project formulates a 4-city Travelling Salesman Problem as a QUBO and solves it using QAOA with the Qiskit simulator.
Benchmark cities:
- Bengaluru
- Pune
- Surat
- Jaipur
Classical vs Quantum Result
Classical Brute Force
Bengaluru -> Pune -> Surat -> Jaipur -> Bengaluru

Distance: 4040 km

QAOA
Bengaluru -> Jaipur -> Surat -> Pune -> Bengaluru

Distance: 4040 km

Both solutions have the same total distance.
Classical: 4040 km
QAOA:      4040 km
Difference: 0 km

This project does not claim quantum advantage.
Data
The current prototype uses synthetic/benchmark route data.
The route distances, travel times, tolls and fuel prices are approximate values created for the hackathon prototype.
The current version does not use live Google Maps data.
Technology
- Python
- Qiskit
- QAOA
- QUBO
- Qiskit Statevector simulator
- Classical brute-force optimization
Tested with:
Python 3.14.7
Qiskit 2.5.2

Running the Project
Install dependencies:
pip install -r requirements.txt

Run the main application:
python demo.py

Run the classical TSP benchmark:
python classical_tsp.py
Run the QAOA demonstration:
python qaoa_route.py

Limitations
This is a small hackathon prototype.
- Route data is synthetic.
- Only four benchmark cities are included.
- Fuel prices are benchmark assumptions.
- Toll values are benchmark assumptions.
- QAOA currently runs on a simulator.
- No quantum advantage is claimed.
Future Work
- Live routing data
- Real-time traffic
- Live toll information
- IBM Quantum hardware
- Larger TSP instances
- Emission-aware optimization
- Route visualization
Hackathon
Built for:
Qiskit Fall Fest 2026 — Quantum Build Challenge
Track:
Industry / Logistics Route Optimization
Disclaimer
All route distances, travel times, toll values and fuel prices are synthetic/benchmark values intended for demonstration purposes.