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

        self.importModule = []
        self.useHandyJSON = True
        self.useObjectMapper = False
        if self.useHandyJSON:
            self.importModule.append('HandyJSON')
        if self.useObjectMapper:
            self.importModule.append('ObjectMapper')
