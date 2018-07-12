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

        # api返回嵌套模型需要写在同一个文件的 同级
        self.inFile = ['ConfigApiModel.App']
        # api返回嵌套模型需要写在类内部的
        self.inClass = ['ConfigApiModel.Channel', 'ConfigApiModel.CoinPage', 'ConfigApiModel.Feed']
        # 不在上面集合内的, 写成独立文件

        self.importModule = ['ObjectMapper']
