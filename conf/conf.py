# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

class Conf():
    def __init__(self):
        self.author = '作者'
        self.dataPath = 'data'

        map = dict()
        self.map = map

        map['ConfigApiModel.json.weexPaths'] = 'WeexPage'
        map['ConfigApiModel.json.coin_page'] = 'CoinInfoPage'
