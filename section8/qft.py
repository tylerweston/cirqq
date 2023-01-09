"""
Quantum Fourier Transform

QFT is a method to set up the amplitudes for measurement that will favor the qubit which has the info we want.
We can implement a QFT circuit on NISQ hardware in a straightforward manner.
"""

import numpy as np
import cirq

def main():
    qft_circuit = generate_2x2_grid_qft_circuit()
    print(f"Circuit:\n{qft_circuit}")

    simulator = cirq.Simulator()
    result = simulator.simulate(qft_circuit)

    # Note in book and website they use final_state but this needs to be final_state_vector in newer Cirq versions
    print(f"\nFinal state:{np.around(result.final_state_vector, 3)}")

def cz_and_swap(q0, q1, rot):
    """ Yields a controlled-R_z gate and SWAP gate on input qubits"""
    yield cirq.CZ(q0, q1)**rot
    yield cirq.SWAP(q0, q1)


def generate_2x2_grid_qft_circuit():
    """ Returns a QFT circuit o a 2x2 planar qubit architecture"""

    a, b, c, d = [cirq.GridQubit(0, 0), cirq.GridQubit(0, 1), cirq.GridQubit(1, 1), cirq.GridQubit(1, 0)]

    circuit = cirq.Circuit(
        cirq.H(a),
        cz_and_swap(a, b, 0.5),
        cz_and_swap(b, c, 0.25),
        cz_and_swap(c, d, 0.125),
        cirq.H(a),
        cz_and_swap(a, b, 0.5),
        cz_and_swap(b, c, 0.25),
        cirq.H(a),
        cz_and_swap(a, b, 0.5),
        cirq.H(a),
        strategy=cirq.InsertStrategy.EARLIEST,
    )

    return circuit

if __name__ == "__main__":
    main()