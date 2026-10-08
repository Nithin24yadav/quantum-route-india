from pathlib import Path

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz

from route_data import ROUTES

CITIES = ["Bengaluru", "Pune", "Surat", "Jaipur"]
N = len(CITIES)
PENALTY = 10000


def variable(city_index, position):
    return city_index * N + position


def get_distance(city_a, city_b):
    routes = ROUTES[(city_a, city_b)]
    return min(routes, key=lambda r: r["distance_km"])["distance_km"]


linear = {}
quadratic = {}
constant = 0


def add_linear(index, value):
    linear[index] = linear.get(index, 0) + value


def add_quadratic(index_a, index_b, value):
    if index_a > index_b:
        index_a, index_b = index_b, index_a
    key = (index_a, index_b)
    quadratic[key] = quadratic.get(key, 0) + value


# Each position contains exactly one city.
for position in range(N):
    indices = [variable(city, position) for city in range(N)]
    constant += PENALTY
    for i in indices:
        add_linear(i, -PENALTY)
    for a in range(len(indices)):
        for b in range(a + 1, len(indices)):
            add_quadratic(indices[a], indices[b], 2 * PENALTY)

# Each city appears exactly once.
for city in range(N):
    indices = [variable(city, position) for position in range(N)]
    constant += PENALTY
    for i in indices:
        add_linear(i, -PENALTY)
    for a in range(len(indices)):
        for b in range(a + 1, len(indices)):
            add_quadratic(indices[a], indices[b], 2 * PENALTY)

# TSP distance objective, including return to the first city.
for position in range(N):
    next_position = (position + 1) % N
    for city_a in range(N):
        for city_b in range(N):
            if city_a == city_b:
                continue
            distance = get_distance(CITIES[city_a], CITIES[city_b])
            add_quadratic(
                variable(city_a, position),
                variable(city_b, next_position),
                distance,
            )


def qubo_to_hamiltonian(linear, quadratic, constant, num_qubits):
    pauli_terms = [("I" * num_qubits, constant)]

    for i, coefficient in linear.items():
        identity = "I" * num_qubits
        z_label = list(identity)
        z_label[num_qubits - 1 - i] = "Z"
        z_label = "".join(z_label)
        pauli_terms.append((identity, coefficient / 2))
        pauli_terms.append((z_label, -coefficient / 2))

    for (i, j), coefficient in quadratic.items():
        identity = "I" * num_qubits

        zi = list(identity)
        zi[num_qubits - 1 - i] = "Z"
        zi = "".join(zi)

        zj = list(identity)
        zj[num_qubits - 1 - j] = "Z"
        zj = "".join(zj)

        zizj = list(identity)
        zizj[num_qubits - 1 - i] = "Z"
        zizj[num_qubits - 1 - j] = "Z"
        zizj = "".join(zizj)

        pauli_terms.append((identity, coefficient / 4))
        pauli_terms.append((zi, -coefficient / 4))
        pauli_terms.append((zj, -coefficient / 4))
        pauli_terms.append((zizj, coefficient / 4))

    return SparsePauliOp.from_list(pauli_terms).simplify()


hamiltonian = qubo_to_hamiltonian(
    linear, quadratic, constant, N * N
)

qaoa_circuit = QAOAAnsatz(
    hamiltonian,
    reps=1,
    flatten=True,
)

# Decompose the QAOA blocks into gates so the visualization is genuinely gate-level.
circuit_for_display = qaoa_circuit.decompose(reps=2)

output = Path(__file__).with_name("qaoa_circuit.png")
fig = circuit_for_display.draw(
    output="mpl",
    fold=-1,
    scale=0.7,
)
fig.savefig(output, dpi=180, bbox_inches="tight")
print(output)
