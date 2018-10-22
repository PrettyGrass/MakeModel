# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from conf import Conf


class OCConf(Conf):
    def __init__(self):
        Conf.__init__(self)

        self.dataPath = 'data'

        self.apiBaseClass = 'NSObject'
        self.apiBaseClassPreFix = 'ST'
        self.apiImport = ['<Foundation/Foundation.h>', '"DTHttpService.h"']
        self.apiFuncReturnType = 'DTOperationID'

        self.baseType = dict()
        self.baseType['string'] = 'NSString *'
        self.baseType['int'] = 'NSInteger'
        self.baseType['float'] = 'float'
        self.baseType['double'] = 'double'
        self.baseType['long'] = 'long'
        self.baseType['void'] = 'void'

        self.importModule = []
        self.importModule.append('ObjectMapper')
