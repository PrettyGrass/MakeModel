# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


import os, OC, java, util, re, sys, json
from APIModel import *

from conf import Conf


# 解析api数据
class ParseApiJson():
    def __init__(self, wkPath):
        self.wkPath = wkPath
        self.modelPath = os.path.join(wkPath, 'Api')
        self.conf = Conf()

    def apiGroups(self):
        apiGroups = []
        print 'PostMan API文件路径', self.modelPath
        path = os.listdir(self.modelPath)
        for p in path:
            file = os.path.join(self.modelPath, p)
            if os.path.isfile(file) and p[-4:] == 'json':
                name = re.split('\.', p, 1)[0]
                apiGroups.extend(self.parseApiGroups(file, name))

        return apiGroups

    def parseApiGroups(self, file, name):
        apiGroups = []

        content = util.readJsonFile(file)
        items = content.get('item', [])
        for index in range(len(items)):
            apiGroup = APIGroupInfo()
            apiGroups.append(apiGroup)
            item = items[index]
            fullName = item.get('name', '')
            apiGroup.description = item.get('description', '')

            # [\u4e00-\u9fa5]{1,}
            # [A-Za-z]{1,}
            apiGroup.name = fullName
            apiGroup.enName = util.firstUpper(self.diffENName(fullName))

            print 'api组:', apiGroup.name, apiGroup.enName
            apis = item.get('item', [])
            apiGroup.apis.extend(self.parseApis(apis))

        return apiGroups

    # 分离英文名
    def diffENName(self, fullName):
        innerNames = []

        def innerMath(math):
            innerNames.append(math.group())
            return math.group()

        re.sub(r'[A-Za-z0-9]{1,}', innerMath, fullName)
        return ''.join(innerNames)

    def parseApis(self, apisJson):
        apis = []
        for index in range(len(apisJson)):
            item = apisJson[index]
            api = APIInfo()
            apis.append(api)
            api.name = item.get('name')

            # 解析请求
            request = item.get('request')
            url = request.get('url')

            if None == url:
                print '--无效的请求:--', api.name, request
                continue

            api.method = request.get('method')
            api.host = '.'.join(url.get('host'))
            api.protocol = url.get('protocol', 'https')

            # get参数
            api.params.extend(self.parseGetParams(url.get('query', [])))

            # post参数
            api.params.extend(self.parsePostParams(request.get('body')))

            # restful参数
            paths = url.get('path')
            api.params.extend(self.parseRestfulParams(paths))
            api.path = '/'.join(paths)
            api.paths = paths

            # 解析响应
            responses = item.get('response')
            api.responses = responses

            p = ''
            for n in api.params:
                p += ' %s:%s' % (n.type, n.name)

            print '     ', api.name, api.protocol, api.host, api.path, api.method, p

        return apis

    # 解析restful参数
    def parseRestfulParams(self, paths):
        pInfos = []
        # 解析restful参数
        for index in range(len(paths)):
            path = paths[index]

            # 判定restful参数 长度大于20位的
            if len(path) > 20:
                name = 'id'
                if index > 0:
                    name = paths[index - 1] + util.firstUpper(name)

                # 生成新的restful路径
                paths[index] = ':' + name
                restParams = ParamsInfo()
                pInfos.append(restParams)
                restParams.type = 'restful'
                restParams.name = name

        return pInfos

    # 解析get参数
    def parseGetParams(self, querys):
        pInfos = []
        # get参数
        for query in querys:
            getParams = ParamsInfo()

            getParams.type = 'get'
            pInfos.append(getParams)
            getParams.name = query.get('key')

        return pInfos

    # 解析post参数
    def parsePostParams(self, body):
        pInfos = []
        if body == None:
            return pInfos

        mode = body.get('mode')

        if mode == 'raw':
            paramsJson = body.get(mode)
            if paramsJson == '':
                paramsJson = '{}'
            params = json.loads(paramsJson)

            # TODO 目前只处理了单层json数据, 嵌套的没有处理
            for key, val in params.items():
                pInfo = ParamsInfo()
                pInfos.append(pInfo)

                pInfo.type = 'post'
                pInfo.name = key
                pInfo.paramType = util.getValueTypeString(val)

        elif mode != None and len(mode) > 0:
            params = body.get(mode)
            for p in params:
                pInfo = ParamsInfo()
                pInfos.append(pInfo)

                pInfo.type = 'post'
                pInfo.name = p.get('key')
                pInfo.paramType = util.getValueTypeString(p.get('value', ''))

        return pInfos
