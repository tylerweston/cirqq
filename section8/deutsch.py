import cirq

q0, q1 = cirq.LineQubit.range(2)

oracles = {
    '0': [],
    '1': [cirq.X(q1)],
    'x': [cirq.CNOT(q0, q1)],
    'notx': [cirq.CNOT(q0, q1), cirq.X(q1)]
}

def deutsch_algorithm(oracle):
    yield cirq.X(q1)
    yield cirq.H(q0), cirq.H(q1)
    yield oracle
    yield cirq.H(q0)
    yield cirq.measure(q0)

for key, oracle in oracles.items():
    print(f'Circuit for {key}...')
    print(cirq.Circuit(deutsch_algorithm(oracle)), end='\n\n')

simulator = cirq.Simulator()

for key, oracle in oracles.items():
    result = simulator.run(
        cirq.Circuit(deutsch_algorithm(oracle)),
        repetitions=10
    )
    print(f'Oracle: {key:<4} result: {result}')