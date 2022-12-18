"""quantum teleportation in Cirq"""

import random
import cirq

def make_quantum_teleportation_circuit(ranX, ranY):
    circ = cirq.Circuit()
    msg, alice, bob = cirq.LineQubit.range(3)

    # Create Bell state to be shared between Alice and Bob
    circ.append([cirq.H(alice), cirq.CNOT(alice, bob)])

    # Creates a random state for the Message
    circ.append([cirq.X(msg)**ranX, cirq.Y(msg)**ranY])

    # Bell measurement of the Message and Alice's entangled qubit
    circ.append([cirq.CNOT(msg, alice), cirq.H(msg)])
    circ.append(cirq.measure(msg, alice))

    # Use the two classical bits from the Bell measurement to recover
    # the original quantum Message on Bob's entangled qubit
    circ.append([cirq.CNOT(alice, bob), cirq.CZ(msg, bob)])

    return msg, circ

def main():
    # Make a random state to teleport
    ranX = random.random()
    ranY = random.random()
    msg, circ = make_quantum_teleportation_circuit(ranX, ranY)

    # Simulate the circuit
    sim = cirq.Simulator()
    message = sim.simulate(cirq.Circuit(cirq.X(msg)**ranX, cirq.Y(msg)**ranY))

    print("Bloch Sphere of Alice's qubit:")
    b0x, b0y, b0z = cirq.bloch_vector_from_state_vector(message.final_state_vector, 0)
    print(f"x: {round(b0x, 4)} y: {round(b0y, 4)} z: {round(b0z, 4)}")

    print("\nCircuit:")
    print(circ)

    final_results = sim.simulate(circ)

    print("\nBloch Sphere of Bob's qubit:")
    b2x, b2y, b2z = cirq.bloch_vector_from_state_vector(final_results.final_state_vector, 2)
    print(f"x: {round(b2x, 4)} y: {round(b2y, 4)} z: {round(b2z, 4)}")

if __name__ == "__main__":
    main()
