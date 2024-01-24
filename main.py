import pypoman
import numpy as np
import re
text = '''
// brush 4
{
( 349.54787234042305 64 79.0904255319148 ) ( 349.54787234042305 29.675531914894236 79.0904255319148 ) ( 349.54787234042305 29.675531914894236 18.75 ) Tx_hlaalu_wall2_01 129.11389 -60.753605 180 0.28892803 0.2509501
( 353.36170212765865 29.675531914894236 79.0904255319148 ) ( 353.3617021276593 29.675531914894236 18.75 ) ( 349.54787234042305 29.675531914894236 18.75 ) Tx_hlaalu_wall2_01 13.389069 19.10417 0 0.9534575 0.7980527
( 353.3617021276593 29.675531914894236 18.75 ) ( 353.3617021276593 64 18.75 ) ( 349.54787234042305 64 18.75 ) Tx_hlaalu_wall2_01 13.389069 3.1241264 0 0.9534575 0.9534575
( 349.54787234042305 64 79.0904255319148 ) ( 353.36170212765865 64 79.0904255319148 ) ( 353.36170212765865 29.675531914894236 79.0904255319148 ) Tx_hlaalu_wall2_01 13.389069 3.1241264 0 0.9534575 0.9534575
( 349.54787234042305 64 18.75 ) ( 353.3617021276593 64 18.75 ) ( 353.36170212765865 64 79.0904255319148 ) Tx_hlaalu_wall2_01 13.389069 19.10417 0 0.9534575 0.7980527
( 353.36170212765865 64 79.0904255319148 ) ( 353.3617021276593 64 18.75 ) ( 353.3617021276593 29.675531914894236 18.75 ) Tx_hlaalu_wall2_01 -3.1241264 19.10417 0 0.9534575 0.7980527
}
'''
# ugly pattern to match input text
pattern = re.compile(r"^\s*\(\s*([\d.]+)\s*([\d.]+)\s*([\d.]+)\s*\)\s*\(\s*([\d.]+)\s*([\d.]+)\s*([\d.]+)\s*\)\s*\(\s*([\d.]+)\s*([\d.]+)\s*([\d.]+)\s*\)")

vector_list = []
# parse pattern to build `vector_list`
for line in text.splitlines():
    m = re.match(pattern, line)
    if m:
        numbers = [float(m[i]) for i in range(1,10)]
        p1 = tuple(numbers[0:3])
        p2 = tuple(numbers[3:6])
        p3 = tuple(numbers[6:9])
        # p1 = (float(m[1]),float(m[2]),float(m[3]))
        # p2 = (float(m[3+1]),float(m[3+2]),float(m[3+3]))
        # p3 = (float(m[6+1]),float(m[6+2]),float(m[6+3]))
        print(f"found line! adding ( {p1}, {p2}, {p3} )")
        vector_list.append((p1,p2,p3))

# vector_list looks like
# vector_list = [
#     (( 256, 64, 16 ), ( 256, 64, 0 ), ( 256, 0, 16 )),
#     (( 0, 0, 0 ), ( 0, 64, 0 ), ( 0, 0, 16 )),
#     (( 64, 256, 16 ), ( 0, 256, 16 ), ( 64, 256, 0 )),
#     (( 0, 0, 0 ), ( 0, 0, 16 ), ( 64, 0, 0 )),
#     (( 64, 64, 0 ), ( 64, 0, 0 ), ( 0, 64, 0 )),
#     (( 0, 0, -64 ), ( 64, 0, -64 ), ( 0, 64, -64 ))
# ]
A = []
b = []
for i in range(0, len(vector_list)):
    p1, p2, p3 = vector_list[i]

    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    print(f"\ncomputing ( {p1}, {p2}, {p3} )")

    
    normal = np.cross(p3 - p1, p2 - p1)
    normal = normal / np.linalg.norm(normal)

    A.append(normal)
    b.append(np.dot(p1, normal))
    
    print(f"\t{normal = !s}")
    print(f"\t{np.dot(p1, normal) = !s}")
    
A = np.array(A)
b = np.array(b)
from pypoman import compute_polytope_vertices

vertices = compute_polytope_vertices(A, b)
print(f"printing vertices...\n{np.array(vertices)}")
# if __name__ == '__main__':
