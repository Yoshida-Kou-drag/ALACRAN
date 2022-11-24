import numpy as np

body_range = np.array([[1,2,3],
                     [4,5,6],
                     [7,8,9,]
                     ])
left_arm = np.array([[1,2],
                     [3,4],
                     ])
print(body_range[:,1:2])
print(left_arm[1:1])
for i in range(5):
    print(i)

l = np.array([0, 1, 2, 3, 4])

l[0], l[3] = l[3], l[0]

print("sort",l)
# [3, 1, 2, 0, 4]
