# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


class OCConf():
    def __init__(self):
        self.author = '作者'
        self.dataPath = 'data'

        self.apiBaseClass = 'NSObject'
        self.apiBaseClassPreFix = 'QTT'
        self.apiImport = ['<Foundation/Foundation.h>', '"DTHttpService.h"']
        self.apiFuncReturnType = 'DTOperationID'

        baseType = dict()
        self.baseType = baseType

        baseType['string'] = 'NSString *'
        baseType['int'] = 'NSInteger'
        baseType['float'] = 'float'
        baseType['double'] = 'double'
        baseType['long'] = 'long'

        self.importModule = []
        self.importModule.append('ObjectMapper')
