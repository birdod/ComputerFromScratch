from CompilationEngine import CompilationEngine
import argparse
import os


if __name__ == "__main__":
    static = 0
    argparser = argparse.ArgumentParser()
    argparser.add_argument('path')
    path = argparser.parse_args().path

    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.split('.')[1]!='jack':
                continue
            with open(path + file, "r") as f:
                data = f.read()
            static = CompilationEngine((path+file).replace('.jack','.vm'), data, static).table.static
    else:
        with open(path, "r") as f:
            data = f.read()

        CompilationEngine(path.replace('.jack','.vm'), data, static)

