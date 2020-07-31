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

    rc = capi.altibase_stmt_prepare(stmt, "INSERT INTO DEMO_EX3 VALUES( ?, ?, ?, ?, ?, ? )")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    # six columns
    col_cnt = 6 

    bind = capi.apx_bind_alloc(col_cnt)
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

    for i in range(10,37):
        # column binding : id
        capi.apx_bind_put_string(bind, 0, str(i) + "000000")
        # column binding : name
        capi.apx_bind_put_string(bind, 1, "name" + str(i))
        # column binding : age
        capi.apx_bind_put_int(bind, 2, i)
        # column binding : birth
        capi.apx_bind_put_date(bind, 3, 1980 + i, 10, 10, 8, 50, 10, 0)
        # column binding : sex
        capi.apx_bind_put_short(bind, 4, i % 2)
        # column binding : etc
        if (i % 2 == 0):
            capi.apx_bind_put_double(bind, 5, 10.2 + i)
        else:
            capi.apx_bind_put_null(bind, 5)

        rc = capi.altibase_stmt_execute(stmt)
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("altibase_stmt_execute")

    capi.altibase_stmt_close(stmt);

    ########## SELECT ##########
    array_size = 10

    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX3")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    rc = capi.altibase_stmt_set_array_fetch(stmt, array_size)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")
     
    # six columns
    col_cnt = 6 

    bind_result = capi.apx_bind_alloc(col_cnt)
    if (bind_result == None):
        raise otherError("apx_bind_alloc")

    # column binding : id
    capi.apx_arraybind_string(array_size, bind_result, 0, 8)
    # column binding : name
    capi.apx_arraybind_string(array_size, bind_result, 1, 20)
    # column binding : age
    capi.apx_arraybind_int(array_size, bind_result, 2)
    # column binding : birth
    capi.apx_arraybind_date(array_size, bind_result, 3)
    # column binding : sex
    capi.apx_arraybind_short(array_size, bind_result, 4)
    # column binding : etc
    capi.apx_arraybind_double(array_size, bind_result, 5)

    rc = capi.altibase_stmt_bind_result(stmt, bind_result)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    # fetches next rowset of data from the result set and print to stdout
    print("id\t\tName\tAge\tbirth\t\t\tsex\tetc")
    print("==========================================================================");

    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_execute")

    rc = capi.altibase_stmt_fetch(stmt)
    while (rc != capi.ALTIBASE_NO_DATA):
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("altibase_stmt_fetch")

        fetched_cnt = capi.altibase_stmt_fetched(stmt)

        for array_num in range(fetched_cnt):
            row_status = capi.altibase_stmt_status2(stmt,array_num)

            if ( row_status != capi.ALTIBASE_ROW_SUCCESS ):
                raise stmtError("altibase_stmt_execute")

            for i in range(col_cnt):
                if (i > 0):
                    print("\t", end='')

                if ( capi.apx_arraybind_get_length(array_num,bind_result, i) == capi.ALTIBASE_NULL_DATA ):
                    print("{null}", end='')
                    continue

                buffer_type = capi.apx_bind_get_buffertype(bind_result, i)
                if (buffer_type == capi.ALTIBASE_BIND_STRING):
                    print("%s" % (capi.apx_arraybind_get_string(array_num,bind_result,i)), end='')
                elif (buffer_type == capi.ALTIBASE_BIND_INTEGER):
                    print("%d" % (capi.apx_arraybind_get_int(array_num,bind_result,i)), end='')
                elif (buffer_type == capi.ALTIBASE_BIND_SMALLINT):
                    print("%d" % (capi.apx_arraybind_get_short(array_num,bind_result,i)), end='')
                elif (buffer_type == capi.ALTIBASE_BIND_DOUBLE):
                    print("%.3f" % (capi.apx_arraybind_get_double(array_num,bind_result,i)), end='')
                elif (buffer_type == capi.ALTIBASE_BIND_DATE):
                    print("%4d/%02d/%02d %02d:%02d:%02d" %
                        ( capi.apx_arraybind_get_date_year(array_num,bind_result,i)
                         ,capi.apx_arraybind_get_date_month(array_num,bind_result,i)
                         ,capi.apx_arraybind_get_date_day(array_num,bind_result,i)
                         ,capi.apx_arraybind_get_date_hour(array_num,bind_result,i)
                         ,capi.apx_arraybind_get_date_minute(array_num,bind_result,i)
                         ,capi.apx_arraybind_get_date_second(array_num,bind_result,i) ) , end='')
                else:
                    print("unreachable")
            print(" ")
        rc = capi.altibase_stmt_fetch(stmt)


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
        capi.apx_bind_free(bind, col_cnt)
    if 'bind_result' in locals():
        capi.apx_bind_free(bind_result, col_cnt)
    if 'meta' in locals():
        capi.altibase_free_result(meta)
    if 'stmt' in locals():
        capi.altibase_stmt_close(stmt)
    if 'ab' in locals():
        capi.altibase_close(ab)
