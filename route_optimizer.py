from route_data import ROUTES, VEHICLES, FUEL_PRICES

def calculate_route_cost(route, vehicle):
    """Calculate fuel cost and vehicle-specific toll."""

    fuel_type = vehicle["fuel_type"]
    mileage = vehicle["mileage_kmpl"]

    distance = route["distance_km"]

    # Two-wheelers are exempt from NH/NE tolls
    if vehicle["type"] == "two_wheeler":
        toll = 0
    else:
        toll = route["toll"]

    fuel_cost = (distance / mileage) * FUEL_PRICES[fuel_type]
    total_cost = fuel_cost + toll

    return fuel_cost, toll, total_cost


def find_best_routes(from_city, to_city, vehicle):
    routes = ROUTES[(from_city, to_city)]

    results = []

    for route in routes:
        for route in routes:
         fuel_cost, toll, total_cost = calculate_route_cost(route, vehicle)

    results.append({
            **route,
            "fuel_cost": fuel_cost,
            "toll":toll,
            "total_cost": total_cost
        })

    fastest = min(results, key=lambda r: r["time_hours"])
    cheapest = min(results, key=lambda r: r["total_cost"])

    return fastest, cheapest


# -----------------------------
# USER INPUT
# -----------------------------

print("\n===================================")
print("       QUANTUMROUTE INDIA")
print("===================================")

cities = [
    "Bengaluru",
    "Pune",
    "Surat",
    "Jaipur"
]

print("\nAvailable cities:")

for i, city in enumerate(cities, 1):
    print(f"{i}. {city}")

from_choice = int(input("\nFrom (enter number): "))
to_choice = int(input("To (enter number): "))

from_city = cities[from_choice - 1]
to_city = cities[to_choice - 1]


print("\nAvailable vehicles:")

vehicle_names = list(VEHICLES.keys())

for i, vehicle in enumerate(vehicle_names, 1):
    print(f"{i}. {vehicle}")

vehicle_choice = int(input("\nVehicle (enter number): "))

vehicle_name = vehicle_names[vehicle_choice - 1]
vehicle = VEHICLES[vehicle_name]


# -----------------------------
# CALCULATE
# -----------------------------

fastest, cheapest = find_best_routes(
    from_city,
    to_city,
    vehicle
)


# -----------------------------
# RESULTS
# -----------------------------

print("\n===================================")
print("             RESULT")
print("===================================")

print(f"\nFrom: {from_city}")
print(f"To:   {to_city}")
print(f"Vehicle: {vehicle_name}")


print("\n---------- FASTEST ROUTE ----------")

print(f"Route: {fastest['route']}")
print(f"Distance: {fastest['distance_km']} km")
print(f"Time: {fastest['time_hours']} hours")
print(f"Toll: ₹{fastest['toll']}")
print(f"Fuel cost: ₹{fastest['fuel_cost']:.2f}")
print(f"Total cost: ₹{fastest['total_cost']:.2f}")


print("\n---------- CHEAPEST ROUTE ----------")

print(f"Route: {cheapest['route']}")
print(f"Distance: {cheapest['distance_km']} km")
print(f"Time: {cheapest['time_hours']} hours")
print(f"Toll: ₹{cheapest['toll']}")
print(f"Fuel cost: ₹{cheapest['fuel_cost']:.2f}")
print(f"Total cost: ₹{cheapest['total_cost']:.2f}")


print("\n===================================\n")