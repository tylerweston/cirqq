"""
Simon's Problem

Soon after BV, Daniel Simon demo'd the ability of a QC to determine periodicity of a function exponentially faster than a CC.

Problem statement:

Consider an oracle that implements a function mapping an n-bit string to an m-bit string,
f:{0,1}^n -> {0,1}^m, where m >= n. It is given that f is a 1:1 function, or a 2:1 function
with a non-zero period s in {0,1}^n s.th. for all x, x_0 we have f(x) = f(x_0) iff x_0 = x (+) s,
where (+) corresponds with addition modulo 2. Determine the type of the function f, and if it is
2:1, determine the period s.

"""

# TODO: Code for this is given on the books website