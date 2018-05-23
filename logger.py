# -*- coding: UTF-8 -*-
#开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
import logging
import logging.handlers
#import readcfg
#cfg=readcfg.Config('config.ini')

class Logger():
    #def __init__(self, logname, loglevel, logger):
    def __init__(self,loggerName):
        #logLevel={'debug':'DEBUG','info':'INFO','warning':logging.WARNING,'error':logging.ERROR,'critical':logging.CRITICAL}
        self.loggerName = loggerName
    def getlogger(self , formatterStr):
        # 创建一个logger
        #logger = self.loggerName
        logfile = self.loggerName+"_log.txt"
        self.logger = logging.getLogger(self.loggerName)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件,每天一个日志文件
        tfilehandler = logging.handlers.TimedRotatingFileHandler(logfile,'D',1)

        tfilehandler.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(logging.DEBUG)

        #创建一个handler，用于发送smtp邮件
        #smtphandler = logging.handlers.SMTPHandler('smtp.139.com', 'test@139.com', ['test@qq.com'], 'FileTran critical log',('test@139.com', 'test'))
        #smtphandler.setLevel(logging.CRITICAL)
        # 定义handler的输出格式
        formatter = logging.Formatter(formatterStr)
        #formatter = logging.Formatter(formatter)
        #formatter = format_dict[int(loglevel)]
        tfilehandler.setFormatter(formatter)
        consolehandler.setFormatter(formatter)
        #smtphandler.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(tfilehandler)
        self.logger.addHandler(consolehandler)
        #self.logger.addHandler(smtphandler)

        return self.logger
#tmpFormatter = '%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s'
tmpFormatter = '%(asctime)s - %(levelname)s - %(message)s'
resFormatter = '%(message)s'
log = Logger("ms17010").getlogger(tmpFormatter)
checkLog = Logger("check").getlogger(resFormatter)
exploitLog = Logger("exploit").getlogger(resFormatter)