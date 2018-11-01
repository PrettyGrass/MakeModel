# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


from swift import *
from ParseModelJson import ParseModelJson
from ObjectiveC import *

if __name__ == '__main__':
    wkPath = os.path.dirname('.')  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath

    pm = ParseModelJson(wkPath)
    ms = pm.getModels()
    
    # swift = Swift(wkPath, ms)
    # swift.init()
    # swift.build()
    trans = TransDataModel2OCClass(ms)
    trans.makeClazzList(trans.trans(), os.path.join(wkPath, 'Product', 'ocmodel'))

