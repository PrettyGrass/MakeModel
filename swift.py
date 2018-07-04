# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import os, json, sys, re
import util


class Swift():
    def __init__(self, wkPath):

        modelPath = os.path.join(wkPath, 'Model')
        confPath = os.path.join(wkPath, 'conf', 'swift.json')
        globalConfPath = os.path.join(wkPath, 'conf', 'conf.json')
        outPath = os.path.join(wkPath, 'Product', 'swift')

        self.wkPath = wkPath
        self.outPath = outPath
        self.modelPath = modelPath
        self.conf = util.readJsonFile(confPath)
        self.globalConf = util.readJsonFile(globalConfPath)

    def build(self):
        print 'build swift'
        self.getModels()

    def clear(self):
        print 'clear swift'

    def init(self):
        print 'init swift'

    def getModels(self):

        print '模型路径', self.modelPath
        path = os.listdir(self.modelPath)
        for p in path:
            file = os.path.join(self.modelPath, p)
            if os.path.isfile(file) and p[-4:] == 'json':
                name = re.split('\.', p, 1)[0]
                self.parseFile(file, name)

    def parseFile(self, file, name):
        self.createModelFile(util.readJsonFile(file), name)

    def createModelFile(self, modelJson, name):
        lines = []
        lines.extend(self.createHeader(modelJson, name))
        lines.extend(self.createClass(modelJson, name))

        outFile = os.path.join(self.outPath, modelJson.get('name', name + '.swift'))
        util.writeLinesFile(lines, outFile)
        print lines

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

    def createClass(self, modelJson, name):
        lines = []
        lines.append('class ' + name + ' {')
        fields = modelJson.get("fields", [])
        for field in fields:
            lines.extend(self.createProp(field, 1))

        lines.append('}')
        return lines

    def createProp(self, field, lvl):
        print field, lvl
        lines = []
        type = self.conf.get('innerType').get(field.get('type'), field.get('type'))
        aVer = util.space(lvl) + 'var ' + field.get('name') + ': ' + type + '?'
        aVer += (u"   //< " +  field.get('remark'))
        lines.append(aVer)
        print lines
        return lines
