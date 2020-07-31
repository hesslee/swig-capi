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

    ########## Insert ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "INSERT INTO DEMO_TRAN1 VALUES( ?, ? )")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindi_cnt = 2 

    bindi = capi.apx_bind_alloc(bindi_cnt)
    if (bindi == None):
        raise otherError("apx_bind_alloc")

    # column binding : name
    capi.apx_bind_string(bindi, 0, 20)
    # column binding : age
    capi.apx_bind_int(bindi, 1)

    rc = capi.altibase_stmt_bind_param(stmt, bindi)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # column value : name
    capi.apx_bind_put_string(bindi, 0, "name1")
    # column value : age
    capi.apx_bind_put_int(bindi, 1, 28)
 
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("First insert altibase_stmt_execute")

    rc = capi.altibase_commit(ab)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise dbcError("First commit")

    # column value : name
    capi.apx_bind_put_string(bindi, 0, "name2")
    # column value : age
    capi.apx_bind_put_int(bindi, 1, 25)
 
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("Second insert altibase_stmt_execute")

    rc = capi.altibase_rollback(ab)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise dbcError("Second rollback")

    # column value : name
    capi.apx_bind_put_string(bindi, 0, "name3")
    # column value : age
    capi.apx_bind_put_null(bindi, 1)
 
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("Third insert altibase_stmt_execute")

    rc = capi.altibase_commit(ab)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise dbcError("Third commit")

    capi.altibase_stmt_close(stmt);

    ########## SELECT ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_TRAN1")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # two columns
    bindr_cnt = 2 

    bindr = capi.apx_bind_alloc(bindr_cnt)
    if (bindr == None):
        raise otherError("apx_bind_alloc")

    # column binding : name
    capi.apx_bind_string(bindr, 0, 20)
    # column binding : age
    capi.apx_bind_int(bindr, 1)

    rc = capi.altibase_stmt_bind_result(stmt, bindr)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    print("Name\tAge")
    print("=========================");

    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_execute")

    rc = capi.altibase_stmt_fetch(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

    while (rc != capi.ALTIBASE_NO_DATA):
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("altibase_stmt_fetch")
        
        for i in range(bindr_cnt):
            if (i > 0):
                print("\t", end='')
            if ( capi.apx_bind_get_length(bindr, i) == capi.ALTIBASE_NULL_DATA ): 
                print("{null}", end='')
                continue

            buffer_type = capi.apx_bind_get_buffertype(bindr, i)
            if (buffer_type == capi.ALTIBASE_BIND_STRING):
                print("%s" % (capi.apx_bind_get_string(bindr,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_INTEGER):
                print("%d" % (capi.apx_bind_get_int(bindr,i)), end='')
            else:
                print("unreachable")
        print(" ")
        rc = capi.altibase_stmt_fetch(stmt)

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
    if 'bindi' in locals():
        capi.apx_bind_free(bindi, bindi_cnt)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'ab' in locals():
        capi.altibase_close(ab)
