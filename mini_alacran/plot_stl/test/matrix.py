import numpy as np
a = np.arange(12).reshape((3, 4))
b = a
a= a[:,1:2]
print(a)
# print(a[:,1:2 ])
print(b)

# for i in a:
#     print("i =",i[0])