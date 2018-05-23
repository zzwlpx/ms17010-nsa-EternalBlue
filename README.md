# ms17010-nsa-EternalBlue
integration ms17010 and nsa-EternalBlue

主要集成nsa的永恒之蓝和ms17010系列poc。
永恒之蓝poc有windows 7/2008 和 windows 8/2012 x64
ms17010 则是win all，Windows Vista以下可以匿名成功获取system权限，
vista以上则需要 命名管道 接入权限，一般需要域用户权限。

Usage: "usage:MyExploiter.py [options] target"

Options:

  --version             show program's version number and exit
  
  -h, --help            show this help message and exit
  
  -m MODE, --mode=MODE  attack mode 0:ms17010 attack one; 1: ms17010 attack by
  
                        file; 2:blue attack one;3:blue attack Mul;4:check
						
                        one;5:check Mul)
						
  -p PORT, --port=PORT  SMB SERVICE PORT
  
  -u USER, --user=USER  SMB USER
  
  -U USERS, --users=USERS user file,SMB USERS
						
  --pwd=password        SMB USER PASSWORD
  
  --pwds=passwords, --pwds=passwords  pwd file,EACH SMB USER PASSWORDS
						
  -t THREADS, --threads=THREADS  thread num
						
  -c COMMOND, --cmd=COMMOND  execute commond on target
						
  -b BATCH, --batch=BATCH    batch file,execute batch file on target
						
基于：https://github.com/worawit/MS17-010 

