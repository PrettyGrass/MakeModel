# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


from MakeClassFile import MakeClassFile
from ClassInfo import *
from APIModel import *
from ParseModelJson import ParseModelJson
from conf import OCConf
import util
import os
import json


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

        # 抽象接口
        hasInterface = self.clazz.hasInterface()
        interfaceFile = self.clazz.name + 'Protocol'
        implInterface = []
        if hasInterface:
            interfaceLines = []
            self.createBeginRemark(interfaceLines)
            self.createInterfaceImport(interfaceLines)
            self.createClassRemark(interfaceLines)
            self.createInterfaceBegin(interfaceLines, isProtocol=True)
            self.createProtocolInterfaceBody(interfaceLines)
            self.createInterfaceEnd(interfaceLines)

            # 内部类接口
            for innerClass in innerClasses:
                inner = ObjectiveC(innerClass, None, None)
                inner.createClassRemark(interfaceLines)
                inner.createInterfaceBegin(interfaceLines, isProtocol=True)
                inner.createProtocolInterfaceBody(interfaceLines)
                inner.createInterfaceEnd(interfaceLines)

            self.createEndRemark(interfaceLines)
            outFile = os.path.join(self.outPath, interfaceFile + '.h')
            util.writeLinesFile(interfaceLines, outFile)
            os.system('clang-format -i %s\n' % outFile)
            print '写入协议文件:', outFile

            self.clazz.imports.append('#import "%s.h"' % (interfaceFile))
            implInterface.append(interfaceFile)

        lines = []
        self.createBeginRemark(lines)
        self.createInterfaceImport(lines)
        self.createClassRemark(lines)
        self.createInterfaceBegin(lines, implProtocol=implInterface)
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
    def createInterfaceBegin(self, lines, isProtocol=False, implProtocol=None):
        if not implProtocol:
            implProtocol = []

        implProtocol = ','.join(implProtocol)
        if len(implProtocol) > 0:
            implProtocol = '<%s>' % implProtocol

        if isProtocol:
            lines.append('@protocol %sProtocol <NSObject>' % (self.clazz.name))
        else:
            lines.append('@interface %s : %s%s' % (self.clazz.name, self.clazz.superClazz, implProtocol))

    # 创建接口
    def createInterfaceBody(self, lines):
        for prop in self.clazz.props:
            self.createProp(lines, prop)

        for method in self.clazz.methods:
            if (method.inner or method.abs):
                continue
            self.createInterfaceFunc(lines, method, True)

    # 创建接口
    def createProtocolInterfaceBody(self, lines):
        for prop in self.clazz.props:
            self.createProp(lines, prop)

        for method in self.clazz.methods:
            if (method.abs):
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
    def __init__(self, apiGroups, wkPath):
        self.apiGroups = apiGroups
        self.conf = OCConf()
        self.wkPath = wkPath
        self.allModelMapper = self.allModels(apiGroups)

    def trans(self):
        clazzs = []
        for index in range(len(self.apiGroups)):
            apiGroup = self.apiGroups[index]
            clazz = self.transSingleGroup(apiGroup)
            if clazz:
                clazzs.append(clazz)

        return clazzs

    def makeClazzList(self, clazzs, outPath):
        for clazz in clazzs:
            objc = ObjectiveC(clazz, clazz.model, outPath)
            objc.run()

    # 获取所有api的数据模型并创建
    def allModels(self, apiGroups):
        modelMapper = {}
        refMappers = {}
        for index in range(len(apiGroups)):
            apiGroup = apiGroups[index]
            for index in range(len(apiGroup.apis)):
                api = apiGroup.apis[index]
                if len(api.paths) == 0 or not api.responses or len(api.responses) == 0:
                    continue
                for response in api.responses:

                    pm = ParseModelJson(self.wkPath)
                    ms = []
                    jsonObj = json.loads(response.get('body'))
                    responseKey = util.firstUpper(api.getMethodName())
                    ms.append(pm.parseContent(jsonObj, responseKey))
                    trans = TransDataModel2OCClass(ms, refMappers)
                    cls = trans.trans()
                    if len(cls) > 0:
                        print 'API数据模型:', api.getMethodName(), cls
                        modelMapper[responseKey.lower()] = cls[0]
                        # trans.makeClazzList(cls, os.path.join(self.wkPath, 'Product', 'ocmodel'))

        # 数据模型关系建立完成之后创建文件
        for model in modelMapper.values():
            trans.makeClazzList([model], os.path.join(self.wkPath, 'Product', 'ocmodel'))

        return modelMapper

    # 转换一组api 为class 类
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

        # inject
        method = MethodInfo()
        method.retType = 'void'
        method.type = 1
        method.inner = True
        method.abs = False
        method.remark = ''
        method.name = 'load'
        method.bodyLines.append(
            '[[TyphoonDefineMapper shared] regWithProvider:self service:@protocol(%sProtocol)];' % apiClazz.name)
        apiClazz.methods.append(method)
        apiClazz.innerImports.append('#import <TyphoonExtra/TyphoonExtra.h>')

        for index in range(len(apiGroup.apis)):
            api = apiGroup.apis[index]
            if len(api.paths) == 0:
                continue

            if api.responses and len(api.responses) > 0:
                print '用于生成模型的 responses:', api.getMethodName()

            method = MethodInfo()
            method.retType = 'int'
            method.type = 0
            method.abs = True
            method.inner = True
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

            # 请求响应数据类型
            if len(self.conf.dataPath) and self.allModelMapper.has_key(api.getMethodName().lower()):
                respClass = self.allModelMapper.get(api.getMethodName().lower())
                method.bodyLines.append(
                    '[oper.dataClasses setObject:NSClassFromString(@"%s") forKey:@"%s"];' % (
                        respClass.name, self.conf.dataPath))
            # 请求路径
            if len(append) == 0:
                method.bodyLines.append('params.path = @"%s";' % (path))
            else:
                method.bodyLines.append('params.path = [NSString stringWithFormat:@"%s" %s];' % (path, append))

            # 请求开始
            method.bodyLines.append('return [service start:oper];')

        return apiClazz


# 模型 对象转成类对象
class TransDataModel2OCClass:
    def __init__(self, ms, globalRefMapper):
        self.dataModels = ms
        self.conf = OCConf()
        self.refMapper = {}
        self.globalRefMapper = globalRefMapper

    def trans(self):
        return self.transClass(self.dataModels)

    # 转换响应数据 为 class类
    def transClass(self, ms):
        classes = []
        for index in range(len(ms)):
            model = ms[index]
            name = '%s%sModel' % (self.conf.apiBaseClassPreFix, model.name)

            dataModel = None
            if self.globalRefMapper.has_key(name):
                dataModel = self.globalRefMapper[name]

            # 如模型不存在, 则新建, 否则做字段增量
            if not dataModel:
                dataModel = ClassInfo()
                dataModel.name = name
                dataModel.superClazz = 'NSObject'
                dataModel.imports.append('#import <Foundation/Foundation.h>')
                classes.append(dataModel)
                self.refMapper[name] = dataModel
                self.globalRefMapper[name] = dataModel

            if len(model.subModels) > 0:
                dataModel.inFileClass.extend(self.transClass(model.subModels))

            # 查找集合类型的自定义数据类型嵌套 只支持一层嵌套
            method = MethodInfo()
            method.bodyLines.append('NSMutableDictionary *mapper = [NSMutableDictionary dictionary];')

            # 根据字段创建属性
            for field in model.fields:

                if field.name in self.conf.protectProp:
                    print '字段受保护:%s.%s' % (model.name, field.name)
                    continue

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

            # 属性
            for prop in dataModel.props:
                subType = ''.join(prop.subTypes)

                if len(subType) > 0:
                    method.remark = '集合类型解析映射'
                    method.retType = 'nullable NSDictionary<NSString *, id> '
                    method.name = 'modelContainerPropertyGenericClass'
                    method.inner = True
                    ptype = self.conf.getPropType(subType).replace(' ', '').replace('*', '')
                    method.bodyLines.append('[mapper setObject:@"%s" forKey:@"%s"];' % (
                        ptype, prop.name))

            method.bodyLines.append('return mapper;')

            if len(method.name):
                dataModel.methods.append(method)

        return classes

    def getType(self, ref):

        if self.refMapper.has_key(ref):
            return self.refMapper.get(ref).name

        return None

    def makeClazzList(self, clazzs, outPath):
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
