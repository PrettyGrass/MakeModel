# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


from MakeClassFile import MakeClassFile
from ClassInfo import *
from APIModel import *
from ParseModelJson import ParseModelJson
from conf import SwiftConf
import util
import os
import json


class Swift(MakeClassFile):
    # 构造方法
    def __init__(self, clazz, model, conf, outPath):
        MakeClassFile.__init__(self, clazz, model)
        self.conf = conf
        self.outPath = outPath

    # 开始
    def run(self):

        # 内部类
        innerClasses = []
        innerClasses.extend(self.clazz.innerClass)
        innerClasses.extend(self.clazz.inFileClass)
        importClass = [c.name for c in innerClasses]
        # if len(importClass):
        #     self.clazz.imports.append('@class %s;' % (', '.join(importClass)))

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
                inner = Swift(innerClass, None, self.conf, None)
                inner.createClassRemark(interfaceLines)
                inner.createInterfaceBegin(interfaceLines, isProtocol=True)
                inner.createProtocolInterfaceBody(interfaceLines)
                inner.createInterfaceEnd(interfaceLines)

            self.createEndRemark(interfaceLines)
            outFile = os.path.join(self.outPath, 'protocol', interfaceFile + '.swift')
            util.writeLinesFile(interfaceLines, outFile)
            os.system('cd %s && swiftformat . \n' % self.outPath)
            print '写入协议文件:', outFile

            implInterface.append(interfaceFile)
            self.clazz.impls.append(interfaceFile)

        lines = []
        self.createBeginRemark(lines)
        self.createImplImport(lines)
        self.createClassRemark(lines)
        self.createImplBegin(lines)
        self.createImplBody(lines)
        self.createImplEnd(lines)

        # 内部类实现
        for innerClass in innerClasses:
            inner = Swift(innerClass, None, self.conf, None)
            inner.createClassRemark(lines)
            inner.createImplBegin(lines)
            inner.createImplBody(lines)
            inner.createImplEnd(lines)

        self.createEndRemark(lines)

        outFile = os.path.join(self.outPath, self.clazz.name + '.swift')
        util.writeLinesFile(lines, outFile)
        os.system('cd %s && swiftformat . \n' % self.outPath)
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
        # lines.append('#import "%s.h"' % (self.clazz.name))
        lines.extend(self.clazz.imports)

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
            lines.append('@objc public protocol %sProtocol :NSObjectProtocol {' % (self.clazz.name))
        else:
            lines.append('@objc open class %s : %s%s {' % (self.clazz.name, self.clazz.superClazz, implProtocol))

    # 创建接口
    def createProtocolInterfaceBody(self, lines):
        for prop in self.clazz.props:
            self.createProp(lines, prop)

        for method in self.clazz.methods:
            if (method.abs):
                self.createInterfaceFunc(lines, method, True)

    # 创建接口
    def createInterfaceFunc(self, lines, method, isProtocol=False):

        mask = ''
        if not isProtocol:
            mask = 'public'

        lines.append('/// %s' % (method.remark))
        lines.append(
            '%s %s func %s -> %s' % (
                self._getFuncType(method), mask, self._getFuncSign(method), self.conf.getPropType(method.retType)))

    # 创建接口
    def createInterfaceEnd(self, lines):
        lines.append('}')

    # 创建实现
    def createImplBegin(self, lines):
        implProtocol = None
        if len(self.clazz.impls) > 0:
            implProtocol = ', %s' % ','.join(self.clazz.impls)
        else:
            implProtocol = ''

        lines.append('@objc open class %s : %s%s {' % (self.clazz.name, self.clazz.superClazz, implProtocol))

    # 创建实现
    def createImplBody(self, lines):

        for prop in self.clazz.props:
            self.createProp(lines, prop)

        # for method in self.clazz.methods:
        #     if (method.inner or method.abs):
        #         continue
        #     self.createInterfaceFunc(lines, method, True)

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
        lines.append('}')

    # 创建属性
    def createProp(self, lines, prop):

        defVal = '?'
        if self.conf.baseType.has_key(prop.type) and self.conf.baseType.get(prop.type).has_key('default'):
            defVal = ' = %s' % self.conf.baseType.get(prop.type)['default']

        lines.append(
            '%s var %s :%s%s' % (self.conf.getPropMask(prop.type),
                                 prop.name,
                                 self.conf.getPropType(prop.type, prop.subTypes),
                                 defVal))

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
            return ''
        return ' static '

    def _getFuncSign(self, method):
        sign = method.name

        # oc swift 混编标准 sWith
        # if len(method.params) > 0:
        #     sign = '%sWith' % (sign)

        firstUpper = True
        ps = []
        for index in range(len(method.params)):
            param = method.params[index]
            name = param.name

            ptype = self.conf.getPropType(param.type, param.subTypes)
            # 集合类型参数 默认
            ptype = ptype.replace('[subtype]', '[Any]')
            ps.append('%s:%s' % (name, ptype))

        sign = '%s(%s)' % (sign, ',\n'.join(ps))
        return sign


# api 对象转成类对象
class TransAPIModel2SwiftClass:
    def __init__(self, apiGroups, conf):
        self.apiGroups = apiGroups
        self.conf = conf
        self.allModelMapper = self.allModels(apiGroups)

    def trans(self):
        clazzs = []
        for index in range(len(self.apiGroups)):
            apiGroup = self.apiGroups[index]
            clazz = self.transSingleGroup(apiGroup)
            if clazz:
                clazzs.append(clazz)

        # 生成注入类
        entryPoint = ClassInfo()
        entryPoint.superClazz = 'NSObject'
        entryPoint.name = 'HttpApiEntry'
        entryPoint.remark = 'api服务注入入口类'
        entryPoint.imports.append('import DTDependContainer')

        method = MethodInfo()
        method.retType = 'void'
        method.type = 1
        method.abs = False
        method.inner = False
        method.remark = 'api服务注入入口'
        method.name = 'regAllApi'
        entryPoint.methods.append(method)

        for index in range(len(clazzs)):
            apiClazz = clazzs[index]
            method.bodyLines.append(
                'DTDependContainerMapper.shared().reg(withProvider: %s.self, service: %sProtocol.self)' % (
                    apiClazz.name, apiClazz.name))

        clazzs.append(entryPoint)
        return clazzs

    def makeClazzList(self, clazzs):
        for clazz in clazzs:
            objc = Swift(clazz, clazz.model, self.conf, self.conf.apiOutPath)
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

                    pm = ParseModelJson(self.conf, '')
                    ms = []
                    jsonObj = json.loads(response.get('body'))
                    responseKey = util.firstUpper(api.getMethodSign())
                    model = pm.parseContent(jsonObj, responseKey)
                    model.remark = '%s响应模型' % api.name
                    ms.append(model)
                    trans = TransDataModel2SwiftClass(ms, self.conf, refMappers)
                    cls = trans.trans()
                    if len(cls) > 0:
                        print 'API数据模型:', api.getMethodName(), cls
                        modelMapper[responseKey.lower()] = cls[0]
                        # trans.makeClazzList(cls, os.path.join(self.wkPath, 'Product', 'SwiftModel'))

        # 数据模型关系建立完成之后创建文件
        for model in modelMapper.values():
            trans.makeClazzList([model], self.conf.apiModelPath)

        return modelMapper

    # 转换一组api 为class 类
    def transSingleGroup(self, apiGroup):
        if len(apiGroup.enName) == 0 or len(apiGroup.apis) == 0:
            return None

        apiClazz = ClassInfo()
        apiClazz.name = '%s%sAPI' % ('', apiGroup.enName)
        apiClazz.remark = apiGroup.name
        apiClazz.fileHeaderRemark = apiGroup.name
        apiClazz.superClazz = 'NSObject'
        apiClazz.imports.extend(self.conf.apiImport)

        # 创建操作实例
        line = '''
        let service = HttpService.shared
        let oper = service.buildSampleOperation(operClass: DTSampleOperation<AnyObject>.self,
                                                responeClass: DTHttpSampleResponse<AnyObject>.self,
                                                success: success,
                                                failure: failure,
                                                complete: complete)
        let params = oper.params
            '''

        for index in range(len(apiGroup.apis)):
            api = apiGroup.apis[index]
            if api.getMethodName() == 'musicsIntro':
                pass
            if len(api.paths) == 0:
                continue

            if api.responses and len(api.responses) > 0:
                print '用于生成模型的 responses:', api.getMethodName()

            respClass = None
            respClassName = 'AnyObject'
            methodSign = api.getMethodSign().lower()
            if len(self.conf.dataPath) and self.allModelMapper.has_key(methodSign):
                respClass = self.allModelMapper.get(methodSign)
                respClassName = respClass.name

            if 'AnyObject' == respClassName:
                pass

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
            success.paramType = '@escaping ((DTSampleOperation<%s>) -> Void)' % respClassName

            failure = ParamsInfo()
            failure.name = 'failure'
            failure.paramType = '@escaping ((DTSampleOperation<%s>) -> Void)' % respClassName

            complete = ParamsInfo()
            complete.name = 'complete'
            complete.paramType = '@escaping ((DTSampleOperation<%s>) -> Void)' % respClassName

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
            for apiParamIndex in range(len(api.params)):
                param = api.params[apiParamIndex]
                if param.type == 'restful':
                    path = path.replace(':' + param.name, '\(%s)' % (param.name))
                else:
                    method.bodyLines.append('params?.addHttpParam(%s, forKey: "%s")' % (param.name, param.name))

            method.bodyLines.append('params?.httpMethod = "%s"' % (api.method))

            # 请求响应数据类型
            if len(self.conf.dataPath) and respClass:
                method.bodyLines.append(
                    'oper.dataClasses.setValue(%s.self, forKey: "%s")' % (
                        respClass.name, self.conf.dataPath))
            # 请求路径
            method.bodyLines.append('params?.path = "%s"' % (path))
            # json表单
            method.bodyLines.append('params?.isJsonForm = true')
            # 请求开始
            method.bodyLines.append('return service.start(oper: oper)')

        return apiClazz


# 模型 对象转成类对象
class TransDataModel2SwiftClass:
    def __init__(self, ms, conf, globalRefMapper):
        self.dataModels = ms
        self.conf = conf
        self.refMapper = {}
        self.globalRefMapper = globalRefMapper

    def trans(self):
        return self.transClass(self.dataModels, True)

    def getClassName(self, name):
        return '%sModel' % (name)

    # 转换响应数据 为 class类
    def transClass(self, ms, root=False):
        classes = []
        for index in range(len(ms)):
            model = ms[index]
            name = self.getClassName(model.name)

            dataModel = None
            if self.globalRefMapper.has_key(name):
                dataModel = self.globalRefMapper[name]

            # 如模型不存在, 则新建, 否则做字段增量
            if not dataModel:
                dataModel = ClassInfo()
                dataModel.impls.extend(self.conf.importModule)
                dataModel.name = name
                dataModel.remark = model.remark
                dataModel.superClazz = 'NSObject'
                dataModel.imports.append('import Foundation')
                if self.conf.useYYModel:
                    dataModel.imports.append('import YYModel')

                classes.append(dataModel)
                self.refMapper[name] = dataModel
                self.globalRefMapper[name] = dataModel

            elif root:
                # 最外层数据的情况, 需要把最外层模型名传回, 做映射
                classes.append(dataModel)

            if len(model.subModels) > 0:
                dataModel.inFileClass.extend(self.transClass(model.subModels))

            transferProps = []
            # 根据字段创建属性
            for field in model.fields:

                # 字段转义
                fname = field.name
                if self.conf.transferProp.has_key(fname):
                    print '字段需转义:%s.%s' % (model.name, fname)

                    tname = self.conf.transferProp.get(fname)
                    transferProps.append('"%s": "%s"' % (tname, fname))
                    fname = tname

                # 重复字段
                if dataModel.hasProp(fname):
                    continue

                prop = PropInfo()
                dataModel.props.append(prop)
                prop.name = fname
                # 字段类型
                if self.getType(field.type):
                    prop.type = self.getType(field.type)
                elif not self.conf.isBaseType(field.type):
                    prop.type = self.getClassName(field.type)
                else:
                    prop.type = field.type

                # 字段子类型
                if self.getType(field.subType):
                    prop.subTypes.append(self.getType(field.subType))
                elif self.conf.isBaseType(field.subType):
                    prop.subTypes.append(self.conf.getPropType(field.subType))
                elif field.subType:
                    prop.subTypes.append(self.getClassName(field.subType))

            # 转义属性
            transm = dataModel.hasMethod('modelCustomPropertyMapper', 1)
            transferDiffProps = []
            if len(transferProps) > 0 and transm:
                for p in transferProps:
                    if transm.bodyLines[0].find(p) < 0:
                        transferDiffProps.append(p)
            else:
                transferDiffProps = transferProps

            mask = '"__mask__": "__mask__"'
            if len(transferDiffProps) > 0:
                transm = dataModel.hasMethod('modelCustomPropertyMapper', 1)
                if not transm:
                    transm = MethodInfo()
                    transm.remark = '转义属性'
                    transm.retType = '[String : Any]?'
                    transm.name = 'modelCustomPropertyMapper'
                    transm.inner = True
                    transm.type = 1
                    transm.bodyLines.append('let mapper = [%s]' % (mask))
                    transm.bodyLines.append('return mapper as [String : Any]')
                    dataModel.methods.append(transm)

                transm.bodyLines[0] = transm.bodyLines[0].replace(']', (',%s]' % ',\n'.join(transferDiffProps)))
                transm.bodyLines[0] = transm.bodyLines[0].replace('%s,' % mask, '')

            # 属性
            # 查找集合类型的自定义数据类型嵌套 只支持一层嵌套
            method = dataModel.hasMethod('modelContainerPropertyGenericClass', 1)
            if not method:
                method = MethodInfo()
                method.bodyLines.append('let mapper = [%s]' % (mask))
                method.bodyLines.append('return mapper as [String : Any]')
                method.remark = '集合类型解析映射'
                method.retType = '[String : Any]'
                method.name = 'modelContainerPropertyGenericClass'
                method.inner = True
                method.type = 1

            for prop in dataModel.props:
                subType = ''.join(prop.subTypes)
                # 集合一类的有子类型的才需要映射
                if len(subType) > 0 and (not self.conf.isBaseType(subType)):
                    ptype = self.conf.getPropType(subType).replace(' ', '').replace('*', '')
                    line = '"%s": %s.self' % (
                        prop.name, ptype)

                    oldLine = method.bodyLines[0]
                    if oldLine.find(line) < 0:
                        # 不存在则添加
                        oldLine = oldLine.replace(']', (',%s]' % line))
                        oldLine = oldLine.replace('%s,' % mask, '')

                    method.bodyLines[0] = oldLine
                    # 没有添加过该方法则添加
                    if not dataModel.hasMethod('modelContainerPropertyGenericClass', 1):
                        dataModel.methods.append(method)

        return classes

    def getType(self, ref):

        if self.refMapper.has_key(ref):
            return self.refMapper.get(ref).name

        return None

    def makeClazzList(self, clazzs, outPath):
        for clazz in clazzs:
            objc = Swift(clazz, clazz.model, self.conf, outPath)
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
    objc = Swift(clazz, model)

    objc.run()
