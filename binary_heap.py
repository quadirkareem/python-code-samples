#!/usr/bin/python

import sys
import math

heap_list = [] # 100, 90, 80, 85, 70, 65, 44 ]

def getElement(i):
    #print i
    if 0 <= i < len(heap_list):
        return heap_list[i]
    else:
        return None

def getParentIndex(i):
    return int(math.floor((i-1)/2))

def getLeftChildIndex(i):
    return ((2 * i) + 1)

def getRightChildIndex(i):
    return ((2 * i) + 2)

def getParent(i):
    p = int(math.floor((i-1)/2))
    return getElement(p)

def getLeftChild(i):
    c = 2 * i + 1
    return getElement(c)

def getRightChild(i):
    c = 2 * i + 2
    return getElement(c)

def bubbleUp2():
    i = len(heap_list) - 1
    while i > 0:
        x = heap_list[i]
        j = getParentIndex(i)
        p = heap_list[j]
        if canBubbleUp(x, p):
            heap_list[j] = x
            heap_list[i] = p
            i = j
        else:
            break

def bubbleDown(i):
    if len(heap_list) < 2:
        return
    print i, heap_list[i]
    while i < len(heap_list):
        print heap_list
        x = heap_list[i]
        j = getLeftChildIndex(i)
        if j < len(heap_list):
            l = heap_list[j]
            if canBubbleDown(x, l):
                heap_list[j] = x
                heap_list[i] = l
                i = j
            else:
                k = getRightChildIndex(i)
                if k < len(heap_list):
                    r = heap_list[k]
                    if canBubbleDown(x, r):
                        heap_list[k] = x
                        heap_list[i] = r
                        i = k
                    else:
                        break
                else:
                    break
        else:
            break

def bubbleDown2(i):
    if len(heap_list) < 2:
        return
    print i, heap_list[i]
    print heap_list
    while i < len(heap_list):
        j = getLeftChildIndex(i)
        ti = i
        if j < len(heap_list):
            x = heap_list[i]
            l = heap_list[j]
            if canBubbleDown(x, l):
                heap_list[j] = x
                heap_list[i] = l
                ti = j
        k = getRightChildIndex(i)
        if k < len(heap_list):
            x = heap_list[i]
            r = heap_list[k]
            if canBubbleDown(x, r):
                heap_list[k] = x
                heap_list[i] = r
                ti = k
        print heap_list
        if ti == i:
            break
        else:
            i = ti

def bubbleUp():
    i = len(heap_list) - 1
    print i, heap_list[i]
    print heap_list
    while i > 0:
        x = heap_list[i]
        j = getParentIndex(i)
        p = heap_list[j]
        if canBubbleUp(x, p):
            heap_list[j] = x
            heap_list[i] = p
            i = j
        else:
            break
        print heap_list

def heapify():
    for i in reversed(range(len(heap_list))):
        bubbleDown(i) #(0)

def sort():
    for i in reversed(range(len(heap_list))):
        #swap(i, 0)
        bubbleDown(0, i)

def swap(i, j):
    tmp = heap_list[i]
    heap_list[i] = heap_list[j]
    heap_list[j] = tmp

def canBubbleUp(x, p):
    return x > p

def canBubbleDown(x, c):
    return x < c

x = """
    0
1       2
3 4     5 6
7       8       9       10      11      12      13      14
15 16   17 18   19 20   21 22   23 24   25 26   27 28   29 30
1
2
4
8
16
"""

def print_heap():
    levels = math.log(len(heap_list), 2)
    st = 0
    for i in range(levels):
        x = math.pow(2, i)
        #for j in heap_list[0, x]
        #print i

ln = len(sys.argv)
for i in range(1, ln):
    heap_list.append(int(sys.argv[i]))
    #bubbleUp(len(heap_list) - 1)

#print heap_list
#sort()

heapify()
print heap_list
for index, item in enumerate(heap_list):
        print index, item
