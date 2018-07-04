# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import os
import oc, java
from swift import Swift

def build(wkPath):
    oc.build(wkPath)
    java.build(wkPath)
    # swift.build(wkPath)


def clear(wkPath):
    oc.clear(wkPath)
    java.clear(wkPath)
    # /swift.clear(wkPath)


def init(wkPath):
    oc.init(wkPath)
    java.init(wkPath)
    # swift.init(wkPath)



if __name__ == '__main__':
    wkPath = os.path.dirname('.')  # 当前的目录
    wkPath = os.path.abspath(wkPath)
    print 'wk:', wkPath
    clear(wkPath)
    init(wkPath)
    build(wkPath)


    swift = Swift(wkPath)
    swift.init()
    swift.clear()
    swift.build()