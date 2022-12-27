import cirq

q0, q1, q2 = cirq.LineQubit.range(3)

constant = ([], [cirq.X(q2)])

balanced = (
    [cirq.CNOT(q0, q2)],
    [cirq.CNOT(q1, q2)],
    [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2)],
    [cirq.CNOT(q0, q2), cirq.X(q2)],
    [cirq.CNOT(q1, q2), cirq.X(q2)],
    [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2), cirq.X(q2)]
)

def your_circuit(oracle):
    """yield a circuit for DJ alg on three qubits"""
    # phase kickback trick
    yield cirq.X(q2), cirq.H(q2)
    # equal superposition over input bits
    yield cirq.H(q0), cirq.H(q1)
    # query the function
    yield oracle
    # interference to get results, put last qubit into |1>
    yield cirq.H(q0), cirq.H(q1), cirq.H(q2)
    # final OR gate to put result in final qubit
    yield cirq.X(q0), cirq.X(q1), cirq.CCX(q0, q1, q2)
    yield cirq.measure(q2)

simulator = cirq.Simulator()

print("Constant functions:")
for oracle in constant:
    result = simulator.run(cirq.Circuit(your_circuit(oracle)), repetitions=10)
    print(result)

print("Balanced functions:")
for oracle in balanced:
    result = simulator.run(cirq.Circuit(your_circuit(oracle)), repetitions=10)
    print(result)