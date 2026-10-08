from route_data import ROUTES, VEHICLES, FUEL_PRICES


CITIES = [
    "Bengaluru",
    "Pune",
    "Surat",
    "Jaipur"
]


def get_route(city_a, city_b):
    """Return the shortest-distance route between two cities."""
    routes = ROUTES[(city_a, city_b)]
    return min(routes, key=lambda r: r["distance_km"])


def calculate_custom_route(route, vehicle):
    """Calculate distance, toll, fuel and total cost for a user-defined route."""

    total_distance = 0
    total_toll = 0
    total_fuel_cost = 0
    legs = []

    for i in range(len(route) - 1):

        city_a = route[i]
        city_b = route[i + 1]

        road = get_route(city_a, city_b)

        distance = road["distance_km"]

        if vehicle["type"] == "two_wheeler":
            toll = 0
        else:
            toll = road["toll"]

        fuel_cost = (
            distance / vehicle["mileage_kmpl"]
        ) * FUEL_PRICES[vehicle["fuel_type"]]

        total_distance += distance
        total_toll += toll
        total_fuel_cost += fuel_cost

        legs.append({
            "from": city_a,
            "to": city_b,
            "route": road["route"],
            "distance": distance,
            "toll": toll,
            "fuel_cost": fuel_cost
        })

    total_cost = total_fuel_cost + total_toll

    return {
        "legs": legs,
        "distance": total_distance,
        "toll": total_toll,
        "fuel_cost": total_fuel_cost,
        "total_cost": total_cost
    }


# ------------------------------------------------
# TEST USER-DEFINED ROUTE
# ------------------------------------------------

my_route = [
    "Jaipur",
    "Bengaluru",
    "Surat",
    "Pune",
    "Jaipur"
]


vehicle = VEHICLES["Petrol Car"]

result = calculate_custom_route(my_route, vehicle)


# ------------------------------------------------
# DISPLAY RESULT
# ------------------------------------------------

print("\n===================================")
print("        MY OWN ROUTE")
print("===================================")

print("\nRoute:")
print(" → ".join(my_route))

print(f"\nVehicle: Petrol Car")

print("\n---------- TRIP SUMMARY ----------")

print(f"Total distance: {result['distance']} km")
print(f"Total toll: ₹{result['toll']:.2f}")
print(f"Fuel cost: ₹{result['fuel_cost']:.2f}")
print(f"Total trip cost: ₹{result['total_cost']:.2f}")

print("\n---------- INDIVIDUAL LEGS ----------")

for leg in result["legs"]:
    print(
        f"{leg['from']} → {leg['to']} | "
        f"{leg['distance']} km | "
        f"Toll ₹{leg['toll']} | "
        f"Fuel ₹{leg['fuel_cost']:.2f}"
    )

print("\n===================================\n")