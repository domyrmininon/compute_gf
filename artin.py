import numpy as np

def r(a, b, n):
    if n == 0:
        return []
    else:
        return [b] + r(b, a, n - 1)
    

def rc_from_coxeter_matrix(matrix):
    def rc(a, b):
        return r(a, b, matrix[a-1, b-1] - 1), r(b, a, matrix[a-1, b-1] - 1)
    return rc
    

def matrix_from_graph(n, edges):
    matrix = np.full((n, n), 2, dtype=int)
    for i in range(n):
        matrix[i, i] = 1
    for edge in edges:
        i, j, m = edge
        matrix[i-1, j-1] = m
        matrix[j-1, i-1] = m
    return matrix

### Classic coxeter matrix

#Spherical
# Type A
def get_coxeter_matrix_of_type_A(n):
    graph = [(i, i+1, 3) for i in range(1, n)]
    return matrix_from_graph(n, graph)

# Type B = Type C
def get_coxeter_matrix_of_type_B(n):
    graph = [(1,2,4)] + [(i, i+1, 3) for i in range(2, n)]
    return matrix_from_graph(n, graph)

def get_coxeter_matrix_of_type_C(n):
    return get_coxeter_matrix_of_type_B(n)

# Type D
def get_coxeter_matrix_of_type_D(n):
    graph = [(1,3,3), (2,3,3)] + [(i, i+1, 3) for i in range(3, n-1)]
    return matrix_from_graph(n, graph)

# Type F
def get_coxeter_matrix_of_type_F(n): # Only for n = 4, type F of rank 4
    assert n == 4
    graph = [(1,2,3), (2,3,4), (3,4,3)]
    return matrix_from_graph(n, graph)

#Affine
# Type A affine
def get_coxeter_matrix_of_type_A_affine(n):  # n generators means type A affine of rank n-1
    graph = [(i, i+1, 3) for i in range(1, n)] + [(n, 1, 3)]
    return matrix_from_graph(n, graph)

# Type B affine
def get_coxeter_matrix_of_type_B_affine(n):  # n generators means type B affine of rank n-1
    graph = [(1,2,4)] + [(i, i+1, 3) for i in range(2, n-1)] + [(n-2, n, 3)]
    return matrix_from_graph(n, graph)

# Type C affine
def get_coxeter_matrix_of_type_C_affine(n):
    graph = [(1,2,4)] + [(i, i+1, 3) for i in range(2, n-1)] + [(n-1, n, 4)]
    return matrix_from_graph(n, graph)

# Type D affine
def get_coxeter_matrix_of_type_D_affine(n): # n generators means type D affine of rank n-1
    graph = [(1,3,3)] + [(i, i+1, 3) for i in range(2, n-1)] + [(n-2, n, 3)]
    return matrix_from_graph(n, graph)

# Type F affine
def get_coxeter_matrix_of_type_F_affine(n): # Only for n = 5, type F affine of rank 4
    assert n == 5
    graph = [(1,2,3), (2,3,4), (3,4,3), (4,5,3)]
    return matrix_from_graph(n, graph)

# Type G affine
def get_coxeter_matrix_of_type_G_affine(n): # Only for n = 3, type G affine of rank 2
    assert n == 3
    graph  = [(1,2,6)] + [(i, i+1, 3) for i in range(2, n)]
    return matrix_from_graph(n, graph)


