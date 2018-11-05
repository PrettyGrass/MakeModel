# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


import os, OC, java, util, re, sys
from ClassInfo import *
from conf import Conf
from DataModel import *


class ParseModelJson():
    def __init__(self, conf, wkPath):
        self.wkPath = wkPath
        self.modelPath = os.path.join(wkPath, 'Model')
        self.conf = conf

    def getModels(self):
        models = []
        print '模型路径', self.modelPath
        path = os.listdir(self.modelPath)
        for p in path:
            file = os.path.join(self.modelPath, p)
            if os.path.isfile(file) and p[-4:] == 'json':
                name = re.split('\.', p, 1)[0]
                models.append(self.parseFile(file, name))

        return models

    def parseFile(self, file, name):
        content = util.readJsonFile(file)
        return self.parseContent(content, name)

    # 递归解析数据结构
    def parseContent(self, content, name, paths=None):
        keyPath = name
        clazz = ModelInfo()
        clazz.name = self.getMapPath(keyPath, name)
        if paths == None:
            paths = re.split('\.', self.conf.dataPath)

        for index in range(len(paths)):
            path = paths[index]
            content = content.get(path)

            self.createModelProps(content, clazz, clazz, keyPath)

        return clazz

    def createModelProps(self, modelJson, rootClass, currentClass, keyPath):
        props = []
        if isinstance(modelJson, list):
            if len(modelJson) == 0:
                modelJson.append(dict())
            modelJson = modelJson[0]

        for key, val in modelJson.items():

            keyP = (keyPath + '.%s' % key)
            # 忽略
            if keyP in self.conf.ignore:
                print '忽略:', keyP
                continue

            prop = FieldInfo()
            prop.name = key

            type = util.getValueTypeString(val)
            refType = None
            subType = ''

            if type == 'dict':
                # 对象 1, 获取映射类型, 获取失败使用key变大驼峰
                innerClass = ModelInfo()
                innerClass.name = self.getMapPath(keyP, key)
                self.createModelProps(val, rootClass, innerClass, keyP)
                rootClass.subModels.append(innerClass)
                type = innerClass.name
                refType = innerClass.name

            elif type == 'list':
                # 列表类型
                if len(val) == 0:
                    val.append(dict())
                itemVal = val[0]
                if util.getValueTypeString(itemVal) == 'dict':
                    # 数组下面的对象
                    innerClass = ModelInfo()
                    innerClass.name = self.getMapPath(keyP, key)
                    self.createModelProps(val, rootClass, innerClass, keyP)
                    rootClass.subModels.append(innerClass)
                    subType = innerClass.name

                elif util.getValueTypeString(itemVal) == 'list':
                    # 集合下面是集合 此种情况暂时未遇见
                    assert '奇葩的数据结构, 去杀了api'
                else:
                    # 集合下面是非对象类型
                    subType = util.getValueTypeString(itemVal)

            prop.subType = subType
            prop.type = type
            prop.ref = refType
            props.append(prop)
        currentClass.fields.extend(props)

    def getMapPath(self, keyPath, key):
        name = self.conf.propMap.get(keyPath, '')
        if len(name) == 0:
            name = util.underlinesToCamel(key)
        return name
