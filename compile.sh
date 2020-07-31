
ALTIBASE_HOME=/home/hess/altibase/altibase_home
swig -python -I${ALTIBASE_HOME}/include capi.i
# debugging info : -g
gcc -c -fPIC capi_wrap.c -g -I${ALTIBASE_HOME}/include -I/usr/include/python2.7
ld -shared -L${ALTIBASE_HOME}/lib capi_wrap.o -lalticapi_sl -lodbccli_sl -lrt -o _capi.so
