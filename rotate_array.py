#!/usr/bin/python

import sys
import math

# 75, 89, 11, 23, 38, 39, 40, 52, 66
#a = [ 39, 40, 52, 66, 75, 89, 11, 23, 38 ]
a = [ 11, 23, 38, 39, 40, 52, 66, 75, 89, 100 ]
#a = [ 45, 50, 60, 10, 20, 30, 40 ]
l = len(a)

def find(x, st, en):
    print st, en
    
    while st <= en:
        m = (st + en)/2
        if x == a[m]:
            return m
        elif x > a[m]:
            if a[en] > a[m] and x <= a[en]:
                st = m + 1
            else:
                en = m - 1
        else:
            if a[st] < a[m] and x >= a[st]:
                en = m -1
            else:
                st = m + 1         
        return find(x, st, en)
    return -1
    
x = int(sys.argv[1])
print a
i = find(x, 0, l-1)
print "i =", i