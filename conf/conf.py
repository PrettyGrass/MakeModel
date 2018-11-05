# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import time


class Conf:
    def __init__(self):
        self.author = 'ylin'
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.mark = '此文件由脚本自动生成, 手动修改文件内容, 将会被覆盖, 如需修改, 可在派生类进行!'

        # 只处理返回的额json的data字段, 最外层结构一样, 是通用的
        self.dataPath = 'data'
        # 生成api时忽略的路径
        self.ignorePath = 'v1'

        propMap = dict()
        self.propMap = propMap

        # 嵌套对象的类名映射
        propMap['TagCategory'] = 'DFFF'

        propMap['PutV1UsersMe'] = 'User'
        propMap['V1UsersMe'] = 'User'
        propMap['V1PassportsFacebook'] = 'User'
        propMap['V1PassportsGoogle'] = 'User'

        propMap['Config.subdataT1'] = 'CoinInfoPage'
        propMap['Config.subdataT2'] = 'CoinInfoPage'

        # api返回嵌套模型写成独立文件
        self.singleFile = []  # ['ConfigApiModel.App']
        # api返回嵌套模型写在同一个文件内, java不支持, oc , swift支持
        self.inFile = []  # ['ConfigApiModel.Channel', 'ConfigApiModel.CoinPage', 'ConfigApiModel.Feed']
        # 不在上面集合内的, 写成内部类

        # 忽略字段
        self.ignore = []  # ['ConfigApiModel.share_tpl.app.xxx']
