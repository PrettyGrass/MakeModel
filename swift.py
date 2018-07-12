# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import os, json, sys, re
import util

sys.path.append('./conf')
sys.path.append('./script')
from conf import Conf
from SwiftConf import SwiftConf


class Swift():
    def __init__(self, wkPath, models):

        outPath = os.path.join(wkPath, 'Product', 'swift')
        self.wkPath = wkPath
        self.outPath = outPath
        self.conf = Conf()
        self.selfConf = SwiftConf()
        self.models = models

    def build(self):
        print 'build swift'
        self.createModels(self.models)

    def clear(self):
        print 'clear swift'

    def init(self):
        print 'init swift'

    def createModels(self, models):

        for model in models:

            inFileClass = []
            inClassClass = []
            inSingle = []
            for sub in model.innerClass:
                path = '%s.%s' % (model.name, sub.name)
                if path in self.selfConf.inFile:
                    inFileClass.append(sub)
                elif path in self.selfConf.inClass:
                    inClassClass.append(sub)
                else:
                    inSingle.append(sub)

            for sub in inSingle:
                lines = self.createModelFile(sub)
                self.writeFile(sub, lines)

            lines = self.createModelFile(model, inFileClass=inFileClass, inClassClass=inClassClass)
            self.writeFile(model, lines)

    def createModelFile(self, model, inFileClass=None, inClassClass=None, inner=False, lvl=0):

        lines = []

        if inner == False:
            lines.extend(self.createHeader(model, model.name))
            lines.extend(self.createImport(model, model.name))

        lines.extend(self.createClassRemark(model, model.name, lvl))
        lines.extend(self.createClass(model, model.name, inFileClass, inClassClass, lvl))

        return lines

    def writeFile(self, model, lines):
        outFile = os.path.join(self.outPath, model.name + '.swift')
        util.writeLinesFile(lines, outFile)
        os.system('cd %s; swiftlint autocorrect\n' % self.outPath)

    def createHeader(self, modelJson, name):
        lines = []
        h = '''//
            //  main.swift
            //  ____
            //
            //  Created by ylin on 2018/6/27.
            //  Copyright © 2018年 QuTui Science and Technology Co., Ltd. All rights reserved.
            //
            
            '''
        lines.append(h.replace('    ', ''))

        return lines

    def createImport(self, modelJson, name):
        lines = []
        for imp in self.selfConf.importModule:
            lines.append('import %s' % (imp))

        lines.append('')
        return lines

    def createClassRemark(self, modelJson, name, lvl=0):
        lines = []
        lines.append('%s/**' % (util.space(lvl)))
        lines.append('%s' % (util.space(lvl)))
        lines.append('%s*/' % (util.space(lvl)))
        return lines

    def createClass(self, model, name, inFile, inClass, lvl=0):
        lines = []
        lines.append('%sclass %s: Mappable {' % (util.space(lvl), name))

        for prop in model.props:
            lines.extend(self.createProp(prop, lvl + 1))
        lines.append('')

        lines.extend(self.createFunc(model, lvl + 1))

        if inClass and len(inClass):
            for sub in inClass:
                lines.extend(self.createModelFile(sub, inner=True, lvl=1))

        lines.append('%s}' % (util.space(lvl)))
        lines.append('')
        lines.append('')
        if inFile and len(inFile):
            for sub in inFile:
                lines.extend(self.createModelFile(sub, inner=True))
        return lines

    def createFunc(self, model, lvl):
        lines = []

        # init
        lines.append('%srequired init?(map: Map) {' % (util.space(lvl)))
        lines.append('%s' % (util.space(lvl)))
        lines.append('%s}' % (util.space(lvl)))
        lines.append('%s' % (util.space(lvl)))

        lines.append('%sfunc mapping(map: Map) {' % (util.space(lvl)))

        for prop in model.props:
            lines.append('%s%s    <- map["%s"]' % (util.space(lvl + 1), prop.name, prop.name))

        lines.append('%s' % (util.space(lvl)))
        lines.append('%s}' % (util.space(lvl)))
        lines.append('%s' % (util.space(lvl)))

        return lines

    def createProp(self, prop, lvl):
        lines = []
        type = prop.type
        if self.selfConf.baseType.has_key(prop.type):
            type = self.selfConf.baseType[prop.type]

        if prop.type == 'list':
            subType = prop.subTypes[0]
            if self.selfConf.baseType.has_key(subType):
                subType = self.selfConf.baseType[subType]
            type = '[%s]' % subType

        aVer = util.space(lvl) + 'var ' + prop.name + ': ' + type + '?'
        aVer += (u"  //< %s" % (prop.name))
        lines.append(aVer)
        return lines
