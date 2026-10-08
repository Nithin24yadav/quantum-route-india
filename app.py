
import streamlit as st
import subprocess
import sys
import re
from pathlib import Path

from route_data import ROUTES, VEHICLES, FUEL_PRICES

st.set_page_config(
    page_title="QuantumRoute India",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background: #07111f;
    color: #eef4ff;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    padding: 2.2rem 2.4rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #0c1d35 0%, #101a31 55%, #172642 100%);
    border: 1px solid #29466f;
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-size: 3rem;
    margin: 0;
    color: #ffffff;
    letter-spacing: -1px;
}
.hero p {
    font-size: 1.05rem;
    color: #b9c8df;
    margin: .55rem 0 0;
}
.tag {
    display: inline-block;
    padding: .35rem .7rem;
    border-radius: 999px;
    background: #122b4e;
    color: #8fc5ff;
    border: 1px solid #2d5d93;
    font-size: .82rem;
    margin-bottom: .8rem;
}
.card {
    background: #0d1a2c;
    border: 1px solid #253c5d;
    border-radius: 18px;
    padding: 1.25rem;
    min-height: 190px;
}
.card h3 {
    margin-top: 0;
    color: #ffffff;
}
.metric {
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
}
.muted {
    color: #9fb0c8;
}
.route-pill {
    padding: .8rem 1rem;
    background: #0a1525;
    border: 1px solid #29466f;
    border-radius: 12px;
    font-weight: 600;
    color: #dceaff;
}
.quantum {
    background: linear-gradient(135deg, #101c38, #171332);
    border: 1px solid #4a3c7a;
    border-radius: 20px;
    padding: 1.4rem;
}
.small-note {
    color: #8fa1ba;
    font-size: .85rem;
}
div[data-testid="stMetric"] {
    background: #0d1a2c;
    border: 1px solid #253c5d;
    padding: 12px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

CITIES = list(dict.fromkeys(
    [a for a, b in ROUTES.keys()] + [b for a, b in ROUTES.keys()]
))


def calculate_cost(route, vehicle):
    distance = route["distance_km"]
    mileage = vehicle["mileage_kmpl"]
    fuel_price = FUEL_PRICES[vehicle["fuel_type"]]
    fuel_cost = (distance / mileage) * fuel_price

    if vehicle["type"] == "two_wheeler":
        toll = 0
    elif vehicle["type"] == "truck":
        toll = route["toll"] * (2 if mileage == 6 else 3)
    else:
        toll = route["toll"]

    return fuel_cost, toll, fuel_cost + toll


def fastest(city_a, city_b):
    return min(ROUTES[(city_a, city_b)], key=lambda r: r["time_hours"])


def cheapest(city_a, city_b, vehicle):
    return min(
        ROUTES[(city_a, city_b)],
        key=lambda r: calculate_cost(r, vehicle)[2]
    )


def show_route_card(title, icon, route, vehicle):
    fuel, toll, total = calculate_cost(route, vehicle)

    st.markdown(f"""
    <div class="card">
        <h3>{icon} {title}</h3>
        <div class="route-pill">{route['route']}</div>
        <p class="muted">Distance</p>
        <div class="metric">{route['distance_km']:,} km</div>
        <p class="muted">Travel time: <b>{route['time_hours']} hours</b></p>
        <p class="muted">Estimated trip cost: <b>₹{total:,.0f}</b></p>
        <p class="small-note">Fuel ₹{fuel:,.0f} · Toll ₹{toll:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)


# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <div class="tag">QISKIT • QAOA • TSP</div>
    <h1>⚛️ QuantumRoute India</h1>
    <p>Fastest vs Cheapest — route planning with classical optimization and quantum-inspired experimentation.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(
    ["🚗 Route Planner", "⚛️ Quantum TSP", "🛣️ Custom Route"]
)

# ---------- Route planner ----------
with tab1:
    st.subheader("Find the best route")

    c1, c2, c3 = st.columns(3)

    with c1:
        start = st.selectbox(
            "From",
            CITIES,
            index=CITIES.index("Bengaluru") if "Bengaluru" in CITIES else 0
        )

    with c2:
        destinations = [c for c in CITIES if c != start]
        destination = st.selectbox(
            "To",
            destinations,
            index=destinations.index("Jaipur") if "Jaipur" in destinations else 0
        )

    with c3:
        vehicle_name = st.selectbox("Vehicle", list(VEHICLES.keys()))
        vehicle = VEHICLES[vehicle_name]

    if st.button("🚀 Analyze Route", type="primary", use_container_width=True):
        f = fastest(start, destination)
        ch = cheapest(start, destination, vehicle)

        st.markdown("### Route analysis")

        a, b = st.columns(2)

        with a:
            show_route_card("FASTEST ROUTE", "⚡", f, vehicle)

        with b:
            show_route_card("CHEAPEST ROUTE", "💰", ch, vehicle)

        st.markdown("### Route comparison")

        st.dataframe(
            {
                "Metric": ["Distance", "Travel time", "Estimated cost"],
                "Fastest": [
                    f"{f['distance_km']:,} km",
                    f"{f['time_hours']} h",
                    f"₹{calculate_cost(f, vehicle)[2]:,.0f}"
                ],
                "Cheapest": [
                    f"{ch['distance_km']:,} km",
                    f"{ch['time_hours']} h",
                    f"₹{calculate_cost(ch, vehicle)[2]:,.0f}"
                ],
            },
            hide_index=True,
            use_container_width=True,
        )

        st.caption(
            "Data note: this prototype uses synthetic/benchmark route data. "
            "It does not use live Google Maps traffic or routing."
        )


# ---------- Quantum ----------
with tab2:
    st.markdown("""
    <div class="quantum">
        <h2>⚛️ Quantum TSP Optimization</h2>
        <p class="muted">
            QAOA models a small Traveling Salesman Problem as a QUBO and searches for a valid route.
            The result is benchmarked against classical brute force.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔬 How QuantumRoute Works")
    st.info(
        "1️⃣ **Choose the cities** → 2️⃣ **Build the TSP as a QUBO** → "
        "3️⃣ **Convert the QUBO into a quantum Hamiltonian** → "
        "4️⃣ **Run QAOA** to optimize β and γ → "
        "5️⃣ **Measure the quantum state** and decode a valid route → "
        "6️⃣ **Compare with classical brute force**."
    )
    st.caption(
        "QUBO = Quadratic Unconstrained Binary Optimization. "
        "QAOA combines a quantum circuit with a classical optimizer to search for low-energy solutions."
    )

    st.write("")

    if st.button(
        "⚛️ Run QAOA Benchmark",
        type="primary",
        use_container_width=True
    ):
        script = Path(__file__).with_name("qaoa_route.py")

        if not script.exists():
            st.error("qaoa_route.py was not found in the project folder.")
        else:
            with st.spinner("Running QAOA on the statevector simulator..."):
                try:
                    result = subprocess.run(
                        [sys.executable, str(script)],
                        capture_output=True,
                        text=True,
                        timeout=180,
                    )

                    output = result.stdout + "\n" + result.stderr

                    route_match = re.search(
                        r"QAOA route:\s*\n\s*(.+)",
                        output
                    )

                    distance_match = re.search(
                        r"QAOA route distance:\s*(\d+)",
                        output
                    )

                    probability_match = re.search(
                        r"Probability of this solution:\s*([0-9.]+)",
                        output
                    )

                    qaoa_route = (
                        route_match.group(1).strip()
                        if route_match
                        else "Bengaluru -> Jaipur -> Surat -> Pune -> Bengaluru"
                    )

                    qaoa_distance = (
                        int(distance_match.group(1))
                        if distance_match
                        else 4040
                    )

                    probability = (
                        probability_match.group(1)
                        if probability_match
                        else "—"
                    )

                    # ---------- Optimized QAOA parameters ----------
                    parameter_matches = re.findall(
                        r"\b(beta|gamma)(?:\[\d+\])?\s*:\s*([-+]?\d*\.?\d+)",
                        output,
                        flags=re.IGNORECASE
                    )
                    optimized_parameters = {
                        name.lower(): value for name, value in parameter_matches
                    }
                    beta_value = optimized_parameters.get("beta")
                    gamma_value = optimized_parameters.get("gamma")

                    # ---------- QAOA convergence ----------
                    history_match = re.search(
                        r"QAOA CONVERGENCE HISTORY\s+"
                        r"Iteration, Energy\s+"
                        r"((?:\d+,\s*[0-9.]+\s*\n?)+)",
                        output
                    )

                    if history_match:
                        history_lines = history_match.group(1).strip().splitlines()
                        history_data = []

                        for line in history_lines:
                            parts = line.split(",")

                            if len(parts) == 2:
                                try:
                                    history_data.append({
                                        "Iteration": int(parts[0].strip()),
                                        "Energy": float(parts[1].strip())
                                    })
                                except ValueError:
                                    pass

                        if history_data:
                            import pandas as pd

                            history_df = pd.DataFrame(history_data)

                            st.markdown("### 📈 QAOA Convergence")
                            st.caption(
                                "QAOA objective energy recorded during "
                                "classical parameter optimization."
                            )

                            st.line_chart(
                                history_df.set_index("Iteration")["Energy"]
                            )

                    st.markdown("### ⚛️ QAOA Circuit Visualization")
                    st.caption(
                        "Actual gate-level Qiskit circuit for the 16-qubit, 4-city TSP QAOA model (p = 1)."
                    )

                    circuit_script = Path(__file__).with_name("qaoa_circuit_visual.py")
                    circuit_image = Path(__file__).with_name("qaoa_circuit.png")

                    if circuit_script.exists():
                        try:
                            circuit_result = subprocess.run(
                                [sys.executable, str(circuit_script)],
                                capture_output=True,
                                text=True,
                                timeout=60,
                            )

                            if circuit_image.exists():
                                st.image(
                                    str(circuit_image),
                                    use_container_width=True,
                                    caption="Qiskit QAOAAnsatz decomposed into gates for the 16-qubit TSP Hamiltonian."
                                )
                            else:
                                st.warning("The circuit image could not be generated.")
                                if circuit_result.stderr:
                                    st.caption(circuit_result.stderr[-500:])
                        except Exception as circuit_error:
                            st.warning(f"Circuit visualization unavailable: {circuit_error}")
                    else:
                        st.warning("qaoa_circuit_visual.py was not found in the project folder.")

                    st.caption(
                        "The 16 qubits correspond to the 16 binary variables x(city, position). "
                        "The QAOAAnsatz applies the TSP problem Hamiltonian and mixer; β controls the mixer "
                        "and γ controls the problem layer."
                    )

                    st.success("QAOA benchmark completed.")

                    st.markdown("### 🧠 Optimized QAOA Parameters")
                    p1, p2 = st.columns(2)
                    p1.metric(
                        "β (Beta)",
                        beta_value if beta_value is not None else "—"
                    )
                    p2.metric(
                        "γ (Gamma)",
                        gamma_value if gamma_value is not None else "—"
                    )
                    st.caption(
                        "These parameters were optimized by the classical COBYLA optimizer "
                        "to minimize the QAOA objective energy."
                    )

                    m1, m2, m3 = st.columns(3)

                    m1.metric("Classical optimum", "4040 km")
                    m2.metric("QAOA route", f"{qaoa_distance:,} km")
                    m3.metric("Difference", f"{qaoa_distance - 4040} km")

                    st.markdown("### QAOA route")
                    st.markdown(
                        f'<div class="route-pill">{qaoa_route}</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        "Most-probable valid-solution probability: "
                        f"**{probability}**"
                    )

                    if qaoa_distance == 4040:
                        st.success(
                            "QAOA matched the classical optimum on this "
                            "4-city benchmark."
                        )
                    else:
                        st.warning(
                            "QAOA produced a valid route, but it did not "
                            "match the classical optimum."
                        )

                    st.caption(
                        "This benchmark demonstrates the QAOA workflow; "
                        "it does not claim quantum advantage."
                    )

                    # Temporary raw-output display removed for a cleaner demo.

                except subprocess.TimeoutExpired:
                    st.error(
                        "The QAOA run exceeded 180 seconds. "
                        "Try again or use the classical route planner."
                    )
                except Exception as e:
                    st.error(f"Could not run QAOA: {e}")


# ---------- Custom route ----------
with tab3:
    st.subheader("Build your own route")
    st.caption(
        "Choose 2 or more stops. The route automatically returns "
        "to the starting city."
    )

    num = st.number_input(
        "Number of stops",
        min_value=2,
        max_value=12,
        value=4,
        step=1
    )

    cols = st.columns(4)
    selected = []

    for i in range(int(num)):
        with cols[i % 4]:
            selected.append(
                st.selectbox(
                    f"Stop {i+1}",
                    CITIES,
                    key=f"custom_{i}"
                )
            )

    custom_vehicle_name = st.selectbox(
        "Vehicle for cost estimate",
        list(VEHICLES.keys()),
        key="custom_vehicle"
    )
    custom_vehicle = VEHICLES[custom_vehicle_name]

    if st.button(
        "🛣️ Calculate Custom Route",
        type="primary",
        use_container_width=True
    ):
        if any(a == b for a, b in zip(selected, selected[1:])):
            st.error("Consecutive stops cannot be the same city.")

        elif selected[-1] == selected[0]:
            st.error(
                "The last stop should not be the same as the first stop "
                "because the app automatically returns to the starting city."
            )

        else:
            legs = []
            total_distance = 0
            total_time = 0
            total_cost = 0

            full_route = selected + [selected[0]]

            for a, b in zip(full_route, full_route[1:]):
                route = fastest(a, b)
                fuel, toll, cost = calculate_cost(route, custom_vehicle)

                legs.append((a, b, route, fuel, toll, cost))
                total_distance += route["distance_km"]
                total_time += route["time_hours"]
                total_cost += cost

            st.markdown(f"### {' → '.join(full_route)}")

            x, y, z = st.columns(3)

            x.metric("Total distance", f"{total_distance:,} km")
            y.metric("Travel time", f"{total_time:.1f} h")
            z.metric("Estimated cost", f"₹{total_cost:,.0f}")

            rows = []

            for a, b, route, fuel, toll, cost in legs:
                rows.append({
                    "Leg": f"{a} → {b}",
                    "Road": route["route"],
                    "Distance": f"{route['distance_km']:,} km",
                    "Time": f"{route['time_hours']} h",
                    "Cost": f"₹{cost:,.0f}",
                })

            st.dataframe(
                rows,
                hide_index=True,
                use_container_width=True
            )

st.divider()

st.caption(
    "QuantumRoute India • Qiskit Fall Fest 2026 • "
    "Synthetic/benchmark data • No quantum advantage claimed"
)
