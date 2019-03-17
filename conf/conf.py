# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import time, os


class Conf:
    def __init__(self):
        self.confDir = ''  # 配置文件路径
        self.author = 'ylin'
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.mark = '此文件由脚本自动生成, 手动修改文件内容, 将会被覆盖, 如需修改, 可在派生类进行!'
        self.apiOutPath = ''
        self.apiModelPath = ''

        # 只处理返回的额json的data字段, 最外层结构一样, 是通用的
        self.dataPath = 'data'
        # 生成api时忽略的路径
        self.ignorePath = 'v1'
    
        propMap = dict()
        self.propMap = propMap

        # 嵌套对象的类名映射
        # propMap['TagCategory'] = 'DFFF'
        #
        # propMap['PutV1UsersMe'] = 'User'
        # propMap['V1UsersMe'] = 'User'
        # propMap['V1PassportsFacebook'] = 'User'
        # propMap['V1PassportsGoogle'] = 'User'
        #
        # propMap['Config.subdataT1'] = 'CoinInfoPage'
        # propMap['Config.subdataT2'] = 'CoinInfoPage'

        # api返回嵌套模型写成独立文件
        self.singleFile = []  # ['ConfigApiModel.App']
        # api返回嵌套模型写在同一个文件内, java不支持, oc , swift支持
        self.inFile = []  # ['ConfigApiModel.Channel', 'ConfigApiModel.CoinPage', 'ConfigApiModel.Feed']
        # 不在上面集合内的, 写成内部类

        # 忽略字段
        self.ignore = []  # ['ConfigApiModel.share_tpl.app.xxx']

        self.propAppend = dict()
        

    # 是否是绝对路径
    def isabs(self, path):
        return path[:1] == '/'

    # 转换成绝对路径
    def toabs(self, path):
        if self.isabs(path):
            return path

        return os.path.abspath(os.path.join(self.confDir, path))

    def fromJson(self, json):
        if json.has_key('propMap'):
            propMap = json['propMap']
            for key in propMap.keys():
                val = propMap[key]
                self.propMap[key] = val

        if json.has_key('confDir'):
            self.confDir = json['confDir']

        if json.has_key('apiModelPath'):
            self.apiModelPath = self.toabs(json['apiModelPath'])

        if json.has_key('apiOutPath'):
            self.apiOutPath = self.toabs(json['apiOutPath'])

        if json.has_key('author'):
            self.author = json['author']

        if json.has_key('date'):
            self.date = json['date']

        if json.has_key('mark'):
            self.mark = json['mark']

        if json.has_key('dataPath'):
            self.dataPath = json['dataPath']

        if json.has_key('ignorePath'):
            self.ignorePath = json['ignorePath']
        
        if json.has_key('propAppend'):
            self.propAppend = json['propAppend']