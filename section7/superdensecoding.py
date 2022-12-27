import cirq

def bitstring(bits):
    return ''.join('1' if e else '0' for e in bits)

qreg = [cirq.LineQubit(x) for x in range(2)]
circ = cirq.Circuit()

message = {
    "01": [cirq.X(qreg[0])],
    "10": [cirq.Z(qreg[0])],
    "11": [cirq.X(qreg[0]), cirq.Z(qreg[0])]
}

# Alice creates a Bell pair
circ.append(cirq.H(qreg[0]))
circ.append(cirq.CNOT(qreg[0], qreg[1]))

# Alice picks a message to send
m = "01"
print(f"Alice's sent message is {m}")

# Alice encodes message
circ.append(message[m])

# Bob measures in Bell basis
circ.append(cirq.CNOT(qreg[0], qreg[1]))
circ.append(cirq.H(qreg[0]))
circ.append([cirq.measure(qreg[0]), cirq.measure(qreg[1])])

print("\nCircuit:")
print(circ)

sim = cirq.Simulator()
res = sim.run(circ, repetitions=1)

print(f"\nBob's received message is {bitstring(res.measurements.values())}")
