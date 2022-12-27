"""Initialize a qubit to 0 and perform a not on it. Repeat 10 trials."""

import cirq

qubit = cirq.GridQubit(0, 0)

circuit = cirq.Circuit(
    cirq.X(qubit),                  # NOT
    cirq.measure(qubit, key='m')    # Measurement
)

print("Circuit:")
print(circuit)

simulator = cirq.Simulator()

result = simulator.run(circuit, repetitions=10)

print("Results:")
print(result)