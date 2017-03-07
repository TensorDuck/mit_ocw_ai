from neural_net import *

# test a basic neural_net and make sure it works.

i0 = Input('i0', -1.0) # this input is immutable
i1 = Input('i1', 1.0)

w1A = Weight('w1A', 1)
wA  = Weight('wA', 1)

wAB = Weight('wAB', 1)
wB = Weight('wB', 1)

# Inputs must be in the same order as their associated weights
A = Neuron('A', [i1,i0], [w1A,wA])
B = Neuron('B', [A,i0], [wAB,wB])

P = PerformanceElem(B, 0.0)

net = Network(P,[A,B])

"""
print i0.output()
print A.output()
print B.output()

print A.dOutdX(w1A)
"""
# Now do a 2-layer thing
i0 = Input('i0', -1.0) # this input is immutable
i1 = Input('i1', 1.0)
i2 = Input('i2', 0.0)

w1A = Weight('w1A', 1)
w2A = Weight('w2A', 1)
w1B = Weight('w1B', 1)
w2B = Weight('w2B', 1)
wA  = Weight('wA', 1)
wB = Weight('wB', 1)
wC = Weight('wC', 1)
wAC = Weight('wAC', 1)
wBC = Weight('wBC', 1)

A = Neuron('A', [i1, i2, i0], [w1A, w2A, wA])
B = Neuron('B', [i1, i2, i0], [w1B, w2B, wB])
C = Neuron('C', [A, B, i0], [wAC, wBC, wC])

P = PerformanceElem(C, 0.0)

net = Network(P,[A,B,C])
print A.output()
print B.output()
print C.output()

print "Second one should be zero"
print C.dOutdX(w1A)
print C.dOutdX(w2A)
