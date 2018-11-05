# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from conf import Conf


class OCConf(Conf):
    def __init__(self):
        Conf.__init__(self)

        self.apiBaseClass = 'NSObject'
        self.apiBaseClassPreFix = 'DP'
        self.apiImport = ['#import <Foundation/Foundation.h>', '#import <DTNetwork/DTNetworkSample.h>']
        self.apiInnerImport = []
        self.apiFuncReturnType = 'DTOperationID'

        self.baseType = dict()
        self.baseType['string'] = 'NSString * '
        self.baseType['int'] = 'NSInteger '
        self.baseType['float'] = 'float '
        self.baseType['double'] = 'double '
        self.baseType['long'] = 'long '
        self.baseType['void'] = 'void'
        self.baseType['list'] = 'NSArray *'

        # 转义字段
        self.transferProp = dict()
        # self.transferProp['copy'] = 'ccopy'
        # self.transferProp['hash'] = 'hashVal'
        # self.transferProp['description'] = 'desc'
        # self.transferProp['id'] = 'Id'

    # 获取属性修饰
    def getPropMask(self, type):
        originType = ''
        mask = ''
        isBase = False
        if self.baseType.has_key(type):
            originType = self.baseType.get(type)
            isBase = True

        if (originType.find('*') > 0 and type == 'string') or originType.find('^') >= 0:
            mask = '(nonatomic, copy)'

        elif originType.find('*') > 0:
            mask = '(nonatomic, strong)'
        elif not isBase:
            mask = '(nonatomic, strong)'
        else:
            mask = '(nonatomic, assign)'
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

        if needAddPoint and type.find('^') > 0:
            needAddPoint = False

        if type == 'list' and len(subTypes) > 0:
            typeStr = typeStr.replace('*', '').replace(' ', '')
            typeStr += ' <%s>' % (self.getPropType(subTypes[0]))
            typeStr = typeStr + ' * '

        if needAddPoint:
            typeStr = typeStr + ' * '

        return typeStr

    def fromJson(self, json):
        Conf.fromJson(self, json)
        if json.has_key('transferProp'):
            transferProp = json['transferProp']
            for key in transferProp.keys():
                val = transferProp[key]
                self.transferProp[key] = val
        if json.has_key('apiImport'):
            self.apiImport = json['apiImport']

        if json.has_key('apiInnerImport'):
            self.apiInnerImport = json['apiInnerImport']

        if json.has_key('apiBaseClassPreFix'):
            self.apiBaseClassPreFix = json['apiBaseClassPreFix']

        if json.has_key('modelBaseClass'):
            self.modelBaseClass = json['modelBaseClass']
