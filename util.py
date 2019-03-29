# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import json, os, sys, types, re

reload(sys)
sys.setdefaultencoding('utf-8')


def readJsonFile(file):
    if False == os.path.exists(file):
        return {}
    f = open(file, 'r')
    contents = f.read()
    jsonObj = json.loads(contents)
    f.close()
    return jsonObj


def writeLinesFile(lines, file):
    dir = os.path.dirname(file)
    if False == os.path.exists(dir):
        os.makedirs(dir)

    fp = open(file, 'w')
    for i in range(len(lines)):
        fp.write(lines[i] + '\n')
    fp.flush()
    fp.close()


def space(lel, type='tab'):
    speed = '    '
    ret = ''
    for l in range(0, lel):
        ret += speed

    return ret


'''types取值：

　　BooleanType 
　　BufferType 
　　BuiltinFunctionType 
　　BuiltinMethodType 
　　ClassType 
　　CodeType 
　　ComplexType 
　　DictProxyType 
　　DictType 
　　DictionaryType 
　　EllipsisType 
　　FileType 
　　FloatType 
　　FrameType 
　　FunctionType 
　　GeneratorType 
　　GetSetDescriptorType 
　　InstanceType 
　　IntType 
　　LambdaType 
　　ListType 
　　LongType 
　　MemberDescriptorType 
　　MethodType 
　　ModuleType 
　　NoneType 
　　NotImplementedType 
　　ObjectType 
　　SliceType 
　　StringType 
　　StringTypes 
　　TracebackType 
　　TupleType 
　　TypeType 
　　UnboundMethodType 
　　UnicodeType 
　　XRangeType

'''


def getValueType(value):
    valueType = type(value)
    return valueType


def getValueTypeString(value):
    tString = 'string'
    valueType = getValueType(value)
    if valueType == types.UnicodeType or valueType == types.StringType:
        tString = 'string'
    elif valueType == types.IntType:
        tString = 'int'
    elif valueType == types.FloatType:
        tString = 'float'
    elif valueType == types.DictType:
        tString = 'dict'
    elif valueType == types.ListType:
        tString = 'list'
    elif valueType == types.BooleanType:
        tString = 'bool'

    return tString


def isDictType(value):
    return getValueType(value) == types.DictType


def isListType(value):
    return getValueType(value) == types.ListType


# 首字母大写
def firstUpper(x):

    if x == None or len(x) == 0:
        return x
    return x[:1].upper() + x[1:]

# 驼峰转下划线
def isNumberBegin(x):

    if x == None or len(x) == 0:
        return False
    return x[:1].isdigit()



# 驼峰转下划线
def camelToUnderlines(x):
    prefix = re.split('([a-zA-Z])', x, 1)[0]
    x = re.sub('([A-Z])', lambda match: '_' + match.group().lower(), x)
    if x[0] == '_':
        x = x[1:]
    return prefix + x


# 下划线转大驼峰
def underlinesToCamel(x):
    prefix = re.split('([a-zA-Z])', x, 1)[0]

    if x[0] != '_':
        x = '_' + x
    x = re.sub('_([a-z])', lambda match: match.group(1).upper(), x)
    if x[0] == '_':
        x = x[1:]
    return prefix + x


def transStr(file_path, cmToUs_or_usToCm):
    print(cmToUs_or_usToCm)
    f = open(file_path, 'r')
    if cmToUs_or_usToCm == '1':
        print("驼峰转下划线")
        for line in f.readlines():
            print(camelToUnderlines(line.strip()))
    elif cmToUs_or_usToCm == '0':
        print("下划线转大驼峰")
        for line in f.readlines():
            print(underlinesToCamel(line.strip()))

    f.close()
