# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

from ObjectiveC import *
from ParseApiJson import *
import os
import json
from ParseModelJson import ParseModelJson


# 获取所有api的数据模型
def allModels(apiGroups):
    modelMapper = {}
    for index in range(len(apiGroups)):
        apiGroup = apiGroups[index]
        for index in range(len(apiGroup.apis)):
            api = apiGroup.apis[index]
            if len(api.paths) == 0:
                continue
            if api.responses and len(api.responses) > 0:
                pm = ParseModelJson(wkPath)
                ms = []
                jsonObj = json.loads(api.responses[0].get('body'))
                responseKey = util.firstUpper(api.getMethodName())
                ms.append(pm.parseContent(jsonObj, responseKey))
                trans = TransDataModel2OCClass(ms)
                cls = trans.trans()
                print 'API数据模型:', api.getMethodName(), cls
                modelMapper[responseKey.lower()] = cls[0]
                trans.makrClazzList(cls, os.path.join(wkPath, 'Product', 'ocmodel'))

    return modelMapper


if __name__ == '__main__':
    wkPath = os.path.dirname('.')  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath

    pm = ParseApiJson(wkPath)
    ms = pm.apiGroups()

    print 'api组:', len(ms)
    # 老的
    # ocApi = OCApi(wkPath, ms)
    # ocApi.init()
    # ocApi.build()

    trans = TransAPIModel2OCClass(ms)
    trans.allModelMapper = allModels(ms)
    trans.makrClazzList(trans.trans(), os.path.join(wkPath, 'Product', 'ocapi'))
