import numpy as np
import cirq

def bitstring(bits):
    return ''.join('1' if e else '0' for e in bits)


def main():
    circ = make_bell_test_circuit()
    print("Circuit:")
    print(circ)

    print()
    repetitions = 75
    print(f"Simulating {repetitions} repetitions...")
    results = cirq.Simulator().run(program=circ, repetitions=repetitions)

    a = np.array(results.measurements['a'][:, 0])
    b = np.array(results.measurements['b'][:, 0])
    x = np.array(results.measurements['x'][:, 0])
    y = np.array(results.measurements['y'][:, 0])

    outcomes = a ^ b == x & y
    win_percent = len([e for e in outcomes if e]) * 100 / repetitions

    print()
    print('Results:')
    print(f'a: {bitstring(a)}')
    print(f'b: {bitstring(b)}')
    print(f'x: {bitstring(x)}')
    print(f'y: {bitstring(y)}')
    print(f'(a XOR b) == (x AND y):\n{bitstring(outcomes)}')
    print(f'Win rate: {win_percent}')

def make_bell_test_circuit():
    alice = cirq.GridQubit(0, 0)
    bob = cirq.GridQubit(1, 0)
    alice_referee = cirq.GridQubit(0, 1)
    bob_referee = cirq.GridQubit(1, 1)

    circ = cirq.Circuit()

    circ.append([
        cirq.H(alice),
        cirq.CNOT(alice, bob),
        cirq.X(alice)**-0.25,
    ])

    circ.append([
        cirq.H(alice_referee),
        cirq.H(bob_referee)
    ])

    circ.append([
        cirq.CNOT(alice_referee, alice)**0.5,
        cirq.CNOT(bob_referee, bob)**0.5,
    ])

    # Record result
    circ.append([
        cirq.measure(alice, key='a'),
        cirq.measure(bob, key='b'),
        cirq.measure(alice_referee, key='x'),
        cirq.measure(bob_referee, key='y'),
    ])

    return circ

if __name__ == "__main__":
    main()
