import numpy as np

# arr1 = np.array([[1,2,3], [3,4,5]])
# arr2 = np.array([[0,0,0], [1,1,1]])

# print(arr1)
# print(arr2)

# arr_list = [arr1,arr2]
# arr3 = np.array([arr for arr in arr_list])
# print(arr3)

zeros = np.zeros(shape=(640, 3431))
zeros_list = [zeros for _ in range(5)]
print(type(zeros_list))

zeross = np.array([np.zeros(shape=(640, i*1000+1000)) for i in range(5)])
print(type(zeross))
print(zeross[:3])