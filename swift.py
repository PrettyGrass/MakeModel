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
            self.createModelFile(model)
            self.createModels(model.innerClass)

    def createModelFile(self, model):
        lines = []
        lines.extend(self.createHeader(model, model.name))
        lines.extend(self.createClass(model, model.name))

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
            
            
            /**
            
            
            */'''
        lines.append(h.replace('    ', ''))

        return lines

    def createClass(self, model, name):
        lines = []
        lines.append('class ' + name + ' {')
        for prop in model.props:
            lines.extend(self.createProp(prop, 1))

        lines.append('}')
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
