from collections import deque


x= deque(maxlen=2)

x.append((1,2))
x.append((3,4))
print(x)
x.append((4,5))
print()