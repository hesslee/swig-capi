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

    rc = capi.altibase_stmt_prepare(stmt, "SELECT * FROM DEMO_META8")
    if ( rc != capi.ALTIBASE_SUCCESS ):
        raise stmtError("altibase_stmt_prepare")

    meta = capi.altibase_stmt_result_metadata(stmt)
    if (meta == None):
        raise stmtError("altibase_stmt_result_metadata")

    fields = capi.altibase_fields(meta)
    col_count = capi.altibase_stmt_field_count(stmt)

    for i in range(col_count):
        field = capi.apx_get_field_from_fields(fields,i)
        field_type = field.type
        field_name = field.name
        field_size = field.size
        field_scale = field.scale

        if (field_type == capi.ALTIBASE_TYPE_CHAR):
            print("%s : CHAR(%d)" % (field_name, field_size))
        elif (field_type == capi.ALTIBASE_TYPE_VARCHAR):
            print("%s : VARCHAR(%d)" % (field_name, field_size))
        elif (field_type == capi.ALTIBASE_TYPE_INTEGER):
            print("%s : INTEGER" % field_name)
        elif (field_type == capi.ALTIBASE_TYPE_SMALLINT):
            print("%s : SMALLINT" % field_name)
        elif (field_type == capi.ALTIBASE_TYPE_NUMERIC):
            print("%s : NUMERIC(%d,%d)" % (field_name, field_size, field_scale))
        elif (field_type == capi.ALTIBASE_TYPE_DATE):
            print("%s : DATE" % field_name)
        else:
            print("Unreachable")

############# Closing #################

except dbcError as e:
    print("DBC Error:", e.msg)
    print(capi.altibase_errno(ab), capi.altibase_sqlstate(ab),  capi.altibase_error(ab))
except stmtError as e:
    print("STMT Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt), capi.altibase_stmt_sqlstate(stmt), capi.altibase_stmt_error(stmt))
except otherError as e:
    print("Other Error:", e.msg)
finally:
    capi.altibase_free_result(meta)
    capi.altibase_stmt_close(stmt)
    capi.altibase_close(ab)
