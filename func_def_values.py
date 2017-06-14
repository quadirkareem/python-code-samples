#!/usr/bin/env python

def f1(a, L=[]):
    print(L)
    L.append(a)
    return L

def f2(a, L=None):
    print(L)
    if L is None:
        L = []
    L.append(a)
    return L
    
print("f1=", f1(1))
print("f1=", f1(2))
print("f1=", f1(3))

print("f2=", f2(1))
print("f2=", f2(2))
print("f2=", f2(3))