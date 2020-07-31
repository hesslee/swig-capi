%module capi
%{

/* Includes the header in the wrapper code */
#include "alticapi.h"

%}

/* Parse the header file to generate wrappers */
%include "alticapi.h"
%include <cstring.i>
%cstring_output_allocate_size(char **binary, int *length, )
%constant ALTIBASE_FAILOVER_EVENT (*SAMPLE_CALLBACK)(ALTIBASE ab, void *app_context, ALTIBASE_FAILOVER_EVENT event) = sample_failover_callback;


%inline %{

static ALTIBASE_FAILOVER_EVENT sample_failover_callback(ALTIBASE ab, void *app_context, ALTIBASE_FAILOVER_EVENT event)
{
    switch(event)
    {
        case ALTIBASE_FO_BEGIN:
            printf("Failover Begin\n");
            break;

        case  ALTIBASE_FO_END:
            printf("Failover End\n");
            break;

        case  ALTIBASE_FO_ABORT:
            printf("Failover Abort\n");
            break;

        default:
            printf("Unknown event\n");
            break;
    }

    /* Random decision */
    if ((time(NULL) % 2) == 0)
    {
        printf("Return with ALTIBASE_FO_GO\n");
        return ALTIBASE_FO_GO;
    }
    else
    {
        printf("Return with ALTIBASE_FO_QUIT\n");
        return ALTIBASE_FO_QUIT;
    }
}


/* debugging purpose function */
void apx_print_bytes(const void *object, size_t size)
{
  const unsigned char * bytes = (const unsigned char *)object;
  size_t i;

  printf("[ ");
  for(i = 0; i < size; i++)
  {
    printf("%02x ", bytes[i]);
  }
  printf("]\n");
}

/* debugging purpose function */
void apx_print_bytes_arraybind_buffer(int array_size, ALTIBASE_BIND *bind, int col_cnt)
{
  int i;

  printf("---print array bind buffer---\n");
  for(i = 0; i < col_cnt; i++)
  {
    apx_print_bytes( bind[i].buffer, (bind[i].buffer_length * array_size) );
  }
}

/* debugging purpose function */
void apx_print_bytes_arraybind_length(int array_size, ALTIBASE_BIND *bind, int col_cnt)
{
  int i;

  printf("---print array bind length---\n");
  for(i = 0; i < col_cnt; i++)
  {
    apx_print_bytes( bind[i].length, (sizeof(ALTIBASE_LONG) * array_size) );
  }
}

ALTIBASE_BOOL apx_ALTIBASE_SUCCEEDED(ALTIBASE_RC rc)
{
    return ( ((rc) & (~1)) == 0 );
}

ALTIBASE_BOOL apx_ALTIBASE_NOT_SUCCEEDED(ALTIBASE_RC rc)
{
    return ( ! apx_ALTIBASE_SUCCEEDED(rc) );
}

ALTIBASE_RES altibase_list_tables2(ALTIBASE alti, char *s0, char *s1, char *s2)
{
    const char *restrictions[3];

    restrictions[0] = s0;
    restrictions[1] = s1;
    restrictions[2] = s2;

    return altibase_list_tables(alti, restrictions);
}

ALTIBASE_RES altibase_list_fields2(ALTIBASE alti, char *s0, char *s1, char *s2)
{
    const char *restrictions[3];

    restrictions[0] = s0;
    restrictions[1] = s1;
    restrictions[2] = s2;

    return altibase_list_fields(alti, restrictions);
}

int altibase_stmt_status2(ALTIBASE_STMT stmt, int array_num)
{
    return altibase_stmt_status(stmt)[array_num];
}

char *apx_row_get_string(char **row, int index)
{
    return row[index];
}

ALTIBASE_BIND *apx_bind_alloc(short col_cnt)
{
    return (ALTIBASE_BIND *) calloc(col_cnt, sizeof(ALTIBASE_BIND));
}

void apx_bind_free(ALTIBASE_BIND *bind, short col_cnt)
{
    int i;

    if (bind != NULL)
    {
        for ( i=0; i<col_cnt; i++ )
        {
            if (bind[i].buffer != NULL)
            {
                free(bind[i].buffer);
            }
            if (bind[i].length != NULL)
            {
                free(bind[i].length);
            }
        }
        free(bind);
    }
}

ALTIBASE_LONG apx_arraybind_get_length(int array_num, ALTIBASE_BIND *bind, short col_num)
{
    return *(ALTIBASE_LONG *)((char *)bind[col_num].length + (sizeof(ALTIBASE_LONG) * array_num) );
}

ALTIBASE_LONG apx_bind_get_length(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_length(0, bind, col_num);
}

ALTIBASE_BIND_TYPE apx_bind_get_buffertype(ALTIBASE_BIND  *bind, short col_num)
{
    return (ALTIBASE_BIND_TYPE) bind[col_num].buffer_type;
}

void apx_arraybind_get_binary(int array_num, ALTIBASE_BIND  *bind, short col_num, char **binary, int *length)
{
    *length = apx_arraybind_get_length(array_num, bind, col_num);
    *binary = (char *)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) );
}

void apx_bind_get_binary(ALTIBASE_BIND  *bind, short col_num, char **binary, int *length)
{
    apx_arraybind_get_binary(0, bind, col_num, binary, length);
}

char *apx_arraybind_get_string(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return (char *)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) );
}

char *apx_bind_get_string(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_string(0, bind, col_num);
}

int apx_arraybind_get_int(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return *(int *)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) );
}

int apx_bind_get_int(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_int(0, bind, col_num);
}

short apx_arraybind_get_short(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return *(short *)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) );
}

short apx_bind_get_short(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_short(0, bind, col_num);
}

double apx_arraybind_get_double(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return *(double *)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) );
}

double apx_bind_get_double(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_double(0, bind, col_num);
}

int apx_arraybind_get_date_year(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return ((ALTIBASE_TIMESTAMP*)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) ))->year;
}

int apx_bind_get_date_year(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_date_year(0, bind, col_num);
}

int apx_arraybind_get_date_month(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return ((ALTIBASE_TIMESTAMP*)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) ))->month;
}

int apx_bind_get_date_month(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_date_month(0, bind, col_num);
}

int apx_arraybind_get_date_day(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return ((ALTIBASE_TIMESTAMP*)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) ))->day;
}

int apx_bind_get_date_day(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_date_day(0, bind, col_num);
}

int apx_arraybind_get_date_hour(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return ((ALTIBASE_TIMESTAMP*)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) ))->hour;
}

int apx_bind_get_date_hour(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_date_hour(0, bind, col_num);
}

int apx_arraybind_get_date_minute(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return ((ALTIBASE_TIMESTAMP*)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) ))->minute;
}

int apx_bind_get_date_minute(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_date_minute(0, bind, col_num);
}

int apx_arraybind_get_date_second(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return ((ALTIBASE_TIMESTAMP*)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) ))->second;
}

int apx_bind_get_date_second(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_date_second(0, bind, col_num);
}

int apx_arraybind_get_date_fraction(int array_num, ALTIBASE_BIND  *bind, short col_num)
{
    return ((ALTIBASE_TIMESTAMP*)(bind[col_num].buffer + (bind[col_num].buffer_length * array_num) ))->fraction;
}

int apx_bind_get_date_fraction(ALTIBASE_BIND  *bind, short col_num)
{
    return apx_arraybind_get_date_fraction(0, bind, col_num);
}

/* # Deprecated
void apx_bind_put_length(ALTIBASE_BIND *bind, short param_num, ALTIBASE_LONG length)
{
    *(ALTIBASE_LONG *)bind[param_num].length = length;
}
*/

void apx_arraybind_put_null(int array_num, ALTIBASE_BIND *bind, short param_num)
{
    *(ALTIBASE_LONG *)((char *)bind[param_num].length + (sizeof(ALTIBASE_LONG) * array_num) ) = ALTIBASE_NULL_DATA;
}
        
void apx_bind_put_null(ALTIBASE_BIND *bind, short param_num)
{
    apx_arraybind_put_null(0, bind, param_num);
}
        
void apx_arraybind_put_string(int array_num, ALTIBASE_BIND *bind, short param_num, char *param_string)
{
    sprintf((char *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ) , "%s", param_string);
    *(ALTIBASE_LONG *)((char *)bind[param_num].length + (sizeof(ALTIBASE_LONG) * array_num) ) = ALTIBASE_NTS;
}
        
void apx_bind_put_string(ALTIBASE_BIND *bind, short param_num, char *param_string)
{
    apx_arraybind_put_string(0, bind, param_num, param_string);
}
        
void apx_arraybind_string(int array_size, ALTIBASE_BIND *bind, short param_num, ALTIBASE_LONG param_size)
{
    int buf_size;

    bind[param_num].buffer_type = ALTIBASE_BIND_STRING;
    buf_size = param_size + 1;
    bind[param_num].buffer = (char*) calloc(array_size, buf_size);
    bind[param_num].buffer_length = buf_size;
    bind[param_num].length = (ALTIBASE_LONG *) calloc(array_size, sizeof(ALTIBASE_LONG));
}
        
void apx_bind_string(ALTIBASE_BIND *bind, short param_num, ALTIBASE_LONG param_size)
{
    apx_arraybind_string(1, bind, param_num, param_size);
}
        
void apx_arraybind_put_binary(int array_num, ALTIBASE_BIND *bind, short param_num, char *binary, ALTIBASE_LONG binary_len)
{
    memcpy((char *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ), binary, binary_len);
    *(ALTIBASE_LONG *)((char *)bind[param_num].length + (sizeof(ALTIBASE_LONG) * array_num) ) = binary_len;
}
        
void apx_bind_put_binary(ALTIBASE_BIND *bind, short param_num, char *binary, ALTIBASE_LONG binary_len)
{
    // memcpy(bind[param_num].buffer, binary, binary_len);
    // *(ALTIBASE_LONG *)bind[param_num].length = binary_len;
    apx_arraybind_put_binary(0, bind, param_num, binary, binary_len);
}
        
void apx_arraybind_binary(int array_size, ALTIBASE_BIND *bind, short param_num, ALTIBASE_LONG param_size)
{
    ALTIBASE_LONG buf_size;

    bind[param_num].buffer_type = ALTIBASE_BIND_BINARY;
    buf_size = param_size;
    bind[param_num].buffer = (char*) calloc(array_size, buf_size);
    bind[param_num].buffer_length = buf_size;
    bind[param_num].length = (ALTIBASE_LONG *) calloc(array_size, sizeof(ALTIBASE_LONG));
}

void apx_bind_binary(ALTIBASE_BIND *bind, short param_num, ALTIBASE_LONG param_size)
{
    apx_arraybind_binary(1, bind, param_num, param_size);
}

void apx_arraybind_put_int(int array_num, ALTIBASE_BIND *bind, short param_num, int param_int)
{
    *(int *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ) = param_int;
    *(ALTIBASE_LONG *)((char *)bind[param_num].length + (sizeof(ALTIBASE_LONG) * array_num) ) = (ALTIBASE_LONG)0;
}
        
void apx_bind_put_int(ALTIBASE_BIND *bind, short param_num, int param_int)
{
    apx_arraybind_put_int(0, bind, param_num, param_int);
}
        
void apx_arraybind_int(int array_size, ALTIBASE_BIND *bind, short param_num)
{
    int buf_size;

    bind[param_num].buffer_type = ALTIBASE_BIND_INTEGER;
    buf_size = sizeof(int);
    bind[param_num].buffer = (char*) calloc(array_size, buf_size);
    bind[param_num].buffer_length = buf_size;
    bind[param_num].length = (ALTIBASE_LONG *) calloc(array_size, sizeof(ALTIBASE_LONG));
}
        
void apx_bind_int(ALTIBASE_BIND *bind, short param_num)
{
    apx_arraybind_int(1, bind, param_num);
}
        
void apx_arraybind_put_short(int array_num, ALTIBASE_BIND *bind, short param_num, short param_short)
{
    *(short *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ) = param_short;
    *(ALTIBASE_LONG *)((char *)bind[param_num].length + (sizeof(ALTIBASE_LONG) * array_num) ) = (ALTIBASE_LONG)0;
}

void apx_bind_put_short(ALTIBASE_BIND *bind, short param_num, short param_short)
{
    apx_arraybind_put_short(0, bind, param_num, param_short);
}
        
void apx_arraybind_short(int array_size, ALTIBASE_BIND *bind, short param_num)
{
    int buf_size;

    bind[param_num].buffer_type = ALTIBASE_BIND_SMALLINT;
    buf_size = sizeof(short);
    bind[param_num].buffer = (char*) calloc(array_size, buf_size);
    bind[param_num].buffer_length = buf_size;
    bind[param_num].length = (ALTIBASE_LONG *) calloc(array_size, sizeof(ALTIBASE_LONG));
}
        
void apx_bind_short(ALTIBASE_BIND *bind, short param_num)
{
    apx_arraybind_short(1, bind, param_num);
}
        
void apx_arraybind_put_double(int array_num, ALTIBASE_BIND *bind, short param_num, double param_double)
{
    *(double *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ) = param_double;
    *(ALTIBASE_LONG *)((char *)bind[param_num].length + (sizeof(ALTIBASE_LONG) * array_num) ) = (ALTIBASE_LONG)0;
}
        
void apx_bind_put_double(ALTIBASE_BIND *bind, short param_num, double param_double)
{
    apx_arraybind_put_double(0, bind, param_num, param_double);
}
        
void apx_arraybind_double(int array_size, ALTIBASE_BIND *bind, short param_num)
{
    int buf_size;

    bind[param_num].buffer_type = ALTIBASE_BIND_DOUBLE;
    buf_size = sizeof(double);
    bind[param_num].buffer = (char*) calloc(array_size, buf_size);
    bind[param_num].buffer_length = buf_size;
    bind[param_num].length = (ALTIBASE_LONG *) calloc(array_size, sizeof(ALTIBASE_LONG));
}
        
void apx_bind_double(ALTIBASE_BIND *bind, short param_num)
{
    apx_arraybind_double(1, bind, param_num);
}
        
void apx_arraybind_put_date(int array_num, ALTIBASE_BIND *bind, short param_num, short aYear, unsigned short aMonth, unsigned short aDay, unsigned short aHour, unsigned short aMinute, unsigned short aSecond, int aFraction)
{
    ((ALTIBASE_TIMESTAMP *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ))->year = aYear;
    ((ALTIBASE_TIMESTAMP *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ))->month = aMonth;
    ((ALTIBASE_TIMESTAMP *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ))->day = aDay;
    ((ALTIBASE_TIMESTAMP *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ))->hour = aHour;
    ((ALTIBASE_TIMESTAMP *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ))->minute = aMinute;
    ((ALTIBASE_TIMESTAMP *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ))->second = aSecond;
    ((ALTIBASE_TIMESTAMP *)(bind[param_num].buffer + (bind[param_num].buffer_length * array_num) ))->fraction = aFraction;
    *(ALTIBASE_LONG *)((char *)bind[param_num].length + (sizeof(ALTIBASE_LONG) * array_num) ) = (ALTIBASE_LONG)0;
}
        
void apx_bind_put_date(ALTIBASE_BIND *bind, short param_num, short aYear, unsigned short aMonth, unsigned short aDay, unsigned short aHour, unsigned short aMinute, unsigned short aSecond, int aFraction)
{
    apx_arraybind_put_date(0, bind, param_num, aYear, aMonth, aDay, aHour, aMinute, aSecond, aFraction);
}
        
void apx_arraybind_date(int array_size, ALTIBASE_BIND *bind, short param_num)
{
    int buf_size;

    bind[param_num].buffer_type = ALTIBASE_BIND_DATE;
    buf_size = sizeof(ALTIBASE_TIMESTAMP);
    bind[param_num].buffer = (char *) calloc(array_size, buf_size);
    bind[param_num].buffer_length = buf_size;
    bind[param_num].length = (ALTIBASE_LONG *) calloc(array_size, sizeof(ALTIBASE_LONG));
}
        
void apx_bind_date(ALTIBASE_BIND *bind, short param_num)
{
    apx_arraybind_date(1, bind, param_num);
}
        
ALTIBASE_FIELD *apx_get_field_from_fields(ALTIBASE_FIELD *fields, int col_num)
{
    return &fields[col_num];
}

%}
