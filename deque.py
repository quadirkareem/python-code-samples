#!/usr/bin/env python

from collections import deque

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")
queue.append("Graham")
print("queue = ", queue)

queue.popleft()
print("queue = ", queue)

queue.pop()
print("queue = ", queue)

