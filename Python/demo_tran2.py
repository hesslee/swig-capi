from __future__ import print_function
import capi

CONN_STR = "Server=127.0.0.1;PORT_NO=20300;User=SYS;Password=MANAGER"

class myError(Exception):
    def __init__(self, msg):
        self.msg = msg

class dbcError(myError):
    pass
class stmtError(myError):
    pass
class stmt_selError(myError):
    pass
class stmt_uptError(myError):
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

    ########## Insert ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "INSERT INTO DEMO_TRAN2 VALUES( ?, ?, ? )")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # Three columns
    bindi_cnt = 3 

    bindi = capi.apx_bind_alloc(bindi_cnt)
    if (bindi == None):
        raise otherError("apx_bind_alloc")

    # column binding : ID
    capi.apx_bind_string(bindi, 0, 8)
    # column binding : name
    capi.apx_bind_string(bindi, 1, 20)
    # column binding : age
    capi.apx_bind_int(bindi, 2)

    rc = capi.altibase_stmt_bind_param(stmt, bindi)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    for i in range(1000):
        # column value : ID
        ID = "%08d" % (i)
        capi.apx_bind_put_string(bindi, 0, ID)
        # column value : name
        name = "NAME%d" % (i)
        capi.apx_bind_put_string(bindi, 1, name)
        # column value : age
        capi.apx_bind_put_int(bindi, 2, 10)
 
        rc = capi.altibase_stmt_execute(stmt)
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("Third insert altibase_stmt_execute")

    capi.altibase_stmt_close(stmt);

    ########## SELECT & UPDATE ##########

    stmt_sel = capi.altibase_stmt_init(ab)
    if (stmt_sel == None):
        raise stmt_selError("altibase_stmt_init")

    stmt_upt = capi.altibase_stmt_init(ab)
    if (stmt_upt == None):
        raise stmt_uptError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt_sel, "SELECT id FROM DEMO_TRAN2 order by id")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmt_selError("altibase_stmt_prepare: stmt_sel")

    rc = capi.altibase_stmt_prepare(stmt_upt, "UPDATE demo_tran2 SET age=? WHERE id=?")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmt_uptError("altibase_stmt_prepare: stmt_upt")

    # One column
    bindr_cnt = 1 

    bindr = capi.apx_bind_alloc(bindr_cnt)
    if (bindr == None):
        raise otherError("apx_bind_alloc")

    # column binding : ID
    capi.apx_bind_string(bindr, 0, 8)

    rc = capi.altibase_stmt_bind_result(stmt_sel, bindr)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmt_selError("altibase_stmt_bind_result")

    # Two columns
    bindu_cnt = 2 

    bindu = capi.apx_bind_alloc(bindu_cnt)
    if (bindu == None):
        raise otherError("apx_bind_alloc")

    # column binding : age
    capi.apx_bind_int(bindu, 0)
    # column binding : ID
    capi.apx_bind_string(bindu, 1, 8)

    rc = capi.altibase_stmt_bind_param(stmt_upt, bindu)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmt_uptError("altibase_stmt_bind_param")

    rc = capi.altibase_stmt_execute(stmt_sel)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmt_selError("altibase_stmt_execute")

    rc = capi.altibase_stmt_fetch(stmt_sel)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmt_selError("altibase_stmt_fetch")

    age = 1
    while (rc != capi.ALTIBASE_NO_DATA):
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmt_selError("altibase_stmt_fetch")
        
        ID = capi.apx_bind_get_string(bindr,0)

        # column value : age
        capi.apx_bind_put_int(bindu, 0, age)
        # column value : ID
        capi.apx_bind_put_string(bindu, 1, ID)
 
        rc = capi.altibase_stmt_execute(stmt_upt)
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmt_uptError("altibase_stmt_execute")

        affected_rows = capi.altibase_stmt_affected_rows(stmt_upt)
        if ( affected_rows != 1 ):
            raise otherError("Failed to update")

        age = age + 1
        rc = capi.altibase_stmt_fetch(stmt)

    capi.altibase_stmt_close(stmt_sel);
    capi.altibase_stmt_close(stmt_upt);

    ########## Updated rows count ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")
    rc = capi.altibase_stmt_prepare(stmt, "SELECT count(*) FROM DEMO_TRAN2 where id+1 = age")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")
    # One column
    bindt_cnt = 1 
    bindt = capi.apx_bind_alloc(bindt_cnt)
    if (bindt == None):
        raise otherError("apx_bind_alloc")
    # column binding : count(*)
    capi.apx_bind_int(bindt, 0)
    rc = capi.altibase_stmt_bind_result(stmt, bindt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_execute")
    rc = capi.altibase_stmt_fetch(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")
    count = capi.apx_bind_get_int(bindt,0)
    print("Updated rows count : %d" % (count))

    capi.altibase_stmt_close(stmt);

    ########## Error handling & Finalization ##########

except dbcError as e:
    print("DBC Error:", e.msg)
    print(capi.altibase_errno(ab), capi.altibase_sqlstate(ab),  capi.altibase_error(ab))
except stmtError as e:
    print("STMT Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt), capi.altibase_stmt_sqlstate(stmt), capi.altibase_stmt_error(stmt))
except stmt_selError as e:
    print("STMT_sel Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt_sel), capi.altibase_stmt_sqlstate(stmt_sel), capi.altibase_stmt_error(stmt_sel))
except stmt_uptError as e:
    print("STMT_upt Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt_upt), capi.altibase_stmt_sqlstate(stmt_upt), capi.altibase_stmt_error(stmt_upt))
except otherError as e:
    print("Other Error:", e.msg)
finally:
    if 'bindr' in locals():
        capi.apx_bind_free(bindr, bindr_cnt)
    if 'bindi' in locals():
        capi.apx_bind_free(bindi, bindi_cnt)
    if 'bindu' in locals():
        capi.apx_bind_free(bindu, bindu_cnt)
    if 'bindt' in locals():
        capi.apx_bind_free(bindt, bindt_cnt)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'stmt_sel' in locals():
        capi.altibase_stmt_close(stmt_sel)
    if 'stmt_upt' in locals():
        capi.altibase_stmt_close(stmt_upt)
    if 'ab' in locals():
        capi.altibase_close(ab)
