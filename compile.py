#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os
import re


def func_call_except(func, *args, **kwargs):
    func(*args, **kwargs)


class Node:
    def __init__(self, currIndex = 0, tag = 0,left=None,right = None):
        self.tag = tag
        self.currIndex = currIndex

        self.left = left
        self.right = right
    
        self.except_func = None     #节点tag 回调
        self.destription = 'node'   #节点描述
        self.runTask = None         #节点的任务
        self.runTaskArgs = []       #节点参数
    
    def appendLeft(self,node):
        self.left = node;
        return node
    
    def appendRight(self,node):
        self.right = node;
        return node

    def getTag(self):
        if callable(self.tag):
            self.tag = self.tag()
        if callable(self.except_func):
            self.tag = self.except_func(self.tag)
        if callable(self.runTask):
            func_call_except(self.runTask,self.runTaskArgs)
        
        return self.tag;


class Instructions:
    def __init__(self):
        self.index = 0
        self.currIndex = 0
    
    def cmd_next(self,head,next):
        head.appendRight(next);
        return next
    
    def cmd_if(self,head,parm,body,else_body):
        node = Node()
        node.destription = 'cmd_if'
        node.tag = parm
        body.destription = "if_true"
        node.appendLeft(body)
        
        node.appendRight(else_body)
        else_body.destription = "if_false"
        head.appendRight(node)

        return node
            
    def cmd_loop(self,head,body,else_body,count):
        node = Node()
        node.destription = 'cmd_loop'
        
        node.tag = (count+1);
        node.except_func = lambda a : a - 1

        node.left = body
        body.destription = "loop_node"
        body.right = node
        node.right = else_body
        else_body.destription = 'loop_break_node'
        head.appendRight(node)
        return node



def post_visit(Tree):
        if Tree:
            post_visit(Tree.left)
            post_visit(Tree.right)
            print Tree.currIndex
def pre_visit(Tree):
        if Tree:
            print Tree.currIndex
            pre_visit(Tree.left)
            pre_visit(Tree.right)


def in_visit(Tree):
    if Tree:
#        print Tree.currIndex
        in_visit(Tree.left)
        print Tree.currIndex
        in_visit(Tree.right)


def runTree(Tree):
    if Tree:

        print  Tree.currIndex, Tree.getTag() ,Tree.destription
#        runTree(Tree.left)
#        runTree(Tree.right)
        if Tree.tag > 0:
            runTree(Tree.left)
        else:
            runTree(Tree.right)





def main():
    
    def test(a):
        print "hello"
    def testParm():
        return 1
    
    node1 = Node(1,0,None,None)
    node1.destription = 'main'
    node2 = Node(2,0,None,None)
    node3 = Node(3,0,None,None)
    node4 = Node(4,0,None,None)
    node5 = Node(5,0,None,None)
    node6 = Node(6,0,None,None)
    node7 = Node(7,0,None,None)
    node8 = Node(8,0,None,None)
    
    node3.runTask = test
    cmd = Instructions()
    
    cmd.cmd_if(node1,testParm,node3,node4)
    cmd.cmd_loop(node4,node6,node7,3)
    
#    node1.appendLeft(node2)
#    node1.appendRight(node3)
#    node2.appendLeft(node4)
#    node2.appendRight(node5)
#    node3.appendLeft(node6)
#    node3.appendRight(node7)
#    node6.appendLeft(node8)
    runTree(node1)

def analysisCmd(cmd):

    m = re.search(r'(if\s*\(\w*\))',cmd)
    print m.groups(1)
    if m:
        n = re.search(r'(\s+[^if]+\(.*\))',cmd)
        print n.groups()


if __name__ == "__main__":  
    #    main()
    import re

#line = "Cats are smarter than dogs"
#
#matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
#
#if matchObj:
#    print "matchObj.group() : ", matchObj.group()
#    print "matchObj.group(1) : ", matchObj.group(1)
#    print "matchObj.group(2) : ", matchObj.group(2)
#else:
#    print "No match!!"
    analysisCmd("if(1) else()")
