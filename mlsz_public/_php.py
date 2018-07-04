# encoding:utf-8

import _com_util
import _config
import getpass
import os


# Android 端需要生成的文件
def createPHPFile(model_lists, php_file_name, proto_name):
    php_file_name = php_file_name + "Model"
    print ("Writing " + php_file_name + _config._php_file_extra + " ...")
 
    
    for model in model_lists:
        #print "model =============  " + bytes(len(model))
        parseModel(model, php_file_name, proto_name)
    
    # 由于swift不需要类名所以最后需要一个'}'进行闭环
    # final_codes.append("}")


# 逐个model解析
def parseModel(model, php_file_name, proto_name):
    # 初始化一个存放該model所有参数变量的数组
    values=[]
    values_asc=[]
    values_type=[]
    num = ""
    hasAddMode = 'False'
    # 记录现在进行的model名字,方便抛异常的时候用到
    to_name = php_file_name
    
    # 这是最终需要写入文件的数组
    final_codes=[]
    
    extra=""
    
    for code_line in model:
        if _config.keycode_package in code_line:
            test = ""
            #addCopyrightNote(final_codes, code_line, php_file_name)
        elif _config.keycode_import in code_line:
            # Do nothing
            test = "";
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
            test = "Fix me"
        elif "}" in code_line:
            addConGetSetMethods(final_codes, values, values_asc, values_type)
            addToArrayMethod(final_codes, values, values_asc, values_type)
            addToJsonMethod(final_codes, values, values_asc, values_type)
            final_codes.append("}\n?>")
            file_folder = _config._php_folder + proto_name + "/"
            if not os.path.isdir(file_folder):
                #print ("Create "+ file_folder + "...")
                os.makedirs(file_folder)
            #print ('path', file_folder + _config._php_file_extra)
            _com_util.WriteFile(file_folder + to_name + _config._php_file_extra, final_codes)
            final_codes=[]
        else :
            # 解析不出来,抛异常出去
            str = ("Can't not parse in file : [" + php_file_name + ".jproto] is there something extra in " + to_name + " ? by " , code_line)
            raise SyntaxError(str)


def addConGetSetMethods(code, values, values_asc, values_type):
    # 理论上来讲两个数组长度是一样的
    code.append("\n")
    code.append(_config.key_value_ios_space + "function __construct()\n")
    code.append(_config.key_value_ios_space + "{\n")
    code.append(_config.key_value_ios_space + "    parent::__construct();\n")
    code.append(_config.key_value_ios_space + "}\n")

    code.append(_config.key_value_ios_space + "public function __set($property_name, $value)\n")
    code.append(_config.key_value_ios_space + "{\n")
    code.append(_config.key_value_ios_space + "    $this->$property_name = $value;\n")
    code.append(_config.key_value_ios_space + "}\n")

    code.append(_config.key_value_ios_space + "public function __get($property_name)\n")
    code.append(_config.key_value_ios_space + "{\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "if(isset($this->$property_name))\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "{\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "    return($this->$property_name);\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "}\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "else\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "{\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "    return(NULL);\n")
    code.append(_config.key_value_ios_space + _config.key_value_ios_space + "}\n")
    code.append(_config.key_value_ios_space + "}\n")


# 添加toJson()方法
def addToJsonMethod(code, values, values_asc, values_type):
    # 理论上来讲两个数组长度是一样的
    code.append(_config.key_value_ios_space + "public function toJson()\n")
    code.append(_config.key_value_ios_space + "{\n")
    code.append(_config.key_value_space + " return $this->json_encode_plus($this->toArray());\n")
    code.append(_config.key_value_ios_space + "}\n")

# 添加toArray()方法
def addToArrayMethod(code, values, values_asc, values_type):
    # 理论上来讲两个数组长度是一样的
    code.append(_config.key_value_ios_space + "public function toArray()\n")
    code.append(_config.key_value_ios_space + "{\n")
    str = _config.key_value_space + " return array("
    for i in range(len(values)):
        name = values[i]
        name_asc = values_asc[i]
        type =values_type[i]
        str = str + "'" + name + "'" + "=>$this->" + name + ", "
    #length = len(str)
    #if length > 9:
    str = str[0 : len(str) - 2]
    code.append(str + ");\n")
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
    code.append(_config.key_value_ios_space + "private $" + name + ";\n")
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
    code.append(_config.key_value_ios_space + "private $" + name + " = array();\n")



# 添加string类型参数
def addStringValue(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_string) + len(_config.keycode_value_string)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    values.append(name)
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_ios_space + 'private $' + name + " = '';\n")


# 添加int类型参数
def addIntValue(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_int) + len(_config.keycode_value_int)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    values.append(name)
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_ios_space + "private $" + name + " = 0;\n")


# 添加方法名
def addModelName(code, code_line):
    name = code_line.replace(_config.keycode_message, "").replace("{", "").replace(" ", '') + "Model"
    addCopyrightNote(code, name)
    code.append("class " + name + " extends BaseModel {\n")
    code.append("\n")
    return name


# 添加注释
def addNote(code, code_line, hasAddMode):
    extra = "";
    if hasAddMode == 'True' :
        extra = "    "
    code.append(extra + "//")
    code.append(code_line.replace("//", "") + "\n")


# 检测到是package关键字，写入版权申明(以后如果申请了需要用到)
def addCopyrightNote(code, php_file_name):
    
    code.append("//  Copyright (c) 2015年 HCFData. All rights reserved.\n")
    code.append("//  For HCF Data Source Project \n")
    code.append("//  Scripts for Protocol To PHP Local Model " + php_file_name + _config._php_file_extra + "\n")
    code.append("//\n")
    code.append("//  Author by " + getpass.getuser() + " in " + _config.protocol_version + "\n")
    code.append("//  Last edit time is " + _com_util.GetCurrentTime()+" \n")
    
    code.append("\n")
    code.append("<?php\n")
    code.append("namespace Common\Model;\n")
    code.append("use \Common\Model\BaseModel;\n")
    code.append("\n")


