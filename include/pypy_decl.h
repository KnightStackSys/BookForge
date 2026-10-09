
#include "cpyext_object.h"

#ifdef _WIN64
#define Signed   Py_ssize_t          /* xxx temporary fix */
#define Unsigned unsigned long long  /* xxx temporary fix */
#else
#define Signed   Py_ssize_t     /* xxx temporary fix */
#define Unsigned unsigned long  /* xxx temporary fix */
#endif
typedef struct { PyObject_HEAD } PyMethodObject;
typedef struct { PyObject_HEAD } PyListObject;
typedef struct { PyObject_HEAD } PyLongObject;
typedef struct { PyObject_HEAD } PyBaseExceptionObject;
PyAPI_FUNC(struct _object *) PyBool_FromLong(int arg0);
PyAPI_FUNC(int) PyBuffer_FillInfo(struct bufferinfo *arg0, struct _object *arg1, void *arg2, Signed arg3, int arg4, int arg5);
PyAPI_FUNC(int) PyBuffer_IsContiguous(struct bufferinfo *arg0, char arg1);
PyAPI_FUNC(Signed) PyBuffer_SizeFromFormat(const char *arg0);
PyAPI_FUNC(char *) PyByteArray_AsString(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyByteArray_Concat(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyByteArray_FromObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyByteArray_FromStringAndSize(const char *arg0, Signed arg1);
PyAPI_FUNC(int) PyByteArray_Resize(struct _object *arg0, Signed arg1);
PyAPI_FUNC(Signed) PyByteArray_Size(struct _object *arg0);
#define PyBytes_AS_STRING PyPyBytes_AS_STRING
PyAPI_FUNC(char *) PyBytes_AS_STRING(void *arg0);
PyAPI_FUNC(char *) PyBytes_AsString(struct _object *arg0);
PyAPI_FUNC(int) PyBytes_AsStringAndSize(struct _object *arg0, char **arg1, Signed *arg2);
PyAPI_FUNC(void) PyBytes_Concat(struct _object **arg0, struct _object *arg1);
PyAPI_FUNC(void) PyBytes_ConcatAndDel(struct _object **arg0, struct _object *arg1);
PyAPI_FUNC(PyObject *) PyBytes_DecodeEscape(char const * arg0, Py_ssize_t arg1, char const * arg2, Py_ssize_t arg3, char const * arg4);
PyAPI_FUNC(struct _object *) PyBytes_FromObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyBytes_FromString(const char *arg0);
PyAPI_FUNC(struct _object *) PyBytes_FromStringAndSize(const char *arg0, Signed arg1);
PyAPI_FUNC(Signed) PyBytes_Size(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyCFunction_Call(struct _object *arg0, struct _object *arg1, struct _object *arg2);
#define PyCFunction_Check PyPyCFunction_Check
PyAPI_FUNC(int) PyCFunction_Check(struct _object *arg0);
PyAPI_FUNC(int) PyCFunction_GetFlags(struct _object *arg0);
PyAPI_FUNC(PyCFunction) PyCFunction_GetFunction(PyObject * arg0);
PyAPI_FUNC(struct _object *) PyCFunction_GetSelf(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyCMethod_New(struct PyMethodDef *arg0, struct _object *arg1, struct _object *arg2, struct _object *arg3);
PyAPI_FUNC(struct _object *) PyCallIter_New(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyCallable_Check(struct _object *arg0);
PyAPI_FUNC(PyObject *) PyCapsule_New(void * arg0, char const * arg1, PyCapsule_Destructor arg2);
PyAPI_FUNC(int) PyCapsule_SetContext(PyObject * arg0, void * arg1);
PyAPI_FUNC(int) PyCapsule_SetDestructor(PyObject * arg0, PyCapsule_Destructor arg1);
PyAPI_FUNC(int) PyCapsule_SetName(PyObject * arg0, char const * arg1);
PyAPI_FUNC(int) PyCapsule_SetPointer(PyObject * arg0, void * arg1);
#define PyClassMethod_New PyPyClassMethod_New
PyAPI_FUNC(struct _object *) PyClassMethod_New(struct _object *arg0);
#define PyCode_Addr2Line PyPyCode_Addr2Line
PyAPI_FUNC(int) PyCode_Addr2Line(PyCodeObject *arg0, int arg1);
#define PyCode_Check PyPyCode_Check
PyAPI_FUNC(int) PyCode_Check(void * arg0);
#define PyCode_CheckExact PyPyCode_CheckExact
PyAPI_FUNC(int) PyCode_CheckExact(void * arg0);
#define PyCode_GetCellvars PyPyCode_GetCellvars
PyAPI_FUNC(struct _object *) PyCode_GetCellvars(PyCodeObject *arg0);
#define PyCode_GetCode PyPyCode_GetCode
PyAPI_FUNC(struct _object *) PyCode_GetCode(PyCodeObject *arg0);
#define PyCode_GetFreevars PyPyCode_GetFreevars
PyAPI_FUNC(struct _object *) PyCode_GetFreevars(PyCodeObject *arg0);
#define PyCode_GetNumFree PyPyCode_GetNumFree
PyAPI_FUNC(Signed) PyCode_GetNumFree(PyCodeObject *arg0);
#define PyCode_GetVarnames PyPyCode_GetVarnames
PyAPI_FUNC(struct _object *) PyCode_GetVarnames(PyCodeObject *arg0);
#define PyCode_NewEmpty PyPyCode_NewEmpty
PyAPI_FUNC(PyCodeObject *) PyCode_NewEmpty(const char *arg0, const char *arg1, int arg2);
PyAPI_FUNC(struct _object *) PyCodec_Decode(struct _object *arg0, const char *arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyCodec_Decoder(const char *arg0);
PyAPI_FUNC(struct _object *) PyCodec_Encode(struct _object *arg0, const char *arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyCodec_Encoder(const char *arg0);
PyAPI_FUNC(struct _object *) PyCodec_IncrementalDecoder(const char *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyCodec_IncrementalEncoder(const char *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyComplex_FromDoubles(double arg0, double arg1);
PyAPI_FUNC(double) PyComplex_ImagAsDouble(struct _object *arg0);
PyAPI_FUNC(double) PyComplex_RealAsDouble(struct _object *arg0);
#define PyContextVar_Get PyPyContextVar_Get
PyAPI_FUNC(int) PyContextVar_Get(struct _object *arg0, struct _object *arg1, struct _object **arg2);
#define PyContextVar_New PyPyContextVar_New
PyAPI_FUNC(struct _object *) PyContextVar_New(const char *arg0, struct _object *arg1);
#define PyContextVar_Reset PyPyContextVar_Reset
PyAPI_FUNC(int) PyContextVar_Reset(struct _object *arg0, struct _object *arg1);
#define PyContextVar_Set PyPyContextVar_Set
PyAPI_FUNC(struct _object *) PyContextVar_Set(struct _object *arg0, struct _object *arg1);
#define PyCoro_Check PyPyCoro_Check
PyAPI_FUNC(int) PyCoro_Check(void * arg0);
#define PyCoro_CheckExact PyPyCoro_CheckExact
PyAPI_FUNC(int) PyCoro_CheckExact(void * arg0);
#define PyDateTime_Check PyPyDateTime_Check
PyAPI_FUNC(int) PyDateTime_Check(struct _object *arg0);
#define PyDateTime_CheckExact PyPyDateTime_CheckExact
PyAPI_FUNC(int) PyDateTime_CheckExact(struct _object *arg0);
#define PyDateTime_DATE_GET_HOUR PyPyDateTime_DATE_GET_HOUR
PyAPI_FUNC(int) PyDateTime_DATE_GET_HOUR(void *arg0);
#define PyDateTime_DATE_GET_MICROSECOND PyPyDateTime_DATE_GET_MICROSECOND
PyAPI_FUNC(int) PyDateTime_DATE_GET_MICROSECOND(void *arg0);
#define PyDateTime_DATE_GET_MINUTE PyPyDateTime_DATE_GET_MINUTE
PyAPI_FUNC(int) PyDateTime_DATE_GET_MINUTE(void *arg0);
#define PyDateTime_DATE_GET_SECOND PyPyDateTime_DATE_GET_SECOND
PyAPI_FUNC(int) PyDateTime_DATE_GET_SECOND(void *arg0);
#define PyDateTime_DATE_GET_TZINFO PyPyDateTime_DATE_GET_TZINFO
PyAPI_FUNC(struct _object *) PyDateTime_DATE_GET_TZINFO(void *arg0);
#define PyDateTime_DELTA_GET_DAYS PyPyDateTime_DELTA_GET_DAYS
PyAPI_FUNC(int) PyDateTime_DELTA_GET_DAYS(void *arg0);
#define PyDateTime_DELTA_GET_MICROSECONDS PyPyDateTime_DELTA_GET_MICROSECONDS
PyAPI_FUNC(int) PyDateTime_DELTA_GET_MICROSECONDS(void *arg0);
#define PyDateTime_DELTA_GET_SECONDS PyPyDateTime_DELTA_GET_SECONDS
PyAPI_FUNC(int) PyDateTime_DELTA_GET_SECONDS(void *arg0);
#define PyDateTime_FromTimestamp PyPyDateTime_FromTimestamp
PyAPI_FUNC(struct _object *) PyDateTime_FromTimestamp(struct _object *arg0);
#define PyDateTime_GET_DAY PyPyDateTime_GET_DAY
PyAPI_FUNC(int) PyDateTime_GET_DAY(void *arg0);
#define PyDateTime_GET_FOLD PyPyDateTime_GET_FOLD
PyAPI_FUNC(int) PyDateTime_GET_FOLD(void *arg0);
#define PyDateTime_GET_MONTH PyPyDateTime_GET_MONTH
PyAPI_FUNC(int) PyDateTime_GET_MONTH(void *arg0);
#define PyDateTime_GET_YEAR PyPyDateTime_GET_YEAR
PyAPI_FUNC(int) PyDateTime_GET_YEAR(void *arg0);
#define PyDateTime_TIME_GET_FOLD PyPyDateTime_TIME_GET_FOLD
PyAPI_FUNC(int) PyDateTime_TIME_GET_FOLD(void *arg0);
#define PyDateTime_TIME_GET_HOUR PyPyDateTime_TIME_GET_HOUR
PyAPI_FUNC(int) PyDateTime_TIME_GET_HOUR(void *arg0);
#define PyDateTime_TIME_GET_MICROSECOND PyPyDateTime_TIME_GET_MICROSECOND
PyAPI_FUNC(int) PyDateTime_TIME_GET_MICROSECOND(void *arg0);
#define PyDateTime_TIME_GET_MINUTE PyPyDateTime_TIME_GET_MINUTE
PyAPI_FUNC(int) PyDateTime_TIME_GET_MINUTE(void *arg0);
#define PyDateTime_TIME_GET_SECOND PyPyDateTime_TIME_GET_SECOND
PyAPI_FUNC(int) PyDateTime_TIME_GET_SECOND(void *arg0);
#define PyDateTime_TIME_GET_TZINFO PyPyDateTime_TIME_GET_TZINFO
PyAPI_FUNC(struct _object *) PyDateTime_TIME_GET_TZINFO(void *arg0);
#define PyDate_Check PyPyDate_Check
PyAPI_FUNC(int) PyDate_Check(struct _object *arg0);
#define PyDate_CheckExact PyPyDate_CheckExact
PyAPI_FUNC(int) PyDate_CheckExact(struct _object *arg0);
#define PyDate_FromTimestamp PyPyDate_FromTimestamp
PyAPI_FUNC(struct _object *) PyDate_FromTimestamp(struct _object *arg0);
#define PyDelta_Check PyPyDelta_Check
PyAPI_FUNC(int) PyDelta_Check(struct _object *arg0);
#define PyDelta_CheckExact PyPyDelta_CheckExact
PyAPI_FUNC(int) PyDelta_CheckExact(struct _object *arg0);
PyAPI_FUNC(PyObject *) PyDescr_NewClassMethod(PyTypeObject * arg0, PyMethodDef * arg1);
PyAPI_FUNC(struct _object *) PyDescr_NewGetSet(struct _typeobject *arg0, struct PyGetSetDef *arg1);
PyAPI_FUNC(PyObject *) PyDescr_NewMethod(PyTypeObject * arg0, PyMethodDef * arg1);
#define PyDictProxy_Check PyPyDictProxy_Check
PyAPI_FUNC(int) PyDictProxy_Check(void * arg0);
#define PyDictProxy_CheckExact PyPyDictProxy_CheckExact
PyAPI_FUNC(int) PyDictProxy_CheckExact(void * arg0);
PyAPI_FUNC(struct _object *) PyDictProxy_New(struct _object *arg0);
PyAPI_FUNC(void) PyDict_Clear(struct _object *arg0);
PyAPI_FUNC(int) PyDict_Contains(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyDict_Copy(struct _object *arg0);
PyAPI_FUNC(int) PyDict_DelItem(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyDict_DelItemString(struct _object *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyDict_GetItem(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyDict_GetItemString(struct _object *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyDict_GetItemWithError(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyDict_Items(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyDict_Keys(struct _object *arg0);
PyAPI_FUNC(int) PyDict_Merge(struct _object *arg0, struct _object *arg1, int arg2);
PyAPI_FUNC(struct _object *) PyDict_New(void);
PyAPI_FUNC(int) PyDict_Next(struct _object *arg0, Signed *arg1, struct _object **arg2, struct _object **arg3);
#define PyDict_SetDefault PyPyDict_SetDefault
PyAPI_FUNC(PyObject *) PyDict_SetDefault(PyObject * arg0, PyObject * arg1, PyObject * arg2);
PyAPI_FUNC(int) PyDict_SetItem(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(int) PyDict_SetItemString(struct _object *arg0, const char *arg1, struct _object *arg2);
PyAPI_FUNC(Signed) PyDict_Size(struct _object *arg0);
PyAPI_FUNC(int) PyDict_Update(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyDict_Values(struct _object *arg0);
PyAPI_FUNC(int) PyErr_BadArgument(void);
PyAPI_FUNC(void) PyErr_BadInternalCall(void);
PyAPI_FUNC(int) PyErr_CheckSignals(void);
PyAPI_FUNC(void) PyErr_Clear(void);
PyAPI_FUNC(void) PyErr_Display(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(void) PyErr_DisplayException(struct _object *arg0);
PyAPI_FUNC(int) PyErr_ExceptionMatches(struct _object *arg0);
PyAPI_FUNC(void) PyErr_Fetch(struct _object **arg0, struct _object **arg1, struct _object **arg2);
PyAPI_FUNC(void) PyErr_GetExcInfo(struct _object **arg0, struct _object **arg1, struct _object **arg2);
PyAPI_FUNC(struct _object *) PyErr_GetHandledException(void);
PyAPI_FUNC(struct _object *) PyErr_GetRaisedException(void);
PyAPI_FUNC(int) PyErr_GivenExceptionMatches(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyErr_NoMemory(void);
PyAPI_FUNC(void) PyErr_NormalizeException(struct _object **arg0, struct _object **arg1, struct _object **arg2);
PyAPI_FUNC(struct _object *) PyErr_Occurred(void);
PyAPI_FUNC(void) PyErr_Print(void);
PyAPI_FUNC(void) PyErr_PrintEx(int arg0);
PyAPI_FUNC(void) PyErr_Restore(struct _object *arg0, struct _object *arg1, struct _object *arg2);
#define PyErr_SetExcFromWindowsErrWithFilenameObject PyPyErr_SetExcFromWindowsErrWithFilenameObject
PyAPI_FUNC(struct _object *) PyErr_SetExcFromWindowsErrWithFilenameObject(struct _object *arg0, int arg1, struct _object *arg2);
#define PyErr_SetExcFromWindowsErrWithFilenameObjects PyPyErr_SetExcFromWindowsErrWithFilenameObjects
PyAPI_FUNC(struct _object *) PyErr_SetExcFromWindowsErrWithFilenameObjects(struct _object *arg0, int arg1, struct _object *arg2, struct _object *arg3);
PyAPI_FUNC(void) PyErr_SetExcInfo(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyErr_SetFromErrno(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyErr_SetFromErrnoWithFilename(struct _object *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyErr_SetFromErrnoWithFilenameObject(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyErr_SetFromErrnoWithFilenameObjects(struct _object *arg0, struct _object *arg1, struct _object *arg2);
#define PyErr_SetFromWindowsErr PyPyErr_SetFromWindowsErr
PyAPI_FUNC(struct _object *) PyErr_SetFromWindowsErr(int arg0);
#define PyErr_SetFromWindowsErrWithFilename PyPyErr_SetFromWindowsErrWithFilename
PyAPI_FUNC(struct _object *) PyErr_SetFromWindowsErrWithFilename(int arg0, const char *arg1);
PyAPI_FUNC(void) PyErr_SetHandledException(struct _object *arg0);
PyAPI_FUNC(void) PyErr_SetNone(struct _object *arg0);
PyAPI_FUNC(void) PyErr_SetObject(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(void) PyErr_SetRaisedException(struct _object *arg0);
PyAPI_FUNC(void) PyErr_SetString(struct _object *arg0, const char *arg1);
#define PyErr_Warn PyPyErr_Warn
PyAPI_FUNC(int) PyErr_Warn(struct _object *arg0, const char *arg1);
PyAPI_FUNC(int) PyErr_WarnEx(struct _object *arg0, const char *arg1, Signed arg2);
PyAPI_FUNC(int) PyErr_WarnExplicit(struct _object *arg0, const char *arg1, const char *arg2, int arg3, const char *arg4, struct _object *arg5);
PyAPI_FUNC(void) PyErr_WriteUnraisable(struct _object *arg0);
PyAPI_FUNC(void) PyEval_AcquireThread(PyThreadState *arg0);
PyAPI_FUNC(struct _object *) PyEval_CallObjectWithKeywords(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyEval_EvalCode(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyEval_EvalCodeEx(struct _object *arg0, struct _object *arg1, struct _object *arg2, struct _object **arg3, int arg4, struct _object **arg5, int arg6, struct _object **arg7, int arg8, struct _object *arg9, struct _object *arg10);
PyAPI_FUNC(struct _object *) PyEval_GetBuiltins(void);
PyAPI_FUNC(PyFrameObject *) PyEval_GetFrame(void);
PyAPI_FUNC(char const *) PyEval_GetFuncName(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyEval_GetGlobals(void);
PyAPI_FUNC(struct _object *) PyEval_GetLocals(void);
PyAPI_FUNC(void) PyEval_InitThreads(void);
#define PyEval_MergeCompilerFlags PyPyEval_MergeCompilerFlags
PyAPI_FUNC(int) PyEval_MergeCompilerFlags(PyCompilerFlags *arg0);
PyAPI_FUNC(void) PyEval_ReleaseThread(PyThreadState *arg0);
PyAPI_FUNC(void) PyEval_RestoreThread(PyThreadState *arg0);
PyAPI_FUNC(PyThreadState *) PyEval_SaveThread(void);
PyAPI_FUNC(int) PyEval_ThreadsInitialized(void);
#define PyExceptionInstance_Class PyPyExceptionInstance_Class
PyAPI_FUNC(struct _object *) PyExceptionInstance_Class(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyException_GetArgs(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyException_GetCause(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyException_GetContext(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyException_GetTraceback(struct _object *arg0);
PyAPI_FUNC(void) PyException_SetArgs(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(void) PyException_SetCause(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(void) PyException_SetContext(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyException_SetTraceback(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyFile_FromFd(int arg0, const char *arg1, const char *arg2, int arg3, const char *arg4, const char *arg5, const char *arg6, int arg7);
#define PyFile_FromString PyPyFile_FromString
PyAPI_FUNC(struct _object *) PyFile_FromString(const char *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyFile_GetLine(struct _object *arg0, int arg1);
PyAPI_FUNC(int) PyFile_WriteObject(struct _object *arg0, struct _object *arg1, int arg2);
PyAPI_FUNC(int) PyFile_WriteString(const char *arg0, struct _object *arg1);
#define PyFloat_AS_DOUBLE PyPyFloat_AS_DOUBLE
PyAPI_FUNC(double) PyFloat_AS_DOUBLE(void *arg0);
PyAPI_FUNC(double) PyFloat_AsDouble(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyFloat_FromDouble(double arg0);
PyAPI_FUNC(struct _object *) PyFloat_FromString(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyFloat_GetInfo(void);
PyAPI_FUNC(double) PyFloat_GetMax(void);
PyAPI_FUNC(double) PyFloat_GetMin(void);
#define PyFrame_GetBuiltins PyPyFrame_GetBuiltins
PyAPI_FUNC(struct _object *) PyFrame_GetBuiltins(PyFrameObject *arg0);
#define PyFrame_GetGenerator PyPyFrame_GetGenerator
PyAPI_FUNC(struct _object *) PyFrame_GetGenerator(PyFrameObject *arg0);
#define PyFrame_GetGlobals PyPyFrame_GetGlobals
PyAPI_FUNC(struct _object *) PyFrame_GetGlobals(PyFrameObject *arg0);
#define PyFrame_GetLasti PyPyFrame_GetLasti
PyAPI_FUNC(int) PyFrame_GetLasti(PyFrameObject *arg0);
PyAPI_FUNC(int) PyFrame_GetLineNumber(PyFrameObject *arg0);
#define PyFrame_GetLocals PyPyFrame_GetLocals
PyAPI_FUNC(struct _object *) PyFrame_GetLocals(PyFrameObject *arg0);
#define PyFrame_GetVar PyPyFrame_GetVar
PyAPI_FUNC(struct _object *) PyFrame_GetVar(PyFrameObject *arg0, struct _object *arg1);
#define PyFrame_GetVarString PyPyFrame_GetVarString
PyAPI_FUNC(struct _object *) PyFrame_GetVarString(PyFrameObject *arg0, char const *arg1);
#define PyFrame_New PyPyFrame_New
PyAPI_FUNC(PyFrameObject *) PyFrame_New(PyThreadState *arg0, PyCodeObject *arg1, struct _object *arg2, struct _object *arg3);
PyAPI_FUNC(struct _object *) PyFrozenSet_New(struct _object *arg0);
#define PyFunction_Check PyPyFunction_Check
PyAPI_FUNC(int) PyFunction_Check(void * arg0);
#define PyFunction_CheckExact PyPyFunction_CheckExact
PyAPI_FUNC(int) PyFunction_CheckExact(void * arg0);
#define PyFunction_GetCode PyPyFunction_GetCode
PyAPI_FUNC(struct _object *) PyFunction_GetCode(struct _object *arg0);
#define PyFunction_GetGlobals PyPyFunction_GetGlobals
PyAPI_FUNC(struct _object *) PyFunction_GetGlobals(struct _object *arg0);
#define PyFunction_GetModule PyPyFunction_GetModule
PyAPI_FUNC(struct _object *) PyFunction_GetModule(struct _object *arg0);
PyAPI_FUNC(Py_ssize_t) PyGC_Collect(void);
PyAPI_FUNC(int) PyGC_Disable(void);
PyAPI_FUNC(int) PyGC_Enable(void);
PyAPI_FUNC(int) PyGC_IsEnabled(void);
#define PyGILState_Check PyPyGILState_Check
PyAPI_FUNC(int) PyGILState_Check(void);
PyAPI_FUNC(int) PyGILState_Ensure(void);
PyAPI_FUNC(PyThreadState *) PyGILState_GetThisThreadState(void);
PyAPI_FUNC(void) PyGILState_Release(int arg0);
#define PyGen_Check PyPyGen_Check
PyAPI_FUNC(int) PyGen_Check(void * arg0);
#define PyGen_CheckExact PyPyGen_CheckExact
PyAPI_FUNC(int) PyGen_CheckExact(void * arg0);
PyAPI_FUNC(struct _object *) PyImport_AddModule(const char *arg0);
PyAPI_FUNC(struct _object *) PyImport_AddModuleObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyImport_ExecCodeModule(char const *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyImport_ExecCodeModuleEx(char const *arg0, struct _object *arg1, char const *arg2);
PyAPI_FUNC(long) PyImport_GetMagicNumber(void);
PyAPI_FUNC(char const *) PyImport_GetMagicTag(void);
PyAPI_FUNC(struct _object *) PyImport_GetModule(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyImport_GetModuleDict(void);
PyAPI_FUNC(struct _object *) PyImport_Import(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyImport_ImportModule(const char *arg0);
PyAPI_FUNC(PyObject *) PyImport_ImportModuleLevelObject(PyObject * arg0, PyObject * arg1, PyObject * arg2, PyObject * arg3, int arg4);
PyAPI_FUNC(struct _object *) PyImport_ImportModuleNoBlock(const char *arg0);
PyAPI_FUNC(struct _object *) PyImport_ReloadModule(struct _object *arg0);
#define PyInstanceMethod_Check PyPyInstanceMethod_Check
PyAPI_FUNC(int) PyInstanceMethod_Check(struct _object *arg0);
#define PyInstanceMethod_Function PyPyInstanceMethod_Function
PyAPI_FUNC(struct _object *) PyInstanceMethod_Function(struct _object *arg0);
#define PyInstanceMethod_GET_FUNCTION PyPyInstanceMethod_GET_FUNCTION
PyAPI_FUNC(struct _object *) PyInstanceMethod_GET_FUNCTION(struct _object *arg0);
#define PyInstanceMethod_New PyPyInstanceMethod_New
PyAPI_FUNC(struct _object *) PyInstanceMethod_New(struct _object *arg0);
PyAPI_FUNC(int) PyInterpreterState_GetID(PyInterpreterState *arg0);
#define PyInterpreterState_Head PyPyInterpreterState_Head
PyAPI_FUNC(PyInterpreterState *) PyInterpreterState_Head(void);
#define PyInterpreterState_Main PyPyInterpreterState_Main
PyAPI_FUNC(PyInterpreterState *) PyInterpreterState_Main(void);
#define PyInterpreterState_Next PyPyInterpreterState_Next
PyAPI_FUNC(PyInterpreterState *) PyInterpreterState_Next(PyInterpreterState *arg0);
PyAPI_FUNC(int) PyIter_Check(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyIter_Next(struct _object *arg0);
PyAPI_FUNC(int) PyIter_Send(struct _object *arg0, struct _object *arg1, struct _object **arg2);
PyAPI_FUNC(int) PyList_Append(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyList_AsTuple(struct _object *arg0);
#define PyList_GET_ITEM PyPyList_GET_ITEM
PyAPI_FUNC(struct _object *) PyList_GET_ITEM(void *arg0, Signed arg1);
#define PyList_GET_SIZE PyPyList_GET_SIZE
PyAPI_FUNC(Signed) PyList_GET_SIZE(void *arg0);
PyAPI_FUNC(struct _object *) PyList_GetItem(struct _object *arg0, Signed arg1);
PyAPI_FUNC(struct _object *) PyList_GetSlice(struct _object *arg0, Signed arg1, Signed arg2);
PyAPI_FUNC(int) PyList_Insert(struct _object *arg0, Signed arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyList_New(Signed arg0);
PyAPI_FUNC(int) PyList_Reverse(struct _object *arg0);
#define PyList_SET_ITEM PyPyList_SET_ITEM
PyAPI_FUNC(void) PyList_SET_ITEM(void *arg0, Signed arg1, struct _object *arg2);
PyAPI_FUNC(int) PyList_SetItem(struct _object *arg0, Signed arg1, struct _object *arg2);
PyAPI_FUNC(int) PyList_SetSlice(struct _object *arg0, Signed arg1, Signed arg2, struct _object *arg3);
PyAPI_FUNC(Signed) PyList_Size(struct _object *arg0);
PyAPI_FUNC(int) PyList_Sort(struct _object *arg0);
PyAPI_FUNC(double) PyLong_AsDouble(struct _object *arg0);
PyAPI_FUNC(int) PyLong_AsLong(struct _object *arg0);
PyAPI_FUNC(int) PyLong_AsLongAndOverflow(struct _object *arg0, int *arg1);
PyAPI_FUNC(long long) PyLong_AsLongLong(PyObject * arg0);
PyAPI_FUNC(long long) PyLong_AsLongLongAndOverflow(PyObject * arg0, int * arg1);
PyAPI_FUNC(size_t) PyLong_AsSize_t(struct _object *arg0);
PyAPI_FUNC(Signed) PyLong_AsSsize_t(struct _object *arg0);
PyAPI_FUNC(unsigned int) PyLong_AsUnsignedLong(struct _object *arg0);
PyAPI_FUNC(unsigned long long) PyLong_AsUnsignedLongLong(PyObject * arg0);
PyAPI_FUNC(unsigned long long) PyLong_AsUnsignedLongLongMask(PyObject * arg0);
PyAPI_FUNC(unsigned int) PyLong_AsUnsignedLongMask(struct _object *arg0);
PyAPI_FUNC(void *) PyLong_AsVoidPtr(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyLong_FromDouble(double arg0);
PyAPI_FUNC(struct _object *) PyLong_FromLong(int arg0);
PyAPI_FUNC(PyObject *) PyLong_FromLongLong(long long arg0);
PyAPI_FUNC(struct _object *) PyLong_FromSize_t(size_t arg0);
PyAPI_FUNC(struct _object *) PyLong_FromSsize_t(Signed arg0);
PyAPI_FUNC(struct _object *) PyLong_FromString(const char *arg0, char **arg1, int arg2);
#define PyLong_FromUnicode PyPyLong_FromUnicode
PyAPI_FUNC(struct _object *) PyLong_FromUnicode(wchar_t *arg0, Signed arg1, int arg2);
#define PyLong_FromUnicodeObject PyPyLong_FromUnicodeObject
PyAPI_FUNC(struct _object *) PyLong_FromUnicodeObject(struct _object *arg0, int arg1);
PyAPI_FUNC(PyObject *) PyLong_FromUnsignedLong(unsigned long arg0);
PyAPI_FUNC(PyObject *) PyLong_FromUnsignedLongLong(unsigned long long arg0);
PyAPI_FUNC(struct _object *) PyLong_FromVoidPtr(void *arg0);
PyAPI_FUNC(int) PyMapping_Check(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyMapping_GetItemString(struct _object *arg0, const char *arg1);
PyAPI_FUNC(int) PyMapping_HasKey(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyMapping_HasKeyString(struct _object *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyMapping_Items(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyMapping_Keys(struct _object *arg0);
PyAPI_FUNC(Signed) PyMapping_Length(struct _object *arg0);
PyAPI_FUNC(int) PyMapping_SetItemString(struct _object *arg0, const char *arg1, struct _object *arg2);
PyAPI_FUNC(Signed) PyMapping_Size(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyMapping_Values(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyMember_GetOne(const char *arg0, struct PyMemberDef *arg1);
PyAPI_FUNC(int) PyMember_SetOne(char *arg0, struct PyMemberDef *arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyMemoryView_FromBuffer(struct bufferinfo *arg0);
PyAPI_FUNC(PyObject *) PyMemoryView_FromMemory(char * arg0, Py_ssize_t arg1, int arg2);
PyAPI_FUNC(struct _object *) PyMemoryView_FromObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyMemoryView_GetContiguous(struct _object *arg0, int arg1, char arg2);
#define PyMethodDescr_Check PyPyMethodDescr_Check
PyAPI_FUNC(int) PyMethodDescr_Check(void * arg0);
#define PyMethodDescr_CheckExact PyPyMethodDescr_CheckExact
PyAPI_FUNC(int) PyMethodDescr_CheckExact(void * arg0);
#define PyMethod_Check PyPyMethod_Check
PyAPI_FUNC(int) PyMethod_Check(void * arg0);
#define PyMethod_CheckExact PyPyMethod_CheckExact
PyAPI_FUNC(int) PyMethod_CheckExact(void * arg0);
#define PyMethod_Function PyPyMethod_Function
PyAPI_FUNC(struct _object *) PyMethod_Function(struct _object *arg0);
#define PyMethod_New PyPyMethod_New
PyAPI_FUNC(struct _object *) PyMethod_New(struct _object *arg0, struct _object *arg1);
#define PyMethod_Self PyPyMethod_Self
PyAPI_FUNC(struct _object *) PyMethod_Self(struct _object *arg0);
PyAPI_FUNC(int) PyModule_AddFunctions(struct _object *arg0, struct PyMethodDef *arg1);
PyAPI_FUNC(struct _object *) PyModule_Create2(struct PyModuleDef *arg0, int arg1);
PyAPI_FUNC(int) PyModule_ExecDef(struct _object *arg0, struct PyModuleDef *arg1);
#define PyModule_FromDefAndSpec PyPyModule_FromDefAndSpec
PyAPI_FUNC(PyObject *) PyModule_FromDefAndSpec(PyModuleDef * arg0, PyObject * arg1);
PyAPI_FUNC(PyObject *) PyModule_FromDefAndSpec2(PyModuleDef * arg0, PyObject * arg1, int arg2);
PyAPI_FUNC(struct _object *) PyModule_GetDict(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyModule_GetFilenameObject(struct _object *arg0);
PyAPI_FUNC(char *) PyModule_GetName(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyModule_GetNameObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyModule_New(const char *arg0);
PyAPI_FUNC(struct _object *) PyModule_NewObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_Absolute(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_Add(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_And(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(Signed) PyNumber_AsSsize_t(struct _object *arg0, struct _object *arg1);
#define PyNumber_Divide PyPyNumber_Divide
PyAPI_FUNC(struct _object *) PyNumber_Divide(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Divmod(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Float(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_FloorDivide(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceAdd(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceAnd(struct _object *arg0, struct _object *arg1);
#define PyNumber_InPlaceDivide PyPyNumber_InPlaceDivide
PyAPI_FUNC(struct _object *) PyNumber_InPlaceDivide(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceFloorDivide(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceLshift(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceMatrixMultiply(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceMultiply(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceOr(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlacePower(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceRemainder(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceRshift(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceSubtract(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceTrueDivide(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_InPlaceXor(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Index(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_Invert(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_Long(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_Lshift(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_MatrixMultiply(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Multiply(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Negative(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_Or(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Positive(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyNumber_Power(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyNumber_Remainder(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Rshift(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Subtract(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_ToBase(struct _object *arg0, int arg1);
PyAPI_FUNC(struct _object *) PyNumber_TrueDivide(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyNumber_Xor(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(void) PyOS_AfterFork(void);
PyAPI_FUNC(struct _object *) PyOS_FSPath(struct _object *arg0);
PyAPI_FUNC(int) PyOS_InterruptOccurred(void);
PyAPI_FUNC(char *) PyOS_double_to_string(double arg0, char arg1, int arg2, int arg3, int *arg4);
PyAPI_FUNC(double) PyOS_string_to_double(char const *arg0, char **arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyObject_ASCII(struct _object *arg0);
PyAPI_FUNC(int) PyObject_AsCharBuffer(struct _object *arg0, const char **arg1, Signed *arg2);
PyAPI_FUNC(int) PyObject_AsFileDescriptor(struct _object *arg0);
PyAPI_FUNC(PyObject *) PyObject_Bytes(PyObject * arg0);
PyAPI_FUNC(struct _object *) PyObject_Call(struct _object *arg0, struct _object *arg1, struct _object *arg2);
#define PyObject_CallMethodNoArgs PyPyObject_CallMethodNoArgs
PyAPI_FUNC(struct _object *) PyObject_CallMethodNoArgs(struct _object *arg0, struct _object *arg1);
#define PyObject_CallMethodOneArg PyPyObject_CallMethodOneArg
PyAPI_FUNC(struct _object *) PyObject_CallMethodOneArg(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(struct _object *) PyObject_CallNoArgs(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyObject_CallObject(struct _object *arg0, struct _object *arg1);
#define PyObject_CallOneArg PyPyObject_CallOneArg
PyAPI_FUNC(struct _object *) PyObject_CallOneArg(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(void *) PyObject_Calloc(size_t arg0, size_t arg1);
PyAPI_FUNC(int) PyObject_DelItem(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyObject_Dir(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyObject_Format(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyObject_GC_IsFinalized(struct _object *arg0);
PyAPI_FUNC(int) PyObject_GC_IsTracked(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyObject_GenericGetAttr(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyObject_GenericGetDict(struct _object *arg0, void *arg1);
PyAPI_FUNC(int) PyObject_GenericSetAttr(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(int) PyObject_GenericSetDict(struct _object *arg0, struct _object *arg1, void *arg2);
PyAPI_FUNC(struct _object *) PyObject_GetAttr(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(PyObject *) PyObject_GetAttrString(PyObject * arg0, char const * arg1);
PyAPI_FUNC(struct _object *) PyObject_GetItem(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyObject_GetIter(struct _object *arg0);
PyAPI_FUNC(int) PyObject_HasAttr(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyObject_HasAttrString(PyObject * arg0, char const * arg1);
PyAPI_FUNC(Signed) PyObject_Hash(struct _object *arg0);
PyAPI_FUNC(Signed) PyObject_HashNotImplemented(struct _object *arg0);
PyAPI_FUNC(int) PyObject_IsInstance(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyObject_IsSubclass(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyObject_IsTrue(struct _object *arg0);
#define PyObject_LengthHint PyPyObject_LengthHint
PyAPI_FUNC(Py_ssize_t) PyObject_LengthHint(PyObject * arg0, Py_ssize_t arg1);
PyAPI_FUNC(void *) PyObject_Malloc(size_t arg0);
PyAPI_FUNC(int) PyObject_Not(struct _object *arg0);
#define PyObject_Print PyPyObject_Print
PyAPI_FUNC(int) PyObject_Print(struct _object *arg0, FILE *arg1, int arg2);
PyAPI_FUNC(void *) PyObject_Realloc(void *arg0, size_t arg1);
PyAPI_FUNC(struct _object *) PyObject_Repr(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyObject_RichCompare(struct _object *arg0, struct _object *arg1, int arg2);
PyAPI_FUNC(int) PyObject_RichCompareBool(struct _object *arg0, struct _object *arg1, int arg2);
PyAPI_FUNC(struct _object *) PyObject_SelfIter(struct _object *arg0);
PyAPI_FUNC(int) PyObject_SetAttr(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(int) PyObject_SetAttrString(PyObject * arg0, char const * arg1, PyObject * arg2);
PyAPI_FUNC(int) PyObject_SetItem(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(Signed) PyObject_Size(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyObject_Str(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyObject_Type(struct _object *arg0);
#define PyObject_Unicode PyPyObject_Unicode
PyAPI_FUNC(struct _object *) PyObject_Unicode(struct _object *arg0);
PyAPI_FUNC(PyObject *) PyObject_Vectorcall(PyObject * arg0, PyObject * const * arg1, size_t arg2, PyObject * arg3);
#define PyObject_VectorcallDict PyPyObject_VectorcallDict
PyAPI_FUNC(PyObject *) PyObject_VectorcallDict(PyObject * arg0, PyObject * const * arg1, size_t arg2, PyObject * arg3);
PyAPI_FUNC(PyObject *) PyObject_VectorcallMethod(PyObject * arg0, PyObject * const * arg1, size_t arg2, PyObject * arg3);
#define PyPyUnicode_Check PyPyUnicode_Check
PyAPI_FUNC(int) PyPyUnicode_Check(void * arg0);
#define PyPyUnicode_CheckExact PyPyUnicode_CheckExact
PyAPI_FUNC(int) PyPyUnicode_CheckExact(void * arg0);
#define PyRun_File PyPyRun_File
PyAPI_FUNC(struct _object *) PyRun_File(FILE *arg0, const char *arg1, int arg2, struct _object *arg3, struct _object *arg4);
#define PyRun_FileExFlags PyPyRun_FileExFlags
PyAPI_FUNC(struct _object *) PyRun_FileExFlags(FILE *arg0, const char *arg1, int arg2, struct _object *arg3, struct _object *arg4, int arg5, PyCompilerFlags *arg6);
#define PyRun_String PyPyRun_String
PyAPI_FUNC(struct _object *) PyRun_String(const char *arg0, int arg1, struct _object *arg2, struct _object *arg3);
#define PyRun_StringFlags PyPyRun_StringFlags
PyAPI_FUNC(struct _object *) PyRun_StringFlags(const char *arg0, int arg1, struct _object *arg2, struct _object *arg3, PyCompilerFlags *arg4);
PyAPI_FUNC(struct _object *) PySeqIter_New(struct _object *arg0);
PyAPI_FUNC(int) PySequence_Check(struct _object *arg0);
PyAPI_FUNC(struct _object *) PySequence_Concat(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PySequence_Contains(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(Signed) PySequence_Count(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PySequence_DelItem(struct _object *arg0, Signed arg1);
PyAPI_FUNC(int) PySequence_DelSlice(struct _object *arg0, Signed arg1, Signed arg2);
PyAPI_FUNC(struct _object *) PySequence_Fast(struct _object *arg0, const char *arg1);
#define PySequence_Fast_GET_ITEM PyPySequence_Fast_GET_ITEM
PyAPI_FUNC(struct _object *) PySequence_Fast_GET_ITEM(void *arg0, Signed arg1);
#define PySequence_Fast_GET_SIZE PyPySequence_Fast_GET_SIZE
PyAPI_FUNC(Signed) PySequence_Fast_GET_SIZE(void *arg0);
#define PySequence_Fast_ITEMS PyPySequence_Fast_ITEMS
PyAPI_FUNC(struct _object **) PySequence_Fast_ITEMS(void *arg0);
PyAPI_FUNC(struct _object *) PySequence_GetItem(struct _object *arg0, Signed arg1);
PyAPI_FUNC(struct _object *) PySequence_GetSlice(struct _object *arg0, Signed arg1, Signed arg2);
#define PySequence_ITEM PyPySequence_ITEM
PyAPI_FUNC(struct _object *) PySequence_ITEM(void *arg0, Signed arg1);
PyAPI_FUNC(struct _object *) PySequence_InPlaceConcat(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PySequence_InPlaceRepeat(struct _object *arg0, Signed arg1);
PyAPI_FUNC(Signed) PySequence_Index(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(Signed) PySequence_Length(struct _object *arg0);
PyAPI_FUNC(struct _object *) PySequence_List(struct _object *arg0);
PyAPI_FUNC(struct _object *) PySequence_Repeat(struct _object *arg0, Signed arg1);
PyAPI_FUNC(int) PySequence_SetItem(struct _object *arg0, Signed arg1, struct _object *arg2);
PyAPI_FUNC(int) PySequence_SetSlice(struct _object *arg0, Signed arg1, Signed arg2, struct _object *arg3);
PyAPI_FUNC(Signed) PySequence_Size(struct _object *arg0);
PyAPI_FUNC(struct _object *) PySequence_Tuple(struct _object *arg0);
PyAPI_FUNC(int) PySet_Add(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PySet_Clear(struct _object *arg0);
PyAPI_FUNC(int) PySet_Contains(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PySet_Discard(struct _object *arg0, struct _object *arg1);
#define PySet_GET_SIZE PyPySet_GET_SIZE
PyAPI_FUNC(Signed) PySet_GET_SIZE(void *arg0);
PyAPI_FUNC(struct _object *) PySet_New(struct _object *arg0);
PyAPI_FUNC(struct _object *) PySet_Pop(struct _object *arg0);
PyAPI_FUNC(Signed) PySet_Size(struct _object *arg0);
PyAPI_FUNC(int) PySlice_GetIndices(struct _object *arg0, Signed arg1, Signed *arg2, Signed *arg3, Signed *arg4);
PyAPI_FUNC(int) PySlice_GetIndicesEx(struct _object *arg0, Signed arg1, Signed *arg2, Signed *arg3, Signed *arg4, Signed *arg5);
PyAPI_FUNC(struct _object *) PySlice_New(struct _object *arg0, struct _object *arg1, struct _object *arg2);
PyAPI_FUNC(int) PySlice_Unpack(struct _object *arg0, Signed *arg1, Signed *arg2, Signed *arg3);
PyAPI_FUNC(int) PyState_AddModule(struct _object *arg0, struct PyModuleDef *arg1);
PyAPI_FUNC(int) PyState_RemoveModule(struct PyModuleDef *arg0);
#define PyStaticMethod_New PyPyStaticMethod_New
PyAPI_FUNC(struct _object *) PyStaticMethod_New(struct _object *arg0);
PyAPI_FUNC(struct _object *) PySys_GetObject(const char *arg0);
PyAPI_FUNC(int) PySys_SetObject(const char *arg0, struct _object *arg1);
#define PyTZInfo_Check PyPyTZInfo_Check
PyAPI_FUNC(int) PyTZInfo_Check(struct _object *arg0);
#define PyTZInfo_CheckExact PyPyTZInfo_CheckExact
PyAPI_FUNC(int) PyTZInfo_CheckExact(struct _object *arg0);
PyAPI_FUNC(void) PyThreadState_Clear(PyThreadState *arg0);
PyAPI_FUNC(void) PyThreadState_Delete(PyThreadState *arg0);
PyAPI_FUNC(void) PyThreadState_DeleteCurrent(void);
#define PyThreadState_EnterTracing PyPyThreadState_EnterTracing
PyAPI_FUNC(void) PyThreadState_EnterTracing(PyThreadState *arg0);
PyAPI_FUNC(PyThreadState *) PyThreadState_Get(void);
PyAPI_FUNC(struct _object *) PyThreadState_GetDict(void);
PyAPI_FUNC(PyFrameObject *) PyThreadState_GetFrame(PyThreadState *arg0);
PyAPI_FUNC(size_t) PyThreadState_GetID(PyThreadState *arg0);
#define PyThreadState_LeaveTracing PyPyThreadState_LeaveTracing
PyAPI_FUNC(void) PyThreadState_LeaveTracing(PyThreadState *arg0);
PyAPI_FUNC(PyThreadState *) PyThreadState_New(PyInterpreterState *arg0);
PyAPI_FUNC(int) PyThreadState_SetAsyncExc(size_t arg0, struct _object *arg1);
PyAPI_FUNC(PyThreadState *) PyThreadState_Swap(PyThreadState *arg0);
PyAPI_FUNC(void) PyThread_exit_thread(void);
#define PyTime_Check PyPyTime_Check
PyAPI_FUNC(int) PyTime_Check(struct _object *arg0);
#define PyTime_CheckExact PyPyTime_CheckExact
PyAPI_FUNC(int) PyTime_CheckExact(struct _object *arg0);
PyAPI_FUNC(int) PyTraceBack_Here(PyFrameObject *arg0);
PyAPI_FUNC(int) PyTraceBack_Print(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyTuple_GetItem(struct _object *arg0, Signed arg1);
PyAPI_FUNC(struct _object *) PyTuple_GetSlice(struct _object *arg0, Signed arg1, Signed arg2);
PyAPI_FUNC(int) PyTuple_SetItem(struct _object *arg0, Signed arg1, struct _object *arg2);
PyAPI_FUNC(Signed) PyTuple_Size(struct _object *arg0);
PyAPI_FUNC(PyObject *) PyType_FromMetaclass(PyTypeObject * arg0, PyObject * arg1, PyType_Spec * arg2, PyObject * arg3);
PyAPI_FUNC(PyObject *) PyType_FromModuleAndSpec(PyObject * arg0, PyType_Spec * arg1, PyObject * arg2);
PyAPI_FUNC(PyObject *) PyType_FromSpecWithBases(PyType_Spec * arg0, PyObject * arg1);
PyAPI_FUNC(void *) PyType_GetSlot(struct _typeobject *arg0, int arg1);
PyAPI_FUNC(void) PyType_Modified(struct _typeobject *arg0);
PyAPI_FUNC(int) PyType_Ready(struct _typeobject *arg0);
PyAPI_FUNC(void) PyUnicode_Append(struct _object **arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyUnicode_AsASCIIString(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_AsEncodedObject(struct _object *arg0, const char *arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_AsEncodedString(struct _object *arg0, const char *arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_AsLatin1String(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_AsMBCSString(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_AsRawUnicodeEscapeString(struct _object *arg0);
PyAPI_FUNC(Py_UCS4 *) PyUnicode_AsUCS4(PyObject * arg0, Py_UCS4 * arg1, Py_ssize_t arg2, int arg3);
PyAPI_FUNC(Py_UCS4 *) PyUnicode_AsUCS4Copy(PyObject * arg0);
PyAPI_FUNC(struct _object *) PyUnicode_AsUTF16String(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_AsUTF32String(struct _object *arg0);
#define PyUnicode_AsUTF8 PyPyUnicode_AsUTF8
PyAPI_FUNC(char *) PyUnicode_AsUTF8(PyObject * arg0);
PyAPI_FUNC(char *) PyUnicode_AsUTF8AndSize(PyObject * arg0, Py_ssize_t * arg1);
PyAPI_FUNC(struct _object *) PyUnicode_AsUTF8String(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_AsUnicodeEscapeString(struct _object *arg0);
PyAPI_FUNC(Signed) PyUnicode_AsWideChar(struct _object *arg0, wchar_t *arg1, Signed arg2);
PyAPI_FUNC(int) PyUnicode_Compare(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyUnicode_CompareWithASCIIString(struct _object *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyUnicode_Concat(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) PyUnicode_Contains(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(Signed) PyUnicode_Count(struct _object *arg0, struct _object *arg1, Signed arg2, Signed arg3);
PyAPI_FUNC(struct _object *) PyUnicode_Decode(const char *arg0, Signed arg1, const char *arg2, const char *arg3);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeASCII(const char *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeFSDefault(const char *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeFSDefaultAndSize(const char *arg0, Signed arg1);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeLatin1(const char *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeLocale(const char *arg0, const char *arg1);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeLocaleAndSize(const char *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeMBCS(const char *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeRawUnicodeEscape(const char *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeUTF16(const char *arg0, Signed arg1, const char *arg2, int *arg3);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeUTF32(const char *arg0, Signed arg1, const char *arg2, int *arg3);
PyAPI_FUNC(struct _object *) PyUnicode_DecodeUTF8(const char *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(PyObject *) PyUnicode_DecodeUnicodeEscape(char const * arg0, Py_ssize_t arg1, char const * arg2);
#define PyUnicode_EncodeASCII PyPyUnicode_EncodeASCII
PyAPI_FUNC(struct _object *) PyUnicode_EncodeASCII(const wchar_t *arg0, Signed arg1, const char *arg2);
#define PyUnicode_EncodeCodePage PyPyUnicode_EncodeCodePage
PyAPI_FUNC(struct _object *) PyUnicode_EncodeCodePage(int arg0, struct _object *arg1, const char *arg2);
#define PyUnicode_EncodeDecimal PyPyUnicode_EncodeDecimal
PyAPI_FUNC(int) PyUnicode_EncodeDecimal(wchar_t *arg0, Signed arg1, char *arg2, const char *arg3);
PyAPI_FUNC(struct _object *) PyUnicode_EncodeFSDefault(struct _object *arg0);
#define PyUnicode_EncodeLatin1 PyPyUnicode_EncodeLatin1
PyAPI_FUNC(struct _object *) PyUnicode_EncodeLatin1(const wchar_t *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(struct _object *) PyUnicode_EncodeLocale(struct _object *arg0, const char *arg1);
#define PyUnicode_EncodeMBCS PyPyUnicode_EncodeMBCS
PyAPI_FUNC(struct _object *) PyUnicode_EncodeMBCS(const wchar_t *arg0, Signed arg1, const char *arg2);
#define PyUnicode_EncodeUTF8 PyPyUnicode_EncodeUTF8
PyAPI_FUNC(struct _object *) PyUnicode_EncodeUTF8(const wchar_t *arg0, Signed arg1, const char *arg2);
PyAPI_FUNC(int) PyUnicode_FSConverter(struct _object *arg0, struct _object **arg1);
PyAPI_FUNC(int) PyUnicode_FSDecoder(struct _object *arg0, struct _object **arg1);
PyAPI_FUNC(Signed) PyUnicode_Find(struct _object *arg0, struct _object *arg1, Signed arg2, Signed arg3, int arg4);
PyAPI_FUNC(Py_ssize_t) PyUnicode_FindChar(PyObject * arg0, Py_UCS4 arg1, Py_ssize_t arg2, Py_ssize_t arg3, int arg4);
PyAPI_FUNC(struct _object *) PyUnicode_Format(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyUnicode_FromEncodedObject(struct _object *arg0, const char *arg1, const char *arg2);
#define PyUnicode_FromKindAndData PyPyUnicode_FromKindAndData
PyAPI_FUNC(PyObject *) PyUnicode_FromKindAndData(int arg0, void const * arg1, Py_ssize_t arg2);
PyAPI_FUNC(struct _object *) PyUnicode_FromObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_FromOrdinal(int arg0);
PyAPI_FUNC(struct _object *) PyUnicode_FromString(const char *arg0);
PyAPI_FUNC(struct _object *) PyUnicode_FromStringAndSize(const char *arg0, Signed arg1);
PyAPI_FUNC(PyObject *) PyUnicode_FromWideChar(wchar_t const * arg0, Py_ssize_t arg1);
PyAPI_FUNC(char *) PyUnicode_GetDefaultEncoding(void);
#define PyUnicode_GetMax PyPyUnicode_GetMax
PyAPI_FUNC(wchar_t) PyUnicode_GetMax(void);
PyAPI_FUNC(struct _object *) PyUnicode_InternFromString(const char *arg0);
PyAPI_FUNC(void) PyUnicode_InternInPlace(struct _object **arg0);
PyAPI_FUNC(struct _object *) PyUnicode_Join(struct _object *arg0, struct _object *arg1);
#define PyUnicode_New PyPyUnicode_New
PyAPI_FUNC(PyObject *) PyUnicode_New(Py_ssize_t arg0, Py_UCS4 arg1);
PyAPI_FUNC(Py_UCS4) PyUnicode_ReadChar(PyObject * arg0, Py_ssize_t arg1);
PyAPI_FUNC(struct _object *) PyUnicode_Replace(struct _object *arg0, struct _object *arg1, struct _object *arg2, Signed arg3);
PyAPI_FUNC(int) PyUnicode_Resize(struct _object **arg0, Signed arg1);
PyAPI_FUNC(struct _object *) PyUnicode_Split(struct _object *arg0, struct _object *arg1, Signed arg2);
PyAPI_FUNC(struct _object *) PyUnicode_Splitlines(struct _object *arg0, int arg1);
PyAPI_FUNC(struct _object *) PyUnicode_Substring(struct _object *arg0, Signed arg1, Signed arg2);
PyAPI_FUNC(Py_ssize_t) PyUnicode_Tailmatch(PyObject * arg0, PyObject * arg1, Py_ssize_t arg2, Py_ssize_t arg3, int arg4);
#define PyUnicode_TransformDecimalToASCII PyPyUnicode_TransformDecimalToASCII
PyAPI_FUNC(struct _object *) PyUnicode_TransformDecimalToASCII(wchar_t *arg0, Signed arg1);
PyAPI_FUNC(int) PyUnicode_WriteChar(PyObject * arg0, Py_ssize_t arg1, Py_UCS4 arg2);
#define PyUnstable_Code_New PyPyUnstable_Code_New
PyAPI_FUNC(PyObject *) PyUnstable_Code_New(int arg0, int arg1, int arg2, int arg3, int arg4, PyObject * arg5, PyObject * arg6, PyObject * arg7, PyObject * arg8, PyObject * arg9, PyObject * arg10, PyObject * arg11, PyObject * arg12, PyObject * arg13, int arg14, PyObject * arg15, PyObject * arg16);
#define PyUnstable_Code_NewWithPosOnlyArgs PyPyUnstable_Code_NewWithPosOnlyArgs
PyAPI_FUNC(PyCodeObject *) PyUnstable_Code_NewWithPosOnlyArgs(int arg0, int arg1, int arg2, int arg3, int arg4, int arg5, struct _object *arg6, struct _object *arg7, struct _object *arg8, struct _object *arg9, struct _object *arg10, struct _object *arg11, struct _object *arg12, struct _object *arg13, struct _object *arg14, int arg15, struct _object *arg16, struct _object *arg17);
#define PyUnstable_InterpreterFrame_GetCode PyPyUnstable_InterpreterFrame_GetCode
PyAPI_FUNC(PyCodeObject *) PyUnstable_InterpreterFrame_GetCode(PyFrameObject *arg0);
#define PyUnstable_InterpreterFrame_GetLasti PyPyUnstable_InterpreterFrame_GetLasti
PyAPI_FUNC(int) PyUnstable_InterpreterFrame_GetLasti(PyFrameObject *arg0);
#define PyUnstable_InterpreterFrame_GetLine PyPyUnstable_InterpreterFrame_GetLine
PyAPI_FUNC(int) PyUnstable_InterpreterFrame_GetLine(PyFrameObject *arg0);
#define PyWeakref_GET_OBJECT PyPyWeakref_GET_OBJECT
PyAPI_FUNC(struct _object *) PyWeakref_GET_OBJECT(void *arg0);
PyAPI_FUNC(struct _object *) PyWeakref_GetObject(struct _object *arg0);
#define PyWeakref_LockObject PyPyWeakref_LockObject
PyAPI_FUNC(struct _object *) PyWeakref_LockObject(struct _object *arg0);
PyAPI_FUNC(struct _object *) PyWeakref_NewProxy(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(struct _object *) PyWeakref_NewRef(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) Py_AddPendingCall(int (*arg0)(void *), void *arg1);
PyAPI_FUNC(int) Py_AtExit(void (*arg0)(void));
#define Py_CompileStringFlags PyPy_CompileStringFlags
PyAPI_FUNC(struct _object *) Py_CompileStringFlags(const char *arg0, const char *arg1, int arg2, PyCompilerFlags *arg3);
PyAPI_FUNC(void) Py_DecRef(struct _object *arg0);
PyAPI_FUNC(int) Py_EnterRecursiveCall(const char *arg0);
#define Py_FindMethod PyPy_FindMethod
PyAPI_FUNC(struct _object *) Py_FindMethod(struct PyMethodDef *arg0, struct _object *arg1, const char *arg2);
PyAPI_FUNC(wchar_t *) Py_GetProgramName(void);
PyAPI_FUNC(int) Py_GetRecursionLimit(void);
PyAPI_FUNC(char *) Py_GetVersion(void);
PyAPI_FUNC(void) Py_IncRef(struct _object *arg0);
PyAPI_FUNC(int) Py_Is(struct _object *arg0, struct _object *arg1);
PyAPI_FUNC(int) Py_IsInitialized(void);
PyAPI_FUNC(void) Py_LeaveRecursiveCall(void);
PyAPI_FUNC(int) Py_MakePendingCalls(void);
PyAPI_FUNC(int) Py_ReprEnter(struct _object *arg0);
PyAPI_FUNC(void) Py_ReprLeave(struct _object *arg0);
PyAPI_FUNC(void) Py_SetRecursionLimit(int arg0);
#define Py_UNICODE_COPY PyPy_UNICODE_COPY
PyAPI_FUNC(void) Py_UNICODE_COPY(wchar_t *arg0, wchar_t *arg1, Signed arg2);
#define _PyBytes_Eq _PyPyBytes_Eq
PyAPI_FUNC(int) _PyBytes_Eq(struct _object *arg0, struct _object *arg1);
#define _PyBytes_Join _PyPyBytes_Join
PyAPI_FUNC(struct _object *) _PyBytes_Join(struct _object *arg0, struct _object *arg1);
#define _PyBytes_Resize _PyPyBytes_Resize
PyAPI_FUNC(int) _PyBytes_Resize(struct _object **arg0, Signed arg1);
#define _PyComplex_AsCComplex _PyPyComplex_AsCComplex
PyAPI_FUNC(int) _PyComplex_AsCComplex(struct _object *arg0, struct Py_complex_t *arg1);
#define _PyComplex_FromCComplex _PyPyComplex_FromCComplex
PyAPI_FUNC(struct _object *) _PyComplex_FromCComplex(struct Py_complex_t *arg0);
#define _PyDateTime_FromDateAndTime _PyPyDateTime_FromDateAndTime
PyAPI_FUNC(struct _object *) _PyDateTime_FromDateAndTime(int arg0, int arg1, int arg2, int arg3, int arg4, int arg5, int arg6, struct _object *arg7, struct _typeobject *arg8);
#define _PyDateTime_FromDateAndTimeAndFold _PyPyDateTime_FromDateAndTimeAndFold
PyAPI_FUNC(struct _object *) _PyDateTime_FromDateAndTimeAndFold(int arg0, int arg1, int arg2, int arg3, int arg4, int arg5, int arg6, struct _object *arg7, int arg8, struct _typeobject *arg9);
#define _PyDateTime_FromTimestamp _PyPyDateTime_FromTimestamp
PyAPI_FUNC(struct _object *) _PyDateTime_FromTimestamp(struct _object *arg0, struct _object *arg1, struct _object *arg2);
#define _PyDateTime_Import _PyPyDateTime_Import
PyAPI_FUNC(PyDateTime_CAPI *) _PyDateTime_Import(void);
#define _PyDate_FromDate _PyPyDate_FromDate
PyAPI_FUNC(struct _object *) _PyDate_FromDate(int arg0, int arg1, int arg2, struct _typeobject *arg3);
#define _PyDate_FromTimestamp _PyPyDate_FromTimestamp
PyAPI_FUNC(struct _object *) _PyDate_FromTimestamp(struct _object *arg0, struct _object *arg1);
#define _PyDelta_FromDelta _PyPyDelta_FromDelta
PyAPI_FUNC(struct _object *) _PyDelta_FromDelta(int arg0, int arg1, int arg2, int arg3, struct _typeobject *arg4);
#define _PyDict_GetItemStringWithError _PyPyDict_GetItemStringWithError
PyAPI_FUNC(struct _object *) _PyDict_GetItemStringWithError(struct _object *arg0, const char *arg1);
#define _PyDict_HasOnlyStringKeys _PyPyDict_HasOnlyStringKeys
PyAPI_FUNC(int) _PyDict_HasOnlyStringKeys(struct _object *arg0);
PyAPI_FUNC(void) _PyErr_BadInternalCall(const char *arg0, int arg1);
#define _PyErr_WriteUnraisableMsg _PyPyErr_WriteUnraisableMsg
PyAPI_FUNC(void) _PyErr_WriteUnraisableMsg(const char *arg0, struct _object *arg1);
#define _PyEval_GetAsyncGenFinalizer _PyPyEval_GetAsyncGenFinalizer
PyAPI_FUNC(struct _object *) _PyEval_GetAsyncGenFinalizer(void);
#define _PyEval_GetAsyncGenFirstiter _PyPyEval_GetAsyncGenFirstiter
PyAPI_FUNC(struct _object *) _PyEval_GetAsyncGenFirstiter(void);
#define _PyEval_SliceIndex _PyPyEval_SliceIndex
PyAPI_FUNC(int) _PyEval_SliceIndex(struct _object *arg0, Signed *arg1);
#define _PyImport_AcquireLock _PyPyImport_AcquireLock
PyAPI_FUNC(void) _PyImport_AcquireLock(void);
#define _PyImport_ReleaseLock _PyPyImport_ReleaseLock
PyAPI_FUNC(int) _PyImport_ReleaseLock(void);
#define _PyList_Extend _PyPyList_Extend
PyAPI_FUNC(struct _object *) _PyList_Extend(struct _object *arg0, struct _object *arg1);
#define _PyLong_AsByteArrayO _PyPyLong_AsByteArrayO
PyAPI_FUNC(int) _PyLong_AsByteArrayO(struct _object *arg0, unsigned char *arg1, size_t arg2, int arg3, int arg4);
PyAPI_FUNC(int) _PyLong_AsInt(struct _object *arg0);
#define _PyLong_FromByteArray _PyPyLong_FromByteArray
PyAPI_FUNC(struct _object *) _PyLong_FromByteArray(unsigned char const *arg0, size_t arg1, int arg2, int arg3);
#define _PyLong_NumBits _PyPyLong_NumBits
PyAPI_FUNC(size_t) _PyLong_NumBits(struct _object *arg0);
#define _PyLong_Sign _PyPyLong_Sign
PyAPI_FUNC(int) _PyLong_Sign(struct _object *arg0);
#define _PyObject_ClearManagedDict _PyPyObject_ClearManagedDict
PyAPI_FUNC(void) _PyObject_ClearManagedDict(struct _object *arg0);
#define _PyObject_FastCall _PyPyObject_FastCall
PyAPI_FUNC(PyObject *) _PyObject_FastCall(PyObject * arg0, PyObject * const * arg1, size_t arg2);
#define _PyObject_GetDictPtr _PyPyObject_GetDictPtr
PyAPI_FUNC(struct _object **) _PyObject_GetDictPtr(struct _object *arg0);
#define _PyPyGC_AddMemoryPressure _PyPyPyGC_AddMemoryPressure
PyAPI_FUNC(void) _PyPyGC_AddMemoryPressure(Signed arg0);
#define _PyPy_Free _PyPyPy_Free
extern void _PyPy_Free(void *arg0);
#define _PyPy_Malloc _PyPyPy_Malloc
extern void * _PyPy_Malloc(Signed arg0);
#define _PySet_Next _PyPySet_Next
PyAPI_FUNC(int) _PySet_Next(struct _object *arg0, Signed *arg1, struct _object **arg2);
#define _PySet_NextEntry _PyPySet_NextEntry
PyAPI_FUNC(int) _PySet_NextEntry(struct _object *arg0, Signed *arg1, struct _object **arg2, Signed *arg3);
#define _PyThreadState_GetDict _PyPyThreadState_GetDict
PyAPI_FUNC(struct _object *) _PyThreadState_GetDict(PyThreadState *arg0);
#define _PyThreadState_UncheckedGet _PyPyThreadState_UncheckedGet
PyAPI_FUNC(PyThreadState *) _PyThreadState_UncheckedGet(void);
#define _PyTimeZone_FromTimeZone _PyPyTimeZone_FromTimeZone
PyAPI_FUNC(struct _object *) _PyTimeZone_FromTimeZone(struct _object *arg0, struct _object *arg1);
#define _PyTime_FromTime _PyPyTime_FromTime
PyAPI_FUNC(struct _object *) _PyTime_FromTime(int arg0, int arg1, int arg2, int arg3, struct _object *arg4, struct _typeobject *arg5);
#define _PyTime_FromTimeAndFold _PyPyTime_FromTimeAndFold
PyAPI_FUNC(struct _object *) _PyTime_FromTimeAndFold(int arg0, int arg1, int arg2, int arg3, struct _object *arg4, int arg5, struct _typeobject *arg6);
#define _PyTuple_Resize _PyPyTuple_Resize
PyAPI_FUNC(int) _PyTuple_Resize(struct _object **arg0, Signed arg1);
#define _PyType_Lookup _PyPyType_Lookup
PyAPI_FUNC(struct _object *) _PyType_Lookup(struct _typeobject *arg0, struct _object *arg1);
#define _PyUnicode_EQ _PyPyUnicode_EQ
PyAPI_FUNC(int) _PyUnicode_EQ(struct _object *arg0, struct _object *arg1);
#define _PyUnicode_EqualToASCIIString _PyPyUnicode_EqualToASCIIString
PyAPI_FUNC(int) _PyUnicode_EqualToASCIIString(struct _object *arg0, const char *arg1);
#define _PyUnicode_IsAlpha _PyPyUnicode_IsAlpha
PyAPI_FUNC(int) _PyUnicode_IsAlpha(unsigned int arg0);
#define _PyUnicode_IsDecimalDigit _PyPyUnicode_IsDecimalDigit
PyAPI_FUNC(int) _PyUnicode_IsDecimalDigit(unsigned int arg0);
#define _PyUnicode_IsDigit _PyPyUnicode_IsDigit
PyAPI_FUNC(int) _PyUnicode_IsDigit(unsigned int arg0);
#define _PyUnicode_IsLowercase _PyPyUnicode_IsLowercase
PyAPI_FUNC(int) _PyUnicode_IsLowercase(unsigned int arg0);
#define _PyUnicode_IsNumeric _PyPyUnicode_IsNumeric
PyAPI_FUNC(int) _PyUnicode_IsNumeric(unsigned int arg0);
#define _PyUnicode_IsPrintable _PyPyUnicode_IsPrintable
PyAPI_FUNC(int) _PyUnicode_IsPrintable(unsigned int arg0);
#define _PyUnicode_IsTitlecase _PyPyUnicode_IsTitlecase
PyAPI_FUNC(int) _PyUnicode_IsTitlecase(unsigned int arg0);
#define _PyUnicode_IsUppercase _PyPyUnicode_IsUppercase
PyAPI_FUNC(int) _PyUnicode_IsUppercase(unsigned int arg0);
#define _PyUnicode_ToDecimalDigit _PyPyUnicode_ToDecimalDigit
PyAPI_FUNC(int) _PyUnicode_ToDecimalDigit(unsigned int arg0);
#define _PyUnicode_ToDigit _PyPyUnicode_ToDigit
PyAPI_FUNC(int) _PyUnicode_ToDigit(unsigned int arg0);
#define _PyUnicode_ToLowercase _PyPyUnicode_ToLowercase
PyAPI_FUNC(unsigned int) _PyUnicode_ToLowercase(unsigned int arg0);
#define _PyUnicode_ToTitlecase _PyPyUnicode_ToTitlecase
PyAPI_FUNC(unsigned int) _PyUnicode_ToTitlecase(unsigned int arg0);
#define _PyUnicode_ToUppercase _PyPyUnicode_ToUppercase
PyAPI_FUNC(unsigned int) _PyUnicode_ToUppercase(unsigned int arg0);
#define _Py_HashDouble _PyPy_HashDouble
PyAPI_FUNC(Signed) _Py_HashDouble(struct _object *arg0, double arg1);
#define _Py_HashPointer _PyPy_HashPointer
PyAPI_FUNC(Signed) _Py_HashPointer(void *arg0);
#define _Py_IsFinalizing _PyPy_IsFinalizing
PyAPI_FUNC(int) _Py_IsFinalizing(void);
#define _Py_strhex _PyPy_strhex
PyAPI_FUNC(PyObject *) _Py_strhex(char const * arg0, Py_ssize_t arg1);
#define _Py_strhex_bytes _PyPy_strhex_bytes
PyAPI_FUNC(PyObject *) _Py_strhex_bytes(char const * arg0, Py_ssize_t arg1);
PyAPI_DATA(PyObject) _Py_NoneStruct;
PyAPI_DATA(PyObject) _Py_TrueStruct;
PyAPI_DATA(PyObject) _Py_FalseStruct;
PyAPI_DATA(PyObject) _Py_NotImplementedStruct;
PyAPI_DATA(PyObject) _Py_EllipsisObject;
#define PyDateTimeAPI PyPyDateTimeAPI
PyAPI_DATA(PyDateTime_CAPI*) PyDateTimeAPI;
PyAPI_DATA(PyTypeObject) Py_GenericAliasType;
PyAPI_DATA(PyObject*) PyExc_ArithmeticError;
PyAPI_DATA(PyObject*) PyExc_AssertionError;
PyAPI_DATA(PyObject*) PyExc_AttributeError;
PyAPI_DATA(PyObject*) PyExc_BaseException;
PyAPI_DATA(PyObject*) PyExc_BaseExceptionGroup;
PyAPI_DATA(PyObject*) PyExc_BlockingIOError;
PyAPI_DATA(PyObject*) PyExc_BrokenPipeError;
PyAPI_DATA(PyObject*) PyExc_BufferError;
PyAPI_DATA(PyObject*) PyExc_BytesWarning;
PyAPI_DATA(PyObject*) PyExc_ChildProcessError;
PyAPI_DATA(PyObject*) PyExc_ConnectionAbortedError;
PyAPI_DATA(PyObject*) PyExc_ConnectionError;
PyAPI_DATA(PyObject*) PyExc_ConnectionRefusedError;
PyAPI_DATA(PyObject*) PyExc_ConnectionResetError;
PyAPI_DATA(PyObject*) PyExc_DeprecationWarning;
PyAPI_DATA(PyObject*) PyExc_EOFError;
PyAPI_DATA(PyObject*) PyExc_EncodingWarning;
PyAPI_DATA(PyObject*) PyExc_Exception;
PyAPI_DATA(PyObject*) PyExc_ExceptionGroup;
PyAPI_DATA(PyObject*) PyExc_FileExistsError;
PyAPI_DATA(PyObject*) PyExc_FileNotFoundError;
PyAPI_DATA(PyObject*) PyExc_FloatingPointError;
PyAPI_DATA(PyObject*) PyExc_FutureWarning;
PyAPI_DATA(PyObject*) PyExc_GeneratorExit;
PyAPI_DATA(PyObject*) PyExc_ImportError;
PyAPI_DATA(PyObject*) PyExc_ImportWarning;
PyAPI_DATA(PyObject*) PyExc_IndentationError;
PyAPI_DATA(PyObject*) PyExc_IndexError;
PyAPI_DATA(PyObject*) PyExc_InterruptedError;
PyAPI_DATA(PyObject*) PyExc_IsADirectoryError;
PyAPI_DATA(PyObject*) PyExc_KeyError;
PyAPI_DATA(PyObject*) PyExc_KeyboardInterrupt;
PyAPI_DATA(PyObject*) PyExc_LookupError;
PyAPI_DATA(PyObject*) PyExc_MemoryError;
PyAPI_DATA(PyObject*) PyExc_ModuleNotFoundError;
PyAPI_DATA(PyObject*) PyExc_NameError;
PyAPI_DATA(PyObject*) PyExc_NotADirectoryError;
PyAPI_DATA(PyObject*) PyExc_NotImplementedError;
PyAPI_DATA(PyObject*) PyExc_OSError;
PyAPI_DATA(PyObject*) PyExc_OverflowError;
PyAPI_DATA(PyObject*) PyExc_PendingDeprecationWarning;
PyAPI_DATA(PyObject*) PyExc_PermissionError;
PyAPI_DATA(PyObject*) PyExc_ProcessLookupError;
PyAPI_DATA(PyObject*) PyExc_RecursionError;
PyAPI_DATA(PyObject*) PyExc_ReferenceError;
PyAPI_DATA(PyObject*) PyExc_ResourceWarning;
PyAPI_DATA(PyObject*) PyExc_RuntimeError;
PyAPI_DATA(PyObject*) PyExc_RuntimeWarning;
PyAPI_DATA(PyObject*) PyExc_StopAsyncIteration;
PyAPI_DATA(PyObject*) PyExc_StopIteration;
PyAPI_DATA(PyObject*) PyExc_SyntaxError;
PyAPI_DATA(PyObject*) PyExc_SyntaxWarning;
PyAPI_DATA(PyObject*) PyExc_SystemError;
PyAPI_DATA(PyObject*) PyExc_SystemExit;
PyAPI_DATA(PyObject*) PyExc_TabError;
PyAPI_DATA(PyObject*) PyExc_TimeoutError;
PyAPI_DATA(PyObject*) PyExc_TypeError;
PyAPI_DATA(PyObject*) PyExc_UnboundLocalError;
PyAPI_DATA(PyObject*) PyExc_UnicodeDecodeError;
PyAPI_DATA(PyObject*) PyExc_UnicodeEncodeError;
PyAPI_DATA(PyObject*) PyExc_UnicodeError;
PyAPI_DATA(PyObject*) PyExc_UnicodeTranslateError;
PyAPI_DATA(PyObject*) PyExc_UnicodeWarning;
PyAPI_DATA(PyObject*) PyExc_UserWarning;
PyAPI_DATA(PyObject*) PyExc_ValueError;
PyAPI_DATA(PyObject*) PyExc_Warning;
PyAPI_DATA(PyObject*) PyExc_ZeroDivisionError;
PyAPI_DATA(PyTypeObject) PyBytes_Type;
PyAPI_DATA(PyTypeObject) PyUnicode_Type;
PyAPI_DATA(PyTypeObject) PyDict_Type;
PyAPI_DATA(PyTypeObject) PyDictProxy_Type;
PyAPI_DATA(PyTypeObject) PyDictValues_Type;
PyAPI_DATA(PyTypeObject) PyDictKeys_Type;
PyAPI_DATA(PyTypeObject) PyDictItems_Type;
PyAPI_DATA(PyTypeObject) PySeqIter_Type;
PyAPI_DATA(PyTypeObject) PyCallIter_Type;
PyAPI_DATA(PyTypeObject) PyTuple_Type;
PyAPI_DATA(PyTypeObject) PyList_Type;
PyAPI_DATA(PyTypeObject) PySet_Type;
PyAPI_DATA(PyTypeObject) PyFrozenSet_Type;
PyAPI_DATA(PyTypeObject) PyBool_Type;
PyAPI_DATA(PyTypeObject) PyFloat_Type;
PyAPI_DATA(PyTypeObject) PyLong_Type;
PyAPI_DATA(PyTypeObject) PyComplex_Type;
PyAPI_DATA(PyTypeObject) PyByteArray_Type;
PyAPI_DATA(PyTypeObject) PyMemoryView_Type;
PyAPI_DATA(PyTypeObject) PyBaseObject_Type;
PyAPI_DATA(PyTypeObject) _PyNone_Type;
PyAPI_DATA(PyTypeObject) _PyNotImplemented_Type;
PyAPI_DATA(PyTypeObject) PyCell_Type;
PyAPI_DATA(PyTypeObject) PyModule_Type;
PyAPI_DATA(PyTypeObject) PyProperty_Type;
PyAPI_DATA(PyTypeObject) PySlice_Type;
PyAPI_DATA(PyTypeObject) PyStaticMethod_Type;
PyAPI_DATA(PyTypeObject) PyClassMethod_Type;
PyAPI_DATA(PyTypeObject) PyCFunction_Type;
PyAPI_DATA(PyTypeObject) PyClassMethodDescr_Type;
PyAPI_DATA(PyTypeObject) PyGetSetDescr_Type;
PyAPI_DATA(PyTypeObject) PyMemberDescr_Type;
PyAPI_DATA(PyTypeObject) PyMethodDescr_Type;
PyAPI_DATA(PyTypeObject) PyWrapperDescr_Type;
PyAPI_DATA(PyTypeObject) PyInstanceMethod_Type;
PyAPI_DATA(PyTypeObject) PyReversed_Type;
PyAPI_DATA(PyTypeObject) PyRange_Type;
PyAPI_DATA(PyTypeObject) PyFunction_Type;
PyAPI_DATA(PyTypeObject) PyMethod_Type;
PyAPI_DATA(PyTypeObject) PyTraceBack_Type;
PyAPI_DATA(PyTypeObject) PyFrame_Type;
PyAPI_DATA(PyTypeObject) PyGen_Type;
PyAPI_DATA(PyTypeObject) _PyWeakref_RefType;
PyAPI_DATA(PyTypeObject) _PyWeakref_ProxyType;
PyAPI_DATA(PyTypeObject) _PyWeakref_CallableProxyType;
#define PyBufferable_Type PyPyBufferable_Type
PyAPI_DATA(PyTypeObject) PyBufferable_Type;
PyAPI_DATA(PyTypeObject) PyCapsule_Type;

#undef Signed    /* xxx temporary fix */
#undef Unsigned  /* xxx temporary fix */

