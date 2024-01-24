import pypoman
import numpy as np
import re
from pathlib import Path
# pattern used to get numbers. it gets run on each line
vector_pattern = re.compile(r"^\s*\(\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+\)\s+\(\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+\)\s+\(\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+\)")

start_pattern = re.compile(r"^\s*\{\s*$")
end_pattern = re.compile(r"^\s*\}\s*$")

OUTPUT_DIR = Path("output")
if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir()

# parses a file to get a list of all planes associated with an entity
def parse_lines(lines:[str], debug_msgs = False):

    all_vectors = []
    vector_list = []
    # parse pattern to build `vector_list`
    finding_vertices = False
    for line in lines:
        # if debug_msgs: print(f"scanning {line = }")
        if (m := re.match(vector_pattern, line)):
            numbers = [float(m[i]) for i in range(1, 10)]
            p1 = tuple(numbers[0:3])
            p2 = tuple(numbers[3:6])
            p3 = tuple(numbers[6:9])
            # p1 = (float(m[1]),float(m[2]),float(m[3]))
            # p2 = (float(m[3+1]),float(m[3+2]),float(m[3+3]))
            # p3 = (float(m[6+1]),float(m[6+2]),float(m[6+3]))
            if debug_msgs: print(f"\nfound line!\n\t{p1 = !s}\n\t{p2 = !s}\n\t{p3 = !s}")
            vector_list.append((p1,p2,p3))
        elif re.match(start_pattern, line):
        # elif line == '{\\n':
            if debug_msgs: print(f"MATCHED START\n\t{line = }")
            vector_list = []
            finding_vertices = True
        elif re.match(end_pattern, line):
            if debug_msgs: print(f"MATCHED END\n\t{line = }")

            finding_vertices = False
            if len(vector_list) > 0: all_vectors.append(vector_list)
    # print(all_vectors)
    return all_vectors
    
   

# takes in a list of vectors constituting an entity and then computes the vertices of that entity
def find_vertices(vector_list, debug_msgs = False):
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
    if debug_msgs: print(f"{A = !s}")
    if debug_msgs: print(f"{b = !s}")
    from pypoman import compute_polytope_vertices

    return compute_polytope_vertices(A, b)


def parse_file(filepath: str, debug_msgs):
    filepath = Path(filepath)
    with open(str(filepath), "r") as f:
        lines = f.readlines()
    
    all_vectors = parse_lines(lines, debug_msgs)

    all_vertices = []
    for i, vector_list in enumerate(all_vectors):
        if debug_msgs:print(f"finding with {vector_list = }")
        vertices = find_vertices(vector_list, debug_msgs)
        all_vertices.append(vertices)
        if debug_msgs: print(f"{vertices = }")
    
    output_stem = Path(filepath).with_suffix(".txt")
    output_path = OUTPUT_DIR / output_stem

    with open(str(output_path), "w") as f:
        for i, vertices in enumerate(all_vertices):
            f.write(f"mesh {i}:\n")
            for v in vertices:
                f.write(f"{v}\n")
            f.write('\n')


if __name__ == '__main__':
    import sys
    args = sys.argv
    lines = None
    filepath, debug_msgs = "data.txt", False
    if len(args) > 1: filepath = args[1]
    if len(args) > 2: debug_msgs = args[2]

    parse_file(filepath, debug_msgs)
    
    
    
