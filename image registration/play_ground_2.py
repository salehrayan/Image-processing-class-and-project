import numpy as np

points_in_sheared = np.array([[130,211], [152,327], [131, 371], [361, 432]])
points_in_original = np.array([[106,117], [107,220], [75, 282], [325, 180]])

A = np.empty((4,4))
B_for_height = np.empty([4])
B_for_width = np.empty([4])
for i in range(4):
    aheight = points_in_sheared[i,0]
    awidth = points_in_sheared[i,1]
    A_temp = np.array([aheight, awidth, aheight*awidth, 1])
    A[i] = A_temp
    B_for_height[i] = points_in_original[i,0]
    B_for_width[i] = points_in_original[i,1]

solution_for_height = np.linalg.solve(A, B_for_height)
solution_for_width = np.linalg.solve(A, B_for_width)

print(solution_for_width)