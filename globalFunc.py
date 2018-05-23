#!/usr/bin/python
# -*- coding:utf-8-*-

import logger
import re

def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False
def readLinesFromFile(fPath,lineList):
    #lineList = []
    try:
        file = open(fPath,'r') 
        for line in file:
            lineList.append(line[:-1])
    except Exception,ex:
        logger.log.warning("read file error! ERROR:%s"%str(ex))   
    finally:
        if file:
            file.close()
    return lineList
    
def writeContent2File(fPath,content):
    with open(fPath,'a+') as file:
        file.write(content)
        file.write("\n")
        
def writeLines2File(fPath,lineList):
    content = "\n".join(lineList)
    with open(fPath,'w+') as file:
        file.write(content)
