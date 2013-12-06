#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
//#include "mrc3_client.h"

#ifdef __cplusplus
extern "C" {
#endif
typedef void (__stdcall mrc3_status_callback_func_t)(int callback_id, int status);
typedef int (__stdcall mrc3_set_status_callback_function)(const int handle, mrc3_status_callback_func_t *function);
#ifdef __cplusplus
}
#endif

static PyObject *py_callback=NULL;

void __stdcall main_callback(int id, int status) {
    PyObject *arglist;
    PyObject *result;
    PyGILState_STATE gstate;

    //printf("cb %d %d\n", id, status);
    if (!py_callback)
        return;

    gstate = PyGILState_Ensure();

    arglist = Py_BuildValue("(ii)", id, status);
    result =  PyEval_CallObject(py_callback, arglist);

    Py_DECREF(arglist);
    Py_XDECREF(result);

    PyGILState_Release(gstate);
}

static PyObject *
set_callback(PyObject *self, PyObject *args)
{
    int mrc3_handle;
    int ret;
    int _dll_handle;
    HMODULE dll_handle;
    PyObject *temp;
    mrc3_set_status_callback_function *fcn;
    if (!PyArg_ParseTuple(args, "iiO:set_callback", &_dll_handle, &mrc3_handle, &temp)) {
        return NULL;
    }
   
    dll_handle = (HMODULE)_dll_handle;
    if (dll_handle < 0) {
        PyErr_SetString(PyExc_TypeError, "Invalid DLL handle");
        return NULL;
    }

    if (!PyCallable_Check(temp) && temp != Py_None) {
        PyErr_SetString(PyExc_TypeError, "Parameter must be callable");
        return NULL;
    }
    
    if (temp == Py_None)
        temp = NULL;

    Py_XINCREF(temp);
    Py_XDECREF(py_callback);
    py_callback = temp;

    // dll_handle = LoadLibrary(...);
    fcn = (mrc3_set_status_callback_function*)GetProcAddress(dll_handle, 
                                            "mrc3_set_status_callback_function");
    if (!fcn) {
        PyErr_SetString(PyExc_TypeError, "GetProcAddress failed");
        return NULL;
    }

    ret = fcn(mrc3_handle, main_callback);
    return Py_BuildValue("i", ret);
}

static PyMethodDef Methods[] =
{
     {"set_callback", set_callback, METH_VARARGS, "Set the Python callback."},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_mrc3_callbacks(void)
{
     (void) Py_InitModule("_mrc3_callbacks", Methods);
}

