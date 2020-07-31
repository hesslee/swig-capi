#-*- coding: utf-8 -*-
from __future__ import print_function
import capi

CONN_STR = "Server=127.0.0.1;PORT_NO=20300;User=SYS;Password=MANAGER;NLS_USE=UTF8"

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

    rc = capi.altibase_set_autocommit(ab, capi.ALTIBASE_AUTOCOMMIT_OFF);
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise dbcError("altibase_set_autocommit")

    ########## CLOB Insert ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "INSERT INTO DEMO_CLOB VALUES( ?, ? )")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindi_cnt = 2 

    bindi = capi.apx_bind_alloc(bindi_cnt)
    if (bindi == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_int(bindi, 0)
    # column binding : val
    val_max_size = 100
    capi.apx_bind_string(bindi, 1, val_max_size)

    rc = capi.altibase_stmt_bind_param(stmt, bindi)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # column value : id
    capi.apx_bind_put_int(bindi, 0, 1)
    # column value : val
    val = "^.................INSERT..한글.........$"
    capi.apx_bind_put_string(bindi, 1, val)
 
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("clob insert altibase_stmt_execute")

    capi.altibase_stmt_close(stmt);

    ########## SELECT: after clob insert ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_CLOB")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # two columns
    bindr_cnt = 2 

    bindr = capi.apx_bind_alloc(bindr_cnt)
    if (bindr == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_int(bindr, 0)
    # column binding : val
    val_max_size = 100
    capi.apx_bind_string(bindr, 1, val_max_size)

    rc = capi.altibase_stmt_bind_result(stmt, bindr)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_execute")

    rc = capi.altibase_stmt_fetch(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

    val_select = capi.apx_bind_get_string(bindr,1)
    print("insert clob: [" + val_select + ']')
    rc = capi.altibase_stmt_free_result(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

    capi.altibase_stmt_close(stmt);


    ########## CLOB Update ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "UPDATE DEMO_CLOB SET val = ? WHERE ID = ?")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindu_cnt = 2 

    bindu = capi.apx_bind_alloc(bindu_cnt)
    if (bindu == None):
        raise otherError("apx_bind_alloc")

    ### Caution : val is the first parameter in this UPDATE query
    # column binding : val
    val_max_size = 100
    capi.apx_bind_string(bindu, 0, val_max_size)
    # column binding : id
    capi.apx_bind_int(bindu, 1)

    rc = capi.altibase_stmt_bind_param(stmt, bindu)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # column value : val
    val = "^.................UPDATE.....업데이트............$"
    capi.apx_bind_put_string(bindu, 0, val)
    # column value : id
    capi.apx_bind_put_int(bindu, 1, 1)
 
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("clob update altibase_stmt_execute")

    capi.altibase_stmt_close(stmt);


    ########## SELECT: after clob update ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_CLOB")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # two columns
    bindr2_cnt = 2 

    bindr2 = capi.apx_bind_alloc(bindr2_cnt)
    if (bindr2 == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_int(bindr2, 0)
    # column binding : val
    val_max_size = 100
    capi.apx_bind_string(bindr2, 1, val_max_size)

    rc = capi.altibase_stmt_bind_result(stmt, bindr2)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_execute")

    rc = capi.altibase_stmt_fetch(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

    val_select = capi.apx_bind_get_string(bindr2,1)
    print("update clob: [" + val_select + ']')
    rc = capi.altibase_stmt_free_result(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

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
    if 'bindr' in locals():
        capi.apx_bind_free(bindr, bindr_cnt)
    if 'bindr2' in locals():
        capi.apx_bind_free(bindr2, bindr2_cnt)
    if 'bindi' in locals():
        capi.apx_bind_free(bindi, bindi_cnt)
    if 'bindu' in locals():
        capi.apx_bind_free(bindu, bindu_cnt)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'ab' in locals():
        capi.altibase_close(ab)
