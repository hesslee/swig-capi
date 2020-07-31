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
    # allocate handle
    ab = capi.altibase_init()
    if (ab == None):
        raise otherError("altibase_init")

    # Connect to Altibase Server
    rc = capi.altibase_connect(ab, CONN_STR)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise dbcError("altibase_connect")

    ########## INSERT ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "INSERT INTO DEMO_EX2 VALUES( ?, ?, ?, ?, ?, ? )")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    col_count = 6 

    bind = capi.apx_bind_alloc(col_count)
    if (bind == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_string(bind, 0, 8)
    # column binding : name
    capi.apx_bind_string(bind, 1, 20)
    # column binding : age
    capi.apx_bind_int(bind, 2)
    # column binding : birth
    capi.apx_bind_date(bind, 3)
    # column binding : sex
    capi.apx_bind_short(bind, 4)
    # column binding : etc
    capi.apx_bind_double(bind, 5)

    rc = capi.altibase_stmt_bind_param(stmt, bind)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # column binding : id
    capi.apx_bind_put_string(bind, 0, "10000000")
    # column binding : name
    capi.apx_bind_put_string(bind, 1, "name1")
    # column binding : age
    capi.apx_bind_put_int(bind, 2, 28)
    # column binding : birth
    capi.apx_bind_put_date(bind, 3, 1980, 10, 10, 8, 50, 10, 0)
    # column binding : sex
    capi.apx_bind_put_short(bind, 4, 1)
    # column binding : etc
    capi.apx_bind_put_double(bind, 5, 10.2)

    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        print("1st Insert")
        raise stmtError("altibase_stmt_execute")

    # column binding : id
    capi.apx_bind_put_string(bind, 0, "20000000")
    # column binding : name
    capi.apx_bind_put_string(bind, 1, "name2")
    # column binding : age
    capi.apx_bind_put_int(bind, 2, 10)
    # column binding : birth
    capi.apx_bind_put_date(bind, 3, 1990, 5, 20, 17, 15, 15, 0)
    # column binding : sex
    capi.apx_bind_put_short(bind, 4, 0)
    # column binding : etc
    capi.apx_bind_put_null(bind, 5)

    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        print("2nd Insert")
        raise stmtError("altibase_stmt_execute")

    # column binding : id
    capi.apx_bind_put_string(bind, 0, "30000000")
    # column binding : name
    capi.apx_bind_put_string(bind, 1, "name3")
    # column binding : age
    capi.apx_bind_put_int(bind, 2, 30)
    # column binding : birth
    capi.apx_bind_put_date(bind, 3, 1970, 12, 7, 9, 20, 8, 0)
    # column binding : sex
    capi.apx_bind_put_short(bind, 4, 1)
    # column binding : etc
    capi.apx_bind_put_double(bind, 5, 30.2)

    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        print("3rd Insert")
        raise stmtError("altibase_stmt_execute")

    capi.altibase_stmt_close(stmt);

    ########## SELECT ##########
    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX2 WHERE id=?")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    bind_param = capi.apx_bind_alloc(1)
    if (bind_param == None):
        raise otherError("apx_bind_alloc")
    capi.apx_bind_string(bind_param, 0, 8)

    rc = capi.altibase_stmt_bind_param(stmt, bind_param)
    if (capi.apx_ALTIBASE_NOT_SUCCEEDED(rc)):
        raise stmtError("altibase_stmt_bind_param")

    # six columns
    col_count = 6 

    bind_result = capi.apx_bind_alloc(col_count)
    if (bind_result == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_bind_string(bind_result, 0, 8)
    # column binding : name
    capi.apx_bind_string(bind_result, 1, 20)
    # column binding : age
    capi.apx_bind_int(bind_result, 2)
    # column binding : birth
    capi.apx_bind_date(bind_result, 3)
    # column binding : sex
    capi.apx_bind_short(bind_result, 4)
    # column binding : etc
    capi.apx_bind_double(bind_result, 5)

    rc = capi.altibase_stmt_bind_result(stmt, bind_result)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("id\t\tName\tAge\tbirth\t\t\tsex\tetc")
    print("==========================================================================");

    for id in ["10000000","20000000","30000000"]:
        capi.apx_bind_put_string(bind_param, 0, id)
        rc = capi.altibase_stmt_execute(stmt)
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("altibase_stmt_execute")

        rc = capi.altibase_stmt_fetch(stmt)
        if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
            raise stmtError("altibase_stmt_fetch")

        for i in range(col_count):
            if (i > 0):
                print("\t", end='')
            if ( capi.apx_bind_get_length(bind_result, i) == capi.ALTIBASE_NULL_DATA ): 
                print("{null}", end='')
                continue

            buffer_type = capi.apx_bind_get_buffertype(bind_result, i)
            if (buffer_type == capi.ALTIBASE_BIND_STRING):
                print("%s" % (capi.apx_bind_get_string(bind_result,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_INTEGER):
                print("%d" % (capi.apx_bind_get_int(bind_result,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_SMALLINT):
                print("%d" % (capi.apx_bind_get_short(bind_result,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DOUBLE):
                print("%.3f" % (capi.apx_bind_get_double(bind_result,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DATE):
                print("%4d/%02d/%02d %02d:%02d:%02d" %
                    ( capi.apx_bind_get_date_year(bind_result,i)
                     ,capi.apx_bind_get_date_month(bind_result,i)
                     ,capi.apx_bind_get_date_day(bind_result,i)
                     ,capi.apx_bind_get_date_hour(bind_result,i)
                     ,capi.apx_bind_get_date_minute(bind_result,i)
                     ,capi.apx_bind_get_date_second(bind_result,i) ) , end='')
            else:
                print("unreachable")

        print(" ")

    rc = capi.altibase_stmt_free_result(stmt)
    if ( capi.apx_ALTIBASE_NOT_SUCCEEDED(rc) ):
        raise stmtError("altibase_stmt_fetch")

    capi.altibase_stmt_close(stmt);

except dbcError as e:
    print("DBC Error:", e.msg)
    print(capi.altibase_errno(ab), capi.altibase_sqlstate(ab),  capi.altibase_error(ab))
except stmtError as e:
    print("STMT Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt), capi.altibase_stmt_sqlstate(stmt), capi.altibase_stmt_error(stmt))
except otherError as e:
    print("Other Error:", e.msg)
finally:
    if 'bind' in locals():
        capi.apx_bind_free(bind, col_count)
    if 'bind_param' in locals():
        capi.apx_bind_free(bind_param, 1)
    if 'bind_result' in locals():
        capi.apx_bind_free(bind_result, col_count)
    if 'meta' in locals():
        capi.altibase_free_result(meta)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'ab' in locals():
        capi.altibase_close(ab)
