import matplotlib.pyplot as plt
import sympy

import cirq

qbit = cirq.LineQubit(0)
circ = cirq.Circuit()

symbol = sympy.Symbol("t")

circ.append(cirq.XPowGate(exponent=symbol)(qbit))

circ.append(cirq.measure(qbit, key="z"))

print("Circuit:")
print(circ)

sweep = cirq.Linspace(key=symbol.name, start=0.0, stop=2.0, length=100)

sim = cirq.Simulator()
res = sim.run_sweep(circ, sweep, repetitions=1000)

angles = [x[0][1] for x in sweep.param_tuples()]
zeroes = [res[i].histogram(key="z")[0] / 1000 for i in range(len(res))]
plt.plot(angles, zeroes, "--", linewidth=3)

plt.ylabel("Frequency of 0 Measurements")
plt.xlabel("Exponent of X gate")
plt.grid()

plt.savefig("param-sweep-cirq.pdf", format="pdf")