#!/usr/bin/env python

a = 0
b = 1
c = 2
def my_function():
    a = 3
    print("a = %d" % (a) )

def my_b():
    global b
    b = 11
    print("b = %d" % (b) )
    
def my_c():
    print("c = %d" % (c) )
    c = 22
    print("c = %d" % (c) )

my_function()
print("a = %d" % (a) )
my_b()
print("b = %d" % (b) )
my_c()
print("c = %d" % (c) )