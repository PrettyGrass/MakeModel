# encoding:utf-8

import _com_util
import _config
import getpass


# Android 端需要生成的文件
def createIOSFile(model_lists, swift_file_name):
    print ("Writing " + swift_file_name + _config._ios_file_extra + " ...")
    # 这是最终需要写入文件的数组
    final_codes=[]
    import_values=[]
    for model in model_lists:
        #print "model =============  " + bytes(len(model))
        parseModel(model, final_codes, swift_file_name, import_values)
    
    # 最后需要一个'}'进行闭环
    # final_codes.append("}")
    _com_util.WriteFile(_config._ios_folder + swift_file_name + _config._ios_file_extra, final_codes)


# 逐个model解析
def parseModel(model, final_codes, swift_file_name, import_values):
    # 初始化一个存放該model所有参数变量的数组
    values=[]
    values_asc=[]
    values_type=[]
    num = ""
    hasAddMode = 'False'
    # 记录现在进行的model名字,方便抛异常的时候用到
    to_name = swift_file_name
    extra=""
    
    for code_line in model:
        for v in import_values:
            code_line = code_line.replace(v, '')
        
        if _config.keycode_package in code_line:
            addCopyrightNote(final_codes, code_line, swift_file_name)
        elif _config.keycode_import in code_line:
            # Add import
            addImportValues(code_line, import_values)
        elif "//" in code_line:
            # 注释
            addNote(final_codes, code_line, hasAddMode)
        elif _config.keycode_message in code_line:
            # Model
            hasAddMode = 'True'
            to_name = addModelName(final_codes, code_line)
        elif _config.keycode_value_int in code_line:
            # int
            values_type.append(_config.keycode_value_int)
            num = _com_util.LetterAutoIncrement(num)
            values_asc.append(num)
            addIntValue(final_codes, code_line, values, num)
        elif _config.keycode_value_string in code_line:
            # String
            values_type.append(_config.keycode_value_string)
            num = _com_util.LetterAutoIncrement(num)
            values_asc.append(num)
            addStringValue(final_codes, code_line, values, num)
        elif _config.keycode_value_list in code_line:
            # List
            values_type.append(_config.keycode_value_list)
            num = _com_util.LetterAutoIncrement(num)
            values_asc.append(num)
            addListValue(final_codes, code_line, values, num)
        elif _config.keycode_value_local in code_line:
            # 内部类引用
            values_type.append(_config.keycode_value_local)
            num = _com_util.LetterAutoIncrement(num)
            values_asc.append(num)
            addInsideModelMethod(final_codes, code_line, values, num)
        elif _config.keycode_value_file in code_line:
            values_type.append(_config.keycode_value_local)
            num = _com_util.LetterAutoIncrement(num)
            values_asc.append(num)
            addFileValueMethod(final_codes, code_line, values, num)
        elif "}" in code_line:
            # 这些定制方法需要添加到最后,因此放在'}'前面
            addMappingMethod(final_codes, values, values_asc, values_type, extra)
            final_codes.append("} \n")
        else :
            # 解析不出来,抛异常出去
            str = ("Can't not parse in file : [" + swift_file_name + ".jproto] is there something extra in " + to_name + " ? by " , code_line)
            raise SyntaxError(str)


def addImportValues(code_line, import_values):
    # 截取引用名
    index = code_line.find(_config.keycode_import) + len(_config.keycode_import)
    end = code_line.find(";")
    name = code_line[index : end].replace(" ", "")
    import_values.append(name + ".")


def addFileValueMethod(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_file) + len(_config.keycode_value_file)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    values.append(name)
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_ios_space + 'var ' + name + ' = ""\n')


def addMappingMethod(code, values, values_asc, values_type, extra):
    # 理论上来讲两个数组长度是一样的
    code.append("\n")
    code.append(_config.key_value_ios_space + "override func mapping(map: Map) {\n")
    code.append(_config.key_value_ios_space + "    super.mapping(map)\n")
    for i in range(len(values)):
        name = values[i]
        name_asc = values_asc[i]
        type = values_type[i]
        value_name = name
        if name == 'description':
            value_name = 'desc'
        if name == 'msg':
            value_name = 'descMsg'
        code.append(_config.key_value_ios_space + '    ' + value_name + ' <- ' + 'map["' + extra + name +'"]' + '\n')
    code.append(_config.key_value_ios_space + "}\n")


def addInsideModelMethod(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_local) + len(_config.keycode_value_local)
    end = code_line.find(";")
    
    # 去空格拿到名字
    start = code_line.find(_config.keycode_value_local) + len(_config.keycode_value_local)
    name = code_line[start : end]
    name = name[code_line.find(" ") : len(name)]
    name = name[name.find(" ") + 1 : len(name)]
    
    model_name=code_line[index : end].strip()
    model_name=model_name[0 : model_name.find(" ")]

    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_ios_space + "var " + name + ": " + model_name + " = " + model_name + "()\n")
    values.append(name)



# 添加List类型参数
def addListValue(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(">")
    end = code_line.find(";")
    
    start = code_line.find(_config.keycode_value_list) + len(_config.keycode_value_list)
    model_name = code_line[start : index]
    
    # 去空格拿到名字
    name=code_line[index + 1 : end].strip()
    values.append(name)
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_ios_space + "var " + name + " = [" + model_name + "]()\n")



# 添加string类型参数
def addStringValue(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_string) + len(_config.keycode_value_string)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    value_name = name
    if name == 'description':
        value_name = 'desc'
    if name == 'msg':
        value_name = 'descMsg'
    values.append(name)
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_ios_space + 'var ' + value_name + ' = ""\n')


# 添加int类型参数
def addIntValue(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_int) + len(_config.keycode_value_int)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    value_name = name
    if name == 'description':
        value_name = 'desc'
    if name == 'msg':
        value_name = 'descMsg'
    values.append(name)
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_ios_space + "var " + value_name + " = 0\n")


# 添加方法名
def addModelName(code, code_line):
    str = code_line.replace(_config.keycode_message, "class ")
    if '{' in str:
        str = str.replace('{', "")
    code.append(str + ": BaseModel {\n")
    code.append("\n")
    return str


# 添加注释
def addNote(code, code_line, hasAddMode):
    extra = "";
    if hasAddMode == 'True' :
        extra = "    "
    code.append(extra + "/// ")
    code.append(code_line.replace("//", "") + "\n")


# 检测到是package关键字，写入版权申明(以后如果申请了需要用到)
def addCopyrightNote(code, code_line, swift_file_name):
    # swift 不需要添加包名
    # code.append(code_line + "\n\n")
    
    code.append("/// \n")
    code.append("///  Copyright (c) 2015年 HCFData. All rights reserved.\n")
    code.append("///  For HCF Data Source Project \n")
    code.append("///  Scripts for Protocol To IOS Local Model " + swift_file_name + _config._ios_file_extra + "\n")
    code.append("///\n")
    code.append("///  Author by " + getpass.getuser() + " in " + _config.protocol_version + "\n")
    code.append("///  Last edit time is " + _com_util.GetCurrentTime()+" \n")
    
    # 添加引用
    code.append("\n")
    code.append("import UIKit;\n")
    code.append("import ObjectMapper;\n")
    code.append("\n")
    
    # 添加类名
    # code.append("class " + swift_file_name + " {\n")

