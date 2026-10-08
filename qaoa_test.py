from qiskit import QuantumCircuit

# Create a 4-qubit quantum circuit
qc = QuantumCircuit(4)

# Put all 4 qubits into superposition
qc.h(range(4))

# Display the circuit
print(qc)