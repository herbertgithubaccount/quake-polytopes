import pypoman
import numpy as np
import re
from pathlib import Path
# ugly pattern to match input text
pattern = re.compile(r"^\s*\(\s*([\d.]+)\s*([\d.]+)\s*([\d.]+)\s*\)\s*\(\s*([\d.]+)\s*([\d.]+)\s*([\d.]+)\s*\)\s*\(\s*([\d.]+)\s*([\d.]+)\s*([\d.]+)\s*\)")

OUTPUT_DIR = Path("output")
if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir()

def parse_str(lines, debug_msgs = False):

    vector_list = []
    # parse pattern to build `vector_list`
    for line in lines:
        m = re.match(pattern, line)
        if m:
            numbers = [float(m[i]) for i in range(1,10)]
            p1 = tuple(numbers[0:3])
            p2 = tuple(numbers[3:6])
            p3 = tuple(numbers[6:9])
            # p1 = (float(m[1]),float(m[2]),float(m[3]))
            # p2 = (float(m[3+1]),float(m[3+2]),float(m[3+3]))
            # p3 = (float(m[6+1]),float(m[6+2]),float(m[6+3]))
            if debug_msgs: print(f"\nfound line!\n\t{p1 = !s}\n\t{p2 = !s}\n\t{p3 = !s}")
            vector_list.append((p1,p2,p3))
    
    A = []
    b = []
    
    for i, (p1, p2, p3) in enumerate(vector_list):
        # p1, p2, p3 = vector_list[i]

        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)
        if debug_msgs: print(f"\ncomputing line {i+1}:\n\t{p1 = !s}\n\t{p2 = !s}\n\t{p3 = !s}")

        
        normal = np.cross(p3 - p1, p2 - p1)
        normal = normal / np.linalg.norm(normal)

        A.append(normal)
        b.append(np.dot(p1, normal))
        
        if debug_msgs: print(f"\t{normal = !s}")
        if debug_msgs: print(f"\tp1 * normal = {np.dot(p1, normal)}")
        
    A = np.array(A)
    b = np.array(b)
    from pypoman import compute_polytope_vertices

    return compute_polytope_vertices(A, b)

# vector_list looks like
# vector_list = [
#     (( 256, 64, 16 ), ( 256, 64, 0 ), ( 256, 0, 16 )),
#     (( 0, 0, 0 ), ( 0, 64, 0 ), ( 0, 0, 16 )),
#     (( 64, 256, 16 ), ( 0, 256, 16 ), ( 64, 256, 0 )),
#     (( 0, 0, 0 ), ( 0, 0, 16 ), ( 64, 0, 0 )),
#     (( 64, 64, 0 ), ( 64, 0, 0 ), ( 0, 64, 0 )),
#     (( 0, 0, -64 ), ( 64, 0, -64 ), ( 0, 64, -64 ))
# ]

# print(f"printing vertices...\n{np.array(vertices)}")
if __name__ == '__main__':
    import sys
    args = sys.argv
    lines = None
    filepath, debug_msgs = "data.txt", False
    if len(args) > 1: filepath = args[1]
    if len(args) > 2: debug_msgs = args[2]
    
    
    filepath = Path(filepath)
    with open(str(filepath),"r") as f:
        lines = f.readlines()

    results = np.array(parse_str(lines, debug_msgs))

    outputpath = OUTPUT_DIR / str(filepath.name)
    with open(str(outputpath), "w") as f:
        f.write(str(results))
