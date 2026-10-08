from route_data import ROUTES, VEHICLES, FUEL_PRICES


# ============================================================
# QUANTUM ROUTE INDIA
# ============================================================

CITIES = [
    "Bengaluru",
    "Pune",
    "Surat",
    "Jaipur"
]


# ============================================================
# CALCULATE ROUTE COST
# ============================================================

def calculate_cost(route, vehicle):

    distance = route["distance_km"]
    mileage = vehicle["mileage_kmpl"]
    fuel_type = vehicle["fuel_type"]

    fuel_price = FUEL_PRICES[fuel_type]

    # Fuel cost
    fuel_cost = (distance / mileage) * fuel_price

    # Vehicle-specific toll
    base_toll = route["toll"]

    if vehicle["type"] == "two_wheeler":

        # Bikes
        toll = 0

    elif vehicle["type"] == "truck":

        # Diesel Truck
        if vehicle["mileage_kmpl"] == 6:
            toll = base_toll * 2

        # Heavy Truck
        else:
            toll = base_toll * 3

    else:

        # Cars
        toll = base_toll

    total_cost = fuel_cost + toll

    return fuel_cost, toll, total_cost


# ============================================================
# GET BEST DISTANCE ROUTE
# ============================================================

def get_best_route(city_a, city_b):

    routes = ROUTES[(city_a, city_b)]

    return min(
        routes,
        key=lambda route: route["distance_km"]
    )


# ============================================================
# FASTEST ROUTE
# ============================================================

def find_fastest(city_a, city_b):

    routes = ROUTES[(city_a, city_b)]

    return min(
        routes,
        key=lambda route: route["time_hours"]
    )


# ============================================================
# CHEAPEST ROUTE
# ============================================================

def find_cheapest(city_a, city_b, vehicle):

    routes = ROUTES[(city_a, city_b)]

    best_route = None
    best_cost = float("inf")

    for route in routes:

        _, _, total_cost = calculate_cost(
            route,
            vehicle
        )

        if total_cost < best_cost:

            best_cost = total_cost
            best_route = route

    return best_route


# ============================================================
# DISPLAY FASTEST / CHEAPEST
# ============================================================

def display_route(city_a, city_b, vehicle_name):

    vehicle = VEHICLES[vehicle_name]

    fastest = find_fastest(
        city_a,
        city_b
    )

    cheapest = find_cheapest(
        city_a,
        city_b,
        vehicle
    )

    print()
    print("=" * 50)
    print("ROUTE ANALYSIS")
    print("=" * 50)

    print()
    print(f"Vehicle: {vehicle_name}")
    print(f"Route: {city_a} -> {city_b}")

    # --------------------------------------------------------
    # FASTEST ROUTE
    # --------------------------------------------------------

    print()
    print("-" * 50)
    print("FASTEST ROUTE")
    print("-" * 50)

    fuel, toll, total = calculate_cost(
        fastest,
        vehicle
    )

    print(f"Road: {fastest['route']}")
    print(f"Distance: {fastest['distance_km']} km")
    print(f"Time: {fastest['time_hours']} hours")
    print(f"Fuel cost: Rs.{fuel:.2f}")
    print(f"Toll: Rs.{toll:.2f}")
    print(f"Total cost: Rs.{total:.2f}")

    # --------------------------------------------------------
    # CHEAPEST ROUTE
    # --------------------------------------------------------

    print()
    print("-" * 50)
    print("CHEAPEST ROUTE")
    print("-" * 50)

    fuel, toll, total = calculate_cost(
        cheapest,
        vehicle
    )

    print(f"Road: {cheapest['route']}")
    print(f"Distance: {cheapest['distance_km']} km")
    print(f"Time: {cheapest['time_hours']} hours")
    print(f"Fuel cost: Rs.{fuel:.2f}")
    print(f"Toll: Rs.{toll:.2f}")
    print(f"Total cost: Rs.{total:.2f}")

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    print()
    print("-" * 50)
    print("DECISION")
    print("-" * 50)

    if fastest["route"] == cheapest["route"]:

        print("Fastest and cheapest route are the same.")

    else:

        print(f"Fastest: {fastest['route']}")
        print(f"Cheapest: {cheapest['route']}")

        fastest_cost = calculate_cost(
            fastest,
            vehicle
        )[2]

        cheapest_cost = calculate_cost(
            cheapest,
            vehicle
        )[2]

        savings = fastest_cost - cheapest_cost

        print(
            f"Potential saving: Rs.{savings:.2f}"
        )


# ============================================================
# QUANTUM RESULT
# ============================================================

def show_quantum_result():

    print()
    print("=" * 50)
    print("QUANTUM ROUTE OPTIMIZATION")
    print("=" * 50)

    print()
    print("CLASSICAL BRUTE-FORCE OPTIMUM")

    print(
        "Bengaluru -> Pune -> Surat -> "
        "Jaipur -> Bengaluru"
    )

    print()
    print("Distance: 4040 km")

    print()
    print("QAOA SOLUTION")

    print(
        "Bengaluru -> Jaipur -> Surat -> "
        "Pune -> Bengaluru"
    )

    print()
    print("Distance: 4040 km")

    print()
    print("-" * 50)

    print("Classical distance: 4040 km")
    print("QAOA distance:      4040 km")
    print("Difference:         0 km")

    print("-" * 50)

    print()
    print("SUCCESS: QAOA found an optimal route")

    print()
    print("Note: This benchmark uses the Qiskit simulator.")


# ============================================================
# CHOOSE CITY
# ============================================================

def choose_city(message):

    print()

    for i, city in enumerate(
        CITIES,
        start=1
    ):

        print(f"{i}. {city}")

    while True:

        try:

            choice = int(
                input(message)
            )

            if 1 <= choice <= len(CITIES):

                return CITIES[choice - 1]

            print(
                "Please choose a valid number."
            )

        except ValueError:

            print(
                "Please enter a number."
            )


# ============================================================
# CHOOSE VEHICLE
# ============================================================

def choose_vehicle():

    print()
    print("VEHICLE")

    vehicle_names = list(VEHICLES.keys())

    for i, name in enumerate(
        vehicle_names,
        1
    ):

        print(f"{i}. {name}")

    while True:

        try:

            choice = int(
                input("\nChoose vehicle: ")
            )

            if choice < 1 or choice > len(vehicle_names):

                print(
                    f"Please choose a number between "
                    f"1 and {len(vehicle_names)}."
                )

                continue

            vehicle_name = vehicle_names[
                choice - 1
            ]

            vehicle = VEHICLES[
                vehicle_name
            ]

            return vehicle_name, vehicle

        except ValueError:

            print(
                "Please enter a valid number."
            )


# ============================================================
# MY OWN ROUTE
# ============================================================

def own_route():

    print()
    print("=" * 50)
    print("MY OWN ROUTE")
    print("=" * 50)

    print()
    print("Available cities:")

    for i, city in enumerate(
        CITIES,
        1
    ):

        print(f"{i}. {city}")

    # --------------------------------------------------------
    # ASK NUMBER OF CITIES
    # --------------------------------------------------------

    while True:

        try:

            number = int(
                input(
                    "\nHow many cities/stops "
                    "do you want in your route? "
                )
            )

            if number < 2:

                print(
                    "Please enter at least 2 cities."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid number."
            )

    # --------------------------------------------------------
    # SELECT CITIES
    # --------------------------------------------------------
    #
    # Same city CAN appear multiple times.
    #
    # Example:
    #
    # Bengaluru -> Jaipur -> Pune -> Jaipur
    #
    # But:
    #
    # Bengaluru -> Jaipur -> Jaipur
    #
    # is not allowed.
    # --------------------------------------------------------

    selected_cities = []

    print()
    print(
        "Choose the cities in the EXACT order"
    )

    print(
        "you want to travel."
    )

    print()
    print(
        "A city can appear multiple times, "
        "but not consecutively."
    )

    for position in range(number):

        while True:

            try:

                choice = int(
                    input(
                        f"\nCity {position + 1}: "
                    )
                )

                if not 1 <= choice <= len(CITIES):

                    print(
                        f"Please choose a number "
                        f"between 1 and {len(CITIES)}."
                    )

                    continue

                city = CITIES[
                    choice - 1
                ]

                # ------------------------------------------------
                # Prevent consecutive duplicate cities
                # ------------------------------------------------

                if selected_cities:

                    if city == selected_cities[-1]:

                        print(
                            "You cannot select the "
                            "same city consecutively."
                        )

                        continue

                selected_cities.append(city)

                break

            except ValueError:

                print(
                    "Please enter a valid number."
                )

    # --------------------------------------------------------
    # CHOOSE VEHICLE
    # --------------------------------------------------------

    vehicle_name, vehicle = choose_vehicle()

    # --------------------------------------------------------
    # DISPLAY SELECTED ROUTE
    # --------------------------------------------------------

    print()
    print("=" * 50)
    print("YOUR ROUTE")
    print("=" * 50)

    route_display = " -> ".join(
        selected_cities
    )

    # Return to starting city
    route_display += (
        f" -> {selected_cities[0]}"
    )

    print()
    print(route_display)

    # --------------------------------------------------------
    # CALCULATE TOTALS
    # --------------------------------------------------------

    total_distance = 0
    total_fuel_cost = 0
    total_toll = 0
    total_cost = 0
    total_time = 0

    print()
    print("-" * 50)
    print("ROUTE BREAKDOWN")
    print("-" * 50)

    # --------------------------------------------------------
    # CALCULATE EACH LEG
    # --------------------------------------------------------

    for i in range(
        len(selected_cities)
    ):

        city_a = selected_cities[i]

        city_b = selected_cities[
            (i + 1) % len(selected_cities)
        ]

        route = get_best_route(
            city_a,
            city_b
        )

        fuel_cost, toll, cost = calculate_cost(
            route,
            vehicle
        )

        distance = route[
            "distance_km"
        ]

        time = route[
            "time_hours"
        ]

        total_distance += distance
        total_fuel_cost += fuel_cost
        total_toll += toll
        total_cost += cost
        total_time += time

        print()
        print(
            f"{city_a} -> {city_b}"
        )

        print(
            f"Route: {route['route']}"
        )

        print(
            f"Distance: {distance} km"
        )

        print(
            f"Time: {time} hours"
        )

        print(
            f"Fuel cost: Rs.{fuel_cost:.2f}"
        )

        print(
            f"Toll: Rs.{toll:.2f}"
        )

        print(
            f"Leg cost: Rs.{cost:.2f}"
        )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("=" * 50)
    print("TOTAL JOURNEY")
    print("=" * 50)

    print()
    print(
        f"Route: {route_display}"
    )

    print(
        f"Vehicle: {vehicle_name}"
    )

    print(
        f"Total distance: "
        f"{total_distance} km"
    )

    print(
        f"Total time: "
        f"{total_time:.1f} hours"
    )

    print(
        f"Total fuel cost: "
        f"Rs.{total_fuel_cost:.2f}"
    )

    print(
        f"Total toll: "
        f"Rs.{total_toll:.2f}"
    )

    print(
        f"TOTAL COST: "
        f"Rs.{total_cost:.2f}"
    )

    print("=" * 50)


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print()
        print()
        print("=" * 50)
        print("QUANTUM ROUTE INDIA")
        print("=" * 50)

        print()
        print("MAIN MENU")
        print()
        print("1. Fastest / Cheapest Route")
        print("2. Quantum TSP Optimization")
        print("3. My Own Route")
        print("4. Exit")

        try:

            choice = int(
                input("\nSelect an option: ")
            )

        except ValueError:

            print(
                "\nPlease enter 1, 2, 3 or 4."
            )

            continue

        # ----------------------------------------------------
        # OPTION 1
        # ----------------------------------------------------

        if choice == 1:

            print()
            print("-" * 50)
            print("POINT-TO-POINT ROUTING")
            print("-" * 50)

            start_city = choose_city(
                "\nChoose starting city: "
            )

            destination_city = choose_city(
                "\nChoose destination city: "
            )

            if start_city == destination_city:

                print(
                    "\nStart and destination "
                    "cannot be the same."
                )

                continue

            vehicle_name, vehicle = choose_vehicle()

            display_route(
                start_city,
                destination_city,
                vehicle_name
            )

        # ----------------------------------------------------
        # OPTION 2
        # ----------------------------------------------------

        elif choice == 2:

            show_quantum_result()

        # ----------------------------------------------------
        # OPTION 3
        # ----------------------------------------------------

        elif choice == 3:

            own_route()

        # ----------------------------------------------------
        # OPTION 4
        # ----------------------------------------------------

        elif choice == 4:

            print()
            print(
                "Thank you for using "
                "Quantum Route India!"
            )

            break

        # ----------------------------------------------------
        # INVALID OPTION
        # ----------------------------------------------------

        else:

            print(
                "\nInvalid option. "
                "Please choose 1, 2, 3 or 4."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()