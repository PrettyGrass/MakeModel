# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from conf import Conf


class SwiftConf(Conf):
    def __init__(self):
        Conf.__init__(self)
        self.dataPath = 'data'

        self.baseType = dict()

        self.baseType['string'] = 'String'
        self.baseType['int'] = 'Int'
        self.baseType['float'] = 'Float'
        self.baseType['double'] = 'Double'
        self.baseType['long'] = 'Long'
        self.baseType['void'] = 'Void'
        self.baseType['list'] = '[subtype]'


        self.apiImport = ['import Foundation', 'import DTDependContainer', 'import DTNetwork', 'import DPIntlModel']
        self.importModule = []
        self.useHandyJSON = True
        self.useObjectMapper = False
        if self.useHandyJSON:
            self.importModule.append('HandyJSON')
        if self.useObjectMapper:
            self.importModule.append('ObjectMapper')

    # 获取属性修饰
    def getPropMask(self, type):
        originType = ''
        mask = '@objc dynamic'
        return mask

    # 是否基础类型
    def isBaseType(self, type):
        return self.baseType.has_key(type)

    # 获取属性类型
    def getPropType(self, type, subTypes=None):

        needAddPoint = True
        typeStr = type
        if self.baseType.has_key(type):
            typeStr = self.baseType.get(type)
            needAddPoint = False

        if type == 'list' and len(subTypes) > 0:
            typeStr = typeStr.replace('subtype', self.getPropType(subTypes[0]))

        return typeStr
