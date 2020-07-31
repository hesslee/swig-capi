import capi

CONN_STR = "Server=127.0.0.1;PORT_NO=20300;User=SYS;Password=MANAGER"

# allocate handle
ab = capi.altibase_init()
if (ab == None):
    print("Error: altibase_init")
    print("DBC error:", capi.altibase_errno(aAB), capi.altibase_sqlstate(aAB),  capi.altibase_error(aAB))
    raise

# Connect to Altibase Server
rc = capi.altibase_connect(ab, CONN_STR)
if ( rc != capi.ALTIBASE_SUCCESS ):
    print("Error: altibase_connect")
    print("DBC error:", capi.altibase_errno(ab), capi.altibase_sqlstate(ab),  capi.altibase_error(ab))
    raise

res = capi.altibase_list_tables2(ab, None, None, None)
if (res == None):
    print("Error: altibase_list_tables2")
    print("DBC error:", capi.altibase_errno(aAB), capi.altibase_sqlstate(aAB),  capi.altibase_error(aAB))
    capi.altibase_close(ab)
    raise

#fetches the next rowset of data from the result set and print to stdout
print("=========================================================================")
print("%-20s%-40s%s" % ("TABLE_SCHEM", "TABLE_NAME" ,"TABLE_TYPE"))
print("=========================================================================")

row = capi.altibase_fetch_row(res)
while (row != None):
    row_1 = capi.apx_row_get_string(row, 1)
    row_2 = capi.apx_row_get_string(row, 2)
    row_3 = capi.apx_row_get_string(row, 3)
    print("%-20s%-40s%s" % (row_1, row_2, row_3))
    row = capi.altibase_fetch_row(res)

capi.altibase_free_result(res)

capi.altibase_close(ab)
