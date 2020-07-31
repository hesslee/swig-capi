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


    ########## SELECT: before operarion(s) ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX6")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindr_cnt = 3 

    bindr = capi.apx_bind_alloc(bindr_cnt)
    if (bindr == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_int(bindr, 0)
    # column binding : name
    capi.apx_bind_string(bindr, 1, 20)
    # column binding : birth
    capi.apx_bind_date(bindr, 2)

    rc = capi.altibase_stmt_bind_result(stmt, bindr)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("id\t\tName\tbirth")
    print("================================================================");

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
            elif (buffer_type == capi.ALTIBASE_BIND_SMALLINT):
                print("%d" % (capi.apx_bind_get_short(bindr,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DOUBLE):
                print("%.3f" % (capi.apx_bind_get_double(bindr,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DATE):
                print("%4d/%02d/%02d %02d:%02d:%02d" %
                    ( capi.apx_bind_get_date_year(bindr,i)
                     ,capi.apx_bind_get_date_month(bindr,i)
                     ,capi.apx_bind_get_date_day(bindr,i)
                     ,capi.apx_bind_get_date_hour(bindr,i)
                     ,capi.apx_bind_get_date_minute(bindr,i)
                     ,capi.apx_bind_get_date_second(bindr,i) ) , end='')
            else:
                print("unreachable")
        print(" ")
        rc = capi.altibase_stmt_fetch(stmt)

    rc = capi.altibase_stmt_free_result(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

    capi.altibase_stmt_close(stmt);


    ########## Calling a Procudure ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "EXEC DEMO_PROC6( ?, ?, ? )")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindproc_cnt = 3 

    bindproc = capi.apx_bind_alloc(bindproc_cnt)
    if (bindproc == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_int(bindproc, 0)
    # column binding : name
    capi.apx_bind_string(bindproc, 1, 20)
    # column binding : birth
    capi.apx_bind_date(bindproc, 2)

    rc = capi.altibase_stmt_bind_param(stmt, bindproc)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # params binding
    capi.apx_bind_put_int(bindproc, 0, 5)
    capi.apx_bind_put_string(bindproc, 1, "name5")
    capi.apx_bind_put_date(bindproc, 2, 2004, 5, 14, 15, 17, 20, 3)

    print("By Procedure Call: insert id=5, name='name5'")
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("proc altibase_stmt_execute")

    row_count = capi.altibase_stmt_affected_rows(stmt)
    print("Affected count : %d" % row_count)

    capi.altibase_stmt_close(stmt);


    ########## SELECT: after operarion(s) ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX6")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindr2_cnt = 3 

    bindr2 = capi.apx_bind_alloc(bindr2_cnt)
    if (bindr2 == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_int(bindr2, 0)
    # column binding : name
    capi.apx_bind_string(bindr2, 1, 20)
    # column binding : birth
    capi.apx_bind_date(bindr2, 2)

    rc = capi.altibase_stmt_bind_result(stmt, bindr2)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("id\t\tName\tbirth")
    print("================================================================");

    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_execute")

    rc = capi.altibase_stmt_fetch(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

    while (rc != capi.ALTIBASE_NO_DATA):
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("altibase_stmt_fetch")
        
        for i in range(bindr2_cnt):
            if (i > 0):
                print("\t", end='')
            if ( capi.apx_bind_get_length(bindr2, i) == capi.ALTIBASE_NULL_DATA ): 
                print("{null}", end='')
                continue

            buffer_type = capi.apx_bind_get_buffertype(bindr2, i)
            if (buffer_type == capi.ALTIBASE_BIND_STRING):
                print("%s" % (capi.apx_bind_get_string(bindr2,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_INTEGER):
                print("%d" % (capi.apx_bind_get_int(bindr2,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_SMALLINT):
                print("%d" % (capi.apx_bind_get_short(bindr2,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DOUBLE):
                print("%.3f" % (capi.apx_bind_get_double(bindr2,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DATE):
                print("%4d/%02d/%02d %02d:%02d:%02d" %
                    ( capi.apx_bind_get_date_year(bindr2,i)
                     ,capi.apx_bind_get_date_month(bindr2,i)
                     ,capi.apx_bind_get_date_day(bindr2,i)
                     ,capi.apx_bind_get_date_hour(bindr2,i)
                     ,capi.apx_bind_get_date_minute(bindr2,i)
                     ,capi.apx_bind_get_date_second(bindr2,i) ) , end='')
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
    if 'bindr2' in locals():
        capi.apx_bind_free(bindr2, bindr2_cnt)
    if 'bindproc' in locals():
        capi.apx_bind_free(bindproc, bindproc_cnt)
    if 'meta' in locals():
        capi.altibase_free_result(meta)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'ab' in locals():
        capi.altibase_close(ab)
