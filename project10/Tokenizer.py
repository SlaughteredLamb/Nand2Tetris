import sys
import os

# Transtate codes in .jack file into seperate tokens
def Constructor(iname, outname):
    keyword=['class','constructor','function','method','field','static','var','int',
             'char','boolean','void','true','false','null','this','let','do','if','else','while','return']
    symbols=['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    f = open(iname, 'r')
    fOut=[]
    mark = 0
    for line in f:
        e=''
        if '//' in line:
            line = line[:line.index('//')]
        line = line.split()
        if line != []:
            if mark == 1:
                if line[-1] == '*/':
                    mark = 0
                    continue
                else:
                    continue
            if line != [] and line[0] == "/**" and mark == 0:
                if line[-1] != '*/':
                    mark = 1
                else:
                    continue
            if mark == 0 and line != []:
                for i in line:
                    e=e+i+' '
        if e!='':
            fOut.append(e)
    f.close()
    array=[]
    for line in fOut:
        word=''
        for s in line:
            if s in symbols:
                word+=' '+s+' '
            else:
                word+=s
        array+=word.split()
    array2=[]
    mark = False
    for e in array:
        if mark==True:
            array2[-1]+=' '+e
            if e[-1]=='"':
                mark=False
        else:
            array2.append(e)
            if e[0]=='"':
                mark=True
    print(array2)
    f = open(outname, 'w')
    f.write('<tokens>\n')
    dict={'<':'&lt;','>':'&gt;','&':'&amp;'}
    for e in array2:
        if e in symbols:
            if e in dict:
                e=dict[e]
            s='<symbol> '+e+' </symbol>'
        elif e in keyword:
            s='<keyword> '+e+' </keyword>'
        elif e.isdigit():
            s = '<integerConstant> ' + e + ' </integerConstant>'
        elif e[0]=='"' and e[-1]=='"':
            s = '<stringConstant> ' + e[1:-1] + ' </stringConstant>'
        else:
            s = '<identifier> '+e+' </identifier>'
        f.write(s)
        f.write('\n')
    f.write('</tokens>')
    f.close()



path = sys.argv[1]
find = 0
fileroot = []
if path[-5:] != '.jack':
    for root, dirc, file in os.walk(path):
        for e in file:
            if e[-5:] == '.jack':
                find += 1
                print('File found:', e)
                fileroot.append((root, e))
    if find == 0:
        print("No file found!")
        exit()
    confirm = input("Input Y to modify all the file found above OR Press ENTER to quit:")
    if confirm == "Y":
        for files in fileroot:
            iname = files[0] + files[1]
            outname = iname[:-5] + 'T.xml'
            Constructor(iname, outname)
else:
    outname = path[:-5] + 'T.xml'
    Constructor(path,outname)
    print(outname)