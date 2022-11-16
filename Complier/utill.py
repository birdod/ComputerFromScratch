symbols = set(['{','}','(',')','[',']','.',',',';','+','-','*','/','&',
'|','<','>','=','~'])
kindmap = {"arg": "argument", "static": "static", "field":"this", "var":"local"}
opmap = {"+":"add", "-": "sub", "*": "call Math.multiply 2","/":"call Math.divide 2", "&": "and", "|": "or", "<": "lt", ">": "gt", "=":"eq"}
uopmap = {"~": "not", "-": "neg"}


class type:
    KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST = [i for i in range(5)]
class lexical:
    symbols = set(['{','}','(',')','[',']','.',',',';','+','-','*','/','&',
    '|','<','>','=','~'])
    keyword = set(['class', 'constructor', 'function', 'methid', 'field', 'static',
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
    'this', 'let', 'do', 'if', 'else', 'while', 'return'])
    statement = set(['let', 'if', 'while', 'do', 'return', 'else'])
    op = set(['+','-','*','/','&','|','<','>','='])
    uop = set(['~','-'])

    
def pre(data):
    data = comment_handle(data)
    tokens = []
    for line in data:
        line_handle(line,tokens)
    ret = []
    for element in tokens:
        if element != "":
            ret.append(element)
    return ret

def comment_handle(data):

    lines = data.split('\n')
    for j, line in enumerate(lines):
        lines[j] = line.strip()
        if len(lines[j])>0 and lines[j][0] == '*':
            lines[j] = ''
            continue
        for i, element in enumerate(line):
            if element=='/' and line[i+1] == '/':
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


def line_handle(line, tokens):
    
    SconstParse = line.split("\"")
    for i in range(len(SconstParse)):
        if i%2:
            tokens.append("\"" + SconstParse[i].strip() + "\"")
        else:
            nonS_handle(SconstParse[i], tokens)


def nonS_handle(part, tokens):
    wordlist = part.split(' ')
    for word in wordlist:
        j = 0
        for i, element in enumerate(word):
            if element in lexical.symbols:
                tokens.append(word[j:i].strip())
                tokens.append(word[i].strip())
                j = i+1
        if j<len(word):
            tokens.append(word[j:].strip())
            
