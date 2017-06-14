#!/usr/bin/env python

a = [66.25, 333, 333, 1, 1234.5]
print("\na=", a)

print("\na.count(333) = %d, a.count(66.25) = %d, a.count('x') = %d" % (a.count(333), a.count(66.25), a.count('x')) )

print("\na.insert(2, -1) = ", a.insert(2, -1))
print("a = ", a)

print("\na.append(333) = ", a.append(333))
print("a = ", a)

print("\na.index(333) = ", a.index(333))
print("a = ", a)

print("\na.remove(333) = ", a.remove(333))
print("a = ", a)

print("\na.reverse() = ", a.reverse())
print("a = ", a)

print("\na.sort() = ", a.sort())
print("a = ", a)

print("\na.pop() = ", a.pop())
print("a = ", a)