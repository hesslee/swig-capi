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

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX7")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindr_cnt = 2 

    bindr = capi.apx_bind_alloc(bindr_cnt)
    if (bindr == None):
        raise otherError("apx_bind_alloc")

    # column binding : i1
    capi.apx_bind_int(bindr, 0)
    # column binding : i2
    capi.apx_bind_int(bindr, 1)

    rc = capi.altibase_stmt_bind_result(stmt, bindr)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("i1\t\ti2")
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


    ########## Array UPDATE ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "UPDATE DEMO_EX7 set i2 = ? where i1=?")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    array_size = 7
    rc = capi.altibase_stmt_set_array_bind(stmt, array_size)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("set_array_bind")

    # six columns
    bindu_cnt = 2 

    bindu = capi.apx_bind_alloc(bindu_cnt)
    if (bindu == None):
        raise otherError("apx_bind_alloc")

    # column binding : i1
    capi.apx_arraybind_int(array_size, bindu, 0)
    # column binding : i2
    capi.apx_arraybind_int(array_size, bindu, 1)

    rc = capi.altibase_stmt_bind_param(stmt, bindu)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # making normal data
    for i in range(array_size):
        capi.apx_arraybind_put_int(i, bindu, 0, (i+1))
        capi.apx_arraybind_put_int(i, bindu, 1, (i+1))

    # making not found data
    capi.apx_arraybind_put_int(4, bindu, 0, 50)
    capi.apx_arraybind_put_int(4, bindu, 1, 50)
 
    print("")
    print("array update for 7 rows with one not found row")
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("array update altibase_stmt_execute")

    row_count = capi.altibase_stmt_processed(stmt)
    print("Processed Count : %d" % row_count)

    for i in range(row_count):
        print("[%d] : " % i, end='')
        status = capi.altibase_stmt_status2(stmt,i)
        if (status == capi.ALTIBASE_PARAM_SUCCESS):
            print("success")
        elif (status == capi.ALTIBASE_NO_DATA_FOUND):
            print("NO_DATA_FOUND")
        else:
            print("Need to check")
        
    capi.altibase_stmt_close(stmt);


    ########## SELECT: after operarion(s) ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX7")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindr2_cnt = 2 

    bindr2 = capi.apx_bind_alloc(bindr2_cnt)
    if (bindr2 == None):
        raise otherError("apx_bind_alloc")

    # column binding : i1
    capi.apx_bind_int(bindr2, 0)
    # column binding : i2
    capi.apx_bind_int(bindr2, 1)

    rc = capi.altibase_stmt_bind_result(stmt, bindr2)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("i1\t\ti2")
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
    if 'bindu' in locals():
        capi.apx_bind_free(bindu, bindu_cnt)
    if 'bindd' in locals():
        capi.apx_bind_free(bindd, bindd_cnt)
    if 'meta' in locals():
        capi.altibase_free_result(meta)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'ab' in locals():
        capi.altibase_close(ab)
