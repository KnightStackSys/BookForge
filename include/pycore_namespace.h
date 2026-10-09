
#include "cpyext_object.h"

#ifdef _WIN64
#define Signed   Py_ssize_t          /* xxx temporary fix */
#define Unsigned unsigned long long  /* xxx temporary fix */
#else
#define Signed   Py_ssize_t     /* xxx temporary fix */
#define Unsigned unsigned long  /* xxx temporary fix */
#endif
#define _PyNamespace_New _PyPyNamespace_New
PyAPI_FUNC(PyObject *) _PyNamespace_New(PyObject * arg0);

#undef Signed    /* xxx temporary fix */
#undef Unsigned  /* xxx temporary fix */

