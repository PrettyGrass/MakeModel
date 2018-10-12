# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26


from MakeClassFile import MakeClassFile
from ClassInfo import ClassInfo
from ClassInfo import MethodInfo
from ClassInfo import PropInfo
from APIModel import APIGroupInfo


class ObjectiveC(MakeClassFile):
    # 构造方法
    def __init__(self, clazz, model):
        MakeClassFile.__init__(self, clazz, model)

    # 开始
    def run(self):
        lines = []
        self.createBeginRemark(lines)
        self.createClassRemark(lines)
        self.createInterfaceBegin(lines)
        self.createInterfaceBody(lines)
        self.createInterfaceEnd(lines)
        self.createEndRemark(lines)
        print '\n'.join(lines)

        # lines = []
        # self.createBeginRemark(lines)
        # self.createClassRemark(lines)
        # self.createImplBegin(lines)
        # self.createImplBody(lines)
        # self.createImplEnd(lines)
        # self.createEndRemark(lines)
        #
        # print '\n'.join(lines)

    # 创建头部注释
    def createBeginRemark(self, lines):
        lines.append('''\
        /**
        头部注释
        */
        ''')

    # 创建头部注释
    def createEndRemark(self, lines):
        lines.append('''\
        /**
        尾部注释
        */
        ''')

    # 创建类注释
    def createClassRemark(self, lines):
        lines.append('''\
        
        
        /**
        类注释
        */
        ''')

    # 创建接口
    def createInterfaceBegin(self, lines):
        lines.append('@interface %s : %s' % (self.clazz.name, self.clazz.name))

    # 创建接口
    def createInterfaceBody(self, lines):
        for prop in self.clazz.props:
            self.createProp(lines, prop)

        for method in self.clazz.methods:
            self.createInterfaceFunc(lines, method)

    # 创建接口
    def createInterfaceFunc(self, lines, method):
        lines.append('- (%s)%s;' % (method.retType, method.name))

    # 创建接口
    def createInterfaceEnd(self, lines):
        lines.append('@end')

    # 创建实现
    def createImplBegin(self, lines):
        pass

    # 创建实现
    def createImplBody(self, lines):
        pass

    # 创建实现
    def createImplEnd(self, lines):
        pass

    # 创建属性
    def createProp(self, lines, prop):
        lines.append('@property %s %s' % (prop.type, prop.name))

    # 创建方法
    def createFuncBegin(self, lines, func):
        pass

    # 创建方法
    def createFuncBody(self, lines, func):
        pass

    # 创建方法
    def createFuncEnd(self, lines, func):
        pass


if __name__ == '__main__':
    clazz = ClassInfo()
    clazz.name = 'User'

    for i in range(10):
        m = MethodInfo()
        m.name = 'method%d' % i
        clazz.methods.append(m)

    for i in range(10):
        p = PropInfo()
        p.name = 'prop%d' % i
        clazz.props.append(p)

    model = APIGroupInfo()
    objc = ObjectiveC(clazz, model)

    objc.run()
