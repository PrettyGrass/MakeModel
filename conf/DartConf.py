# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from conf import Conf


class DartConf(Conf):
    def __init__(self):
        Conf.__init__(self)

        self.apiBaseClassPreFix = 'DP'
        self.modelBaseClass = 'Object'
        self.apiBaseClass = 'Object'
        self.apiImport = []
        self.baseType = dict()

        self.baseType['string'] = {'name': 'String', 'default': '""'}
        self.baseType['int'] = {'name': 'Int', 'default': 0}
        self.baseType['float'] = {'name': 'Float', 'default': 0.0}
        self.baseType['double'] = {'name': 'Double', 'default': 0.0}
        self.baseType['long'] = {'name': 'Int', 'default': 0}
        self.baseType['void'] = {'name': 'Void'}
        self.baseType['list'] = {'name': '[subtype]', 'default': '[]'}

        self.apiImport = ['import Foundation', 'import DTDependContainer', 'import DTNetwork', 'import DPIntlModel']
        self.importModule = []
        self.useHandyJSON = False
        self.useObjectMapper = False
        self.useYYModel = False
        if self.useHandyJSON:
            self.importModule.append('HandyJSON')
        if self.useObjectMapper:
            self.importModule.append('ObjectMapper')
        if self.useYYModel:
            self.importModule.append('YYModel')

        # 转义字段
        self.transferProp = dict()
        # self.transferProp['copy'] = 'ccopy'
        # self.transferProp['hash'] = 'hashVal'
        # self.transferProp['description'] = 'desc'
        # self.transferProp['id'] = 'Id'

    # 获取属性修饰
    def getPropMask(self, type):
        mask = ''
        return mask

    # 是否基础类型
    def isBaseType(self, type):
        for key in self.baseType.keys():
            val = self.baseType[key]
            if key == type or val['name'] == type:
                return True

        return self.baseType.has_key(type)

    # 获取属性类型
    def getPropType(self, type, subTypes=None):

        needAddPoint = True
        typeStr = type
        if self.baseType.has_key(type):
            typeStr = self.baseType.get(type)['name']
            needAddPoint = False

        if type == 'list' and len(subTypes) > 0:
            typeStr = typeStr.replace('subtype', self.getPropType(subTypes[0]))

        return typeStr

    def fromJson(self, json):
        Conf.fromJson(self, json)
        if json.has_key('transferProp'):
            transferProp = json['transferProp']
            for key in transferProp.keys():
                val = transferProp[key]
                self.transferProp[key] = val

        if json.has_key('baseType'):
            baseType = json['baseType']
            for key in baseType.keys():
                val = baseType[key]
                self.baseType[key] = val

        if json.has_key('apiImport'):
            self.apiImport = json['apiImport']

        if json.has_key('apiBaseClassPreFix'):
            self.apiBaseClassPreFix = json['apiBaseClassPreFix']

        if json.has_key('apiBaseClass'):
            self.apiBaseClass = json['apiBaseClass']

        if json.has_key('modelBaseClass'):
            self.modelBaseClass = json['modelBaseClass']

        if json.has_key('importModule'):
            self.importModule = json['importModule']

        if json.has_key('useYYModel'):
            self.useYYModel = json['useYYModel']

        if json.has_key('useHandyJSON'):
            self.useHandyJSON = json['useHandyJSON']

        if json.has_key('useObjectMapper'):
            self.useObjectMapper = json['useObjectMapper']
