# encoding:utf-8

import _com_util
import _config
import getpass


# Android 端需要生成的文件
def createAndroidFile(model_lists, java_file_name):
    print ("Writing " + java_file_name + ".java ...")
    # 这是最终需要写入文件的数组
    final_codes=[]
    
    for model in model_lists:
        #print "model =============  " + bytes(len(model))
        parseModel(model, final_codes, java_file_name)
    
    # 最后需要一个'}'进行闭环
    final_codes.append("}")
    _com_util.WriteFile(_config._android_folder + java_file_name + ".java", final_codes)


# 逐个model解析
def parseModel(model, final_codes, java_file_name):
    # 初始化一个存放該model所有参数变量的数组
    values=[]
    values_asc=[]
    values_type=[]
    num = ""
    hasAddMode = 'False'
    # 记录现在进行的model名字,方便抛异常的时候用到
    to_name = java_file_name
 
    for code_line in model:
        if _config.keycode_package in code_line:
            addCopyrightNote(final_codes, code_line, java_file_name)
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
            values_type.append(_config.keycode_value_local)
            num = _com_util.LetterAutoIncrement(num)
            values_asc.append(num)
            addFileValueMethod(final_codes, code_line, values, num)
        elif '}' in code_line:
            # 这些定制方法需要添加到最后,因此放在'}'前面
            addParamsMethod(final_codes, values, values_asc, values_type)
            addToStringMethod(final_codes, values, values_asc, values_type)
            addJsonMethod(final_codes)
            final_codes.append("   } \n")
        else :
            # 解析不出来,抛异常出去
            str = ("Can't not parse in file : [" + java_file_name + ".jproto] is there something extra in " + to_name + " ? by " , code_line)
            raise SyntaxError(str)


def addFileValueMethod(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_file) + len(_config.keycode_value_file)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    values.append(name)
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_space + "private File " + num + ";\n")
    # Set 方法
    code.append(_config.key_value_space + "public void set" + name.capitalize() + "(File " + num + ") {\n")
    code.append(_config.key_value_space + "    this." + num + " = " + num + ";\n")
    code.append(_config.key_value_space + "}\n")
    # Get 方法
    code.append(_config.key_value_space + "public File get" + name.capitalize() + "() {\n")
    code.append(_config.key_value_space + "   return this." + num + ";\n")
    code.append(_config.key_value_space + "}\n")


def addInsideModelMethod(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_local) + len(_config.keycode_value_local)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    index = name.find(" ")
    model_name = name[0 : index]
    name = name[index : ].replace(" ", "")
    
    values.append(name)
    
    name = name[0 : 1].capitalize() + name[1 : len(name)]
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_space + "private " + model_name + " " + num + ";\n")
    # Set 方法
    code.append(_config.key_value_space + "public void set" + name.capitalize() + "(" + model_name + " " + num + ") {\n")
    code.append(_config.key_value_space + "    this." + num + " = " + num + ";\n")
    code.append(_config.key_value_space + "}\n")
    # Get 方法
    code.append(_config.key_value_space + "public " + model_name + " get" + name + "() {\n")
    code.append(_config.key_value_space + "   return this." + num + ";\n")
    code.append(_config.key_value_space + "}\n")

# 添加请求addParams()方法
def addParamsMethod(code, values, values_asc, values_type):
    # 理论上来讲两个数组长度是一样的
    addNote(code, "添加上报数据", 'True')
    code.append(_config.key_value_space + "public void addParams(FormBody.Builder builder) {\n")
    for i in range(len(values)):
        name = values[i]
        name_asc = values_asc[i]
        type = values_type[i]
        if type == _config.keycode_value_int:
            code.append(_config.key_value_space + "   builder.add(" + '"' + name + '"' + ", this." + name_asc + ' + "");\n')
        elif type == _config.keycode_value_string:
            code.append(_config.key_value_space + "   if(null != this." + name_asc + " && this." + name_asc + ".length() > 0) {\n")
            code.append(_config.key_value_space + "      builder.add(" + '"' + name + '"' + ", this." + name_asc + ');\n')
            code.append(_config.key_value_space + "   }\n")
    code.append(_config.key_value_space + "}\n")


# 添加toJson()方法
def addJsonMethod(code):
    addNote(code, "得到转后的Json数据", 'True')

    code.append(_config.key_value_space + "public String toJson() {\n")
    code.append(_config.key_value_space + "   try {\n")
    code.append(_config.key_value_space + "      return JSON.toJSONString(this);\n")
    code.append(_config.key_value_space + "   } catch (Throwable e) {\n")
    code.append(_config.key_value_space + _config.key_value_space + "e.printStackTrace();\n")
    code.append(_config.key_value_space + "   }\n")
    code.append(_config.key_value_space + "   return null;\n")
    code.append(_config.key_value_space + "}\n")

# 添加toString()方法
def addToStringMethod(code, values, values_asc, values_type):
    # 理论上来讲两个数组长度是一样的
    code.append(_config.key_value_space + "public String toString() {\n")
    str = _config.key_value_space + "   return "
    for i in range(len(values)):
        name = values[i]
        name_asc = values_asc[i]
        type =values_type[i]
        if type == _config.keycode_value_local:
            str = str + '" ' + name + ' = " + (this.' + name_asc +' == null ? '+'"'+'" : this.'+ name_asc +".toString()) + "
        else:
            str = str + '" ' + name + ' = " + this.' + name_asc + " + "
    code.append(str + '""' + ";\n")
    code.append(_config.key_value_space + "}\n")

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
    
    name = name[0 : 1].capitalize() + name[1 : len(name)]
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_space + "private List<" + model_name + "> " + num + ";\n")
    # Set 方法
    code.append(_config.key_value_space + "public void set" + name + "(List<" + model_name + "> " + num + ") {\n")
    code.append(_config.key_value_space + "   this." + num + " = " + num + ";\n")
    code.append(_config.key_value_space + "}\n")
    # Get 方法
    code.append(_config.key_value_space + "public List<" + model_name + "> get" + name + "() {\n")
    code.append(_config.key_value_space + "   return this." + num + ";\n")
    code.append(_config.key_value_space + "}\n")


# 添加string类型参数
def addStringValue(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_string) + len(_config.keycode_value_string)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    values.append(name)
    
    name = name[0 : 1].capitalize() + name[1 : len(name)]
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_space + "private String " + num + ";\n")
    # Set 方法
    code.append(_config.key_value_space + "public void set" + name + "(String " + num + ") {\n")
    code.append(_config.key_value_space + "    this." + num + " = " + num + ";\n")
    code.append(_config.key_value_space + "}\n")
    # Get 方法
    code.append(_config.key_value_space + "public String get" + name + "() {\n")
    code.append(_config.key_value_space + "   return this." + num + ";\n")
    code.append(_config.key_value_space + "}\n")


# 添加int类型参数
def addIntValue(code, code_line, values, num):
    # 截取变量名
    index = code_line.find(_config.keycode_value_int) + len(_config.keycode_value_int)
    end = code_line.find(";")
    
    # 去空格拿到名字
    name=code_line[index : end].strip()
    values.append(name)
    
    name = name[0 : 1].capitalize() + name[1 : len(name)]
    
    # 变量定义(取名为混淆过后的)
    code.append(_config.key_value_space + "private int " + num + ";\n")
    # Set 方法
    code.append(_config.key_value_space + "public void set" + name + "(int " + num + ") {\n")
    code.append(_config.key_value_space + "   this." + num + " = " + num + ";\n")
    code.append(_config.key_value_space + "}\n")
    # Get 方法
    code.append(_config.key_value_space + "public int get" + name + "() {\n")
    code.append(_config.key_value_space + "   return this." + num + ";\n")
    code.append(_config.key_value_space + "}\n")


# 添加方法名
def addModelName(code, code_line):
    str = code_line.replace(_config.keycode_message, "   public static class ")
    code.append(str + "\n")
    return str


# 添加注释
def addNote(code, code_line, hasAddMode):
    extra = "";
    if hasAddMode == 'True' :
        extra = "   "
    code.append(extra + "   /** \n")
    code.append(extra + "    *  ")
    code.append(code_line.replace("//", "") + "\n")
    code.append(extra + "    */ \n")


# 检测到是package关键字，写入版权申明(以后如果申请了需要用到)
def addCopyrightNote(code, code_line, java_file_name):
    # 添加包名
    code.append(code_line + "\n\n")
    # 添加引用
    code.append("import com.alibaba.fastjson.JSON;\n")
    code.append("import java.util.List;\n")
    # OKhttp3后改成这个了
    code.append("import okhttp3.FormBody;\n")
    code.append("\n")
    
    code.append("/** \n")
    code.append(" *  Copyright (c) 2015 HCFData. All rights reserved.\n")
    code.append(" *  For HCF Data Source Project \n")
    code.append(" *  Scripts for Protocol To Android Local Model " + java_file_name + _config._android_file_extra + "\n")
    code.append(" *  Author by " + getpass.getuser() + " in " + _config.protocol_version + "\n")
    code.append(" *  Last edit time is " + _com_util.GetCurrentTime()+" \n")
    code.append(" */ \n")
    # 添加类名
    code.append("public class " + java_file_name + " { \n")


