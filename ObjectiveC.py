# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


from MakeClassFile import MakeClassFile
from ClassInfo import *
from APIModel import *
from conf import OCConf
import util
import os


class ObjectiveC(MakeClassFile):
    # 构造方法
    def __init__(self, clazz, model, outPath):
        MakeClassFile.__init__(self, clazz, model)
        self.conf = OCConf()
        self.outPath = outPath

    # 开始
    def run(self):
        # 内部类
        innerClasses = []
        innerClasses.extend(self.clazz.innerClass)
        innerClasses.extend(self.clazz.inFileClass)
        importClass = [c.name for c in innerClasses]
        if len(importClass):
            self.clazz.imports.append('@class %s;' % (', '.join(importClass)))

        lines = []
        self.createBeginRemark(lines)
        self.createInterfaceImport(lines)
        self.createClassRemark(lines)
        self.createInterfaceBegin(lines)
        self.createInterfaceBody(lines)
        self.createInterfaceEnd(lines)

        # 内部类接口
        for innerClass in innerClasses:
            inner = ObjectiveC(innerClass, None, None)
            inner.createClassRemark(lines)
            inner.createInterfaceBegin(lines)
            inner.createInterfaceBody(lines)
            inner.createInterfaceEnd(lines)

        self.createEndRemark(lines)

        outFile = os.path.join(self.outPath, self.clazz.name + '.h')
        util.writeLinesFile(lines, outFile)
        os.system('clang-format -i %s\n' % outFile)
        print '写入文件:', outFile
        lines = []
        self.createBeginRemark(lines)
        self.createImplImport(lines)
        self.createClassRemark(lines)
        self.createImplBegin(lines)
        self.createImplBody(lines)
        self.createImplEnd(lines)

        # 内部类实现
        for innerClass in innerClasses:
            inner = ObjectiveC(innerClass, None, None)
            inner.createClassRemark(lines)
            inner.createImplBegin(lines)
            inner.createImplBody(lines)
            inner.createImplEnd(lines)

        self.createEndRemark(lines)

        outFile = os.path.join(self.outPath, self.clazz.name + '.m')
        util.writeLinesFile(lines, outFile)
        os.system('clang-format -i %s\n' % outFile)
        print '写入文件:', outFile

    # 创建头部注释
    def createBeginRemark(self, lines):
        lines.append('''/**\
        \n  %s: %s\
        \n\n  Created by %s on %s. \
        \n\n  %s\
        \n*/\
        \n''' % (self.clazz.name, self.clazz.fileHeaderRemark, self.conf.author, self.conf.date, self.conf.mark))

    # 创建头部注释
    def createInterfaceImport(self, lines):
        lines.extend(self.clazz.imports)

    # 创建头部注释
    def createImplImport(self, lines):
        lines.append('#import "%s.h"' % (self.clazz.name))
        lines.extend(self.clazz.innerImports)

    # 创建头部注释
    def createEndRemark(self, lines):
        lines.append('\n')

    # 创建类注释
    def createClassRemark(self, lines):
        lines.append('''\
        \n
        \n/**\
        \n%s\
        \n*/''' % (self.clazz.remark))

    # 创建接口
    def createInterfaceBegin(self, lines):
        lines.append('@interface %s : %s' % (self.clazz.name, self.clazz.superClazz))

    # 创建接口
    def createInterfaceBody(self, lines):
        for prop in self.clazz.props:
            self.createProp(lines, prop)

        for method in self.clazz.methods:
            self.createInterfaceFunc(lines, method, True)

    # 创建接口
    def createInterfaceFunc(self, lines, method, needEnd=False):

        end = ''
        if needEnd:
            end = ';'
        lines.append('/// %s' % (method.remark))
        lines.append(
            '%s (%s)%s%s' % (
                self._getFuncType(method), self.conf.getPropType(method.retType), self._getFuncSign(method), end))

    # 创建接口
    def createInterfaceEnd(self, lines):
        lines.append('@end')

    # 创建实现
    def createImplBegin(self, lines):
        lines.append('@implementation %s' % (self.clazz.name))

    # 创建实现
    def createImplBody(self, lines):

        for method in self.clazz.methods:
            self.createImplFuncBegin(lines, method)
            self.createImplFuncBody(lines, method)
            self.createImplFuncEnd(lines, method)

    def createImplFuncBegin(self, lines, method):
        self.createInterfaceFunc(lines, method)
        lines.append('{')

    def createImplFuncBody(self, lines, method):
        lines.extend(method.bodyLines)

    def createImplFuncEnd(self, lines, method):
        lines.append('}')

    # 创建实现
    def createImplEnd(self, lines):
        lines.append('@end')

    # 创建属性
    def createProp(self, lines, prop):
        lines.append(
            '@property %s %s %s;' % (
                self.conf.getPropMask(prop.type), self.conf.getPropType(prop.type, prop.subTypes), prop.name))

    # 创建方法
    def createFuncBegin(self, lines, func):
        pass

    # 创建方法
    def createFuncBody(self, lines, func):
        pass

    # 创建方法
    def createFuncEnd(self, lines, func):
        pass

    def _getFuncType(self, method):
        if method.type == 0:
            return '-'
        return '+'

    def _getFuncSign(self, method):
        sign = method.name

        # oc swift 混编标准 sWith
        if len(method.params) > 0:
            sign = '%sWith' % (sign)

        firstUpper = True
        for index in range(len(method.params)):
            param = method.params[index]
            name = param.name
            if firstUpper:
                name = util.firstUpper(name)
                firstUpper = False

            sign = '%s%s:(%s)%s ' % (sign, name, self.conf.getPropType(param.type, param.subTypes), param.name,)

        return sign


# api 对象转成类对象
class TransAPIModel2OCClass:
    def __init__(self, apiGroups):
        self.apiGroups = apiGroups
        self.conf = OCConf()

    def trans(self):
        clazzs = []
        for index in range(len(self.apiGroups)):
            apiGroup = self.apiGroups[index]
            clazz = self.transSingleGroup(apiGroup)
            if clazz:
                clazzs.append(clazz)

        return clazzs

    def makrClazzList(self, clazzs, outPath):
        for clazz in clazzs:
            objc = ObjectiveC(clazz, clazz.model, outPath)
            objc.run()

    # 转换一组api
    def transSingleGroup(self, apiGroup):
        if len(apiGroup.enName) == 0 or len(apiGroup.apis) == 0:
            return None

        apiClazz = ClassInfo()
        apiClazz.name = '%s%sAPI' % (self.conf.apiBaseClassPreFix, apiGroup.enName)
        apiClazz.remark = apiGroup.name
        apiClazz.fileHeaderRemark = apiGroup.name
        apiClazz.superClazz = 'NSObject'
        apiClazz.imports.extend(self.conf.apiImport)
        apiClazz.innerImports.extend(self.conf.apiInnerImport)

        # 创建操作实例
        line = '''
            DTHttpService *service = [DTHttpService shareInstanse];
            DTSampleOperation *oper = [service buildOperationWithSuccess:success
                                                                 failure:failure
                                                                complete:complete
                                                               operClass:DTSampleOperation.class
                                                            responeClass:nil];
            DTRequestParams *params = oper.params;
            '''

        for index in range(len(apiGroup.apis)):
            api = apiGroup.apis[index]
            if len(api.paths) == 0:
                continue

            if api.responses and len(api.responses) > 0:
                print '用于生成模型的 responses:', api.responses

            method = MethodInfo()
            method.retType = 'int'
            method.type = 1
            method.remark = api.name
            method.name = api.getMethodName()
            apiClazz.methods.append(method)

            for apiParamIndex in range(len(api.params)):
                param = api.params[apiParamIndex]
                prop = PropInfo()
                prop.name = param.name
                prop.type = param.paramType
                method.params.append(prop)

            # 回调函数
            success = ParamsInfo()
            success.name = 'success'
            success.paramType = 'void (^)(DTSampleOperation *oper)'

            failure = ParamsInfo()
            failure.name = 'failure'
            failure.paramType = 'void (^)(DTSampleOperation *oper)'

            complete = ParamsInfo()
            complete.name = 'complete'
            complete.paramType = 'void (^)(DTSampleOperation *oper)'

            # 回调参数
            calls = [
                success,
                failure,
                complete
            ]
            for apiParamIndex in range(len(calls)):
                param = calls[apiParamIndex]
                prop = PropInfo()
                prop.name = param.name
                prop.type = param.paramType
                method.params.append(prop)

            # 方法实现
            method.bodyLines.append(line)
            path = api.path
            append = ''
            for apiParamIndex in range(len(api.params)):
                param = api.params[apiParamIndex]
                if param.type == 'restful':
                    path = path.replace(':' + param.name, '%@')
                    append += ', %s' % (param.name)
                else:
                    method.bodyLines.append('[params addHttpParam:%s forKey:@"%s"];' % (param.name, param.name))

            method.bodyLines.append('params.httpMethod = @"%s";' % (api.method))
            if len(append) == 0:
                method.bodyLines.append('params.path = @"%s";' % (path))
            else:
                method.bodyLines.append('params.path = [NSString stringWithFormat:@"%s" %s];' % (path, append))
            method.bodyLines.append('return [service start:oper];')
        return apiClazz


# 模型 对象转成类对象
class TransDataModel2OCClass:
    def __init__(self, ms):
        self.dataModels = ms
        self.conf = OCConf()
        self.refMapper = {}

    def trans(self):
        return self.transClass(self.dataModels)

    def transClass(self, ms):
        classes = []
        for index in range(len(ms)):
            model = ms[index]
            dataModel = ClassInfo()
            dataModel.name = '%s%sModdel' % (self.conf.apiBaseClassPreFix, model.name)
            dataModel.superClazz = 'NSObject'
            dataModel.imports.append('#import <Foundation/Foundation.h>')
            classes.append(dataModel)
            self.refMapper[model.name] = dataModel

            if len(model.subModels) > 0:
                dataModel.inFileClass.extend(self.transClass(model.subModels))

            # 查找集合类型的自定义数据类型嵌套 只支持一层嵌套
            method = MethodInfo()
            method.bodyLines.append('NSMutableDictionary *mapper = [NSMutableDictionary dictionary];')

            # 根据字段创建属性
            for field in model.fields:
                prop = PropInfo()
                dataModel.props.append(prop)
                prop.name = field.name
                if self.getType(field.type):
                    prop.type = self.getType(field.type)
                else:
                    prop.type = field.type

                if self.getType(field.subType):
                    prop.subTypes.append(self.getType(field.subType))

                elif field.subType:
                    prop.subTypes.append(field.subType)

            for prop in dataModel.props:
                subType = ''.join(prop.subTypes)

                if len(subType) > 0:
                    method.remark = '集合类型解析映射'
                    method.retType = 'nullable NSDictionary<NSString *, id> '
                    method.name = 'modelContainerPropertyGenericClass'

                    type = self.conf.getPropType(subType).replace(' ', '').replace('*', '')
                    method.bodyLines.append('[mapper setObject:@"%s" forKey:@"%s"];' % (
                        type, prop.name))

            method.bodyLines.append('return mapper;')

            if len(method.name):
                dataModel.methods.append(method)

        return classes

    def getType(self, ref):
        if ref == 'Lang':
            pass
        if self.refMapper.has_key(ref):
            return self.refMapper.get(ref).name

        return None

    def makrClazzList(self, clazzs, outPath):
        for clazz in clazzs:
            objc = ObjectiveC(clazz, clazz.model, outPath)
            objc.run()


if __name__ == '__main__':
    clazz = ClassInfo()
    clazz.name = 'User'

    for i in range(10):
        m = MethodInfo()
        m.name = 'method%d' % i
        clazz.methods.append(m)

    for i in range(10):
        p = PropInfo()
        p.name = 'prop%d' % i
        p.type = 'string'
        clazz.props.append(p)

    model = APIGroupInfo()
    objc = ObjectiveC(clazz, model)

    objc.run()
