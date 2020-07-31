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

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX5")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindr_cnt = 6 

    bindr = capi.apx_bind_alloc(bindr_cnt)
    if (bindr == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_string(bindr, 0, 8)
    # column binding : name
    capi.apx_bind_string(bindr, 1, 20)
    # column binding : age
    capi.apx_bind_int(bindr, 2)
    # column binding : birth
    capi.apx_bind_date(bindr, 3)
    # column binding : sex
    capi.apx_bind_short(bindr, 4)
    # column binding : etc
    capi.apx_bind_double(bindr, 5)

    rc = capi.altibase_stmt_bind_result(stmt, bindr)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("id\t\tName\tAge\tbirth\t\t\tsex\tetc")
    print("==========================================================================");

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


    ########## UPDATE ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "UPDATE DEMO_EX5 set age = 15 where id=?")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindu_cnt = 1 

    bindu = capi.apx_bind_alloc(bindu_cnt)
    if (bindu == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_string(bindu, 0, 8)

    rc = capi.altibase_stmt_bind_param(stmt, bindu)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # column binding : id
    capi.apx_bind_put_string(bindu, 0, "10000000")

    print("1. update ... where id='10000000'")
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("update altibase_stmt_execute")

    row_count = capi.altibase_stmt_affected_rows(stmt)
    print("UPDATED COUNT : %d" % row_count)

    # column binding : id
    capi.apx_bind_put_string(bindu, 0, "80000000")

    print("2. update ... where id='80000000'")
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("update altibase_stmt_execute")

    row_count = capi.altibase_stmt_affected_rows(stmt)
    print("UPDATED COUNT : %d" % row_count)

    capi.altibase_stmt_close(stmt);


    ########## DELETE ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "DELETE FROM DEMO_EX5 where id=?")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindd_cnt = 1 

    bindd = capi.apx_bind_alloc(bindd_cnt)
    if (bindd == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_string(bindd, 0, 8)

    rc = capi.altibase_stmt_bind_param(stmt, bindd)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # column binding : id
    capi.apx_bind_put_string(bindd, 0, "20000000")

    print("3. delete ... where id='20000000'")
    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("update altibase_stmt_execute")

    row_count = capi.altibase_stmt_affected_rows(stmt)
    print("DELETED COUNT : %d" % row_count)

    capi.altibase_stmt_close(stmt);

    ########## SELECT: after operarion(s) ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX5")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    bindr2_cnt = 6 

    bindr2 = capi.apx_bind_alloc(bindr2_cnt)
    if (bindr2 == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_string(bindr2, 0, 8)
    # column binding : name
    capi.apx_bind_string(bindr2, 1, 20)
    # column binding : age
    capi.apx_bind_int(bindr2, 2)
    # column binding : birth
    capi.apx_bind_date(bindr2, 3)
    # column binding : sex
    capi.apx_bind_short(bindr2, 4)
    # column binding : etc
    capi.apx_bind_double(bindr2, 5)

    rc = capi.altibase_stmt_bind_result(stmt, bindr2)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("id\t\tName\tAge\tbirth\t\t\tsex\tetc")
    print("==========================================================================");

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
