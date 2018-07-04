#encoding:utf-8

import os
import time

# 获取指定路径下所有指定后缀的文件
# dir 指定路径
# ext 指定后缀，链表&不需要带点 或者不指定。例子：['.xml', '.java']
def GetFileFromThisRootDir(dir,ext):
    allfiles = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == ext:
                filepath = os.path.join(dir, filename)
                print ("Find [" + ext + "] file >> " + filepath)
                allfiles.append(filepath)
    return allfiles

# 写文件
def WriteFile(file_path,infos):
    file_object = open(file_path, "a") # 追加写文件
    try:
        file_object.writelines(infos)
    finally:
        file_object.close()

# 拿到文件名+后缀名
def GetFileNameAndExt(filename):
    (filepath,tempfilename) = os.path.split(filename);
    (shotname,extension) = os.path.splitext(tempfilename);
    return [shotname,extension]

# 拿到当前时间
def GetCurrentTime():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    return time.strftime( ISOTIMEFORMAT, time.localtime() )

# 实现字母自增
def LetterAutoIncrement(letter):
    lst=list(letter)
    length=len(lst)
    if not length == 0:
        # 不为空
        needAdd = 'True'
        # 倒叙遍历
        for i in range(len(lst))[::-1]:
            str=lst[i]
            if needAdd == 'True':
                if not str=='z':
                    needAdd='False'
                    assValue=ord(str)
                    assValue+=1
                    lst[i]=chr(assValue)
                else:
                    lst[i]='a'
            
            if needAdd == 'True' and i == 0:
                # 需要向前进一位了
                lst.insert(0, 'a')
    else:
        # 如果传进来的参数为空那么就从a开始吧
        return 'a'
    
    return ''.join(lst)


