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
            lines = self.createModelFile(model, True)
            self.writeFile(model, lines)

    def createModelFile(self, model, checkSub=False, inner=False):

        inFileClass = []
        inClassClass = []
        inSingle = []
        if checkSub:
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

        lines = []

        if inner == False:
            lines.extend(self.createHeader(model, model.name))

        lines.extend(self.createClassRemark(model, model.name))
        lines.extend(self.createClass(model, model.name, inFileClass, inClassClass))

        return lines

    def writeFile(self, model, lines):
        outFile = os.path.join(self.outPath, model.name + '.swift')
        util.writeLinesFile(lines, outFile)

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

    def createClassRemark(self, modelJson, name, lvl=0):
        lines = []
        h = '''/**

            */'''
        lines.append(h.replace('    ', ''))

        return lines

    def createClass(self, model, name, inFile, inClass, lvl=0):
        lines = []
        lines.append('class ' + name + ' {')
        for prop in model.props:
            lines.extend(self.createProp(prop, lvl + 1))

        if len(inClass):
            for sub in inClass:
                lines.extend(self.createModelFile(sub, inner=True))

        lines.append('}')
        if len(inFile):
            for sub in inFile:
                lines.extend(self.createModelFile(sub, inner=True))
        return lines

    def createProp(self, prop, lvl):
        lines = []
        type = prop.type
        if self.selfConf.baseType.has_key(prop.type):
            type = self.selfConf.baseType[prop.type]

        if prop.type == 'list':
            type = '[%s]' % prop.subTypes[0]

        aVer = util.space(lvl) + 'var ' + prop.name + ': ' + type + '?'
        aVer += (u"  //< %s" % (prop.name))
        lines.append(aVer)
        return lines
