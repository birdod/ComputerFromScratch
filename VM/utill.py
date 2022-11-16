def pre(data):
    lines = data.split('\n')
    for j, line in enumerate(lines):
        lines[j] = line.strip()
        for i, element in enumerate(line):
            if element=='/':
                if i==0:
                    lines[j] = ''
                    break
                else:
                    lines[j] = line[:i].strip()
                    break
    ret = []
    for i in lines:
        if i!='':
            ret.append(i)
    
    return ret


def arithmetic_cmdtoasm(ifcnt, command):
    if command=='add':
        ret = \
"""

    @SP
    A=M
    A=A-1
    D=M
    A=A-1
    M=D+M
    @SP
    M=M-1

"""
    elif command == 'sub':
        ret = \
"""

    @SP
    A=M
    A=A-1
    D=M
    A=A-1
    M=M-D
    @SP
    M=M-1

"""
    elif command == 'neg':
        ret = \
"""

    @SP
    A=M
    A=A-1
    M=-M

"""
    elif command == 'eq':
        ret = \
f"""

    @SP
    A=M
    A=A-1
    D=M
    A=A-1
    D=D-M;
    @true{ifcnt}
    D;JEQ
    @SP
    A=M
    A=A-1
    A=A-1
    M=0
    @end{ifcnt}
    1;JMP
(true{ifcnt})
    @SP
    A=M
    A=A-1
    A=A-1
    M=1
    M=-M
(end{ifcnt})
    @SP
    M=M-1

"""
    elif command == 'gt':
        ret = \
f"""

    @SP
    A=M
    A=A-1
    D=M
    A=A-1
    D=M-D;
    @true{ifcnt}
    D;JGT
    @SP
    A=M
    A=A-1
    A=A-1
    M=0
    @end{ifcnt}
    1;JMP
(true{ifcnt})
    @SP
    A=M
    A=A-1
    A=A-1
    M=1
    M=-M
(end{ifcnt})
    @SP
    M=M-1

"""
    elif command == 'lt':
        ret = \
f"""

    @SP
    A=M
    A=A-1
    D=M
    A=A-1
    D=M-D;
    @true{ifcnt}
    D;JLT
    @SP
    A=M
    A=A-1
    A=A-1
    M=0
    @end{ifcnt}
    1;JMP
(true{ifcnt})
    @SP
    A=M
    A=A-1
    A=A-1
    M=1
    M=-M
(end{ifcnt})
    @SP
    M=M-1

"""
    elif command == 'and':
        ret = \
"""

    @SP
    A=M
    A=A-1
    D=M
    A=A-1
    M=D&M
    @SP
    M=M-1

"""
    elif command == 'or':
        ret = \
"""

    @SP
    A=M
    A=A-1
    D=M
    A=A-1
    M=D|M
    @SP
    M=M-1

"""
    elif command == 'not':
        ret = \
"""

    @SP
    A=M
    A=A-1
    M=!M

"""
    return ret


def pushpop_cmdtoasm(Xxx, command, segment, index):


    if command == 'push':
        if segment == 'constant':
            ret = \
f"""

    @{index}
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
        elif segment == 'local':
            ret = \
f"""

    @LCL
    D=M
    @{index}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
        elif segment == 'argument':
            ret = \
f"""

    @ARG
    D=M
    @{index}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
        elif segment == 'this':
            ret = \
f"""

    @THIS
    D=M
    @{index}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
        elif segment == 'that':
            ret = \
f"""

    @THAT
    D=M
    @{index}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
        elif segment == 'pointer':
            ret = \
f"""

    @3
    D=A
    @{index}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
        elif segment == 'temp':
            ret = \
f"""

    @5
    D=A
    @{index}
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
        elif segment == 'static':
            ret = \
f"""

    @{Xxx+'.'+str(index)}
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

"""
    elif command == 'pop':
        if segment == 'local':
            ret = \
f"""

    @{index}
    D=A
    @LCL
    M=M+D

    @SP
    M=M-1
    A=M
    D=M

    @LCL
    A=M
    M=D

    @{index}
    D=A
    @LCL
    M=M-D

"""
        elif segment == 'argument':
            ret = \
f"""

    @{index}
    D=A
    @ARG
    M=M+D

    @SP
    M=M-1
    A=M
    D=M

    @ARG
    A=M
    M=D

    @{index}
    D=A
    @ARG
    M=M-D

"""
        elif segment == 'this':
            ret = \
f"""

    @{index}
    D=A
    @THIS
    M=M+D

    @SP
    M=M-1
    A=M
    D=M

    @THIS
    A=M
    M=D

    @{index}
    D=A
    @THIS
    M=M-D

"""
        elif segment == 'that':
            ret = \
f"""

    @{index}
    D=A
    @THAT
    M=M+D

    @SP
    M=M-1
    A=M
    D=M

    @THAT
    A=M
    M=D

    @{index}
    D=A
    @THAT
    M=M-D

"""
        elif segment == 'pointer':
            ret = \
f"""

    @{index}
    D=A
    @3
    D=D+A
    @SP
    A=M
    M=D

    @SP
    A=M-1
    D=M
    @SP
    A=M
    A=M
    M=D

    @SP
    M=M-1

"""
        elif segment == 'temp':
            ret = \
f"""

    @{index}
    D=A
    @5
    D=D+A
    @SP
    A=M
    M=D

    @SP
    A=M-1
    D=M
    @SP
    A=M
    A=M
    M=D

    @SP
    M=M-1

"""
        elif segment == 'static':
            ret = \
f"""
    
    @SP
    M=M-1
    A=M
    D=M
    @{Xxx+'.'+str(index)}
    M=D

"""
    return ret


def label_cmdtoasm(functionName, label):
    ret =\
f"""

({functionName}${label})

"""
    return ret


def goto_command(functionName, label):
    ret =\
f"""

    @{functionName}${label}
    0;JMP

"""
    return ret


def if_command(functionName, label):
    ret =\
f"""

    @SP
    M=M-1
    A=M
    D=M
    @{functionName}${label}
    D;JNE

"""
    return ret


def call_command(call_cnt, functionName, numArgs):
    ret =\
f"""

    @return{call_cnt}
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1

    @LCL
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

    @ARG
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

    @THIS
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

    @THAT
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1

    @{numArgs}
    D=A
    @5
    D=A+D
    @SP
    D=M-D
    @ARG
    M=D

    @SP
    D=M
    @LCL
    M=D

    @{functionName}
    0;JMP
(return{call_cnt})
"""
    return ret


def return_command():
    ret =\
f"""
    @LCL
    D=M
    @FRAME
    M=D

    @5
    A=D-A
    D=M
    @RET
    M=D

    @SP
    M=M-1
    A=M
    D=M
    @ARG
    A=M
    M=D

    @ARG
    D=M+1
    @SP
    M=D

    @FRAME
    D=M
    @1
    A=D-A
    D=M
    @THAT
    M=D

    @FRAME
    D=M
    @2
    A=D-A
    D=M
    @THIS
    M=D

    @FRAME
    D=M
    @3
    A=D-A
    D=M
    @ARG
    M=D

    @FRAME
    D=M
    @4
    A=D-A
    D=M
    @LCL
    M=D

    @RET
    A=M
    0;JMP

"""
    return ret

def function_command(functionName, numLocals):
    ret =\
f"""
({functionName})
"""
    for i in range(numLocals):
        ret +=\
f"""
    @SP
    A=M
    M=0
    @SP
    M=M+1
"""
    return ret