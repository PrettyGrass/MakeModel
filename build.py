# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import os, oc, java, util, re, sys
from ClassInfo import *
from swift import *
from ParseJson import ParseJson

sys.path.append('./conf')
sys.path.append('./script')
import cm2us
from conf import Conf



if __name__ == '__main__':
    wkPath = os.path.dirname('.')  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath

    pm = ParseJson(wkPath)
    ms = pm.getModels()
    
    swift = Swift(wkPath, ms)
    swift.init()
    swift.build()
