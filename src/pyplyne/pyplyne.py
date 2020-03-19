import os

def pyplyne(f, directory):
    for file in os.listdir(directory):
        f(file)

pyplyne(lambda x: print(x), "/")
