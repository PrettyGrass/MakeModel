# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


class SwiftConf():
    def __init__(self):
        self.author = '作者'
        self.dataPath = 'data'

        baseType = dict()
        self.baseType = baseType

        baseType['string'] = 'String'
        baseType['int'] = 'Int'
        baseType['float'] = 'Float'
        baseType['double'] = 'Double'
        baseType['long'] = 'Long'

        self.importModule = []
        self.useHandyJSON = True
        self.useObjectMapper = False
        if self.useHandyJSON:
            self.importModule.append('HandyJSON')
        if self.useObjectMapper:
            self.importModule.append('ObjectMapper')



