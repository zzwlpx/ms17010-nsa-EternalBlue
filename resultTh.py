#coding=utf-8
import threading
import Queue
import logger
import sys
import time
import globalFunc 
reload(sys)
c=sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''

'''
class resultTh(threading.Thread):
    def __init__(self,resultQueue,fileName ,flag):
        threading.Thread.__init__(self, name='resultTh')
        #self.checkQueue=checkQueue
        self.resultQueue=resultQueue
        self.flag = flag
        self.fileName = fileName
    def run(self):
        #while结构内，一直监听此端口直到程序结束
        fpath = self.fileName + time.strftime("%m%d%Y%H%M%S")
        
        while(1):
          try:
              #ckItem = self.checkQueue.get(True,1)
              #writeContent2File("checkReult.txt",str(ckItem))
              item = self.resultQueue.get(True)
              globalFunc.writeContent2File(fpath,str(item))
              if(self.flag == 0):
                  logger.log.info( "\n target:%s is succeed!"%item['addr'] )
              if(self.flag == 1):
                  logger.log.info( str(item) )
          except Exception as e:
              #doorSocket.close()
              logger.log.warning(str(e))   
             