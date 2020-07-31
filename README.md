### swig-capi
- SWIG for Altibase C Interface(CAPI)
- This is not a complete SWIG conversion of Altibase CAPI. Currently, only the CAPI [samples](#samples) are converted and tested.
- Currently there is only Python [samples](#samples) but these will be expanded to other SWIG supported languages.
- swig-capi appended several functions to [capi.i](#capii) to bridge the gap between Altibase CAPI and SWIG supported languages.
- Reference
  * SWIG : http://www.swig.org/
  * Altibase resources : http://altibase.com/resources/manuals/
  * Korean Altibase resources : http://support.altibase.com

### License, Q&A, Bug Report, Support and Contribution
- swig-capi is an open source with GNU Lesser General Public License version 3(GNU LGPLv3). 
- swig-capi is only provided as an open source community product by this repository. There is no other commercially supported enterprise swig-capi product.
- swig-capi is maintained and supported by open source community.
- Q&A or bug reports can be registered as Issues(https://github.com/ALTIBASE/swig-capi/issues) and these issues will be supported by open source community.
- Contributions can be registered as Pull requests(https://github.com/ALTIBASE/swig-capi/pulls) and these requests will be supported by open source community. 
- Altibase Corp. will support swig-capi with best effort basis as one of open source community members. But there is no guaranteed support for swig-capi by Altibase Corp.

### Test environment
swig 3.0.8
Ubuntu 16.04
Altibase v7.1

### Python test
Python 2.7.12
```
swig -python -I${ALTIBASE_HOME}/include capi.i
# debugging info : -g
gcc -c -fPIC capi_wrap.c -g -I${ALTIBASE_HOME}/include -I/usr/include/python2.7
ld -shared -L${ALTIBASE_HOME}/lib capi_wrap.o -lalticapi_sl -lodbccli_sl -lrt -o _capi.so
```
### Debugging tips
- Going back and forth between Python layer debugging and C layer debugging
  * Prepare Python break points using pdb.
  * `gdb python`
  * `break sample-C-layer-function-name`
  * `run sample.py`
  * It will stop at pdb break points with Python layer and it will also stop at C layer break points.
- CDBCLOG_ENABLE
  * Prepare debugging enabled Altibase libraries.(using Altibase open source)
  * Set environment by : `export CDBCLOG_ENABLE=1`
  * Execute allpication which is using one of the Altibase CAPI SWIG drivers.
  
### Samples
- Almost all of samples requires as a preparation to execute the same name SQL file for DB schema creation.
- demo_ex1 : simple SELECT using altibase_stmt_result_metadata and altibase_fields
- demo_ex2 : simple INSERT and SELECT using altibase_stmt_bind_param
- demo_ex3 : array fetch SELECT
- demo_ex4 : array bind INSERT
- demo_ex5 : simple UPDATE and DELETE
- demo_ex6 : exec procedure
- demo_ex7 : array bind UPDATE
- demo_tran1 : transaction handling with altibase_commit and altibase_rollback
- demo_tran2 : two statements(SELECT and UPDATE) concurrent handling
- demo_meta1 : altibase_list_tables
- demo_meta2 : altibase_list_fields
- demo_meta8 : altibase_stmt_result_metadata, altibase_fields
- demo_blob : BLOB handling
- demo_clob_hangul : CLOB and Hangul handling
- demo_STF : Session Time Failover handling with sample callback function


### capi.i
- All original CAPI API names have the pattern of **altibase_ + _some-name_**.
- SWIG-CAPI provides same name API with CAPI when that is possible.
- **altibase_ + _some-name_ + 2** pattern name APIs are provided when corresponding CAPI API is not appropriate to a target language.
- **apx_ + _some-name_** pattern name APIs are provided when there is no corresponding CAPI API but these new APIs are needed for a target language.
- Most of them are about bridging the difference of array handling between target languages and C language. 
- SWIG cstring.i %cstring_output_allocate_size macro is used for binary return functions(apx_arraybind_get_binary, apx_bind_get_binary)

- altibase_list_tables2 : wrapping function for altibase_list_tables
- altibase_list_fields2 : wrapping function for altibase_list_fields
- altibase_stmt_status2 : wrapping function for altibase_stmt_status with an array index argument

- apx_print_bytes : debugging purpose function
- apx_print_bytes_arraybind_buffer : debugging purpose function
- apx_print_bytes_arraybind_length : debugging purpose function

- apx_ALTIBASE_SUCCEEDED : wrapping function for ALTIBASE_SUCCEEDED
- apx_ALTIBASE_NOT_SUCCEEDED : wrapping function for ALTIBASE_NOT_SUCCEEDED

- apx_get_field_from_fields : get a ALTIBASE_FIELD from ALTIBASE_FIELD array
- apx_row_get_string : get string from ALTIBASE_ROW with array index argument

- apx_bind_alloc : memory allocation for ALTIBASE_BIND
- apx_bind_free : free of allocated memory for ALTIBASE_BIND

- apx_bind_get_length : get length element from ALTIBASE_BIND
- apx_bind_get_buffertype : get buffer_type element from an ALTIBASE_BIND

- apx_bind_binary : setting for binary type of ALTIBASE_BIND
- apx_bind_string : setting for string type of ALTIBASE_BIND
- apx_bind_int : setting for int type of ALTIBASE_BIND
- apx_bind_short : setting for short type of ALTIBASE_BIND
- apx_bind_double : setting for double type of ALTIBASE_BIND
- apx_bind_date : setting for date type of ALTIBASE_BIND

- apx_bind_get_binary : get binary from buffer element of ALTIBASE_BIND
- apx_bind_get_string : get string from buffer element of ALTIBASE_BIND
- apx_bind_get_int : get int from buffer element of ALTIBASE_BIND
- apx_bind_get_short : get short from buffer element of ALTIBASE_BIND
- apx_bind_get_double : get double from buffer element of ALTIBASE_BIND
- apx_bind_get_date_year : get year from buffer element of ALTIBASE_BIND
- apx_bind_get_date_month : get month from buffer element of ALTIBASE_BIND
- apx_bind_get_date_day : get day from buffer element of ALTIBASE_BIND
- apx_bind_get_date_hour : get hour from buffer element of ALTIBASE_BIND
- apx_bind_get_date_minute : get minute from buffer element of ALTIBASE_BIND
- apx_bind_get_date_second : get second from buffer element of ALTIBASE_BIND
- apx_bind_get_date_fraction : get fraction from buffer element of ALTIBASE_BIND

- apx_bind_put_null : put NULL for buffer element of ALTIBASE_BIND
- apx_bind_put_binary : put binary for buffer element of ALTIBASE_BIND
- apx_bind_put_string : put string for buffer element of ALTIBASE_BIND
- apx_bind_put_int : put int for buffer element of ALTIBASE_BIND
- apx_bind_put_short : put short for buffer element of ALTIBASE_BIND
- apx_bind_put_double : put double for buffer element of ALTIBASE_BIND
- apx_bind_put_date : put date for buffer element of ALTIBASE_BIND

- apx_arraybind_get_length : get length element from array ALTIBASE_BIND
- apx_arraybind_get_binary : get binary from buffer element of array ALTIBASE_BIND

- apx_arraybind_binary : setting for binary type of array ALTIBASE_BIND
- apx_arraybind_string : setting for string type of array ALTIBASE_BIND
- apx_arraybind_int : setting for int type of array ALTIBASE_BIND
- apx_arraybind_short : setting for short type of array ALTIBASE_BIND
- apx_arraybind_double : setting for double type of array ALTIBASE_BIND
- apx_arraybind_date : setting for date type of array ALTIBASE_BIND

- apx_arraybind_get_string : get string from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_int : get int from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_short : get short from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_double : get double from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_date_year : get year from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_date_month : get month from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_date_day : get day from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_date_hour : get hour from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_date_minute : get minute from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_date_second : get second from buffer element of array ALTIBASE_BIND
- apx_arraybind_get_date_fraction : get fraction from buffer element of array ALTIBASE_BIND

- apx_arraybind_put_null : put NULL for buffer element of array ALTIBASE_BIND
- apx_arraybind_put_binary : put binary for buffer element of array ALTIBASE_BIND
- apx_arraybind_put_string : put string for buffer element of array ALTIBASE_BIND
- apx_arraybind_put_int : put int for buffer element of array ALTIBASE_BIND
- apx_arraybind_put_short : put short for buffer element of array ALTIBASE_BIND
- apx_arraybind_put_double : put double for buffer element of array ALTIBASE_BIND
- apx_arraybind_put_date : put date for buffer element of array ALTIBASE_BIND

