from mysmb import MYSMB
from impacket import smb, smbconnection, nt_errors
from impacket.uuid import uuidtup_to_bin
from impacket.dcerpc.v5.rpcrt import DCERPCException
from struct import pack
import threading
import sys
import logger
'''
Script for
- check target if MS17-010 is patched or not.
- find accessible named pipe

USERNAME = ''
PASSWORD = ''
target = ''
'''
NDR64Syntax = ('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0')

MSRPC_UUID_BROWSER  = uuidtup_to_bin(('6BFFD098-A112-3610-9833-012892020162','0.0'))
MSRPC_UUID_SPOOLSS  = uuidtup_to_bin(('12345678-1234-ABCD-EF00-0123456789AB','1.0'))
MSRPC_UUID_NETLOGON = uuidtup_to_bin(('12345678-1234-ABCD-EF00-01234567CFFB','1.0'))
MSRPC_UUID_LSARPC   = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AB','0.0'))
MSRPC_UUID_SAMR     = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AC','1.0'))

pipes = {
    'browser'  : MSRPC_UUID_BROWSER,
    'spoolss'  : MSRPC_UUID_SPOOLSS,
    'netlogon' : MSRPC_UUID_NETLOGON,
    'lsarpc'   : MSRPC_UUID_LSARPC,
    'samr'     : MSRPC_UUID_SAMR,
}

'''
if len(sys.argv) != 2:
    print("{} <ip>".format(sys.argv[0]))
    sys.exit(1)

target = sys.argv[1]
'''
def checkVuln(target,user,pwd):
    result = {'target':target,'user':user,'pwd':pwd,'logon':'','vuln':'','piped':'','OS':'','arch':''}
    logger.log.info('check target:%s user:%s pwd:%s'%(target,user,pwd))
    conn = MYSMB(target)
    try:
        conn.login(user, pwd)
        result['logon'] = 'OK'
    except smb.SessionError as e:
        logger.log.info(target + ' Login failed: ' + nt_errors.ERROR_MESSAGES[e.error_code][0])
        result['logon'] = 'NO'
        return result
    finally:
        result['OS'] = conn.get_server_os()
        logger.log.info(target + ' OS:' + conn.get_server_os())
    
    tid = conn.tree_connect_andx('\\\\'+target+'\\'+'IPC$')
    conn.set_default_tid(tid)
    
    
    # test if target is vulnerable
    TRANS_PEEK_NMPIPE = 0x23
    recvPkt = conn.send_trans(pack('<H', TRANS_PEEK_NMPIPE), maxParameterCount=0xffff, maxDataCount=0x800)
    status = recvPkt.getNTStatus()
    if status == 0xC0000205:  # STATUS_INSUFF_SERVER_RESOURCES
        logger.log.info(target + ' is not patched')
        result['vuln'] = 'OK'
    else:
        result['vuln'] = 'NO'
        logger.log.info(target + ' is patched')
        return result
    
    #print('')
    #print('=== Testing named pipes ===')
    for pipe_name, pipe_uuid in pipes.items():
        try:
            dce = conn.get_dce_rpc(pipe_name)
            dce.connect()
            try:
                dce.bind(pipe_uuid, transfer_syntax=NDR64Syntax)
                result['piped'] += pipe_name + " "
                logger.log.info('{}: Ok (64 bit)'.format(pipe_name))
            except DCERPCException as e:
                if 'transfer_syntaxes_not_supported' in str(e):
                    result['piped'] += pipe_name + " "
                    logger.log.info('{}: Ok (32 bit)'.format(pipe_name))
                else:
                    result['piped'] += pipe_name + " "
                    logger.log.info('{}: Ok ({})'.format(pipe_name, str(e)))
            dce.disconnect()
        except smb.SessionError as e:
            logger.log.info('{}: {}'.format(pipe_name, nt_errors.ERROR_MESSAGES[e.error_code][0]))
        except smbconnection.SessionError as e:
            logger.log.info('{}: {}'.format(pipe_name, nt_errors.ERROR_MESSAGES[e.error][0]))
    
    conn.disconnect_tree(tid)
    conn.logoff()
    conn.get_socket().close()
    
    return result

def checkVulnFromQueue(addrQueue,resultQueue,checkResultDic,signal):
    #while not addrQueue.empty():
    while True:
        #if(signal['stop'] == 1):
        #    break
        try:
            
            try:
                item = addrQueue.get(True,3)
            except Exception,ex:
                break 
            #item = addrQueue.get(True,3)
            target = item['target']
            if(checkResultDic.get(target)):
                continue
            user = item['user']
            pwd = item['pwd']
            
            result = checkVuln(target,user,pwd)
            if(result['vuln'] == 'OK' and result['piped'] != ''):
                #signal['stop'] = 1
                logger.log.info('check succeed target:%s user:%s pwd:%s'%(target,user,pwd))
                checkResultDic[str(target)] = item
                resultQueue.put(item,True)
            else:
                logger.log.info('check failure target:%s user:%s pwd:%s'%(target,user,pwd))
        except Exception,ex:
            logger.log.warning("checkVulnFromQueue error! ERROR:%s"%str(ex))   
            
def checkTh(addrQueue,resultQueue,count,checkResultDic,thlist):
    #thlist = []
    signal = {'stop':0}
    for i in range(count):
        try:
            checkerth = threading.Thread(target=checkVulnFromQueue,args=(addrQueue,resultQueue,checkResultDic,signal))
            thlist.append(checkerth)
            checkerth.setDaemon(True)
            checkerth.start()
            logger.log.info("check THREAD:%d started!"%i) 
            #checkerth.join()
        except Exception,ex:
            logger.log.warning("checkTh error! ERROR:%s"%str(ex))
    #return signal           