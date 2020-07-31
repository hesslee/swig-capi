from __future__ import print_function
import capi
import time

CONN_STR = "Server=127.0.0.1;PORT_NO=20300;User=SYS;Password=MANAGER;AlternateServers=(128.1.3.53:20300,128.1.3.52:20301);ConnectionRetryCount=3;ConnectionRetryDelay=10;SessionFailOver=on;"


class myError(Exception):
    def __init__(self, msg):
        self.msg = msg

class dbcError(myError):
    pass
class stmtError(myError):
    pass
class otherError(myError):
    pass

try:
    ########## Connect ##########
    # allocate handle
    ab = capi.altibase_init()
    if (ab == None):
        raise otherError("altibase_init")

    # Connect to Altibase Server
    rc = capi.altibase_connect(ab, CONN_STR)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise dbcError("altibase_connect")

    rc = capi.altibase_set_failover_callback(ab, capi.SAMPLE_CALLBACK, None);
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise dbcError("altibase_set_failover_callback")

    ## Kill Altibase server to see Session-Time-Failover(STF) steps ##
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")
    rc = capi.altibase_stmt_prepare(stmt, "SELECT to_char(sysdate,'HH:MI:SS') FROM dual")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")
    # One column
    bindt_cnt = 1 
    bindt = capi.apx_bind_alloc(bindt_cnt)
    if (bindt == None):
        raise otherError("apx_bind_alloc")
    # column binding : HHMISS
    capi.apx_bind_string(bindt, 0, 20)
    rc = capi.altibase_stmt_bind_result(stmt, bindt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    for i in range(100):
        rc = capi.altibase_stmt_execute(stmt)
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("altibase_stmt_execute")
        rc = capi.altibase_stmt_fetch(stmt)
        if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
            raise stmtError("altibase_stmt_fetch")
        HHMISS = capi.apx_bind_get_string(bindt,0)
        print("HH:MI:SS : %s" % (HHMISS))
        time.sleep(1)

    capi.altibase_stmt_close(stmt);

    ########## Error handling & Finalization ##########

except dbcError as e:
    print("DBC Error:", e.msg)
    print(capi.altibase_errno(ab), capi.altibase_sqlstate(ab),  capi.altibase_error(ab))
except stmtError as e:
    print("STMT Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt), capi.altibase_stmt_sqlstate(stmt), capi.altibase_stmt_error(stmt))
except otherError as e:
    print("Other Error:", e.msg)
finally:
    if 'bindt' in locals():
        capi.apx_bind_free(bindt, bindt_cnt)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'ab' in locals():
        capi.altibase_close(ab)
