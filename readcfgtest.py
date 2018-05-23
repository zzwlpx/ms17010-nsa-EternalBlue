import sys,os,time
import readcfg
cfg=readcfg.Config('logconfig.ini')
level=cfg.get('logfilecfg','logLevel')
print level