# encoding:utf-8

# Android File create scripts

import os, sys, os.path
import _com_util
import _config
import _android
import _ios
import _php

def do_search():
    print ("do search : "+_config.out_put_path)

    allfiles = _com_util.GetFileFromThisRootDir(_config.out_put_path, ".jproto")
    # print allfiles
    for file in allfiles:
        read_file(file)

def read_file(file):
    print ("Reading " + file)
    file_object = open(file);
    model_lists = [[]]
    model_line = []
    tag = _config.keycode_package
    line_num = 0
    try:
        for line in file_object:
            line_num += 1
            # 先保证该行有字
            line=line.strip('\n')
            if line.strip():
                # 逐行读取，让其分成多维数组存放，以model为层级标识，其中 package、注释 也是一级
                code = line
                
                if "//" in line:
                    # 如果有注释那么就提取出来单独成一行
                    start = line.index("//")
                    code = line[0:start]
                    note = line[start:]
                    model_line.append(note)
                
                if tag in code:
                    if tag == _config.keycode_package:
                        tag = _config.keycode_message
                    elif tag == _config.keycode_message:
                        tag = "}"
                    elif tag == "}":
                        model_line.append(code)
                        code = ""
                        tag = _config.keycode_message
                    else:
                        # 提示语法错误
                        str = (["Are you missing " ,tag ," in file : [" ,file,  "] line : " ,bytes(line_num)])
                        raise SyntaxError(str)
                    
                    # 证明找到标识了，清空
                    if len(model_line) > 0:
                        model_lists.append(model_line)
                        model_line = []

                if code.strip():
                    model_line.append(code)


    finally:
        file_object.close()

    protocol_file_name = _com_util.GetFileNameAndExt(file)[0]
    protocol_file_name = protocol_file_name[0 : 1].capitalize() + protocol_file_name[1 : len(protocol_file_name)]
    _android.createAndroidFile(model_lists, protocol_file_name)
    _ios.createIOSFile(model_lists, protocol_file_name)
    _php.createPHPFile(model_lists, protocol_file_name, _com_util.GetFileNameAndExt(file)[0])
    

