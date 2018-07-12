# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import json, os, sys, types

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
    print valueType
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
    return tString


def isDictType(value):
    return getValueType(value) == types.DictType


def isListType(value):
    return getValueType(value) == types.ListType
