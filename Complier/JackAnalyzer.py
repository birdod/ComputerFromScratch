from CompilationEngine import CompilationEngine
import argparse

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('path')
    path = argparser.parse_args().path
    with open(path, "r") as f:
        data = f.read()
    print(path.replace('.jack','.vm'))
    static = 0
    CompilationEngine(path.replace('.jack','.vm'), data,static)
