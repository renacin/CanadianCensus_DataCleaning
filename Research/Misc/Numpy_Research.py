def matrix_math():
    # Using A Numpy Array, Create A 3x3 Matrix
    mat_a = np.array([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]], dtype='int16')

    mat_b = np.array([[1, 3, 3],
                      [1, 4, 3],
                      [1, 3, 4]], dtype='int16')

    # Get The Dimensions Of Both Matrices
    print("Dimensions Of Matrix A: {}, Matrix B: {}".format(mat_a.shape, mat_b.shape))

    # Matrix Inverse
    inv_b = np.linalg.inv(mat_b)
    print(inv_b)

    # Matrix Multiplication
    print("\n")
    mul_ab = np.matmul(mat_a, mat_b)
    print(mul_ab)

    # Matrix Division
    print("\n")
    inv_b = np.linalg.inv(mat_b)
    mul_ab = np.matmul(mat_a, inv_b)
    print(mul_ab)
