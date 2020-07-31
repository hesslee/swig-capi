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

    stmt = capi.altibase_stmt_init(ab)
    if (stmt == None):
        raise stmtError("altibase_stmt_init")

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_EX1")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    meta = capi.altibase_stmt_result_metadata(stmt)
    if (meta == None):
        raise stmtError("altibase_stmt_result_metadata")

    fields = capi.altibase_fields(meta)
    col_count = capi.altibase_stmt_field_count(stmt)

    bind = capi.apx_bind_alloc(col_count)
    if (bind == None):
        raise otherError("apx_bind_alloc")

    for i in range(col_count):
        field = capi.apx_get_field_from_fields(fields,i)
        field_type = field.type
        field_name = field.name
        field_size = field.size
        field_scale = field.scale

        if (field_type == capi.ALTIBASE_TYPE_CHAR):
            capi.apx_bind_string(bind,i,field_size)
        elif (field_type == capi.ALTIBASE_TYPE_VARCHAR):
            capi.apx_bind_string(bind,i,field_size)
        elif (field_type == capi.ALTIBASE_TYPE_INTEGER):
            capi.apx_bind_int(bind,i)
        elif (field_type == capi.ALTIBASE_TYPE_SMALLINT):
            capi.apx_bind_short(bind,i)
        elif (field_type == capi.ALTIBASE_TYPE_NUMERIC):
            capi.apx_bind_double(bind,i)
        elif (field_type == capi.ALTIBASE_TYPE_DATE):
            capi.apx_bind_date(bind,i)
        else:
            print("Unreachable")

    rc = capi.altibase_stmt_bind_result(stmt, bind)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_bind_result")

    rc = capi.altibase_stmt_execute(stmt)
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_execute")

    # fetches next rowset of data from the result set and print to stdout
    print("========================================================================");
    rc = capi.altibase_stmt_fetch(stmt)
    while (rc != capi.ALTIBASE_NO_DATA):
        if ( rc != capi.ALTIBASE_SUCCESS ):
            raise stmtError("altibase_stmt_fetch")

        for i in range(col_count):
            if (i > 0):
                print("\t", end='')
            if ( capi.apx_bind_get_length(bind, i) == capi.ALTIBASE_NULL_DATA ): 
                print("{null}", end='')
                continue

            buffer_type = capi.apx_bind_get_buffertype(bind, i)
            if (buffer_type == capi.ALTIBASE_BIND_STRING):
                print("%s" % (capi.apx_bind_get_string(bind,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_INTEGER):
                print("%d" % (capi.apx_bind_get_int(bind,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_SMALLINT):
                print("%d" % (capi.apx_bind_get_short(bind,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DOUBLE):
                print("%.3f" % (capi.apx_bind_get_double(bind,i)), end='')
            elif (buffer_type == capi.ALTIBASE_BIND_DATE):
                print("%4d/%02d/%02d %02d:%02d:%02d" %
                    ( capi.apx_bind_get_date_year(bind,i)
                     ,capi.apx_bind_get_date_month(bind,i)
                     ,capi.apx_bind_get_date_day(bind,i)
                     ,capi.apx_bind_get_date_hour(bind,i)
                     ,capi.apx_bind_get_date_minute(bind,i)
                     ,capi.apx_bind_get_date_second(bind,i) ) , end='')
            else:
                print("unreachable")

        print(" ")
        rc = capi.altibase_stmt_fetch(stmt)

except dbcError as e:
    print("DBC Error:", e.msg)
    print(capi.altibase_errno(ab), capi.altibase_sqlstate(ab),  capi.altibase_error(ab))
except stmtError as e:
    print("STMT Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt), capi.altibase_stmt_sqlstate(stmt), capi.altibase_stmt_error(stmt))
except otherError as e:
    print("Other Error:", e.msg)
finally:
    capi.apx_bind_free(bind, col_count)
    capi.altibase_free_result(meta)
    capi.altibase_stmt_close(stmt)
    capi.altibase_close(ab)
