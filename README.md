this wonderful project finds the vertices of objects stored in quake map files, so that they may be turned into `nif` files. this is accomplished via vertex enumeration.

usage: 
1. install the pip requirements (python 3.10-3.11 required unless you want to build from source)
2. run the `main.py` file, inputting the filepath of the quake map file to decode as a commandline argument
3. the vertices will be saved to a file in the `output` directory. this file will have the same name as the input file.
