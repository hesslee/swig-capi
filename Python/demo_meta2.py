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

    ########## List Fields of a table ##########
    res = capi.altibase_list_fields2(ab, "SYS", "DEMO_META2", None)
    if (res == None):
        raise dbcError("altibase_list_fields2")

    print("POSITION\tCOL_NAME\tDATA_TYPE\tPRECISION\tSCALE\tIsNullable")
    print("=======================================================================================")

    row = capi.altibase_fetch_row(res)
    while (row != None):
        row_16 = capi.apx_row_get_string(row, 16)
        row_3 = capi.apx_row_get_string(row, 3)
        row_5 = capi.apx_row_get_string(row, 5)
        row_6 = capi.apx_row_get_string(row, 6)
        row_8 = capi.apx_row_get_string(row, 8)
        row_17 = capi.apx_row_get_string(row, 17)
        print("%-10s\t%-20s%-20s%-10s%-10s%s" % (row_16, row_3, row_5, row_6, row_8, row_17))
        row = capi.altibase_fetch_row(res)

    capi.altibase_free_result(res)

    capi.altibase_close(ab)

except dbcError as e:
    print("DBC Error:", e.msg)
    print(capi.altibase_errno(ab), capi.altibase_sqlstate(ab),  capi.altibase_error(ab))
except stmtError as e:
    print("STMT Error:", e.msg)
    print(capi.altibase_stmt_errno(stmt), capi.altibase_stmt_sqlstate(stmt), capi.altibase_stmt_error(stmt))
except otherError as e:
    print("Other Error:", e.msg)
finally:
    if 'res' in locals():
        capi.altibase_free_result(res)
    if 'ab' in locals():
        capi.altibase_close(ab)
