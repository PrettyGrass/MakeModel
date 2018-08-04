# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import os, json, sys, re
import util

sys.path.append('./conf')
from conf import Conf
from OCConf import OCConf


class OCApi():
    def __init__(self, wkPath, apiGroups):

        outPath = os.path.join(wkPath, 'Api', 'oc')
        self.wkPath = wkPath
        self.outPath = outPath
        self.conf = Conf()
        self.selfConf = OCConf()
        self.apiGroups = apiGroups
        self.currentClass = None

        self.createdHeaderFunctions = []
        self.createdImplFunctions = []

    def build(self):
        print 'build OC'
        self.createApis(self.apiGroups)

    def clear(self):
        print 'clear OC'
        os.system('rm \"%s/*\"' % self.outPath)

    def init(self):
        print 'init OC'
        self.clear()

    def createApis(self, apiGroups):

        apiImport = []
        for group in apiGroups:

            if group.enName == None or group.enName == '' or len(group.apis) == 0:
                continue

            # 头文件
            print 'api', group.name
            headerName = group.getFileName(self.selfConf.apiBaseClassPreFix) + '.h'
            lines = self.createHeaderFile(group)
            self.writeFile(headerName, lines)

            # # 实现文件
            lines = self.createImplFile(group)
            self.writeFile(group.getFileName(self.selfConf.apiBaseClassPreFix) + '.m', lines)

            self.createdHeaderFunctions = []
            self.createdImplFunctions = []

            apiImport.append('/// "%s"' % (group.name))
            apiImport.append('#import "%s"' % (headerName))
            apiImport.append('')

        self.writeFile('%sAPI.h' % (self.selfConf.apiBaseClassPreFix), apiImport)

    def createHeaderFile(self, group):

        lines = []

        lines.extend(self.createHeader(group))
        lines.extend(self.createHeaderImport(group))

        lines.extend(self.createClassRemark(group, 0))
        lines.extend(self.createInterface(group))

        return lines

    def createImplFile(self, group):

        lines = []

        lines.extend(self.createHeader(group))
        lines.extend(self.createImplImport(group))

        lines.extend(self.createClassRemark(group, 0))
        lines.extend(self.createImpl(group))

        return lines

    def writeFile(self, fileName, lines):
        outFile = os.path.join(self.outPath, fileName)
        util.writeLinesFile(lines, outFile)
        print '创建:', fileName
        os.system('clang-format -i %s\n' % outFile)

    def createHeader(self, group):
        lines = []
        h = '''//
            //  __firename__
            //  ____
            //
            //  Created by %s on %s.
            //  Copyright © 2018年 QuTui Science and Technology Co., Ltd. All rights reserved.
            //
            //  MARK: %s

            ''' % (self.conf.author, self.conf.date, self.conf.mark)
        h = h.replace('__firename__', group.name)
        lines.append(h.replace('    ', ''))
        return lines

    def createHeaderImport(self, group):
        lines = []
        for index in range(len(self.selfConf.apiImport)):
            lines.append('#import %s' % (self.selfConf.apiImport[index]))
        lines.append('')
        return lines

    def createImplImport(self, group):
        lines = []
        lines.append('#import "%s.h"' % (group.getFileName(self.selfConf.apiBaseClassPreFix)))
        lines.append('')
        return lines

    def createClassRemark(self, group, lvl=0):
        lines = []
        lines.append('%s/**' % (util.space(lvl)))
        lines.append('%s' % (util.space(lvl)))

        lines.append('%s' % (group.name))

        lines.append('%s*/' % (util.space(lvl)))
        return lines

    def createInterface(self, group):
        lines = []
        lines.append('@interface %s : %s' % (group.getFileName(self.selfConf.apiBaseClassPreFix), self.selfConf.apiBaseClass))

        lines.append('')
        for api in group.apis:
            func = self.createFuncSign(api, True)
            funcStr = ''.join(func)
            if funcStr in self.createdHeaderFunctions:
                continue
            self.createdHeaderFunctions.append(funcStr)

            lines.extend(self.createFunc(api, True))
        lines.append('@end')
        return lines

    def createImpl(self, group):
        lines = []
        lines.append('@implementation %s' % (group.getFileName(self.selfConf.apiBaseClassPreFix)))

        lines.append('')
        for api in group.apis:

            func = self.createFuncSign(api, False)
            funcStr = ''.join(func)
            if funcStr in self.createdImplFunctions:
                continue

            self.createdImplFunctions.append(funcStr)

            lines.extend(self.createFunc(api, False))
            lines.extend(self.createFuncImpl(api))

        lines.append('@end')
        return lines

    def createFunc(self, api, needEnd=False):
        lines = []
        lines.append('/// %s' % (api.name))
        lines.extend(self.createFuncSign(api, needEnd))
        return lines

    def createFuncSign(self, api, needEnd=False):

        if len(api.paths) == 0:
            return []

        funcName = ''
        use = False
        for index in range(len(api.paths)):
            p = api.paths[index]
            if index == 0 and util.isNumberBegin(p):
                # 开头是数字忽略
                continue
            if use:
                p = util.firstUpper(p)

            if p.find(':') == -1:
                # .不能做方法名
                p = p.replace('.', '_')
                funcName += p
                use = True

        if api.method.lower() == 'delete':
            funcName += util.firstUpper(api.method.lower())
        if api.method.lower() == 'put':
            funcName += util.firstUpper(api.method.lower())

        params = ''
        for index in range(len(api.params)):
            p = api.params[index]
            params = '%s%s:(NSString *)%s ' % (params, p.name, p.name)

        callbacks = ['success', 'failure', 'complete']
        for index in range(len(callbacks)):
            callback = callbacks[index]
            params = '%s%s:(void(^)(DTOperation *oper))%s ' % (params, callback, callback)

        funcName += util.firstUpper(params)

        if needEnd:
            funcName += ';'

        lines = []
        lines.append('+ (%s)%s' % (self.selfConf.apiFuncReturnType, funcName))

        if needEnd:
            lines.append('')

        return lines

    def createFuncImpl(self, api):

        if len(api.paths) == 0:
            return []

        lines = []
        lines.append('{')

        lines.append('''
        DTHttpService *service = [DTHttpService shareInstanse];
        DTOperation *oper = [service buildOperationWithSuccess:success
                                                       failure:failure
                                                      complete:complete
                                                  responeClass:%s];''' % ('nil'))

        lines.append('DTRequestParams *params = oper.params;')
        lines.append('params.path = @"%s";' % (api.path) )
        lines.append('params.httpMethod = @"%s";' % (api.method))
        for index in range(len(api.params)):
            p = api.params[index]
            lines.append('[params addHttpParam:%s forKey:@"%s"];' % (p.name, p.name))

        lines.append('return [service start:oper];')

        lines.append('}')
        lines.append('')

        return lines

    def createProp(self, group, lvl):
        lines = []
        return lines
