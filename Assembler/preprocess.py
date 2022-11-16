

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
                    lines[j] = line[:i].replace(' ', '')
                    break
    ret = []
    for i in lines:
        if i!='':
            ret.append(i)
    
    return ret

def symbol(data):
    st = {'SP':'0','LCL':'1','ARG':'2','THIS':'3','THAT':'4','SCREEN':'16384','KBD':'24576'}
    for i in range(16):
        st['R'+str(i)] = str(i)
    cnt = 0
    for i, line in enumerate(data):
        if line[0]=='(':
            st[line[1:-1]] = str(cnt)
        else:
            cnt += 1
    cnt = 16
    for i, line in enumerate(data):
        if line[0]=='@':
            if line[1:] in st.keys():
                data[i]=data[i].replace(line[1:], st[line[1:]])
            else:
                st[line[1:]] = cnt
                cnt += 1
                data[i]=data[i].replace(line[1:], st[line[1:]])
                
    return data

def clear(data):
    data = pre(data)
    data = symbol(data)
    return data