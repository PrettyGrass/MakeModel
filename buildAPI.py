# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from ObjectiveC import *
from Swift import *
from ParseApiJson import *
import os
import util
from conf import *


# 参数
class Params:
    def __init__(self):
        self.confPath = ''
        self.confJson = None
        self.coreJson = None

        self.coreConf = None

        self.apiJsonPath = None

        self.enableSwift = False
        self.swiftConf = None
        self.swiftApiOutPath = ""
        self.swiftModelOutPath = ""

        self.enableOC = False
        self.ocConf = None
        self.ocApiOutPath = ""
        self.ocModelOutPath = ""

    def parse(self):
        if not os.path.exists(self.confPath):
            return None

        confJson = util.readJsonFile(self.confPath)
        if confJson.has_key('core'):
            self.coreJson = confJson.get('core')
            self.apiJsonPath = self.coreJson.get('apiJsonPath').encode('utf-8')
            self.coreConf = Conf()
            self.coreConf.fromJson(self.coreJson)

        self.confJson = confJson
        if confJson.has_key('swift'):
            swift = confJson.get('swift')
            self.enableSwift = True
            self.swiftApiOutPath = swift['apiOutPath']
            self.swiftModelOutPath = swift['apiModelPath']
            self.swiftConf = SwiftConf()
            self.swiftConf.fromJson(self.coreJson)
            self.swiftConf.fromJson(swift)

        if confJson.has_key('oc'):
            oc = confJson.get('oc')
            self.enableSwift = True
            self.ocApiOutPath = oc['apiOutPath']
            self.ocModelOutPath = oc['apiModelPath']
            self.ocConf = OCConf()
            self.ocConf.fromJson(self.coreJson)
            self.ocConf.fromJson(oc)

        return self


# 获取命令行参数
def getParams():
    print "脚本名:", sys.argv[0]
    pName = ''
    params = Params()
    for i in range(1, len(sys.argv)):
        pValue = sys.argv[i]
        if pValue.find('-') == 0:
            pName = sys.argv[i]
            if pName == '-h':
                print '''
                -c 配置文件
                '''
        elif pName == '-c':
            params.confPath = pValue
    params.confPath = '/Users/ylin/.wk_space/MakeModel/conf/sample.config.json'
    return params.parse()


if __name__ == '__main__':

    params = getParams()
    if not params:
        print '配置文件异常'
        exit(-1)

    wkPath = params.apiJsonPath  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath, params.ocConf.mark

    pm = ParseApiJson(wkPath, params.coreConf)
    ms = pm.apiGroups()

    print 'api组:', len(ms)
    # 老的
    # ocApi = OCApi(wkPath, ms)
    # ocApi.init()
    # ocApi.build()

    trans = TransAPIModel2OCClass(ms, params.ocConf)
    trans.makeClazzList(trans.trans())

    trans = TransAPIModel2SwiftClass(ms, params.swiftConf)
    trans.makeClazzList(trans.trans())
