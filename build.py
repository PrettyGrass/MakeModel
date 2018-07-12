# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import os, oc, java, util, re, sys
from ClassInfo import *
from swift import *

sys.path.append('./conf')
sys.path.append('./script')
import cm2us
from conf import Conf


class ParseModel():
    def __init__(self, wkPath):
        self.wkPath = wkPath
        self.modelPath = os.path.join(wkPath, 'Model')
        self.conf = Conf()

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
        clazz = ClassInfo()
        clazz.name = name

        paths = re.split('\.', self.conf.dataPath)
        content = util.readJsonFile(file)
        for index in range(len(paths)):
            path = paths[index]
            content = content.get(path)
        keyPath = name
        self.createModelProps(content, clazz, clazz, keyPath)

        return clazz

    def createModelProps(self, modelJson, rootClass, currentClass, keyPath):
        props = []
        if isinstance(modelJson, list):
            if len(modelJson) == 0:
                modelJson.append(dict())
            modelJson = modelJson[0]

        for key, val in modelJson.items():
            prop = PropInfo()
            prop.name = key

            type = util.getValueTypeString(val)
            subTypes = []
            keyP = (keyPath + '.%s' % key)
            if type == 'dict':
                # 对象 1, 获取映射类型, 获取失败使用key变大驼峰
                innerClass = ClassInfo()
                innerClass.name = self.getMapPath(keyP, key)
                self.createModelProps(val, rootClass, innerClass, keyP)
                rootClass.innerClass.append(innerClass)
                type = innerClass.name
            elif type == 'list':
                # 列表类型
                if len(val) == 0:
                    val.append(dict())
                itemVal = val[0]
                if util.getValueTypeString(itemVal) == 'dict':
                    # 数组下面的对象
                    innerClass = ClassInfo()
                    innerClass.name = self.getMapPath(keyP, key)
                    self.createModelProps(val, rootClass, innerClass, keyP)
                    rootClass.innerClass.append(innerClass)
                    subTypes.append(innerClass.name)

                elif util.getValueTypeString(itemVal) == 'list':
                    # 集合下面是集合 此种情况暂时未遇见
                    assert '奇葩的数据结构, 去杀了api'
                else:
                    # 集合下面是非对象类型
                    subTypes.append(util.getValueTypeString(itemVal))

            prop.subTypes = subTypes
            prop.type = type
            props.append(prop)
        currentClass.props.extend(props)

    def getMapPath(self, keyPath, key):
        name = self.conf.map.get(keyPath, '')
        if len(name) == 0:
            name = cm2us.underlinesToCamel(key)
        return name


if __name__ == '__main__':
    wkPath = os.path.dirname('.')  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath

    pm = ParseModel(wkPath)
    ms = pm.getModels()
    
    swift = Swift(wkPath, ms)
    swift.init()
    swift.clear()
    swift.build()
