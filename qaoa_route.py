from route_data import ROUTES

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.circuit.library import QAOAAnsatz

import numpy as np
from scipy.optimize import minimize


# ============================================================
# CITY DATA
# ============================================================

CITIES = [
    "Bengaluru",
    "Pune",
    "Surat",
    "Jaipur"
]

N = len(CITIES)


# ============================================================
# VARIABLE INDEX
# ============================================================

# Each city can occupy one of four positions.
#
# x(city, position)
#
# x0  = Bengaluru at position 1
# x1  = Bengaluru at position 2
# x2  = Bengaluru at position 3
# x3  = Bengaluru at position 4
#
# x4  = Pune at position 1
# ...
#
# x15 = Jaipur at position 4


def variable(city_index, position):
    return city_index * N + position


# ============================================================
# GET DISTANCE
# ============================================================

def get_distance(city_a, city_b):

    routes = ROUTES[(city_a, city_b)]

    # Use the shortest-distance road
    best = min(
        routes,
        key=lambda r: r["distance_km"]
    )

    return best["distance_km"]


# ============================================================
# QUBO STORAGE
# ============================================================

# Q(x) =
#
# constant
# + linear terms
# + quadratic terms

linear = {}
quadratic = {}
constant = 0


def add_linear(index, value):

    linear[index] = (
        linear.get(index, 0) + value
    )


def add_quadratic(index_a, index_b, value):

    # Keep indices in a consistent order
    if index_a > index_b:
        index_a, index_b = index_b, index_a

    key = (index_a, index_b)

    quadratic[key] = (
        quadratic.get(key, 0) + value
    )


# ============================================================
# PENALTY STRENGTH
# ============================================================

# Large enough to discourage invalid routes.

PENALTY = 10000


# ============================================================
# CONSTRAINT 1
#
# Each position must contain exactly ONE city.
#
# (x1 + x2 + x3 + x4 - 1)^2
# ============================================================

for position in range(N):

    indices = [
        variable(city, position)
        for city in range(N)
    ]

    constant += PENALTY

    # Linear terms
    for i in indices:

        add_linear(
            i,
            -PENALTY
        )

    # Quadratic terms
    for a in range(len(indices)):

        for b in range(a + 1, len(indices)):

            add_quadratic(
                indices[a],
                indices[b],
                2 * PENALTY
            )


# ============================================================
# CONSTRAINT 2
#
# Each city must appear exactly ONE time.
#
# (x1 + x2 + x3 + x4 - 1)^2
# ============================================================

for city in range(N):

    indices = [
        variable(city, position)
        for position in range(N)
    ]

    constant += PENALTY

    # Linear terms
    for i in indices:

        add_linear(
            i,
            -PENALTY
        )

    # Quadratic terms
    for a in range(len(indices)):

        for b in range(a + 1, len(indices)):

            add_quadratic(
                indices[a],
                indices[b],
                2 * PENALTY
            )


# ============================================================
# DISTANCE OBJECTIVE
# ============================================================

# If city A is at position p
# and city B is at position p+1,
# add the distance between them.
#
# The final position also connects back
# to the first position.

for position in range(N):

    next_position = (position + 1) % N

    for city_a in range(N):

        for city_b in range(N):

            if city_a == city_b:
                continue

            distance = get_distance(
                CITIES[city_a],
                CITIES[city_b]
            )

            index_a = variable(
                city_a,
                position
            )

            index_b = variable(
                city_b,
                next_position
            )

            add_quadratic(
                index_a,
                index_b,
                distance
            )


# ============================================================
# DISPLAY QUBO
# ============================================================

print()
print("===================================")
print("          TSP QUBO MODEL")
print("===================================")

print()
print(f"Cities: {N}")
print(f"Binary variables: {N * N}")
print(f"Qubits required: {N * N}")

print()
print(f"Penalty strength: {PENALTY}")

print()
print(f"Constant term: {constant}")

print()
print(f"Linear terms: {len(linear)}")

print()
print(f"Quadratic terms: {len(quadratic)}")

print()
print("Example linear terms:")

for index, value in list(linear.items())[:5]:

    print(
        f"x{index}: {value}"
    )

print()
print("Example quadratic terms:")

for key, value in list(quadratic.items())[:10]:

    print(
        f"x{key[0]} * x{key[1]}: {value}"
    )

print()
print("===================================")


# ============================================================
# QUBO EVALUATOR
# ============================================================

def evaluate_qubo(solution):
    """
    Calculate the QUBO score for a binary solution.

    solution:
        list of 16 values containing only 0 or 1.
    """

    score = constant

    # Linear terms
    for index, coefficient in linear.items():

        score += (
            coefficient
            * solution[index]
        )

    # Quadratic terms
    for (index_a, index_b), coefficient in quadratic.items():

        score += (
            coefficient
            * solution[index_a]
            * solution[index_b]
        )

    return score


# ============================================================
# TEST KNOWN CLASSICAL SOLUTION
# ============================================================

# Classical solution:
#
# Bengaluru -> Pune -> Surat -> Jaipur -> Bengaluru

known_solution = [0] * 16

known_solution[
    variable(0, 0)
] = 1

known_solution[
    variable(1, 1)
] = 1

known_solution[
    variable(2, 2)
] = 1

known_solution[
    variable(3, 3)
] = 1


score = evaluate_qubo(
    known_solution
)


print()
print("===================================")
print("       QUBO SOLUTION TEST")
print("===================================")

print()
print("Known classical route:")
print(
    "Bengaluru -> Pune -> Surat -> Jaipur -> Bengaluru"
)

print()
print("Binary solution:")
print(known_solution)

print()
print(f"QUBO score: {score}")

print()
print("Expected distance: 4040 km")

print()
print("===================================")


# ============================================================
# TEST INVALID SOLUTION
# ============================================================

invalid_solution = [0] * 16

invalid_score = evaluate_qubo(
    invalid_solution
)

print()
print("Invalid solution test:")

print(
    "Binary solution:",
    invalid_solution
)

print(
    f"QUBO score: {invalid_score}"
)


# ============================================================
# QUBO -> QUANTUM HAMILTONIAN
# ============================================================

# We convert binary variables using:
#
# x_i = (1 - Z_i) / 2
#
# and:
#
# x_i x_j =
# (1 - Z_i - Z_j + Z_i Z_j) / 4


def qubo_to_hamiltonian(
    linear,
    quadratic,
    constant,
    num_qubits
):

    pauli_terms = []

    # --------------------------------------------------------
    # Constant term
    # --------------------------------------------------------

    pauli_terms.append(
        (
            "I" * num_qubits,
            constant
        )
    )

    # --------------------------------------------------------
    # Linear terms
    #
    # x_i = (1 - Z_i) / 2
    # --------------------------------------------------------

    for i, coefficient in linear.items():

        identity = "I" * num_qubits

        z_label = list(identity)

        z_label[
            num_qubits - 1 - i
        ] = "Z"

        z_label = "".join(z_label)

        # coefficient / 2 * I
        pauli_terms.append(
            (
                identity,
                coefficient / 2
            )
        )

        # - coefficient / 2 * Z_i
        pauli_terms.append(
            (
                z_label,
                -coefficient / 2
            )
        )

    # --------------------------------------------------------
    # Quadratic terms
    #
    # x_i*x_j =
    # (1 - Zi - Zj + ZiZj) / 4
    # --------------------------------------------------------

    for (i, j), coefficient in quadratic.items():

        identity = "I" * num_qubits

        # Z_i
        zi = list(identity)

        zi[
            num_qubits - 1 - i
        ] = "Z"

        zi = "".join(zi)

        # Z_j
        zj = list(identity)

        zj[
            num_qubits - 1 - j
        ] = "Z"

        zj = "".join(zj)

        # Z_i Z_j
        zizj = list(identity)

        zizj[
            num_qubits - 1 - i
        ] = "Z"

        zizj[
            num_qubits - 1 - j
        ] = "Z"

        zizj = "".join(zizj)

        # Constant contribution
        pauli_terms.append(
            (
                identity,
                coefficient / 4
            )
        )

        # -Zi contribution
        pauli_terms.append(
            (
                zi,
                -coefficient / 4
            )
        )

        # -Zj contribution
        pauli_terms.append(
            (
                zj,
                -coefficient / 4
            )
        )

        # ZiZj contribution
        pauli_terms.append(
            (
                zizj,
                coefficient / 4
            )
        )

    return SparsePauliOp.from_list(
        pauli_terms
    ).simplify()


# ============================================================
# CREATE QUANTUM HAMILTONIAN
# ============================================================

hamiltonian = qubo_to_hamiltonian(
    linear,
    quadratic,
    constant,
    len(linear)
)


print()
print("===================================")
print("       QUANTUM HAMILTONIAN")
print("===================================")

print(
    "Number of qubits:",
    len(linear)
)

print(
    "Number of Pauli terms:",
    len(hamiltonian)
)

print()
print("First few Pauli terms:")

for pauli, coefficient in zip(
    hamiltonian.paulis[:10],
    hamiltonian.coeffs[:10]
):

    print(
        pauli,
        coefficient
    )


# ============================================================
# HAMILTONIAN VERIFICATION
# ============================================================

# Create a quantum circuit representing
# our known classical solution.

qc_verify = QuantumCircuit(
    N * N
)

for i, bit in enumerate(
    known_solution
):

    if bit == 1:
        qc_verify.x(i)


# Convert the circuit into a quantum state.

state = Statevector.from_instruction(
    qc_verify
)


# Calculate the Hamiltonian energy.

hamiltonian_energy = (
    state
    .expectation_value(hamiltonian)
    .real
)


print()
print("===================================")
print("     HAMILTONIAN VERIFICATION")
print("===================================")

print()
print(
    f"QUBO energy:         {score}"
)

print(
    f"Hamiltonian energy:  {hamiltonian_energy:.0f}"
)

print(
    "Expected distance:   4040 km"
)

print()
print("===================================")


# ============================================================
# QAOA
# ============================================================

print()
print("===================================")
print("          STARTING QAOA")
print("===================================")


# QAOA depth
REPS = 1


# Build the QAOA circuit

qaoa_circuit = QAOAAnsatz(
    hamiltonian,
    reps=REPS,
    flatten=True
)


print()
print("QAOA circuit created.")
print("Number of qubits:", qaoa_circuit.num_qubits)
print("QAOA depth (reps):", REPS)

print()
print("QAOA parameters:")
for parameter in qaoa_circuit.parameters:
    print("QAOA parameter:", str(parameter).replace("β", "beta").replace("γ", "gamma"))


# ============================================================
# QAOA EXPECTATION VALUE
# ============================================================

def qaoa_energy(parameter_values):

    # Insert beta/gamma values
    # into the QAOA circuit.

    circuit = qaoa_circuit.assign_parameters(
        parameter_values
    )

    # Simulate the quantum state

    state = Statevector.from_instruction(
        circuit
    )

    # Calculate expected energy

    energy = state.expectation_value(
        hamiltonian
    ).real

    return energy


# ============================================================
# QAOA PARAMETER OPTIMIZATION
# ============================================================

print()
print("===================================")
print("   OPTIMIZING QAOA PARAMETERS")
print("===================================")


# Keep parameters in a fixed order

parameter_list = list(
    qaoa_circuit.parameters
)


# Initial values for beta and gamma

initial_parameters = np.array(
    [1.0, 1.0]
)
print()
print("Starting classical optimizer...")
print(
    "Initial parameters:",
    initial_parameters
)

# Store QAOA energy at every optimizer iteration
qaoa_history = []


def qaoa_callback(parameters):
    energy = qaoa_energy(parameters)
    qaoa_history.append(float(energy))


# COBYLA is a classical optimizer.
#
# It adjusts the QAOA parameters
# to minimize the quantum energy.

result = minimize(
    qaoa_energy,
    initial_parameters,
    method="COBYLA",
    callback=qaoa_callback,
    options={
        "maxiter": 100,
        "rhobeg": 1.0
    }
)


best_parameters = result.x
best_energy = result.fun
print()
print("QAOA CONVERGENCE HISTORY")
print("Iteration, Energy")

for iteration, energy in enumerate(qaoa_history, start=1):
    print(f"{iteration}, {energy:.2f}")

print()
print("===================================")
print("    QAOA OPTIMIZATION COMPLETE")
print("===================================")

print()
print(
    "Optimizer success:",
    result.success
)

print()
print(
    "Best QAOA energy:",
    round(best_energy, 2)
)

print()
print("Best parameters:")

for parameter, value in zip(
    parameter_list,
    best_parameters
):

   parameter_name = str(parameter).replace("β", "beta").replace("γ", "gamma")

print(
    f"{parameter_name}: {value:.6f}"
)


# ============================================================
# EXTRACT ROUTE FROM QAOA RESULT
# ============================================================

print()
print("===================================")
print("     EXTRACTING QAOA ROUTE")
print("===================================")


# Build the QAOA circuit using
# the best parameters.

optimized_circuit = (
    qaoa_circuit.assign_parameters(
        best_parameters
    )
)


# Simulate the optimized quantum circuit.

optimized_state = (
    Statevector.from_instruction(
        optimized_circuit
    )
)


# Get probabilities for all
# possible 16-bit solutions.

probabilities = (
    optimized_state.probabilities_dict()
)


# ============================================================
# CHECK VALID TSP SOLUTION
# ============================================================

def is_valid_solution(solution):

    # Every position must contain
    # exactly one city.

    for position in range(N):

        total = 0

        for city in range(N):

            total += solution[
                variable(city, position)
            ]

        if total != 1:
            return False


    # Every city must appear
    # exactly once.

    for city in range(N):

        total = 0

        for position in range(N):

            total += solution[
                variable(city, position)
            ]

        if total != 1:
            return False


    return True


# ============================================================
# DECODE BINARY SOLUTION
# ============================================================

def decode_solution(solution):

    route = []

    for position in range(N):

        for city in range(N):

            if solution[
                variable(city, position)
            ] == 1:

                route.append(
                    CITIES[city]
                )

                break

    return route


# ============================================================
# FIND VALID QAOA SOLUTIONS
# ============================================================

valid_solutions = []


for bitstring, probability in probabilities.items():

    # Qiskit displays bitstrings with
    # qubit 0 on the RIGHT.
    #
    # Reverse it so that index 0
    # matches our QUBO variable 0.

    solution = [
        int(bit)
        for bit in bitstring[::-1]
    ]


    if is_valid_solution(solution):

        energy = evaluate_qubo(
            solution
        )

        valid_solutions.append(
            (
                probability,
                energy,
                solution
            )
        )


# ============================================================
# SORT VALID SOLUTIONS BY ENERGY
# ============================================================

# Lower QUBO energy = better route.
# We choose the best valid solution produced
# by the optimized QAOA state.

valid_solutions.sort(
    key=lambda item: item[1]
)


print()
print(
    "Number of valid solutions found:",
    len(valid_solutions)
)


# ============================================================
# DISPLAY QAOA RESULT
# ============================================================

if len(valid_solutions) == 0:

    print()
    print(
        "WARNING: QAOA did not produce "
        "a valid TSP solution."
    )

else:

    # Most probable valid solution

    probability, energy, solution = (
        valid_solutions[0]
    )


    route = decode_solution(
        solution
    )


    # Rotate route so Bengaluru
    # appears first.

    start_index = route.index(
        "Bengaluru"
    )


    route = (
        route[start_index:]
        + route[:start_index]
    )


    # Return to Bengaluru

    displayed_route = (
        route
        + ["Bengaluru"]
    )


    print()
    print("===================================")
    print("        QAOA ROUTE FOUND")
    print("===================================")

    print()
    print("Binary solution:")
    print(solution)

    print()
    print("QAOA route:")

    print(
        " -> ".join(
            displayed_route
        )
    )

    print()
    print(
        f"QAOA route energy: {energy:.2f}"
    )

    print()
    print(
        f"Probability of this solution: "
        f"{probability:.6f}"
    )


    # ========================================================
    # CLASSICAL VS QAOA
    # ========================================================

    print()
    print("===================================")
    print("        CLASSICAL VS QAOA")
    print("===================================")


    # Calculate classical optimal distance

    classical_distance = 4040


    print()
    print(
        "Classical optimal distance:",
        classical_distance,
        "km"
    )


    # Calculate actual QAOA route distance

    qaoa_distance = 0


    for i in range(len(route) - 1):

        city_a = route[i]
        city_b = route[i + 1]

        qaoa_distance += get_distance(
            city_a,
            city_b
        )


    # Return to Bengaluru

    qaoa_distance += get_distance(
        route[-1],
        route[0]
    )


    print(
        "QAOA route distance:",
        qaoa_distance,
        "km"
    )


    # ========================================================
    # PERFORMANCE COMPARISON
    # ========================================================

    difference = (
        qaoa_distance
        - classical_distance
    )


    percentage_difference = (
        difference
        / classical_distance
        * 100
    )


    print()
    print(
        "Difference:",
        difference,
        "km"
    )

    print(
        f"QAOA is {percentage_difference:.2f}% "
        "longer than the classical optimum."
    )


    print()


    # ========================================================
    # FINAL RESULT
    # ========================================================

    if qaoa_distance == classical_distance:

        print(
            "SUCCESS: QAOA found the "
            "classical optimal route!"
        )

    else:

        print(
            "QAOA found a valid route, "
            "but not the classical optimum."
        )