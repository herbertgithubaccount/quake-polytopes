import pypoman
import numpy as np
vector_list = [
    (( 256, 64, 16 ), ( 256, 64, 0 ), ( 256, 0, 16 )),
    (( 0, 0, 0 ), ( 0, 64, 0 ), ( 0, 0, 16 )),
    (( 64, 256, 16 ), ( 0, 256, 16 ), ( 64, 256, 0 )),
    (( 0, 0, 0 ), ( 0, 0, 16 ), ( 64, 0, 0 )),
    (( 64, 64, 0 ), ( 64, 0, 0 ), ( 0, 64, 0 )),
    (( 0, 0, -64 ), ( 64, 0, -64 ), ( 0, 64, -64 ))
]
A = []
b = []
for i in range(0, len(vector_list)):
    p1, p2, p3 = vector_list[i]

    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    print(f"{p1 = !s}")
    print(f"{p2 = !s}")
    print(f"{p3 = !s}")
    
    normal = np.cross(p3 - p1, p2 - p1)
    normal = normal / np.linalg.norm(normal)

    A.append(normal)
    b.append(np.dot(p1, normal))
    
    print(f"{normal = !s}")
    print(f"{np.dot(p1, normal) = !s}")
    
A = np.array(A)
b = np.array(b)
from pypoman import compute_polytope_vertices

vertices = compute_polytope_vertices(A, b)

# if __name__ == '__main__':
