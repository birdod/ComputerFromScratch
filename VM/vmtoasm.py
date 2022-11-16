import argparse
import os
from Myparser import Parser
from CodeWriter import CodeWriter
C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, \
C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL = [i for i in range(9)]

def parser_list():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('path')
    path = argparser.parse_args().path
    ret = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.split('.')[1]!='vm':
                continue
            with open(path + file, "r") as f:
                ret.append((Parser(f.read()), file.split('.')[0]))
    else:
        with open(path, "r") as f:
            ret.append((Parser(f.read()), path.split('/')[-1].split('.')[0]))
    return ret, path



if __name__=='__main__':
    Plist, path = parser_list()
    writer = CodeWriter()
    if os.path.isdir(path):
        writer.setFileName(path + path.split('/')[-2] + '.asm')
    else:
        writer.setFileName(path[:-3] + 'asm')

    writer.writeInit()
    for parser, name in Plist:
        writer.current_file = name
        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType()==C_ARITHMETIC:
                writer.writeArithmetic(parser.arg1())
            elif parser.commandType()==C_PUSH:
                writer.writePushPop('push', parser.arg1(), parser.arg2())
            elif parser.commandType()==C_POP:
                writer.writePushPop('pop', parser.arg1(), parser.arg2())
            elif parser.commandType()==C_LABEL:
                writer.writeLabel(parser.arg1())
            elif parser.commandType()==C_GOTO:
                writer.writeGoto(parser.arg1())
            elif parser.commandType()==C_IF:
                writer.writeIf(parser.arg1())
            elif parser.commandType()==C_FUNCTION:
                writer.writeFunction(parser.arg1(),parser.arg2())
            elif parser.commandType()==C_CALL:
                writer.writeCall(parser.arg1(), parser.arg2())
            elif parser.commandType()==C_RETURN:
                writer.writeReturn()

    writer.close()



