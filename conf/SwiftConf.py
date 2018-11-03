# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from conf import Conf


class SwiftConf(Conf):
    def __init__(self):
        Conf.__init__(self)
        self.dataPath = 'data'

        self.baseType = dict()

        self.baseType['string'] = {'name': 'String', 'default': '""'}
        self.baseType['int'] = {'name': 'Int', 'default': 0}
        self.baseType['float'] = {'name': 'Float', 'default': 0.0}
        self.baseType['double'] = {'name': 'Double', 'default': 0.0}
        self.baseType['long'] = {'name': 'Int', 'default': 0}
        self.baseType['void'] = {'name': '[Void]'}
        self.baseType['list'] = {'name': '[subtype]', 'default': '[]'}

        self.apiImport = ['import Foundation', 'import DTDependContainer', 'import DTNetwork', 'import DPIntlModel']
        self.importModule = []
        self.useHandyJSON = False
        self.useObjectMapper = False
        self.useYYModel = True
        if self.useHandyJSON:
            self.importModule.append('HandyJSON')
        if self.useObjectMapper:
            self.importModule.append('ObjectMapper')
        if self.useYYModel:
            self.importModule.append('YYModel')

        # 转义字段
        self.transferProp = dict()
        self.transferProp['copy'] = 'ccopy'
        self.transferProp['hash'] = 'hashVal'
        self.transferProp['description'] = 'desc'
        self.transferProp['id'] = 'Id'
        self.transferProp['openInDouPai'] = 'dde'

    # 获取属性修饰
    def getPropMask(self, type):
        originType = ''
        mask = '@objc public'
        return mask

    # 是否基础类型
    def isBaseType(self, type):
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
