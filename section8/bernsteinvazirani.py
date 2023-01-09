"""
The Bernstein-Vazirani (BV) alg. is used to determine the nature of a black-box boolean function.
BV was the first alg. developed that showe a clear separation between quantum and classical computing EVEN allowing for small errors.
BV problem statement:
Given an unknown function f of n inputs:
f(x_{n-1}, x_{n-2}, ... x_1, x_0),

let a be an unknown non-negative integer x and modulo-2 sum x multiplied by a.
So the output of the function is:

a * x = a_0x_0 (+) a_1x_1 (+) a_2x_2 ...

find a in one query of the oracle
"""

import random
import cirq

def main():
    qubit_count = 8

    circuit_sample_count = 3

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)

    # Pick coefficients for oracle and create a circuit to query it
    secret_bias_bit = random.randint(0, 1)
    secret_factor_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    oracle = make_oracle(input_qubits, output_qubit, secret_factor_bits, secret_bias_bit)
    print(f"Secret function:\nf(x) = x*<{''.join(str(e) for e in secret_factor_bits)}> + {secret_bias_bit} (mod 2)")

    # Embed oracle into special quantum circuit, querying it exactly once
    circuit = make_bernstein_vazirani_circuit(input_qubits, output_qubit, oracle)
    print(f"Circuit:\n{circuit}")

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)
    frequencies = result.histogram(key='result', fold_func=bitstring)
    print(f"Sampled results:\n{frequencies}")

    # Make sure we found secret value
    most_common_bitstring = frequencies.most_common(1)[0][0]
    print(f"Most common matches secret factors:\n{most_common_bitstring == bitstring(secret_factor_bits)}")

def make_oracle(input_qubits, output_qubit, secret_factor_bits, secret_bias_bit):
    """ Gates implementing the function f(a) = a*factors + bias (mod 2)"""
    if secret_bias_bit:
        yield cirq.X(output_qubit)
    
    for qubit, bit in zip(input_qubits, secret_factor_bits):
        if bit:
            yield cirq.CNOT(qubit, output_qubit)

def make_bernstein_vazirani_circuit(input_qubits, output_qubit, oracle):
    """ Solves for factors in f(a) = a*factors + bias (mod 2) with one query. """
    c = cirq.Circuit()

    c.append([
        cirq.X(output_qubit),
        cirq.H(output_qubit),
        cirq.H.on_each(*input_qubits),
    ])

    # Query oracle once
    c.append(oracle)

    # Measure in X basis
    c.append([
        cirq.H.on_each(*input_qubits),
        cirq.measure(*input_qubits, key='result'),
    ])

    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == "__main__":
    main()
